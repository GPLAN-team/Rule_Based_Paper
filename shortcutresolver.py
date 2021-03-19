"""Shortcut Resolver Module

This module allows user to identify shortcuts (refer Documentation) in
the graph and helps in removing shortcuts if required.

This module contains the following functions:

    * get_shortcut - returns shortcuts in the graph.
    * remove_shortcut - removes a shortcut from the graph.
"""
import numpy as np
import networkx as nx 


def get_shortcut(graph):
    """Returns shortcuts in the input graph.

    Args:
        graph: An instance of InputGraph class.

    Returns:
        shortcuts: A list containing shortcuts of the input graph.
    """
    shortcuts =[]
    for node1 in range(0,len(graph.bdy_nodes)):
        for node2 in range(0,len(graph.bdy_nodes)):
            if(graph.matrix[graph.bdy_nodes[node1]][graph.bdy_nodes[node2]] == 1 
                and (graph.bdy_nodes[node1],graph.bdy_nodes[node2]) not in graph.bdy_edges 
                and [graph.bdy_nodes[node2],graph.bdy_nodes[node1]] not in shortcuts):
                shortcuts.append([graph.bdy_nodes[node1],graph.bdy_nodes[node2]])
    return shortcuts

def remove_shortcut(shortcut,graph,irreg_nodes1,irreg_nodes2,mergednodes):
    """Removes particular shortcut from the input graph.

    Args:
        shortcut: A list containing vertices of shortcut to be removed.
        graph: An instance of InputGraph class.
        irreg_nodes1: A list of nodes which will have irregular rooms.
        irreg_nodes2: A list of nodes which will have irregular rooms.
        mergednodes: A list of nodes which will be merged.

    Returns:
        None.
    """
    nbr_nodes =[]
    trngls = graph.trngls.copy()
    for trngl in trngls:
        if(shortcut[0] in trngl and shortcut[1] in trngl):
            for node in trngl:
                if(node not in shortcut and node not in nbr_nodes):
                    nbr_nodes.append(node)
    graph.nodecnt +=1		#extra vertex added
    adjmatrix = np.zeros([graph.nodecnt, graph.nodecnt], int)
    adjmatrix[0:graph.matrix.shape[0],0:graph.matrix.shape[1]] = graph.matrix
    irreg_nodes1.append(shortcut[0])
    irreg_nodes2.append(shortcut[1])
    mergednodes.append(graph.nodecnt-1)
    adjmatrix[shortcut[0]][shortcut[1]] = 0
    adjmatrix[shortcut[1]][shortcut[0]] = 0
    adjmatrix[graph.nodecnt-1][shortcut[0]] = 1
    adjmatrix[graph.nodecnt-1][shortcut[1]] = 1
    adjmatrix[graph.nodecnt-1][nbr_nodes[0]] = 1
    adjmatrix[graph.nodecnt-1][nbr_nodes[1]] = 1
    adjmatrix[shortcut[0]][graph.nodecnt-1] = 1
    adjmatrix[shortcut[1]][graph.nodecnt-1] = 1
    adjmatrix[nbr_nodes[0]][graph.nodecnt-1] = 1
    adjmatrix[nbr_nodes[1]][graph.nodecnt-1] = 1
    graph.edgecnt += 3
    graph.matrix = adjmatrix
    graph.north +=1
    graph.east +=1
    graph.west +=1
    graph.south +=1