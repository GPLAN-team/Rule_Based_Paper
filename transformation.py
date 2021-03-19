"""Transformation Module

This module allows user to transform each additional
edge into a node.

This module contains the following functions:

    * transform - transforms given esge in graph into node.
    * find_nbr - finds neigbour of the given vertex.
"""
import numpy as np

def transform(graph,edge):
    """Transforms edge into vertex.

    Args:
        graph: An instance of InputGraph object.
        edge: A list representing edge to be transformed.

    Returns:
        None
    """
    nbd1= find_nbr(graph,edge[0])
    nbd2 = find_nbr(graph,edge[1])
    common_nbrs = nbd1.intersection(nbd2)
    graph.nodecnt +=1
    adjmatrix = np.zeros([graph.nodecnt, graph.nodecnt], int)
    adjmatrix[0:graph.matrix.shape[0],0:graph.matrix.shape[1]] = graph.matrix
    adjmatrix[edge[0]][edge[1]] = 0
    adjmatrix[edge[1]][edge[0]] = 0
    adjmatrix[graph.nodecnt-1][edge[0]] = 1
    adjmatrix[graph.nodecnt-1][edge[1]] = 1
    adjmatrix[edge[0]][graph.nodecnt-1] = 1
    adjmatrix[edge[1]][graph.nodecnt-1] = 1
    for vertex in common_nbrs:
        adjmatrix[vertex][graph.nodecnt-1]=1
        adjmatrix[graph.nodecnt-1][vertex]=1
    if(len(common_nbrs)==1):
        graph.edgecnt+=2
    else:
        graph.edgecnt+=3
    graph.matrix = adjmatrix
    graph.north +=1
    graph.east +=1
    graph.west +=1
    graph.south +=1 

def find_nbr(graph,vertex):
    """Finds neighbour of the given vertex.

    Args:
        graph: An instance of InputGraph object.
        vertex: An integer whose neighbours are to be found.

    Returns:
        nbr: A set representing neighbours of vertex.
    """
    nbr = set()
    for i in range(0,graph.nodecnt):
        if(graph.matrix[vertex][i]==1):
            nbr.add(i)
    return nbr