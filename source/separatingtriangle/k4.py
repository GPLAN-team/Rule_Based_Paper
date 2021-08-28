"""K4 Module

This module contains K4 class and allows user to remove K4
cycle from the graph.

This module contains the following functions:

    * findk4 - finds K4 cycle in the graph.
    * find_sep_tri - finds separating triangle and interior node in the K4.
    * get_edge - finds edge to be removed and case in the K4.

"""
import numpy as np
import networkx as nx
import itertools as itr
import source.graphoperations.operations as opr
import source.floorplangen.contraction as contraction

class K4:
    """A K4 class for K4 cycle in the graph.
    This class provides methods to resolve K4 cycle.

    Attributes:
        node: A list representing nodes of K4.
        sep_tri: A list representing nodes in separating triangle.
        int_node: An integer representing interior node.
        edge: A list representing edge to be removed.
        nbr_node: A list containing nodes in neighbour of removing edge.
        case: An integer representing K4 case (refer Doc).
        identified: A boolean representing if K4 is identified.
        edges: A list containing edges in K4 cycle.
    """

    def __init__(self):
        self.nodes = []
        self.sep_tri = []
        self.int_node = 0
        self.edge = []
        self.nbr_node = 0
        self.case = 0
        self.identified = 0
        self.edges = []

def findk4(graph):
    """Finds K4 cycle in the graph.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        None
    """
    digraph = graph.digraph
    nxgraph = nx.from_numpy_matrix(graph.matrix)
    cycles=[x for x in nx.enumerate_all_cliques(nxgraph) if len(x)==4 ]
    quads = []
    k4 =[]
    for cycle in cycles:
        if((cycle[0],cycle[2]) in digraph.edges and (cycle[1],cycle[3])  in digraph.edges ):
            if  not opr.list_comparer(cycle,quads,4):
                quads.append(cycle)
                temp = K4()
                temp.nodes = cycle
                sep_tri,int_node = find_sep_tri(cycle,graph)
                temp.sep_tri = sep_tri
                temp.int_node = int_node
                case,edge = get_edge(graph,temp.sep_tri)
                temp.case = case
                temp.edge = edge
                if(temp.case != 2):
                    temp.edges.append([temp.sep_tri[0],temp.sep_tri[1]])
                    temp.edges.append([temp.sep_tri[1],temp.sep_tri[2]])
                    temp.edges.append([temp.sep_tri[2],temp.sep_tri[0]])
                graph.k4.append(temp)

            

def find_sep_tri(cycle,graph):
    """Finds separating triangle and interior node in the K4 cycle.

    Args:
        cycle: A list representing the K4 cycle.
        graph: An instance of InputGraph object.

    Returns:
        sep_tri: A list representing separating triangle in K4.
        int_node: A integer representing internal node.
    """
    sep_tri =[]
    int_node = 0
    for vertex in cycle:
        contraction.init_degrees(graph)
        if(graph.degrees[vertex] == 3):
            int_node = vertex
            break
    for vertex in cycle:
        if(vertex!=int_node):
            sep_tri.append(vertex)
    return sep_tri,int_node

def get_edge(graph,sep_tri):
    """Finds edge to be removed and case in the K4 cycle.

    Args:
        graph: An instance of InputGraph object.
        sep_tri: A list representing separating triangle
                 in K4 cycle.

    Returns:
        case: An integer representing case of K4.
        edge: A list representing edge to be removed.
    """
    trngls = graph.trngls
    edge_set = [[sep_tri[0],sep_tri[1]],[sep_tri[1],sep_tri[2]],[sep_tri[2],sep_tri[0]]]
    case = 0
    edge = []
    for subset in edge_set:
        count = 0
        for triangle in trngls:
            if(subset[0] in triangle and subset[1] in triangle):
                count +=1
        if(count == 4 and [subset[0],subset[1]] != edge):
            case = 2
            edge =[subset[0],subset[1]]
            break
        if(count == 3 and [subset[0],subset[1]] != edge):
            case = 1
            edge = [subset[0],subset[1]]
    if(case == 0):
        edge = [sep_tri[0],sep_tri[1]]
    return case,edge

    
def get_nbr_nodes(graph,k4,edge):
    """Removes given k4 from the graph.

    Args:
        graph: An instance of InputGraph object.
        k4: An instance of K4 object.
        edge: A list representing edge to be removed.

    Returns:
        None
    """
    if(k4.case == 1):
        nxgraph = nx.from_numpy_matrix(graph.matrix)
        trngls=[x for x in nx.enumerate_all_cliques(nxgraph)
         if len(x)==3]
        for triangle in trngls:
            if(edge[0] in triangle and edge[1] in triangle):
                if(len([x for x in triangle if x not in k4.nodes])!=0 ):
                    k4.nbr_node = [x for x in triangle if x not in k4.nodes][0]
    elif(k4.case == 2):
        for k4s in graph.k4:
            if(k4s.case == 2 and k4s != k4):
                if(edge[0] in k4s.nodes and edge[1] in k4s.nodes):
                    k4.nbr_node = k4s.int_node
                    k4s.identified = 1


def removek4(graph,k4,edge,irreg_nodes1,irreg_nodes2,mergednodes):
    """Removes given k4 from the graph.

    Args:
        graph: An instance of InputGraph object.
        k4: An instance of K4 object.
        edge: A list representing edge to be removed.
        irreg_nodes1: A list containing irregular nodes.
        irreg_nodes2: A list containing irregular nodes.
        mergednodes: A list cintaining nodes to be merged.

    Returns:
        None
    """
    if(k4.case!= 0 and k4.identified!=1):
        get_nbr_nodes(graph,k4,edge)
        k4.identified = 1
        irreg_nodes1.append(edge[0])
        irreg_nodes2.append(edge[1])
        graph.nodecnt +=1
        adjmatrix = np.zeros([graph.nodecnt, graph.nodecnt], int)
        adjmatrix[0:graph.matrix.shape[0],0:graph.matrix.shape[1]] = graph.matrix
        mergednodes.append(graph.nodecnt-1)
        adjmatrix[edge[0]][edge[1]] = 0
        adjmatrix[edge[1]][edge[0]] = 0
        adjmatrix[graph.nodecnt-1][edge[0]] = 1
        adjmatrix[graph.nodecnt-1][edge[1]] = 1
        adjmatrix[graph.nodecnt-1][k4.int_node] = 1
        adjmatrix[graph.nodecnt-1][k4.nbr_node] = 1
        adjmatrix[edge[0]][graph.nodecnt-1] = 1
        adjmatrix[edge[1]][graph.nodecnt-1] = 1
        adjmatrix[k4.int_node][graph.nodecnt-1] = 1
        adjmatrix[k4.nbr_node][graph.nodecnt-1] = 1
        graph.edgecnt += 3
        graph.matrix = adjmatrix
        graph.north +=1
        graph.east +=1
        graph.west +=1
        graph.south +=1     
    elif(k4.case == 0):
        irreg_nodes1.append(edge[0])
        irreg_nodes2.append(edge[1])
        graph.nodecnt +=1
        adjmatrix = np.zeros([graph.nodecnt, graph.nodecnt], int)
        adjmatrix[0:graph.matrix.shape[0],0:graph.matrix.shape[1]] = graph.matrix
        mergednodes.append(graph.nodecnt-1)
        adjmatrix[edge[0]][edge[1]] = 0
        adjmatrix[edge[1]][edge[0]] = 0
        adjmatrix[graph.nodecnt-1][edge[0]] = 1
        adjmatrix[graph.nodecnt-1][edge[1]] = 1
        adjmatrix[graph.nodecnt-1][k4.int_node] = 1
        adjmatrix[edge[0]][graph.nodecnt-1] = 1
        adjmatrix[edge[1]][graph.nodecnt-1] = 1
        adjmatrix[k4.int_node][graph.nodecnt-1] = 1
        graph.edgecnt += 2
        graph.matrix = adjmatrix
        graph.north +=1
        graph.east +=1
        graph.west +=1
        graph.south +=1