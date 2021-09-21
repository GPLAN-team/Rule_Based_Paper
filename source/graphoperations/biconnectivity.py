"""Biconnectivity Augmentation Module

This module allows user to check if the graph is biconnected and can
make it biconnected.

This module contains the following functions:

    * is_biconnected - returns a boolean representing whether the graph
        is biconnected or not.
    * biconnect - checks if a graph needs to be biconnected 
        and returns edges to be added to make it biconnected
"""
import numpy as np
import networkx as nx


def is_biconnected(nxgraph):
    """returns a boolean representing whether the graph
     is biconnected or not.

    Args:
        nxgraph: An instance of NetworkX Graph object.

    Returns:
        boolean: indicating TRUE if biconnected, FALSE otherwise.
    """
    return nx.is_k_edge_connected(nxgraph, k=2)

def biconnect(matrix):
    """ checks if a graph needs to be biconnected 
    and returns edges to be added to make it biconnected
    
    Args:
        matrix: Adjacency matrix of the said graph.
    
    Returns:
        bicon_edges: Edges to be added to make the graph biconnected
    """
    nxgraph = nx.from_numpy_matrix(matrix)
    bicon_edges = []
    if not is_biconnected(nxgraph):
        bicon_edges = sorted((nx.k_edge_augmentation(nxgraph, k=2)))
    return bicon_edges