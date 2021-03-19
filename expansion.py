"""Expansion Module

This module allows user to perform expansion on a trivial 
Regular Edge Labelling (REL) to transform it into a
complete Regular Edge Labelling (REL).

This module contains the following functions:

    * basecase - obtains the base case of the expansion step.
    * expand - performs the expansion step.
    * get_case - returns the case of expansion.
    * handle_orig_nbrs - handles the original neighbours.
    * case_a - handles case A of expansion.
    * case_b - handles case B of expansion.
    * case_c - handles case C of expansion.
    * case_d - handles case D of expansion.
    * case_e - handles case E of expansion.
    * case_f - handles case F of expansion.
    * case_g - handles case G of expansion.
    * case_h - handles case H of expansion.
    * case_i - handles case I of expansion.
    * case_j - handles case J of expansion.

"""

import networkx as nx 
import numpy as np
import operations as opr 

def basecase(graph):
    """Obtains the base case of expansion step.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        None
    """
    for node in range(graph.matrix.shape[0]):
        if graph.matrix[graph.north][node] == 1\
         and node not in [graph.east,graph.west]:
            graph.matrix[node][graph.north] = 2
            graph.matrix[graph.north][node] = 0
            graph.matrix[graph.south][node] = 2
            graph.matrix[node][graph.south] = 0
            graph.matrix[node][graph.east] = 3
            graph.matrix[graph.east][node] = 0
            graph.matrix[graph.west][node] = 3
            graph.matrix[node][graph.west] = 0

def expand(graph):
    """Performs the process of expansion.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        None
    """
    cntr = graph.cntrs.pop()
    case = get_case(graph,cntr)
    nbr = cntr['nbr']
    node = cntr['node']
    case(graph
        ,nbr
        ,node
        ,cntr['mut_nbrs'][0]
        ,cntr['mut_nbrs'][1]
        ,cntr['node_nbrs'])

def get_case(graph,cntr):
    """Identifies the case of expansion (Refer documentation).

    Args:
        graph: An instance of InputGraph object.
        cntr: A dict representing contraction to be expanded.

    Returns:
        None
    """
    nbr = cntr['nbr']
    mut_nbrs = cntr['mut_nbrs']
    mut_nbr1 = mut_nbrs[0]
    mut_nbr2 = mut_nbrs[1]
    if graph.matrix[nbr][mut_nbr1] == 2:
        if graph.matrix[nbr][mut_nbr2] == 3:
            return case_a
        elif graph.matrix[nbr][mut_nbr2] == 2:
            vertex = mut_nbr1
            while(vertex!=mut_nbr2):
                label = opr.ordered_nbr_label(graph,nbr,vertex,cw=False)
                vertex = opr.ordered_nbr(graph,nbr,vertex,False)
                if(label == 3):
                    mut_nbrs[0], mut_nbrs[1] = mut_nbrs[1], mut_nbrs[0]
                    break
            return case_b
        elif graph.matrix[mut_nbr2][nbr] == 3:
            return case_d
        elif graph.matrix[mut_nbr2][nbr] == 2:
            return case_f
        else:
            print("ERROR")

    if graph.matrix[mut_nbr1][nbr] == 2:
        if graph.matrix[nbr][mut_nbr2] == 3:
            mut_nbrs[0], mut_nbrs[1] = mut_nbrs[1], mut_nbrs[0]
            return case_e
        elif graph.matrix[nbr][mut_nbr2] == 2:
            mut_nbrs[0], mut_nbrs[1] = mut_nbrs[1], mut_nbrs[0]
            return case_f
        elif graph.matrix[mut_nbr2][nbr] == 3:
            return case_h
        elif graph.matrix[mut_nbr2][nbr] == 2:
            vertex = mut_nbr1
            while(vertex!=mut_nbr2):
                label = opr.ordered_nbr_label(graph,nbr,vertex,cw=False)
                vertex = opr.ordered_nbr(graph,nbr,vertex,False)
                if(label == 3):
                    mut_nbrs[0], mut_nbrs[1] = mut_nbrs[1], mut_nbrs[0]
                    break
            return case_i
        else:
            print("ERROR")
            
    if graph.matrix[nbr][mut_nbr1] == 3:
        if graph.matrix[nbr][mut_nbr2] == 3:
            vertex = mut_nbr1
            while(vertex!=mut_nbr2):
                label = opr.ordered_nbr_label(graph,nbr,vertex,cw=False)
                vertex = opr.ordered_nbr(graph,nbr,vertex,False)
                if(label == 2):
                    mut_nbrs[0], mut_nbrs[1] = mut_nbrs[1], mut_nbrs[0]
                    break
            return case_c
        elif graph.matrix[nbr][mut_nbr2] == 2:
            mut_nbrs[0], mut_nbrs[1] = mut_nbrs[1], mut_nbrs[0]
            return case_a
        elif graph.matrix[mut_nbr2][nbr] == 3:
            return case_g
        elif graph.matrix[mut_nbr2][nbr] == 2:
            return case_e
        else:
            print("ERROR")

    if graph.matrix[mut_nbr1][nbr] == 3:
        if graph.matrix[nbr][mut_nbr2] == 3:
            mut_nbrs[0], mut_nbrs[1] = mut_nbrs[1], mut_nbrs[0]
            return case_g
        elif graph.matrix[nbr][mut_nbr2] == 2:
            mut_nbrs[0], mut_nbrs[1] = mut_nbrs[1], mut_nbrs[0]
            return case_d
        elif graph.matrix[mut_nbr2][nbr] == 3:
            vertex = mut_nbr1
            while(vertex!=mut_nbr2):
                label = opr.ordered_nbr_label(graph,nbr,vertex,cw=False)
                vertex = opr.ordered_nbr(graph,nbr,vertex,False)
                if(label == 2):
                    mut_nbrs[0], mut_nbrs[1] = mut_nbrs[1], mut_nbrs[0]
                    break
            return case_j
        elif graph.matrix[mut_nbr2][nbr] == 2:
            mut_nbrs[0], mut_nbrs[1] = mut_nbrs[1], mut_nbrs[0]
            return case_h
        else:
            print("ERROR")

def handle_orig_nbrs(graph,nbr,node,mut_nbr1,mut_nbr2,node_nbrs):
    """Handles original neighbours in contraction.

    Args:
        graph: An instance of InputGraph object.
        nbr: An integer representing neighbour in contraction.
        node: An integer representing node in contraction.
        mut_nbr1: An integer representing mut_nbr1 in contraction.
        mut_nbr2: An integer representing mut_nbr2 in contraction.
        node_nbrs: A list representing node_nbrs in contraction

    Returns:
        None
    """
    for alpha in node_nbrs:
        if alpha != mut_nbr1 and alpha != mut_nbr2 and alpha != nbr:
            if graph.matrix[nbr][alpha] != 0:
                graph.matrix[node][alpha] = graph.matrix[nbr][alpha]
                graph.matrix[nbr][alpha] = 0
            if graph.matrix[alpha][nbr] != 0:
                graph.matrix[alpha][node] = graph.matrix[alpha][nbr]
                graph.matrix[alpha][nbr] = 0

def case_a(graph,nbr,node,mut_nbr1,mut_nbr2,node_nbrs):
    """Resolves Case A of expansion.

    Args:
        graph: An instance of InputGraph object.
        nbr: An integer representing neighbour in contraction.
        node: An integer representing node in contraction.
        mut_nbr1: An integer representing mut_nbr1 in contraction.
        mut_nbr2: An integer representing mut_nbr2 in contraction.
        node_nbrs: A list representing node_nbrs in contraction

    Returns:
        None
    """
    if opr.ordered_nbr_label(graph,nbr,mut_nbr1,cw=True) == 2:
        if opr.ordered_nbr(graph,nbr,mut_nbr1,True) in node_nbrs:
            handle_orig_nbrs(graph
                ,nbr
                ,node
                ,mut_nbr1
                ,mut_nbr2
                ,node_nbrs)
            graph.matrix[mut_nbr1][node] = 3
            graph.matrix[node][mut_nbr2] = 3
            graph.matrix[nbr][node] = 2
        else:
            handle_orig_nbrs(graph
                ,nbr
                ,node
                ,mut_nbr1
                ,mut_nbr2
                ,node_nbrs)     
            graph.matrix[node][mut_nbr1] = 2
            graph.matrix[node][mut_nbr2] = 3
            graph.matrix[node][nbr] = 2
            graph.matrix[nbr][mut_nbr1] = 0
            graph.matrix[mut_nbr1][nbr] = 3
    else:
        if opr.ordered_nbr(graph,nbr,mut_nbr1,True) in node_nbrs:
            handle_orig_nbrs(graph
                ,nbr
                ,node
                ,mut_nbr1
                ,mut_nbr2
                ,node_nbrs)
            graph.matrix[node][mut_nbr1] = 2
            graph.matrix[mut_nbr2][node] = 2
            graph.matrix[nbr][node] = 3
        else:
            handle_orig_nbrs(graph
                ,nbr
                ,node
                ,mut_nbr1
                ,mut_nbr2
                ,node_nbrs) 
            graph.matrix[nbr][mut_nbr2] = 0
            graph.matrix[mut_nbr2][nbr] = 2
            graph.matrix[node][nbr] = 3
            graph.matrix[node][mut_nbr1] = 2
            graph.matrix[node][mut_nbr2] = 3

def case_b(graph,nbr,node,mut_nbr1,mut_nbr2,node_nbrs):
    """Resolves Case B of expansion.

    Args:
        graph: An instance of InputGraph object.
        nbr: An integer representing neighbour in contraction.
        node: An integer representing node in contraction.
        mut_nbr1: An integer representing mut_nbr1 in contraction.
        mut_nbr2: An integer representing mut_nbr2 in contraction.
        node_nbrs: A list representing node_nbrs in contraction

    Returns:
        None
    """
    handle_orig_nbrs(graph
        ,nbr
        ,node
        ,mut_nbr1
        ,mut_nbr2
        ,node_nbrs)
    graph.matrix[mut_nbr2][node] = 3
    graph.matrix[node][mut_nbr1] = 3
    graph.matrix[nbr][node] = 2 
    

def case_c(graph,nbr,node,mut_nbr1,mut_nbr2,node_nbrs):
    """Resolves Case C of expansion.

    Args:
        graph: An instance of InputGraph object.
        nbr: An integer representing neighbour in contraction.
        node: An integer representing node in contraction.
        mut_nbr1: An integer representing mut_nbr1 in contraction.
        mut_nbr2: An integer representing mut_nbr2 in contraction.
        node_nbrs: A list representing node_nbrs in contraction

    Returns:
        None
    """
    handle_orig_nbrs(graph
        ,nbr
        ,node
        ,mut_nbr1
        ,mut_nbr2
        ,node_nbrs)
    graph.matrix[mut_nbr1][node] = 2
    graph.matrix[node][mut_nbr2] = 2
    graph.matrix[nbr][node] = 3

def case_d(graph,nbr,node,mut_nbr1,mut_nbr2,node_nbrs):
    """Resolves Case D of expansion.

    Args:
        graph: An instance of InputGraph object.
        nbr: An integer representing neighbour in contraction.
        node: An integer representing node in contraction.
        mut_nbr1: An integer representing mut_nbr1 in contraction.
        mut_nbr2: An integer representing mut_nbr2 in contraction.
        node_nbrs: A list representing node_nbrs in contraction

    Returns:
        None
    """
    if opr.ordered_nbr_label(graph,nbr,mut_nbr1,cw=False) == 2:
        if opr.ordered_nbr(graph,nbr,mut_nbr1,False) in node_nbrs:
            handle_orig_nbrs(graph
                ,nbr
                ,node
                ,mut_nbr1
                ,mut_nbr2
                ,node_nbrs)
            graph.matrix[node][mut_nbr1] = 3
            graph.matrix[mut_nbr2][node] = 3
            graph.matrix[nbr][node] = 2
        else:
            handle_orig_nbrs(graph
                ,nbr
                ,node
                ,mut_nbr1
                ,mut_nbr2
                ,node_nbrs)
            graph.matrix[nbr][mut_nbr1] = 3
            graph.matrix[node][mut_nbr1] = 2
            graph.matrix[mut_nbr2][node] = 3
            graph.matrix[node][nbr] = 2
    else:
        if opr.ordered_nbr(graph,nbr,mut_nbr1,False) in node_nbrs:
            handle_orig_nbrs(graph
                ,nbr
                ,node
                ,mut_nbr1
                ,mut_nbr2
                ,node_nbrs)
            graph.matrix[node][mut_nbr1] = 2
            graph.matrix[mut_nbr2][node] = 2
            graph.matrix[node][nbr] = 3
        else:
            handle_orig_nbrs(graph
                ,nbr
                ,node
                ,mut_nbr1
                ,mut_nbr2
                ,node_nbrs)
            graph.matrix[mut_nbr2][nbr] = 2
            graph.matrix[mut_nbr2][node] = 3
            graph.matrix[node][mut_nbr1] = 2
            graph.matrix[nbr][node] = 3

def case_e(graph,nbr,node,mut_nbr1,mut_nbr2,node_nbrs):
    """Resolves Case E of expansion.

    Args:
        graph: An instance of InputGraph object.
        nbr: An integer representing neighbour in contraction.
        node: An integer representing node in contraction.
        mut_nbr1: An integer representing mut_nbr1 in contraction.
        mut_nbr2: An integer representing mut_nbr2 in contraction.
        node_nbrs: A list representing node_nbrs in contraction

    Returns:
        None
    """
    if opr.ordered_nbr_label(graph,nbr,mut_nbr1,cw=True) == 2:
        if opr.ordered_nbr(graph,nbr,mut_nbr1,True) in node_nbrs:
            handle_orig_nbrs(graph
                ,nbr
                ,node
                ,mut_nbr1
                ,mut_nbr2
                ,node_nbrs)
            graph.matrix[node][mut_nbr1] = 3
            graph.matrix[mut_nbr2][node] = 3
            graph.matrix[node][nbr] = 2
        else:
            handle_orig_nbrs(graph
                ,nbr
                ,node
                ,mut_nbr1
                ,mut_nbr2
                ,node_nbrs)
            graph.matrix[mut_nbr2][nbr] = 3
            graph.matrix[mut_nbr2][node] = 2
            graph.matrix[node][mut_nbr1] = 3
            graph.matrix[nbr][node] = 2

    else:
        if opr.ordered_nbr(graph,nbr,mut_nbr1,True) in node_nbrs:
            handle_orig_nbrs(graph
                ,nbr
                ,node
                ,mut_nbr1
                ,mut_nbr2
                ,node_nbrs)
            graph.matrix[node][mut_nbr1] = 2
            graph.matrix[mut_nbr2][node] = 2
            graph.matrix[nbr][node] = 3
        else:
            handle_orig_nbrs(graph
                ,nbr
                ,node
                ,mut_nbr1
                ,mut_nbr2
                ,node_nbrs)
            graph.matrix[nbr][mut_nbr1] = 2
            graph.matrix[node][nbr] = 3
            graph.matrix[node][mut_nbr1] = 3
            graph.matrix[mut_nbr2][node] = 2

def case_f(graph,nbr,node,mut_nbr1,mut_nbr2,node_nbrs):
    """Resolves Case F of expansion.

    Args:
        graph: An instance of InputGraph object.
        nbr: An integer representing neighbour in contraction.
        node: An integer representing node in contraction.
        mut_nbr1: An integer representing mut_nbr1 in contraction.
        mut_nbr2: An integer representing mut_nbr2 in contraction.
        node_nbrs: A list representing node_nbrs in contraction

    Returns:
        None
    """
    if opr.ordered_nbr(graph,nbr,mut_nbr1,True) in node_nbrs:
        handle_orig_nbrs(graph
            ,nbr
            ,node
            ,mut_nbr1
            ,mut_nbr2
            ,node_nbrs)
        graph.matrix[node][mut_nbr1] = 2
        graph.matrix[mut_nbr2][node] = 2
        graph.matrix[nbr][node] = 3
    else:
        handle_orig_nbrs(graph
            ,nbr
            ,node
            ,mut_nbr1
            ,mut_nbr2
            ,node_nbrs)
        graph.matrix[node][mut_nbr1] = 2
        graph.matrix[mut_nbr2][node] = 2
        graph.matrix[node][nbr] = 3

def case_g(graph,nbr,node,mut_nbr1,mut_nbr2,node_nbrs):
    """Resolves Case G of expansion.

    Args:
        graph: An instance of InputGraph object.
        nbr: An integer representing neighbour in contraction.
        node: An integer representing node in contraction.
        mut_nbr1: An integer representing mut_nbr1 in contraction.
        mut_nbr2: An integer representing mut_nbr2 in contraction.
        node_nbrs: A list representing node_nbrs in contraction

    Returns:
        None
    """
    if opr.ordered_nbr(graph,nbr,mut_nbr1,True) in node_nbrs:
        handle_orig_nbrs(graph
            ,nbr
            ,node
            ,mut_nbr1
            ,mut_nbr2
            ,node_nbrs)
        graph.matrix[node][mut_nbr1] = 3
        graph.matrix[mut_nbr2][node] = 3
        graph.matrix[node][nbr] = 2
    else:
        handle_orig_nbrs(graph
            ,nbr
            ,node
            ,mut_nbr1
            ,mut_nbr2
            ,node_nbrs)
        graph.matrix[node][mut_nbr1] = 3
        graph.matrix[mut_nbr2][node] = 3
        graph.matrix[nbr][node] = 2

def case_h(graph,nbr,node,mut_nbr1,mut_nbr2,node_nbrs):
    """Resolves Case H of expansion.

    Args:
        graph: An instance of InputGraph object.
        nbr: An integer representing neighbour in contraction.
        node: An integer representing node in contraction.
        mut_nbr1: An integer representing mut_nbr1 in contraction.
        mut_nbr2: An integer representing mut_nbr2 in contraction.
        node_nbrs: A list representing node_nbrs in contraction

    Returns:
        None
    """
    if opr.ordered_nbr_label(graph,nbr,mut_nbr1,cw=True) == 2:
        if opr.ordered_nbr(graph,nbr,mut_nbr1,True) in node_nbrs:
            handle_orig_nbrs(graph
                ,nbr
                ,node
                ,mut_nbr1
                ,mut_nbr2
                ,node_nbrs)
            graph.matrix[node][mut_nbr1] = 3
            graph.matrix[mut_nbr2][node] = 3
            graph.matrix[node][nbr] = 2
        else:
            handle_orig_nbrs(graph
                ,nbr
                ,node
                ,mut_nbr1
                ,mut_nbr2
                ,node_nbrs)
            graph.matrix[mut_nbr1][nbr] = 0
            graph.matrix[nbr][mut_nbr1] = 3
            graph.matrix[mut_nbr1][node] = 2
            graph.matrix[mut_nbr2][node] = 3
            graph.matrix[nbr][node] = 2
    else:
        if opr.ordered_nbr(graph,nbr,mut_nbr1,True) in node_nbrs:
            handle_orig_nbrs(graph
                ,nbr
                ,node
                ,mut_nbr1
                ,mut_nbr2
                ,node_nbrs)
            graph.matrix[mut_nbr1][node] = 2
            graph.matrix[node][mut_nbr2] = 2
            graph.matrix[node][nbr] = 3
        else:
            handle_orig_nbrs(graph
                ,nbr
                ,node
                ,mut_nbr1
                ,mut_nbr2
                ,node_nbrs)
            graph.matrix[mut_nbr2][nbr] = 0
            graph.matrix[nbr][mut_nbr2] = 2
            graph.matrix[mut_nbr1][node] = 2
            graph.matrix[mut_nbr2][node] = 3
            graph.matrix[nbr][node] = 3 

def case_i(graph,nbr,node,mut_nbr1,mut_nbr2,node_nbrs):
    """Resolves Case I of expansion.

    Args:
        graph: An instance of InputGraph object.
        nbr: An integer representing neighbour in contraction.
        node: An integer representing node in contraction.
        mut_nbr1: An integer representing mut_nbr1 in contraction.
        mut_nbr2: An integer representing mut_nbr2 in contraction.
        node_nbrs: A list representing node_nbrs in contraction

    Returns:
        None
    """
    handle_orig_nbrs(graph
        ,nbr
        ,node
        ,mut_nbr1
        ,mut_nbr2
        ,node_nbrs)
    graph.matrix[mut_nbr1][node] = 3
    graph.matrix[node][mut_nbr2] = 3
    graph.matrix[node][nbr] = 2

def case_j(graph,nbr,node,mut_nbr1,mut_nbr2,node_nbrs):
    """Resolves Case J of expansion.

    Args:
        graph: An instance of InputGraph object.
        nbr: An integer representing neighbour in contraction.
        node: An integer representing node in contraction.
        mut_nbr1: An integer representing mut_nbr1 in contraction.
        mut_nbr2: An integer representing mut_nbr2 in contraction.
        node_nbrs: A list representing node_nbrs in contraction

    Returns:
        None
    """
    handle_orig_nbrs(graph
        ,nbr
        ,node
        ,mut_nbr1
        ,mut_nbr2
        ,node_nbrs)
    graph.matrix[node][mut_nbr1] = 2
    graph.matrix[mut_nbr2][node] = 2
    graph.matrix[node][nbr] = 3
