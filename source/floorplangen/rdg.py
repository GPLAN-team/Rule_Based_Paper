"""Rectangular Dual Generation Module

This module allows user to generate rectangular dual for a
given PTPG.

This module contains the following functions:

    * get_rectangular_coordinates - populates rectangular
                                    coordinates
    * get_direction - populates rectangular coordinates for
                      irregular rooms
    * construct_dual - constructs rectangular dual for PTPG.
    * get_dimensions - finds dimension of each room.
"""
import networkx as nx 
import numpy as np 
import source.floorplangen.dual as dual
import math

def get_rectangle_coordinates(graph,mergednodes,irreg_nodes1):
    """Populates rectangular coordinates for each room.

    Args:
        graph: An instance of InputGraph object.
        mergednodes: A list representing nodes to be merged.
        irreg_nodes1: A list representing nodes for irregular rooms.

    Returns:
        None
    """
    for i in range(0,graph.north):
        graph.room_x_bottom_left[i] = graph.room_x[i]
        graph.room_x_bottom_right[i] = graph.room_x[i]
        graph.room_x_top_left[i] = graph.room_x[i]+graph.room_width[i]
        graph.room_x_top_right[i] = graph.room_x[i]+graph.room_width[i]
        graph.room_y_right_bottom[i] = graph.room_y[i]
        graph.room_y_right_top[i] = graph.room_y[i]
        graph.room_y_left_bottom[i] = graph.room_y[i] + graph.room_height[i]
        graph.room_y_left_top[i] = graph.room_y[i] + graph.room_height[i]
    
    for i in range(0,len(mergednodes)):
        vertices = [irreg_nodes1[i],mergednodes[i]]
        get_direction(graph,vertices)


def get_direction(graph,vertices):
    """Populates rectangular coordinates for irregular rooms.

    Args:
        graph: An instance of InputGraph object.
        vertices: A list containing two vertices which need to be merged.

    Returns:
        None
    """
    if(graph.room_y[vertices[0]] + graph.room_height[vertices[0]] == graph.room_y[vertices[1]]):
        if graph.room_x[vertices[0]]>graph.room_x[vertices[1]]:
            graph.room_x_top_left[vertices[0]]= graph.room_x[vertices[0]]
            graph.room_x_bottom_left[vertices[1]]= graph.room_x[vertices[0]]
        else:
            graph.room_x_top_left[vertices[0]] = graph.room_x[vertices[1]]
            graph.room_x_bottom_left[vertices[1]]=graph.room_x[vertices[1]]
        if graph.room_x[vertices[0]]+graph.room_width[vertices[0]]<graph.room_x[vertices[1]]+graph.room_width[vertices[1]]:
            graph.room_x_top_right[vertices[0]] = graph.room_x[vertices[0]] + graph.room_width[vertices[0]]
            graph.room_x_bottom_right[vertices[1]] = graph.room_x[vertices[0]] + graph.room_width[vertices[0]]
        else:
            graph.room_x_top_right[vertices[0]] = graph.room_x[vertices[1]]+ graph.room_width[vertices[1]]
            graph.room_x_bottom_right[vertices[1]]=graph.room_x[vertices[1]]+ graph.room_width[vertices[1]]
    elif(graph.room_y[vertices[0]] == graph.room_y[vertices[1]] + graph.room_height[vertices[1]]):
        if graph.room_x[vertices[0]]>graph.room_x[vertices[1]]:
            graph.room_x_bottom_left[vertices[0]]= graph.room_x[vertices[0]]
            graph.room_x_top_left[vertices[1]] = graph.room_x[vertices[0]]
        else:
            graph.room_x_bottom_left[vertices[0]]= graph.room_x[vertices[1]]
            graph.room_x_top_left[vertices[1]] = graph.room_x[vertices[1]]
        if graph.room_x[vertices[0]]+graph.room_width[vertices[0]]<graph.room_x[vertices[1]]+graph.room_width[vertices[1]]:
            graph.room_x_bottom_right[vertices[0]]= graph.room_x[vertices[0]] + graph.room_width[vertices[0]]
            graph.room_x_top_right[vertices[1]] = graph.room_x[vertices[0]] + graph.room_width[vertices[0]]
        else:
            graph.room_x_bottom_right[vertices[0]]= graph.room_x[vertices[1]]+ graph.room_width[vertices[1]]
            graph.room_x_top_right[vertices[1]] = graph.room_x[vertices[1]]+ graph.room_width[vertices[1]]
    elif(graph.room_x[vertices[0]] + graph.room_width[vertices[0]] == graph.room_x[vertices[1]]):
        if graph.room_y[vertices[0]]>graph.room_y[vertices[1]]:
            graph.room_y_right_bottom[vertices[0]]=graph.room_y[vertices[0]]
            graph.room_y_left_bottom[vertices[1]]=graph.room_y[vertices[0]]
        else:
            graph.room_y_right_bottom[vertices[0]]= graph.room_y[vertices[1]]
            graph.room_y_left_bottom[vertices[1]]= graph.room_y[vertices[1]]
        if graph.room_y[vertices[0]]+graph.room_height[vertices[0]]<graph.room_y[vertices[1]]+graph.room_height[vertices[1]]:
            graph.room_y_right_top[vertices[0]]=graph.room_y[vertices[0]] + graph.room_height[vertices[0]]
            graph.room_y_left_top[vertices[1]]=graph.room_y[vertices[0]] + graph.room_height[vertices[0]]
        else:
            graph.room_y_right_top[vertices[0]]=graph.room_y[vertices[1]]+ graph.room_height[vertices[1]]
            graph.room_y_left_top[vertices[1]]= graph.room_y[vertices[1]]+ graph.room_height[vertices[1]]
    elif(graph.room_x[vertices[0]] == graph.room_x[vertices[1]] + graph.room_width[vertices[1]]):
        if graph.room_y[vertices[0]]>graph.room_y[vertices[1]]:
            graph.room_y_left_bottom[vertices[0]]= graph.room_y[vertices[0]]
            graph.room_y_right_bottom[vertices[1]]= graph.room_y[vertices[0]]
        else:
            graph.room_y_left_bottom[vertices[0]]=graph.room_y[vertices[1]]
            graph.room_y_right_bottom[vertices[1]]=graph.room_y[vertices[1]]
        if graph.room_y[vertices[0]]+graph.room_height[vertices[0]]<graph.room_y[vertices[1]]+graph.room_height[vertices[1]]:
            graph.room_y_left_top[vertices[0]]=graph.room_y[vertices[0]] + graph.room_height[vertices[0]]
            graph.room_y_right_top[vertices[1]]=graph.room_y[vertices[0]] + graph.room_height[vertices[0]]
        else:
            graph.room_y_left_top[vertices[0]]=graph.room_y[vertices[1]]+ graph.room_height[vertices[1]]
            graph.room_y_right_top[vertices[1]]=graph.room_y[vertices[1]]+ graph.room_height[vertices[1]]

def construct_dual(graph,mergednodes,irreg_nodes1):
    """Constructs dual for a PTPG.

    Args:
        graph: An instance of InputGraph object.
        mergednodes: A list representing nodes to be merged.
        irreg_nodes1: A list representing nodes for irregular rooms.

    Returns:
        None
    """
    graph.t1_matrix = None
    graph.t2_matrix = None
    graph.t1longestdist = [-1] * (graph.west + 1)
    graph.t2longestdist = [-1] * (graph.west + 1)
    graph.t1longestdistval = -1
    graph.t2longestdistval = -1
    graph.nspaths = []
    graph.wepaths = []

    graph.room_x = np.zeros(graph.west - 3)
    graph.room_y = np.zeros(graph.west - 3)
    graph.room_height = np.zeros(graph.west - 3)
    graph.room_width = np.zeros(graph.west - 3)
    graph.room_x_bottom_right = np.zeros(graph.west - 3)
    graph.room_x_bottom_left = np.zeros(graph.west - 3)
    graph.room_x_top_right = np.zeros(graph.west - 3)
    graph.room_x_top_left = np.zeros(graph.west - 3)
    graph.room_y_right_top = np.zeros(graph.west - 3)
    graph.room_y_left_top = np.zeros(graph.west - 3)
    graph.room_y_right_bottom = np.zeros(graph.west - 3)
    graph.room_y_left_bottom = np.zeros(graph.west - 3)
    dual.populate_t1_matrix(graph)
    dual.populate_t2_matrix(graph)
    get_dimensions(graph)
    get_rectangle_coordinates(graph,mergednodes,irreg_nodes1)

def construct_rfp(G,hor_dgph,mergednodes,irreg_nodes1):
    G.t1_matrix = None
    G.t2_matrix = None
    G.t1_longest_distance = [-1] * (G.west + 1)
    G.t2_longest_distance = [-1] * (G.west + 1)
    G.t1_longest_distance_value = -1
    G.t2_longest_distance_value = -1
    G.nspaths = []
    G.wepaths = []

    G.room_x = np.zeros(G.west - 3)
    G.room_y = np.zeros(G.west - 3)
    # G.room_height = np.zeros(G.west - 3)
    # G.room_width = np.zeros(G.west - 3)
    dual.populate_t1_matrix(G)
    dual.populate_t2_matrix(G)
    dual.get_coordinates(G,hor_dgph)
    get_rectangle_coordinates(G,mergednodes,irreg_nodes1)

def get_dimensions(graph):
    """Gets dimension for each room.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        None
    """
    for node in range(graph.matrix.shape[0]):
        if node in [graph.north, graph.east, graph.south, graph.west]:
            continue
        row, col = np.where(graph.t1_matrix[1:-1] == node)
        if row.shape[0] == 0:#remove this later
            continue
        counts = np.bincount(row)
        max_row = np.argmax(counts)
        indexes, = np.where(row == max_row)
        graph.room_x[node] = col[indexes[0]]
        graph.room_width[node] = col[indexes[-1]] - col[indexes[0]] + 1
        row, col = np.where(graph.t2_matrix[:, 1:-1] == node)
        counts = np.bincount(col)
        max_col = np.argmax(counts)
        indexes, = np.where(col == max_col)
        graph.room_y[node] = row[indexes[0]]
        graph.room_height[node] = row[indexes[-1]] - row[indexes[0]] + 1