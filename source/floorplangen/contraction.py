"""Contraction Module

This module allows user to perform contraction on a Proper Triangulated
Planar Graph (PTPG) to transform it into a trivial Regular Edge
Labelling (REL).

This module contains the following functions:

    * init_degrees - finds degree of each node in the graph.
    * init_goodnodes - finds good vertices in the graph.
    * is_goodvertex - finds if a vertex is a good vertex.
    * cntr_nbr - finds contractible neighbour of given vertex.
    * update_adjmat - updates adjacency matrix post contraction.
    * update_goodnodes - updates good vertices post contraction.
    * check - checks if a vertex is god vertex post contraction.
    * contract - performs contraction on the graph.

"""

import networkx as nx 
import numpy as np 

def init_degrees(graph):
    """Populates degrees attributes of InputGraph object.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        None
    """
    graph.degrees = [np.count_nonzero(graph.matrix[node])
     for node in range(graph.nodecnt)]

def init_goodnodes(graph):
    """Finds good vertces of the graph.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        None
    """
    graph.goodnodes = []
    for node in range(graph.matrix.shape[0]):
        if is_goodvertex(graph,node):
            graph.goodnodes.append(node)

def is_goodvertex(graph, node):
    """Checks if the given vertex is a good vertex.

    Args:
        graph: An instance of InputGraph object.
        node: An integer representing vertex to be checked.

    Returns:
        boolean: A boolean indicating if given vertex is a good vertex.
    """
    if node not in [graph.north, graph.east, graph.south, graph.west]:
        if graph.degrees[node] == 5:
            heavy_nbrcnt = 0
            nbrs, = np.where(graph.matrix[node] == 1)
            for nbr in nbrs:  
                if graph.degrees[nbr] >= 20:
                    heavy_nbrcnt += 1
            if heavy_nbrcnt <= 1:
                return True

        elif graph.degrees[node] == 4:
            heavynbr = []
            nbrs, = np.where(graph.matrix[node] == 1)
            for nbr in nbrs: 
                if graph.degrees[nbr] >= 20:
                    heavynbr.append(nbr)
            if (len(heavynbr) <= 1) \
            or (len(heavynbr) == 2 
                and graph.matrix[heavynbr[0]][heavynbr[1]] != 1):
                return True
    return False

def cntr_nbr(graph, node):
    """Finds contractible neghbour of given vertex

    Args:
        graph: An instance of InputGraph object.
        node: An integer representing vertex.

    Returns:
        nbr: An integer representing contractibl neighbour of vertex.
        mut_nbrs: A list containiing mutual neighbours of node and nbr.
    """
    nbrs, = np.where(graph.matrix[node] == 1)
    for nbr in nbrs:
        if nbr in [graph.north, graph.east, graph.south, graph.west]:
            continue
        contractible = True
        node_nbrs, = np.where(graph.matrix[nbr] == 1)
        mut_nbrs = np.intersect1d(nbrs
            , node_nbrs
            , assume_unique=True)
        if len(mut_nbrs) != 2:
            print("Input graph might contain a complex triangle.")
        for vertex in nbrs:
            if vertex in mut_nbrs or vertex == nbr:
                continue
            vertex_nbr, = np.where(graph.matrix[vertex] == 1)
            intersection = np.intersect1d(vertex_nbr
                , node_nbrs
                , assume_unique=True)
            for vertex_int in intersection:
                if vertex_int not in mut_nbrs\
                 and vertex_int != node:
                    contractible = False
                    break
            if not contractible:
                break
        if contractible:
            return nbr, mut_nbrs
    return -1, []

def update_adjmat(graph,node,nbr):
    """Updates adjacency matrix post contraction.

    Args:
        graph: An instance of InputGraph object.
        node: An integer representing vertex.
        nbr: An integer representing contractible neighbour of node.

    Returns:
        None
    """
    node_nbrs, = np.where(graph.matrix[node] == 1)
    for vertex in node_nbrs:
        graph.matrix[node][vertex] = 0
        graph.matrix[vertex][node] = 0
        if vertex != nbr:
            graph.matrix[vertex][nbr] = 1
            graph.matrix[nbr][vertex] = 1

def update_goodnodes(graph,node,nbr,mut_nbrs):
    """Updates list of good nodes post contraction.

    Args:
        graph: An instance of InputGraph object.
        node: An integer representing vertex.
        nbr: An integer representing contractible neighbour of node.
        mut_nbrs: A list containing mutual neighbours of node and nbr.

    Returns:
        None
    """
    graph.degrees[nbr] += graph.degrees[node] - 4
    graph.degrees[mut_nbrs[0]] -= 1
    graph.degrees[mut_nbrs[1]] -= 1
    graph.degrees[node] = 0
    check(graph,nbr)
    check(graph,mut_nbrs[0])
    check(graph,mut_nbrs[1])

def check(graph,node):
    """Checks if given node is good vertex post contraction.

    Args:
        graph: An instance of InputGraph object.
        node: An integer representing vertex.

    Returns:
        None
    """
    if is_goodvertex(graph,node)\
     and (node not in graph.goodnodes):
        graph.goodnodes.append(node)
    elif (not is_goodvertex(graph,node))\
     and (node in graph.goodnodes):
        graph.goodnodes.remove(node)
    

def contract(graph):
    """Performs contractio on the graph.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        node: An integer representing good vertex for contraction.
        nbr: An integer representing contractible neighbour of node.
    """
    attempts = len(graph.goodnodes)
    while attempts > 0:
        node = graph.goodnodes.pop(0)
        nbr, mut_nbrs = cntr_nbr(graph,node)
        if nbr == -1:
            graph.goodnodes.append(node)
            attempts -= 1
            continue
        graph.cntrs.append({'node': node
            , 'nbr': nbr
            , 'mut_nbrs': mut_nbrs
            , 'node_nbrs': np.where(graph.matrix[node] == 1)[0]})
        update_adjmat(graph,node,nbr)
        update_goodnodes(graph,node,nbr,mut_nbrs)
        graph.nodecnt -= 1
        graph.edgecnt -= 3
        return node, nbr
    return -1, -1





