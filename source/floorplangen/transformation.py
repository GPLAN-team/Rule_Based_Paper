"""Transformation Module

This module allows user to transform each additional
edge into a node.

This module contains the following functions:

    * transform - transforms given edge in graph into node.
    * find_nbr - finds neigbour of the given vertex.
"""
import numpy as np

def transform_edges(matrix, edge):
    """Transforms edge into vertex.

    Args:
        matrix: A matrix representing the adjacency matrix of the graph.
        edge: A list representing edge to be transformed.

    Returns:
        adjmatrix: A modified matrix after edge transformation.
        edgecnt: An integer representing the increase in edgecnt (2 or 3).
    """
    nbd1 = find_nbr(matrix,edge[0])
    nbd2 = find_nbr(matrix,edge[1])
    common_nbrs = nbd1.intersection(nbd2)
    adjmatrix = np.zeros([matrix.shape[0]+1, matrix.shape[0]+1], int)
    adjmatrix[0:matrix.shape[0], 0:matrix.shape[1]] = matrix
    adjmatrix[edge[0]][edge[1]] = 0
    adjmatrix[edge[1]][edge[0]] = 0
    adjmatrix[matrix.shape[0]][edge[0]] = 1
    adjmatrix[matrix.shape[0]][edge[1]] = 1
    adjmatrix[edge[0]][matrix.shape[0]] = 1
    adjmatrix[edge[1]][matrix.shape[0]] = 1
    for vertex in common_nbrs:
        adjmatrix[vertex][matrix.shape[0]] = 1
        adjmatrix[matrix.shape[0]][vertex] = 1
    if(len(common_nbrs) == 1):
        return adjmatrix, 2 # 2 edges are added if it was external edge
    else:
        return adjmatrix, 3 # 3 edges are added if it was internal edge

def find_nbr(matrix, vertex):
    """Finds neighbour of the given vertex.

    Args:
        matrix: A matrix representing the adjacency matrix of the graph.
        vertex: An integer whose neighbours are to be found.

    Returns:
        nbr: A set representing neighbours of vertex.
    """
    nbr = set()
    for i in range(0,matrix.shape[0]):
        if(matrix[vertex][i]==1):
            nbr.add(i)
    return nbr