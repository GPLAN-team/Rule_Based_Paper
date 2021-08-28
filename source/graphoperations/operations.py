"""Graph Theoretical Operations Module

This module allows user to perform different graph theoretical operations
on InputGraph class object.

This module contains the following functions:
    * list_comparer - checks if there exists an element in list 2
                      whose intersection with list 2 is of given 
                      size.
    * get_directed - returns a directed graph.
    * get_trngls - returns all triangles in the graph.
    * get_bdy - returns outer boundary of the graph.
    * ordered_nbr_label - returns label of ordered 
                          neighbour of the vertex.
    * ordered_nbr - returns ordered neighbour 
                    of the vertex.
    * order_nbrs - returns ordered neighbours around
                   a given vertex.
"""
import numpy as np
import networkx as nx 


def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3
 
def list_comparer(lst1,lst2,size):
    """Checks if there exists an element in liat 2
       whoae intersectioj with list 1 is of given size. 

    Args:
        lst1: A list containing elements of list 1.
        lst2: A list containing elements of list 2.
        size: An integer representing size to be compared.

    Returns:
        boolena: A boolean representing if such an element exists.
    """
    for elem in lst2:
        if(len(intersection(lst1,elem)) == size):
            return True
    return False

def get_directed(graph):
    """Returns a directed graph of the input graph.

    Args:
        graph: An instance of InputGraph class.

    Returns:
        digraph: A networkx directed graph of the input graph.
    """
    digraph = nx.from_numpy_matrix(graph.matrix,create_using=nx.DiGraph)
    return digraph


def get_trngls(graph):
    """Returns all triangular cycles in a graph.

    Args:
        graph: An instance of InputGraph class.

    Returns:
        trngles: A list containing all triangular cycles in the graph.
    """
    nxgraph = nx.from_numpy_matrix(graph.matrix)
    all_cliques= nx.enumerate_all_cliques(nxgraph)
    trngles=[x for x in all_cliques if len(x)==3 ]
    return trngles

def get_bdy(graph):
    """Returns outer boundary of the graph.

    Args:
        graph: An instance of InputGraph class.

    Returns:
        bdy_nodes: A list containing nodes on the outer boundary.
        bdy_edges: A list containing edges on the outer boundary.
    """
    trngls = graph.trngls
    digraph = get_directed(graph)
    bdy_edges = []
    for edge in digraph.edges:
        count = 0
        for trngl in trngls:
            if edge[0] in trngl and edge[1] in trngl:
                count += 1
        if count == 1:
            bdy_edges.append(edge)
    bdy_nodes = []
    for edge in bdy_edges:
        if edge[0] not in bdy_nodes:
            bdy_nodes.append(edge[0])
        if edge[1] not in bdy_nodes:
            bdy_nodes.append(edge[1])
    return bdy_nodes,bdy_edges




def ordered_nbr_label(graph, centre, nbr, cw=False):
    """Returns label of ordered neighbour of the vertex.

    Args:
        graph: An instance of InputGraph class.
        centre: An integer indicating representing the vertex.
        nbr: An integer represening neighbour of the vertex.
        cw: A boolean representing direction to move.

    Returns:
        integer: An integer representing label (2 or 3).
    """
    next = ordered_nbr(graph,centre, nbr, cw)
    if graph.matrix[centre][next] == 2 or graph.matrix[next][centre] == 2:
        return 2
    else:
        return 3

def ordered_nbr(graph, centre, nbr, cw=False):
    """Returns ordered neighbour of the vertex.

    Args:
        graph: An instance of InputGraph class.
        centre: An integer indicating representing the vertex.
        nbr: An integer represening neighbour of the vertex.
        cw: A boolean representing direction to move.

    Returns:
        integer: An integer representing ordered neighbour.
    """
    ordered_nbrs = order_nbrs(graph,centre, cw)
    return ordered_nbrs[(ordered_nbrs.index(nbr) + 1) % len(ordered_nbrs)]

def order_nbrs(graph, centre, cw=False):
    """Returns neighbour of the vertex in ordered fashion.

    Args:
        graph: An instance of InputGraph class.
        centre: An integer indicating representing the vertex.
        cw: A boolean representing direction to move.

    Returns:
        ord_set: A list representing ordered neighbours of the vertex.
    """  
    vertex_set = np.concatenate([np.where(np.logical_or(graph.matrix[centre] == 2
        ,graph.matrix[centre] == 3))[0]
        ,np.where(np.logical_or(graph.matrix[:, centre] == 2
        ,graph.matrix[:, centre] == 3))[0]]).tolist()
    ord_set = [vertex_set.pop(0)]
    while len(vertex_set) != 0:
        for i in vertex_set:
            if graph.matrix[ord_set[len(ord_set) - 1]][i] != 0 \
                    or graph.matrix[i][ord_set[len(ord_set) - 1]] != 0:
                ord_set.append(i)
                vertex_set.remove(i)
                break
            elif graph.matrix[ord_set[0]][i] != 0 \
            or graph.matrix[i][ord_set[0]] != 0:
                ord_set.insert(0, i)
                vertex_set.remove(i)
                break
    current = 0
    if centre == graph.south:
        if graph.matrix[graph.west][ord_set[0]] != 0:
            ord_set.reverse()
    elif centre == graph.west:
        if graph.matrix[ord_set[0]][graph.north] != 0:
            ord_set.reverse()
    elif graph.matrix[centre][ord_set[0]] == 2:
        while graph.matrix[centre][ord_set[current]] == 2:
            current += 1
        if graph.matrix[centre][ord_set[current]] == 3:
            ord_set.reverse()
    elif graph.matrix[ord_set[0]][centre] == 3:
        while graph.matrix[ord_set[current]][centre] == 3:
            current += 1
        if graph.matrix[centre][ord_set[current]] == 2:
            ord_set.reverse()
    elif graph.matrix[ord_set[0]][centre] == 2:
        while graph.matrix[ord_set[current]][centre] == 2:
            current += 1
        if graph.matrix[ord_set[current]][centre] == 3:
            ord_set.reverse()
    elif graph.matrix[centre][ord_set[0]] == 3:
        while graph.matrix[centre][ord_set[current]] == 3:
            current += 1
        if graph.matrix[ord_set[current]][centre] == 2:
            ord_set.reverse()
    if cw:
        ord_set.reverse()
    return ord_set


def get_encoded_matrix(graph):
    encoded_matrix =  np.zeros((graph.t2_matrix.shape[0],graph.t1_matrix.shape[1]), int)
    room_width = np.array(graph.room_width, dtype='int')
    room_height = np.array(graph.room_height, dtype='int')
    room_x = np.array(graph.room_x, dtype='int')
    room_y = np.array(graph.room_y, dtype='int')
    for node in range(graph.matrix.shape[0]-4):
        for width in range(room_width[node]):
            for height in range(room_height[node]):
                encoded_matrix[room_y[node]+height][room_x[node]+width] = node
    return encoded_matrix

def is_complex_triangle(graph):
    for node in range(0,graph.original_node_count):
        value = np.count_nonzero(graph.matrix[node])
        if(value <4):
            return True
    H = nx.from_numpy_matrix(graph.matrix,create_using=nx.DiGraph)
    all_cycles = list(nx.simple_cycles(H))
    all_triangles = 0
    for cycle in all_cycles:
        if len(cycle) == 3:
            all_triangles+=1
    vertices = graph.matrix.shape[0]
    edges = int(np.count_nonzero(graph.matrix)/2)
    if(int(all_triangles/2) == (edges-vertices + 1)):
        return False
    else:
        return True

def ordered_bdy(graph):
    """Returns ordered boundary of the input graph.

    Args:
        graph: An instance of InputGraph class.

    Returns:
        ordered_bdy: A list containing boundary nodes in circular order.
    """
    bdy_nodes = get_bdy(graph)[0]
    bdy_edges = get_bdy(graph)[1]
    ordered_bdy = [bdy_nodes[0]]
    while(len(ordered_bdy) != len(bdy_nodes)):
        temp = ordered_bdy[len(ordered_bdy)-1]
        for vertex in bdy_nodes:
            if((temp,vertex) in bdy_edges
             and vertex not in ordered_bdy):
                ordered_bdy.append(vertex)
                break
    return ordered_bdy

def find_possible_boundary(boundary):
    list_of_boundaries = []
    for i in boundary:
        index = boundary.index(i)
        temp1 = boundary[0:index]
        temp2 = boundary[index:len(boundary)]
        temp = temp2 + temp1
        temp.append(temp[0])
        list_of_boundaries.append(temp)
        # print(list_of_boundaries)
    return list_of_boundaries

def calculate_area(graph,to_be_merged_vertices,rdg_vertices):
    for i in range(graph.room_x.shape[0]):
        if graph.room_width[i] == 0 or i in graph.biconnected_vertices or i in to_be_merged_vertices:
            continue
        area = graph.room_width[i]*graph.room_height[i]
        if(i in rdg_vertices):
            area+= graph.room_width[to_be_merged_vertices[rdg_vertices.index(i)]]*graph.room_height[to_be_merged_vertices[rdg_vertices.index(i)]]
        graph.area.append(round(area,3))

