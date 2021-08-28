"""Triangularity Module

This module allows user to triangulate a given biconnected
planar graph.

This module contains the following functions:

    * make_chordal - finds edges to be added to
                     make graph triangulated.
    * chk_chordality - checks if the graph is chordal.
    * triangulate - triangulates a given graph.
    * addedges - adds given edge to the graph.
"""   

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms.components import connected_components
from networkx.utils import arbitrary_element, not_implemented_for


def make_chordal(nxgraph):
    """Finds edges to be added to make graph triangulated.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        edges: A list representing edges to be added.
    """
    nxgraphcopy = nxgraph.copy()
    alpha = {node: 0 for node in nxgraphcopy}
    if nx.is_chordal(nxgraphcopy):
        return []
    chords = set()
    weight = {node: 0 for node in nxgraphcopy.nodes()}
    unnumbered_nodes = list(nxgraphcopy.nodes())
    for i in range(len(nxgraphcopy.nodes()), 0, -1):
        z = max(unnumbered_nodes, key=lambda node: weight[node])
        unnumbered_nodes.remove(z)
        alpha[z] = i
        update_nodes = []
        for y in unnumbered_nodes:
            if nxgraph.has_edge(y, z):
                update_nodes.append(y)
            else:
                y_weight = weight[y]
                lower_nodes = [
                    node for node in unnumbered_nodes if weight[node] < y_weight
                ]
                if nx.has_path(nxgraphcopy.subgraph(lower_nodes + [z, y]), y, z):
                    update_nodes.append(y)
                    chords.add((z, y))
        for node in update_nodes:
            weight[node] += 1
    nxgraphcopy.add_edges_from(chords)
    edges=chords
    return edges

def chk_chordality(nxgraph):
    """Checks chordality of a given graph.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        boolean: A boolean representing if graph
                 requires triangulation.
    """
    if nx.is_chordal(nxgraph):
        return True
    else:
        triad_cliques=[x for x in nx.enumerate_all_cliques(nxgraph) if len(x)==3]
        if (len(triad_cliques)+len(nxgraph.nodes())-len(nxgraph.edges())==1):
            return True
        return False


def triangulate(graph):
    """Triangulates a given input graph.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        None
    """
    nxgraph = nx.from_numpy_matrix(graph.matrix)
    alpha = {node: 0 for node in nxgraph}
    list=[]
    if not chk_chordality(nxgraph):
        graph.trng_edges= make_chordal(nxgraph)

def addedge(graph,edge):
    """Adds extra edges to the graph.

    Args:
        graph: An instance of InputGraph object.
        edge: A list representing the edge to be added.

    Returns:
        None
    """
    graph.edgecnt +=1
    graph.matrix[edge[0]][edge[1]] = 1
    graph.matrix[edge[1]][edge[0]] = 1