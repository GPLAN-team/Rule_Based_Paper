"""Performs contraction on 4-connected Proper Triangulated Planar Graph (PTPG) to transform into a trivial Regular Edge Labelling (REL)

"""
import networkx as nx 
import numpy as np 

def initialize_degrees(graph):
    """Finds the degree of each vertex in the graph and populates the degreees atribute of PTPG object.

    Args:
        graph: an instance of PTPG object

    Returns:
        void

    """
    graph.degrees = [np.count_nonzero(graph.matrix[node]) for node in range(graph.node_count)]

def initialize_good_vertices(graph):
    """Finds the good vertices of the graph and populates the good_vertices attribute in the PTPG object.

    Args:
        graph: an instance of PTPG object

    Returns:
        void


    """
    graph.good_vertices = []
    for node in range(graph.matrix.shape[0]):
        if is_good_vertex(graph,node):
            graph.good_vertices.append(node)

"""
    Definitions:
    1) Light vertex: vertex whose degree <= 19
    2) Heavy vertex: vertex whose degree >= 20
    3) Degree 5 good vertex: (vertex who has degree 5) and (has 0 or 1  heavy neighbours)
    4) Degree 4 good vertex: (vertex who has degree 4) and
                             ((has 0 or 1 heavy neighbour) or (has 2 heavy neighbours which are not adjacent))
    5) Good vertex: Degree 4 good vertex or Degree 5 good vertex
    Note: We do not want any of the 4 boundary NESW vertices to be a good vertex since we never want to contract
        any edge connected to these vertices. LookUp: Assusmption 1 for detailed reason
"""
def is_good_vertex(graph, node):
    
    """Checks if the given vertex is a good vertex or not.

    Args:
        graph: an instance of PTPG object
        node: vertex

    Returns:
        boolean: representing if vertex is good vertex or not


    """

    if node not in [graph.north, graph.east, graph.south, graph.west]:
        if graph.degrees[node] == 5:
            heavy_neighbour_count = 0
            neighbours, = np.where(graph.matrix[node] == 1)
            for neighbour in neighbours:  # iterating over neighbours and checking if any of them is heavy vertex
                if graph.degrees[neighbour] >= 20:
                    heavy_neighbour_count += 1
            if heavy_neighbour_count <= 1:
                return True  # satisfies all conditions for degree 5 good vertex

        elif graph.degrees[node] == 4:
            heavy_neighbours = []
            neighbours, = np.where(graph.matrix[node] == 1)
            for neighbour in neighbours:  # iterating over neighbours and checking if any of them is heavy vertex
                if graph.degrees[neighbour] >= 20:
                    heavy_neighbours.append(neighbour)
            if (len(heavy_neighbours) <= 1) or (
                    len(heavy_neighbours) == 2 and graph.matrix[heavy_neighbours[0]][heavy_neighbours[1]] != 1):
                return True  # satisfies all conditions for degree 4 good ertex
    return False

def get_contractible_neighbour(graph, v):

    """Finds the contractible neighbour for a given vertex along with common neighbours 

    Args:
        graph: an instance of PTPG object
        v: vertex

    Returns:
        u: contractible neighbour of vertex v; -1 in case of no contractible neighbour
        y_and_z: list containing common neighbours for vertex v and u; empty list in case of no contractib;e neighbour

    Raises:
        Error: A complex triangle exists in the graph
    """

    v_nbr, = np.where(graph.matrix[v] == 1)
    # checking if any of neighbors of the good vertex v is contractible
    # by lemma we will find one but it can be one of nesw so we need to ignore this v
    for u in v_nbr:
        if u in [graph.north, graph.east, graph.south, graph.west]:
            continue
        contractible = True
        u_nbr, = np.where(graph.matrix[u] == 1)
        y_and_z = np.intersect1d(v_nbr, u_nbr, assume_unique=True)
        if len(y_and_z) != 2:
            print("Input graph might contain a complex triangle")
        for x in v_nbr:
            if x in y_and_z or x == u:
                continue
            x_nbr, = np.where(graph.matrix[x] == 1)
            intersection = np.intersect1d(x_nbr, u_nbr, assume_unique=True)
            for node in intersection:
                if node not in y_and_z and node != v:
                    contractible = False
                    break
            if not contractible:
                break
        if contractible:
            return u, y_and_z
    return -1, []

def update_adjacency_matrix(graph, v, u):
    """Removes the vertex v from the graph and connect its adjacencies to vertex u (Base of contraction)

    Args:
        graph: an instance of PTPG object
        v: vertex to be removed
        u: contractible neighbour vertex of v

    Returns:
        void

    """
    v_nbr, = np.where(graph.matrix[v] == 1)
    for node in v_nbr:
        graph.matrix[v][node] = 0
        graph.matrix[node][v] = 0
        if node != u:
            graph.matrix[node][u] = 1
            graph.matrix[u][node] = 1

def update_good_vertices(graph, v, u, y_and_z):
    graph.degrees[u] += graph.degrees[v] - 4
    graph.degrees[y_and_z[0]] -= 1
    graph.degrees[y_and_z[1]] -= 1
    graph.degrees[v] = 0
    check(graph,u)
    check(graph,y_and_z[0])
    check(graph,y_and_z[1])

def check(graph,node):
    if is_good_vertex(graph,node) and (node not in graph.good_vertices):
        graph.good_vertices.append(node)
    elif (not is_good_vertex(graph,node)) and (node in graph.good_vertices):
        graph.good_vertices.remove(node)
    

def contract(graph):
    attempts = len(graph.good_vertices)
    while attempts > 0:
        v = graph.good_vertices.pop(0)
        u, y_and_z = get_contractible_neighbour(graph,v)
        if u == -1:
            graph.good_vertices.append(v)
            attempts -= 1
            continue
        graph.contractions.append({'v': v, 'u': u, 'y_and_z': y_and_z, 'v_nbr': np.where(graph.matrix[v] == 1)[0]})
        update_adjacency_matrix(graph,v, u)
        update_good_vertices(graph,v, u, y_and_z)
        graph.node_count -= 1
        graph.edge_count -= 3
        return v, u
    return -1, -1





