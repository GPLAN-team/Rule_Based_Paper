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

def get_rectangle_coordinates(room_x, room_y, room_width, room_height, nodecnt, mergednodes,irreg_nodes1):
    """Populates rectangular coordinates for each room.

    Args:
        graph: An instance of InputGraph object.
        mergednodes: A list representing nodes to be merged.
        irreg_nodes1: A list representing nodes for irregular rooms.

    Returns:
        None
    """
    room_x_bottom_right = np.zeros(nodecnt-4)
    room_x_bottom_left = np.zeros(nodecnt-4)
    room_x_top_right = np.zeros(nodecnt-4)
    room_x_top_left = np.zeros(nodecnt-4)
    room_y_right_top = np.zeros(nodecnt-4)
    room_y_left_top = np.zeros(nodecnt-4)
    room_y_right_bottom = np.zeros(nodecnt-4)
    room_y_left_bottom = np.zeros(nodecnt-4)
    for i in range(0,nodecnt-4):
        room_x_bottom_left[i] = room_x[i]
        room_x_bottom_right[i] = room_x[i]
        room_x_top_left[i] = room_x[i]+room_width[i]
        room_x_top_right[i] = room_x[i]+room_width[i]
        room_y_right_bottom[i] = room_y[i]
        room_y_right_top[i] = room_y[i]
        room_y_left_bottom[i] = room_y[i] + room_height[i]
        room_y_left_top[i] = room_y[i] + room_height[i]
    for i in range(0,len(mergednodes)):
        vertices = [irreg_nodes1[i],mergednodes[i]]
        get_direction(room_x_bottom_left
        , room_x_bottom_right
        , room_x_top_left
        , room_x_top_right
        , room_y_left_bottom
        , room_y_right_bottom
        ,room_y_left_top
        ,room_y_right_top
        ,room_x
        ,room_y
        ,room_height
        ,room_width
        ,vertices)
    return room_x_bottom_left,room_x_bottom_right,room_x_top_left,room_x_top_right,room_y_left_bottom,room_y_right_bottom,room_y_left_top,room_y_right_top

def get_direction(room_x_bottom_left
        , room_x_bottom_right
        , room_x_top_left
        , room_x_top_right
        , room_y_left_bottom
        , room_y_right_bottom
        ,room_y_left_top
        ,room_y_right_top
        ,room_x
        ,room_y
        ,room_height
        ,room_width
        ,vertices):
    """Populates rectangular coordinates for irregular rooms.

    Args:
        graph: An instance of InputGraph object.
        vertices: A list containing two vertices which need to be merged.

    Returns:
        None
    """
    if(room_y[vertices[0]] + room_height[vertices[0]] == room_y[vertices[1]]):
        if room_x[vertices[0]]>room_x[vertices[1]]:
            room_x_top_left[vertices[0]]= room_x[vertices[0]]
            room_x_bottom_left[vertices[1]]= room_x[vertices[0]]
        else:
            room_x_top_left[vertices[0]] = room_x[vertices[1]]
            room_x_bottom_left[vertices[1]]=room_x[vertices[1]]
        if room_x[vertices[0]]+room_width[vertices[0]]<room_x[vertices[1]]+room_width[vertices[1]]:
            room_x_top_right[vertices[0]] = room_x[vertices[0]] + room_width[vertices[0]]
            room_x_bottom_right[vertices[1]] = room_x[vertices[0]] + room_width[vertices[0]]
        else:
            room_x_top_right[vertices[0]] = room_x[vertices[1]]+ room_width[vertices[1]]
            room_x_bottom_right[vertices[1]]=room_x[vertices[1]]+ room_width[vertices[1]]
    elif(room_y[vertices[0]] == room_y[vertices[1]] + room_height[vertices[1]]):
        if room_x[vertices[0]]>room_x[vertices[1]]:
            room_x_bottom_left[vertices[0]]= room_x[vertices[0]]
            room_x_top_left[vertices[1]] = room_x[vertices[0]]
        else:
            room_x_bottom_left[vertices[0]]= room_x[vertices[1]]
            room_x_top_left[vertices[1]] = room_x[vertices[1]]
        if room_x[vertices[0]]+room_width[vertices[0]]<room_x[vertices[1]]+room_width[vertices[1]]:
            room_x_bottom_right[vertices[0]]= room_x[vertices[0]] + room_width[vertices[0]]
            room_x_top_right[vertices[1]] = room_x[vertices[0]] + room_width[vertices[0]]
        else:
            room_x_bottom_right[vertices[0]]= room_x[vertices[1]]+ room_width[vertices[1]]
            room_x_top_right[vertices[1]] = room_x[vertices[1]]+ room_width[vertices[1]]
    elif(room_x[vertices[0]] + room_width[vertices[0]] == room_x[vertices[1]]):
        if room_y[vertices[0]]>room_y[vertices[1]]:
            room_y_right_bottom[vertices[0]]=room_y[vertices[0]]
            room_y_left_bottom[vertices[1]]=room_y[vertices[0]]
        else:
            room_y_right_bottom[vertices[0]]= room_y[vertices[1]]
            room_y_left_bottom[vertices[1]]= room_y[vertices[1]]
        if room_y[vertices[0]]+room_height[vertices[0]]<room_y[vertices[1]]+room_height[vertices[1]]:
            room_y_right_top[vertices[0]]=room_y[vertices[0]] + room_height[vertices[0]]
            room_y_left_top[vertices[1]]=room_y[vertices[0]] + room_height[vertices[0]]
        else:
            room_y_right_top[vertices[0]]=room_y[vertices[1]]+ room_height[vertices[1]]
            room_y_left_top[vertices[1]]= room_y[vertices[1]]+ room_height[vertices[1]]
    elif(room_x[vertices[0]] == room_x[vertices[1]] + room_width[vertices[1]]):
        if room_y[vertices[0]]>room_y[vertices[1]]:
            room_y_left_bottom[vertices[0]]= room_y[vertices[0]]
            room_y_right_bottom[vertices[1]]= room_y[vertices[0]]
        else:
            room_y_left_bottom[vertices[0]]=room_y[vertices[1]]
            room_y_right_bottom[vertices[1]]=room_y[vertices[1]]
        if room_y[vertices[0]]+room_height[vertices[0]]<room_y[vertices[1]]+room_height[vertices[1]]:
            room_y_left_top[vertices[0]]=room_y[vertices[0]] + room_height[vertices[0]]
            room_y_right_top[vertices[1]]=room_y[vertices[0]] + room_height[vertices[0]]
        else:
            room_y_left_top[vertices[0]]=room_y[vertices[1]]+ room_height[vertices[1]]
            room_y_right_top[vertices[1]]=room_y[vertices[1]]+ room_height[vertices[1]]

def construct_dual(matrix, nodecnt,mergednodes,irreg_nodes1):
    """Constructs dual for a PTPG.

    Args:
        graph: An instance of InputGraph object.
        mergednodes: A list representing nodes to be merged.
        irreg_nodes1: A list representing nodes for irregular rooms.

    Returns:
        None
    """
    t1_matrix = dual.populate_t1_matrix(matrix,nodecnt)
    t2_matrix = dual.populate_t2_matrix(matrix,nodecnt)
    room_x, room_y, room_width, room_height = get_dimensions(matrix, nodecnt, t1_matrix, t2_matrix)
    room_x_bottom_left,room_x_bottom_right,room_x_top_left,room_x_top_right,room_y_left_bottom,room_y_right_bottom,room_y_left_top,room_y_right_top = get_rectangle_coordinates(room_x
        , room_y
        , room_width
        , room_height
        , nodecnt,mergednodes,irreg_nodes1)
    return room_x, room_y, room_width, room_height, room_x_bottom_left,room_x_bottom_right,room_x_top_left,room_x_top_right,room_y_left_bottom,room_y_right_bottom,room_y_left_top,room_y_right_top

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

def get_dimensions(matrix, nodecnt, t1_matrix, t2_matrix):
    """Gets dimension for each room.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        None
    """
    room_x = np.zeros(nodecnt-4)
    room_y = np.zeros(nodecnt-4)
    room_height = np.zeros(nodecnt-4)
    room_width = np.zeros(nodecnt-4)
    for node in range(matrix.shape[0]):
        if node >= nodecnt-4:
            continue
        row, col = np.where(t1_matrix[1:-1] == node)
        if row.shape[0] == 0:#remove this later
            continue
        counts = np.bincount(row)
        max_row = np.argmax(counts)
        indexes, = np.where(row == max_row)
        room_x[node] = col[indexes[0]]
        room_width[node] = col[indexes[-1]] - col[indexes[0]] + 1
        row, col = np.where(t2_matrix[:, 1:-1] == node)
        counts = np.bincount(col)
        max_col = np.argmax(counts)
        indexes, = np.where(col == max_col)
        room_y[node] = row[indexes[0]]
        room_height[node] = row[indexes[-1]] - row[indexes[0]] + 1
    return room_x, room_y, room_width, room_height