"""Shortcut Resolver Module

This module allows user to identify shortcuts (refer Documentation) in
the graph and helps in removing shortcuts if required.

This module contains the following functions:

    * sign - calculates value of (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3).
    * point_in_triangle - checks if a point is inside the triangle.
    * get_edges - returns edges of a cycle.
    * add_edge_to_cover - add edge of separating triangle to edge cover.
    * generate_alternate_graph - returns transformed graph for given graph.
    * get_graph_cover - returns edge cover of a graph.
    * get_separating_edge_cover - returns separating edge cover of the input graph.
    * get_multiple_separating_edge_covers - returns smultiple eparating edge cover of the input graph.
    * remove_separating_triangles - removes separating triangles by bisecting the cover edge.
    * handle_STs - handles separating triangles in a given adjacency matrix.

"""
import networkx as nx
import numpy as np
from shapely.geometry import Point, Polygon
import random, copy
from pythongui.filter_shape_gui import filter_shape

from matplotlib import pyplot as plt

node_positions = []
choices = []

def sign(x1, y1, x2, y2, x3, y3):
    """Calculates value of (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)

    Args:
        x1, x2, x3, y1, y2, y3

    Returns:
        (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)
    """
    return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)

def point_in_triangle(x1, y1, x2, y2, x3, y3, x, y):
    """Checks if a point is inside the triangle.

    Args:
        x, y: Coordinate of the point.
        x1, y1, x2, y2, x3, y3: Coordinates of triangle vertices.

    Returns:
        A boolean indicating if the point is inside triangle or not.
    """
    d1 = sign(x, y, x1, y1, x2, y2)
    d2 = sign(x, y, x2, y2, x3, y3)
    d3 = sign(x, y, x3, y3, x1, y1)
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)

def point_in_triangle_wrapper_nodes(node1, node2, node3, node_inner):

    x = node_positions[node_inner][0]
    y = node_positions[node_inner][1]
    x1 = node_positions[node1][0]
    y1 = node_positions[node1][1]
    x2 = node_positions[node2][0]
    y2 = node_positions[node2][1]
    x3 = node_positions[node3][0]
    y3 = node_positions[node3][1]
    
    d1 = sign(x, y, x1, y1, x2, y2)
    d2 = sign(x, y, x2, y2, x3, y3)
    d3 = sign(x, y, x3, y3, x1, y1)
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)

def get_edges(cycle, containing = None):
    
    ## Return edges of a cycle as a list of tuples containing each edge's vertices in sorted order

    edges = [tuple(sorted([cycle[i], cycle[(i+1)%len(cycle)]])) for i in range(len(cycle))]
    if(containing != None):
        containing_edges = [edge for edge in edges if containing in edge and edge[0] == containing] + [tuple(reversed(edge)) for edge in edges if containing in edge and edge[1] == containing]
        return containing_edges
    return edges

def add_edge_to_cover(edge, edge_cover, separating_triangles, separating_edges, separating_edge_to_triangles, force = False):
    """Add edge of separating triangle to edge cover.

    Args:
        edge: A list representing the edge to be removed.
        edge_cover: A list containing the edge cover.
        separating_triangles: A list of separating triangles.
        separating_edges: A list of separating triangles.
        separating_edge_to_triangles:  A dictionary of separating triangles and their edge.

    Returns:
        None
    """
    ## Add edge to edge_cover, update separating_triangles, separating_edges, separating_edge_to_triangles accordingly
    if(edge in edge_cover):
        return
    
    if(edge not in separating_edges and force == False):
        return

    edge_cover.append(edge)

    edge = (min(edge), max(edge))

    for triangle in separating_edge_to_triangles[edge]:
        ## Prior to removing triangle from separating_edge_to_triangles, all references to it must be handled
        for other_edge in get_edges(triangle):
            if(other_edge == edge or other_edge not in separating_edges):
                continue
            ## As triangle will no longer be an ST, other_edge forgets triangle
            separating_edge_to_triangles[other_edge].remove(triangle)
            if(separating_edge_to_triangles[other_edge] == []):
                ## If other_edge is no longer a separating edge, remove it
                separating_edges.remove(other_edge)
        ## Remove triangle from consideration
        separating_triangles.remove(triangle)
    separating_edge_to_triangles[edge] = []
    
    ## Edge has been handles and can be removed
    if(edge in separating_edges):
        separating_edges.remove(edge)

def generate_alternate_graph(separating_triangles, separating_edges, separating_edge_to_triangles):
    """Returns transformed graph for given graph.(Check algorithm)

    Args:
        separating_triangles: A list of separating triangles.
        separating_edges: A list of separating triangles.
        separating_edge_to_triangles:  A dictionary of separating triangles and their edge.

    Returns:
        alternate_graph: A NxGraph containing the transformed graph.
    """
    ## Generate a transformed graph where edges of STs form nodes, and each ST is represented by at least 1 edge between such nodes
    ## A node cover on this graph generates a cover of separating edges

    alternate_graph = nx.Graph()
    node_edges = set([edge for edge in separating_edges if len(separating_edge_to_triangles[edge]) > 1])

    for triangle in separating_triangles:
        edges = set(get_edges(triangle))
        non_common_edges = list(edges.difference(node_edges))
        new_edges = []
        if(len(non_common_edges) == 3):
            new_edges.append(random.choice(non_common_edges))
            non_common_edges.remove(new_edges[0])
            new_edges.append(random.choice(non_common_edges))
        elif(len(non_common_edges) == 2):
            new_edges.append(random.choice(non_common_edges))
        node_edges.update(new_edges)
    
    for triangle in separating_triangles:
        relevant_edges = list(set(get_edges(triangle)).intersection(node_edges))
        if(len(relevant_edges) == 3):
            alternate_graph.add_edges_from([(relevant_edges[0], relevant_edges[1]), (relevant_edges[1], relevant_edges[2]), (relevant_edges[2], relevant_edges[0])])
        else:
            alternate_graph.add_edge(relevant_edges[0], relevant_edges[1])
    
    return alternate_graph

def get_graph_cover(graph, cover):
    """Returns edge cover of a graph.

    Args:
        graph. A networkx graph object representing the graph.
        cover: A list containing the cover.

    Returns:
        A list containing the edge cover.
    """
    edges = list(graph.edges())
    if(edges == []):
        return cover
    
    random_edge = random.choice(edges)
    graph.remove_nodes_from(list(random_edge))
    cover.extend(list(random_edge))
    return get_graph_cover(graph, cover)

def get_separating_edge_cover(edge_cover, separating_triangles, separating_edges, separating_edge_to_triangles):
    """Returns separating edge cover of the input graph.

    Args:
        edge_cover: A list containing the edge cover.
        separating_triangles: A list of separating triangles.
        separating_edges: A list of separating triangles.
        separating_edge_to_triangles:  A dictionary of separating triangles and their edge.

    Returns:
        edge_cover: A list containing the edge cover.
    """
    ## Calls itself recursively
    ## Handles isolated STs
    ## Greedily selects separating_edge that handles the most STs, and adds it to the cover

    alternate_graph = generate_alternate_graph(separating_triangles, separating_edges, separating_edge_to_triangles)
    edge_cover = get_graph_cover(alternate_graph, edge_cover)
    return edge_cover
    
    # ## Recursive base case
    # if(separating_triangles == []):
    #     return edge_cover

    # ## Greedily find best_edge to add to cover
    # longest_length = 0
    # best_edge = separating_edges[0]
    # for edge in separating_edges:
    #     if(len(separating_edge_to_triangles[edge]) > longest_length):
    #         longest_length = len(separating_edge_to_triangles[edge])
    #         best_edge = edge
            
    # ## Add best_edge to cover
    # add_edge_to_cover(best_edge, edge_cover, separating_triangles, separating_edges, separating_edge_to_triangles)

    # ## Recursively call in order to repeat
    # get_separating_edge_cover(edge_cover, separating_triangles, separating_edges, separating_edge_to_triangles)

def get_choice(separating_triangles, separating_edges, separating_edge_to_triangles):

    possibles = []
    if(find_L_shape(separating_triangles, separating_edges, separating_edge_to_triangles)):
        possibles.append("L")
    if(find_T_shape(separating_triangles, separating_edges, separating_edge_to_triangles)):
        possibles.append("T")
    if(find_F_shape(separating_triangles, separating_edges, separating_edge_to_triangles)):
        possibles.append("F")
    if(find_C_shape(separating_triangles, separating_edges, separating_edge_to_triangles)):
        possibles.append("C")
    # if(find_weird_shape(separating_triangles, separating_edges, separating_edge_to_triangles)):
    #     possibles.append("W")
    if(find_stair_shape(separating_triangles, separating_edges, separating_edge_to_triangles)):
        possibles.append("S")
    return possibles

def get_multiple_separating_edge_covers(expected_count, separating_triangles, separating_edges, separating_edge_to_triangles, edges):
    """Returns smultiple eparating edge cover of the input graph.

    Args:
        expected_count: An integer indicating the expected number of solutions.
        separating_triangles: A list of separating triangles.
        separating_edges: A list of separating triangles.
        separating_edge_to_triangles:  A dictionary of separating triangles and their edge.

    Returns:
       covers: A list containing multiple edge covers.
    """
    covers = set()
    futility_counter = 0
    while(len(covers) < expected_count):
        separating_triangles_copy = separating_triangles.copy()
        separating_edges_copy = separating_edges.copy()
        separating_edge_to_triangles_copy = copy.deepcopy(separating_edge_to_triangles)
        edge_cover = []
        edges = []

        global choices
        funcs = {"L": find_L_shape, "T": find_T_shape, "C": find_C_shape, "F": find_F_shape, "W": find_weird_shape, "S": find_stair_shape}
        for choice in choices:
            edges = funcs[choice](separating_triangles_copy, separating_edges_copy, separating_edge_to_triangles_copy)
            for edge in edges:
                add_edge_to_cover(edge, edge_cover, separating_triangles_copy, separating_edges_copy, separating_edge_to_triangles_copy, force=True)
        # edges = find_L_shape(separating_triangles, separating_edges, separating_edge_to_triangles)
        # edges = find_T_shape(separating_triangles, separating_edges, separating_edge_to_triangles)
        # edges = find_weird_shape(separating_triangles, separating_edges, separating_edge_to_triangles)
        # edges = find_Z_shape(separating_triangles, separating_edges, separating_edge_to_triangles, edges)
        # edges = find_F_shape(separating_triangles, separating_edges, separating_edge_to_triangles)
        # edges = find_C_shape(separating_triangles, separating_edges, separating_edge_to_triangles)
        # edges = find_stair_shape(separating_triangles, separating_edges, separating_edge_to_triangles)
        separating_edge_cover = frozenset(get_separating_edge_cover(edge_cover, separating_triangles_copy, separating_edges_copy, separating_edge_to_triangles_copy))
        if(separating_edge_cover not in covers):
            futility_counter = 0
            covers.add(separating_edge_cover)
        if(futility_counter > expected_count/2):
            break
        futility_counter += 1
    return covers

def remove_separating_triangles(graph, separating_edges, edge_to_faces):
    """Removes separating triangles by bisecting the cover edge.

    Args:
        graph: A NetworkX object representing the graph.
        separating_edges: A list representing the separating edges.
        edge_to_faces: A dictionary mapping each edge to respective face.

    Returns:
        extra_nodes: A dictionary containing extra nodes added for removing separating triangle.
    """
    ## Remove separating triangles by bisecting each edge in the cover, separating_edges

    ## Get initial graph data
    origin_pos = nx.get_node_attributes(graph, 'pos')
    total_no_of_vertices = graph.number_of_nodes()
    extra_nodes = {}
    for edge in separating_edges:
        ## Bisect edge
        graph.remove_edge(edge[0], edge[1])
        position = ((origin_pos[edge[0]][0] + origin_pos[edge[1]][0]) /2, (origin_pos[edge[0]][1] + origin_pos[edge[1]][1]) /2)
        graph.add_node(total_no_of_vertices, pos = position)
        graph.add_edges_from([(total_no_of_vertices, edge[0]), (total_no_of_vertices, edge[1])])
        extra_nodes[total_no_of_vertices] = [edge[0],edge[1]]
        
        edge = (min(edge), max(edge))
        ## Handle triangulation and update edge_to_faces
        for triangle in edge_to_faces[edge]:
            ## Retriangulate graph after addition of new vertex total_no_of_vertices
            other_vertex = list(set(triangle).difference(edge))[0]
            graph.add_edge(total_no_of_vertices, other_vertex)

            ## Update edge_to_faces due to changes in faces caused by above bisection and triangulation
            new_triangle0 = sorted([other_vertex, edge[0], total_no_of_vertices])
            new_triangle1 = sorted([other_vertex, edge[1], total_no_of_vertices])
            edge_to_faces[tuple(sorted([other_vertex, edge[0]]))].remove(triangle)
            edge_to_faces[tuple(sorted([other_vertex, edge[1]]))].remove(triangle)
            edge_to_faces[tuple(sorted([other_vertex, edge[0]]))].append(new_triangle0)
            edge_to_faces[tuple(sorted([other_vertex, edge[1]]))].append(new_triangle1)

            ## Add edges from new vertex total_no_of_vertices to edge_to_faces
            if(tuple(sorted([other_vertex, total_no_of_vertices])) not in edge_to_faces):
                edge_to_faces[tuple(sorted([other_vertex, total_no_of_vertices]))] = []
            if(tuple(sorted([total_no_of_vertices, edge[0]])) not in edge_to_faces):
                edge_to_faces[tuple(sorted([total_no_of_vertices, edge[0]]))] = []
            if(tuple(sorted([total_no_of_vertices, edge[1]])) not in edge_to_faces):
                edge_to_faces[tuple(sorted([total_no_of_vertices, edge[1]]))] = []
            edge_to_faces[tuple(sorted([other_vertex, total_no_of_vertices]))] = [new_triangle0, new_triangle1]
            edge_to_faces[tuple(sorted([total_no_of_vertices, edge[0]]))].append(new_triangle0)
            edge_to_faces[tuple(sorted([total_no_of_vertices, edge[1]]))].append(new_triangle1)
        total_no_of_vertices += 1
    return extra_nodes

def find_C_shape(separating_triangles, separating_edges, separating_edge_to_triangles):

    if(separating_triangles == []):
        return []
    some_triangle = random.choice(separating_triangles)
    edges = get_edges(some_triangle, some_triangle[0])
    return edges

def find_F_shape(separating_triangles, separating_edges, separating_edge_to_triangles):

    possible_special_edges = [edge for edge in separating_edges if len(separating_edge_to_triangles[edge]) > 1]
    if(possible_special_edges == []):
        return []
    special_edge = random.choice(possible_special_edges)
    some_triangle = separating_edge_to_triangles[special_edge][0]
    edges = get_edges(some_triangle, special_edge[0])
    return edges

def find_L_shape(separating_triangles, separating_edges, separating_edge_to_triangles):

    global choices
    # choices.append("L")
    if(separating_triangles == []):
        return []
    some_triangle = random.choice(separating_triangles)
    edges = [get_edges(some_triangle)[0],]
    return edges

def find_T_shape(separating_triangles, separating_edges, separating_edge_to_triangles):

    global choices
    # choices.append("T")
    possible_special_edges = [edge for edge in separating_edges if len(separating_edge_to_triangles[edge]) > 1]
    if(possible_special_edges == []):
        return []
    special_edge = random.choice(possible_special_edges)
    edges = [special_edge,]
    return edges

def find_weird_shape(separating_triangles, separating_edges, separating_edge_to_triangles):

    possible_special_edges = [edge for edge in separating_edges if len(separating_edge_to_triangles[edge]) > 1]
    if(possible_special_edges == []):
        return []
    special_edge = random.choice(possible_special_edges)
    triangle1 = separating_edge_to_triangles[special_edge][0]
    triangle2 = separating_edge_to_triangles[special_edge][1]
    edges1 = get_edges(triangle1, special_edge[0])
    edges2 = get_edges(triangle2, special_edge[0])
    edges1.remove(special_edge)
    edges2.remove(special_edge)
    edges = edges1 + edges2
    return edges

def find_Z_shape(separating_triangles, separating_edges, separating_edge_to_triangles, edges):

    vertices_count = dict()
    for triangle in separating_triangles:
        for node in triangle:
            if(node not in vertices_count):
                vertices_count[node] = 0
            vertices_count[node] += 1
    common_vertices = [node for node in vertices_count if vertices_count[node] > 1]
    for common_vertex in common_vertices:
        relevant_triangles = [triangle for triangle in separating_triangles if common_vertex in triangle]
        relavant_other_nodes = []
        for i in range(len(relevant_triangles)):
            relavant_other_nodes.extend([edge[1] for edge in get_edges(relevant_triangles[i], common_vertex)])
        relavant_other_nodes = list(set(relavant_other_nodes))
        found = 0
        for i in range(len(relavant_other_nodes)):
            for j in range(i+1, len(relavant_other_nodes)):
                if(sorted([relavant_other_nodes[i], relavant_other_nodes[j]]) in edges and tuple(sorted([relavant_other_nodes[i], relavant_other_nodes[j], common_vertex])) not in separating_triangles):
                    found = 1
                    break
            if(found):
                break
        triangle1 = [triangle for triangle in relevant_triangles if relavant_other_nodes[i] in triangle][0]
        triangle2 = [triangle for triangle in relevant_triangles if relavant_other_nodes[j] in triangle][0]
        edge1 = [common_vertex, relavant_other_nodes[i]]
        edge2 = [common_vertex, list(set(triangle2).difference(set([common_vertex, relavant_other_nodes[j]])))[0]]
    return [tuple(edge1), tuple(edge2)]

def find_stair_shape(separating_triangles, separating_edges, separating_edge_to_triangles):

    possible_edges = [edge for edge in separating_edges if len(separating_edge_to_triangles[edge]) > 1]
    if(possible_edges == []):
        return []
    random.shuffle(possible_edges)
    for special_edge in possible_edges:
        triangle_pair = separating_edge_to_triangles[special_edge]
        extra1 = list(set(triangle_pair[0]).difference(set(triangle_pair[1])))[0]
        extra2 = list(set(triangle_pair[1]).difference(set(triangle_pair[0])))[0]
        if(point_in_triangle_wrapper_nodes(triangle_pair[0][0], triangle_pair[0][1], triangle_pair[0][2], extra2)):
            continue
        if(point_in_triangle_wrapper_nodes(triangle_pair[1][0], triangle_pair[1][1], triangle_pair[1][2], extra1)):
            continue
        break
    possible1 = get_edges(triangle_pair[0], special_edge[0])
    possible1.remove(special_edge)
    possible2 = get_edges(triangle_pair[1], special_edge[0])
    possible2.remove(special_edge)
    edge1 = possible1[0]
    edge2 = possible2[0]
    edges = [edge1, edge2]
    return edges

def handle_STs(adjacency, positions, num_expected_outputs):
    """Handles separating triangles in a given adjacency matrix.

    Args:
        adjacency: A matrix representing the adjacency matrix.
        positions: A list representing coordinates of each node.
        num_expected_outputs: An integer representing the expected number of solutions.

    Returns:
        adjacencies: A list containing the multiple modified adjacency matrices.
        extra_nodes_pair: A list containing the extra nodes added.
    """
    ## Remove separating triangles by finding a cover of separating edges, bisecting them and retriangulating the graph

    ## Input display
    graph = nx.Graph()
    num_nodes = len(adjacency)
    for i in range(num_nodes):
        graph.add_node(i, pos = positions[i])
    for row in range(num_nodes):
        for column in range(num_nodes):
            if(adjacency[row][column]):
                graph.add_edge(row, column)
    origin_pos = positions
    global node_positions
    node_positions = nx.get_node_attributes(graph, 'pos')

    # nx.draw(graph, pos=nx.get_node_attributes(graph, 'pos'), with_labels=True)
    # plt.show()

    ## Get all cycles of length 3
    all_cliques = list(nx.enumerate_all_cliques(graph))
    all_triangles = [sorted(i) for i in all_cliques if len(i) == 3]
    all_triangles = [list(triangle) for triangle in np.unique(all_triangles, axis=0)]

    trianlular_faces = []
    separating_triangles = []
    separating_edges = []       ## edges of separating triangles
    separating_edge_to_triangles = dict()
    edge_to_faces = dict()

    for face in all_triangles:
        flag = False
        for NodeID in range(num_nodes):
            if NodeID in face:
                continue

            ## Search for node within triangle
            if (point_in_triangle(origin_pos[face[0]][0], origin_pos[face[0]][1], origin_pos[face[1]][0],
                                origin_pos[face[1]][1], origin_pos[face[2]][0],
                                origin_pos[face[2]][1], origin_pos[NodeID][0], origin_pos[NodeID][1])):
                flag = True
                break

        if not flag:
            ## Add face information to edge_to_faces
            trianlular_faces.append(face)
            for edge in get_edges(face):
                if(edge not in edge_to_faces):
                    edge_to_faces[edge] = []
                edge_to_faces[edge].append(face)

        else:
            ## Add ST information to separating_triangles, separating_edges and separating_edge_to_triangles
            separating_triangle = tuple(sorted([face[0], face[1], face[2]]))
            separating_triangles.append(separating_triangle)

            edges = get_edges(face)
            separating_edges.extend(edges)

            for edge in edges:
                if(edge not in separating_edge_to_triangles):
                    separating_edge_to_triangles[edge] = []
                separating_edge_to_triangles[edge].append(separating_triangle)
        
    ## Get unique separating edges, handle STs
    separating_edges = list(set(separating_edges))
    edges = list(nx.edges(graph))
    graph_edges = [sorted(edge) for edge in edges]

    separating_triangles_copy = separating_triangles.copy()
    separating_edges_copy = separating_edges.copy()
    separating_edge_to_triangles_copy = copy.deepcopy(separating_edge_to_triangles)
    edge_cover = []
    edges = []

    global choices
    choices = []

    funcs = {"L": find_L_shape, "T": find_T_shape, "C": find_C_shape, "F": find_F_shape, "W": find_weird_shape, "S": find_stair_shape}
    while(True):
        possibles = get_choice(separating_triangles_copy, separating_edges_copy, separating_edge_to_triangles_copy)
        for choice in choices:
            if(choice in possibles):
                possibles.remove(choice)
        if(possibles == []):
            print("Choices - ", choices)
            break
        choice = filter_shape(possibles)
        # print("Type a letter to filter including shape (S - Stair, W - Weird), or N for no further preference - ", possibles)
        # choice = input().upper()
        if(choice in possibles):
            edges = funcs[choice](separating_triangles_copy, separating_edges_copy, separating_edge_to_triangles_copy)
            for edge in edges:
                add_edge_to_cover(edge, edge_cover, separating_triangles_copy, separating_edges_copy, separating_edge_to_triangles_copy, force=True)
            choices.append(choice)
        else:
            print("Choices - ", choices)
            break

    covers = list(get_multiple_separating_edge_covers(num_expected_outputs, separating_triangles, separating_edges, separating_edge_to_triangles, graph_edges))

    graphs = []
    extra_nodes_pair = []
    for i in range(len(covers)):
        graph_copy = graph.copy()
        extra_nodes = remove_separating_triangles(graph_copy, covers[i], copy.deepcopy(edge_to_faces))
        extra_nodes_pair.append(extra_nodes)
        graphs.append(graph_copy)

    # nx.draw(graph_copy, pos=nx.get_node_attributes(graph_copy, 'pos'), with_labels=True)
    # plt.show()

    adjacencies = [nx.to_numpy_array(graph).astype(int) for graph in graphs]
    return adjacencies, extra_nodes_pair

def filter_L(room_x, room_y, room_width, room_height, mergednodes, parents):
    relevant_parents = [parent for parent in parents if parents.count(parent) == 1]
    for parent in relevant_parents:
        child = mergednodes[parents.index(parent)]

        x = list(set([room_x[parent], room_x[parent] + room_width[parent], room_x[child], room_x[child] + room_width[child]]))
        y = list(set([room_y[parent], room_y[parent] + room_height[parent], room_y[child], room_y[child] + room_height[child]]))
        if(len(x) == 3 and len(y) == 3):
            return True
    return False

def filter_T(room_x, room_y, room_width, room_height, mergednodes, parents):
    relevant_parents = [parent for parent in parents if parents.count(parent) == 1]
    for parent in relevant_parents:
        child = mergednodes[parents.index(parent)]

        x = list(set([room_x[parent], room_x[parent] + room_width[parent], room_x[child], room_x[child] + room_width[child]]))
        y = list(set([room_y[parent], room_y[parent] + room_height[parent], room_y[child], room_y[child] + room_height[child]]))
        if(len(x) == 4 and len(y) == 3):
            return True
        if(len(x) == 3 and len(y) == 4):
            return True
    return False

def filter_F(room_x, room_y, room_width, room_height, mergednodes, parents):
    relevant_parents = [parent for parent in parents if parents.count(parent) == 2]
    for parent in relevant_parents:
        child_indices = [index for index, parent_elem in enumerate(parents) if parent_elem == parent]
        child1 = mergednodes[child_indices[0]]
        child2 = mergednodes[child_indices[1]]

        x_s = [room_x[parent], room_x[parent] + room_width[parent], room_x[child1], room_x[child1] + room_width[child1], room_x[child2], room_x[child2] + room_width[child2]]
        y_s = [room_y[parent], room_y[parent] + room_height[parent], room_y[child1], room_y[child1] + room_height[child1], room_y[child2], room_y[child2] + room_height[child2]]
        x = list(set(x_s))
        y = list(set(y_s))
        x_counts = tuple([x_s.count(value) for value in sorted(x)])
        y_counts = tuple([y_s.count(value) for value in sorted(y)])

        valid_combinations = set([((2,1,1,1,1), (1,3,2)), ((2,1,1,1,1), (1,3,1,1)), ((1,2,1,1,1), (2,2,2)), ((1,2,1,1,1), (2,2,1,1))])
        if((x_counts, y_counts) in valid_combinations or (x_counts[::-1], y_counts) in valid_combinations or (x_counts, y_counts[::-1]) in valid_combinations or (x_counts[::-1], y_counts[::-1]) in valid_combinations):
            return True
    return False

def filter_C(room_x, room_y, room_width, room_height, mergednodes, parents):
    relevant_parents = [parent for parent in parents if parents.count(parent) == 2]
    for parent in relevant_parents:
        child_indices = [index for index, parent_elem in enumerate(parents) if parent_elem == parent]
        child1 = mergednodes[child_indices[0]]
        child2 = mergednodes[child_indices[1]]

        x_s = [room_x[parent], room_x[parent] + room_width[parent], room_x[child1], room_x[child1] + room_width[child1], room_x[child2], room_x[child2] + room_width[child2]]
        y_s = [room_y[parent], room_y[parent] + room_height[parent], room_y[child1], room_y[child1] + room_height[child1], room_y[child2], room_y[child2] + room_height[child2]]
        x = list(set(x_s))
        y = list(set(y_s))
        x_counts = tuple([x_s.count(value) for value in sorted(x)])
        y_counts = tuple([y_s.count(value) for value in sorted(y)])

        valid_combinations = set([((2,1,1,2), (1,3,2)), ((2,1,1,2), (1,3,1,1)), ((1,2,1,2), (2,2,2)), ((1,2,1,2), (2,2,1,1)), ((1,2,2,1), (3,1,2)), ((1,2,2,1), (3,1,1,1))])
        if((x_counts, y_counts) in valid_combinations or (x_counts[::-1], y_counts) in valid_combinations or (x_counts, y_counts[::-1]) in valid_combinations or (x_counts[::-1], y_counts[::-1]) in valid_combinations):
            return True
    return False

def filter_Stair(room_x, room_y, room_width, room_height, mergednodes, parents):
    relevant_parents = [parent for parent in parents if parents.count(parent) == 2]
    for parent in relevant_parents:
        child_indices = [index for index, parent_elem in enumerate(parents) if parent_elem == parent]
        child1 = mergednodes[child_indices[0]]
        child2 = mergednodes[child_indices[1]]

        x_s = [room_x[parent], room_x[parent] + room_width[parent], room_x[child1], room_x[child1] + room_width[child1], room_x[child2], room_x[child2] + room_width[child2]]
        y_s = [room_y[parent], room_y[parent] + room_height[parent], room_y[child1], room_y[child1] + room_height[child1], room_y[child2], room_y[child2] + room_height[child2]]
        x = list(set(x_s))
        y = list(set(y_s))
        x_counts = tuple([x_s.count(value) for value in sorted(x)])
        y_counts = tuple([y_s.count(value) for value in sorted(y)])

        valid_combinations = set([((1,1,3,1), (1,1,2,2)), ((1,2,1,2), (1,2,1,2))])
        if((x_counts, y_counts) in valid_combinations or (x_counts[::-1], y_counts) in valid_combinations or (x_counts, y_counts[::-1]) in valid_combinations or (x_counts[::-1], y_counts[::-1]) in valid_combinations):
            return True
    return False

def filter(room_x, room_y, room_width, room_height, mergednodes, parents):
    global choices
    choices_copy = choices.copy()
    if("L" in choices_copy):
        present = filter_L(room_x, room_y, room_width, room_height, mergednodes, parents)
        if(present):
            choices_copy = [choice for choice in choices_copy if choice != "L"]
    if("T" in choices_copy):
        present = filter_T(room_x, room_y, room_width, room_height, mergednodes, parents)
        if(present):
            choices_copy = [choice for choice in choices_copy if choice != "T"]
    if("F" in choices_copy):
        present = filter_F(room_x, room_y, room_width, room_height, mergednodes, parents)
        if(present):
            choices_copy = [choice for choice in choices_copy if choice != "F"]
    if("C" in choices_copy):
        present = filter_C(room_x, room_y, room_width, room_height, mergednodes, parents)
        if(present):
            choices_copy = [choice for choice in choices_copy if choice != "C"]
    if("S" in choices_copy):
        present = filter_Stair(room_x, room_y, room_width, room_height, mergednodes, parents)
        if(present):
            choices_copy = [choice for choice in choices_copy if choice != "S"]
    choices_copy = [choice for choice in choices_copy if choice != "W"]
    # if("W" in choices_copy):
    #     present = 1
    #     if(present):
    #         choices_copy = [choice for choice in choices_copy if choice != "W"]
    # print("Choices not found -", choices_copy)
    if(choices_copy == []):
        return True
    return False