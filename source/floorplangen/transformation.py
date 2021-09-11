"""Transformation Module

This module allows user to transform each additional
edge into a node.

This module contains the following functions:

    * transform - transforms given esge in graph into node.
    * find_nbr - finds neigbour of the given vertex.
"""
import numpy as np

def transform(matrix,edge):
    """Transforms edge into vertex.

    Args:
        graph: An instance of InputGraph object.
        edge: A list representing edge to be transformed.

    Returns:
        None
    """
    nbd1= find_nbr(matrix,edge[0])
    nbd2 = find_nbr(matrix,edge[1])
    common_nbrs = nbd1.intersection(nbd2)
    adjmatrix = np.zeros([matrix.shape[0]+1, matrix.shape[0]+1], int)
    adjmatrix[0:matrix.shape[0],0:matrix.shape[1]] = matrix
    adjmatrix[edge[0]][edge[1]] = 0
    adjmatrix[edge[1]][edge[0]] = 0
    adjmatrix[matrix.shape[0]][edge[0]] = 1
    adjmatrix[matrix.shape[0]][edge[1]] = 1
    adjmatrix[edge[0]][matrix.shape[0]] = 1
    adjmatrix[edge[1]][matrix.shape[0]] = 1
    for vertex in common_nbrs:
        adjmatrix[vertex][matrix.shape[0]]=1
        adjmatrix[matrix.shape[0]][vertex]=1
    if(len(common_nbrs)==1):
        return adjmatrix,2
    else:
        return adjmatrix,3

def find_nbr(matrix,vertex):
    """Finds neighbour of the given vertex.

    Args:
        graph: An instance of InputGraph object.
        vertex: An integer whose neighbours are to be found.

    Returns:
        nbr: A set representing neighbours of vertex.
    """
    nbr = set()
    for i in range(0,matrix.shape[0]):
        if(matrix[vertex][i]==1):
            nbr.add(i)
    return nbr