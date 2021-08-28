"""Dual Module

This module allows user to populate t1 and t2 matrix which
are used for generation of rectangular floorplans.

This module contains the following functions:

    * populate_t1_matrix - populates t1_matrix.
    * get_n_s_paths - finds north-south paths in the graph.
    * get_t1_ordered_children - obtain t1 children for given vertex.
    * populate_t2_matrix - populates t2_matrix.
    * get_w_e_paths - finds west-east paths in the graph.
    * get_t2_ordered_children - obtain t2 children for given vertex.

"""
import networkx as nx 
import numpy as np 
import source.graphoperations.operations as opr

def populate_t1_matrix(graph):
    """Populates t1_matrix attribute of InputGraph object.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        None
    """
    get_n_s_paths(graph,graph.south, [graph.south])
    graph.t1_matrix = np.empty((0, graph.t1longestdistval + 1), int)
    row_index = 0
    for path in graph.nspaths:
        is_valid_path = True
        row = [-1] * (graph.t1longestdistval + 1)
        path_index = 0
        current_vertex = path[path_index]
        for distance in range(graph.t1longestdistval + 1):
            if path_index + 1 < len(path) and graph.t1longestdist[path[path_index + 1]] <= distance:
                path_index += 1
                current_vertex = path[path_index]
            if row_index != 0 and graph.t1_matrix[row_index - 1][distance] != current_vertex \
                    and current_vertex in graph.t1_matrix[:, distance]:
                is_valid_path = False
                break
            row[distance] = current_vertex
        if is_valid_path:
            graph.t1_matrix = np.append(graph.t1_matrix, [row], axis=0)
            row_index += 1
    graph.t1_matrix = graph.t1_matrix.transpose()

# while populating the t1_matrix we need N-S paths such that they are obtained in a DFS ordered manner with children
# obtained in anticlockwise direction..... but in the REL we have S-N paths... so we construct the S-N path with
# children obtained in clockwise direction and reverse the path when we reach N.
def get_n_s_paths(graph, source, path):
    """Obtain north-south paths in the graph.

    Args:
        graph: An instance of InputGraph object.
        source: An integer representing the source vertex.
        path: A list containing paths.

    Returns:
        None
    """
    if source == graph.north: # base case of this recursive function as every S-N ends at N

        # making a deep copy of the path array as it changes during the recursive calls and wew want o save the
        # current state of this array
        path_deep_copy = [i for i in path]

        path_deep_copy.reverse() # reversing the array to get N-S path from the S-N path

        #iterating over the nodes in path and updating their longest distance from north
        for i in range(len(path_deep_copy)):
            node = path_deep_copy[i]
            graph.t1longestdist[node] = max(graph.t1longestdist[node], i) # index i represent the distance of node from north
            # updating the length of the longest N-S path
            graph.t1longestdistval = max(graph.t1longestdistval, graph.t1longestdist[node])

        # adding this path in the n_s_paths
        graph.nspaths.append(path_deep_copy)
        return

    # if we have not reached north yet then we get the children of the current source node and continue this DFS
    # to reach N from each children
    ordered_children = get_t1_ordered_children(graph,source)
    for child in ordered_children:
        path.append(child)
        get_n_s_paths(graph,child, path)
        path.remove(child)

def get_t1_ordered_children(graph, centre):
    """Obtain children of the node in south-north direction for t1 matrix.

    Args:
        graph: An instance of InputGraph object.
        centre: An integer representing the source vertex.

    Returns:
        ordered_children: A list containing ordered children of the vertex.
    """
    ordered_nbrs = opr.order_nbrs(graph,centre, cw=True)
    index = 0
    ordered_children = []
    if centre == graph.south:
        return ordered_nbrs
    while graph.matrix[ordered_nbrs[index]][centre] != 3:
        index = (index + 1) % len(ordered_nbrs)
    while graph.matrix[ordered_nbrs[index]][centre] == 3:
        index = (index + 1) % len(ordered_nbrs)
    while graph.matrix[centre][ordered_nbrs[index]] == 2:
        ordered_children.append(ordered_nbrs[index])
        index = (index + 1) % len(ordered_nbrs)
    return ordered_children

def populate_t2_matrix(graph):
    """Populates t2_matrix attribute of InputGraph object.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        None
    """
    get_w_e_paths(graph,graph.west, [graph.west])
    graph.t2_matrix = np.empty((0, graph.t2longestdistval + 1), int)
    row_index = 0
    for path in graph.wepaths:
        is_valid_path = True
        row = [-1] * (graph.t2longestdistval + 1)
        path_index = 0
        current_vertex = path[path_index]
        for distance in range(graph.t2longestdistval + 1):
            if path_index + 1 < len(path) and graph.t2longestdist[path[path_index + 1]] <= distance:
                path_index += 1
                current_vertex = path[path_index]
            if row_index != 0 and graph.t2_matrix[row_index - 1][distance] != current_vertex \
                    and current_vertex in graph.t2_matrix[:, distance]:
                is_valid_path = False
                break
            row[distance] = current_vertex
        if is_valid_path:
            graph.t2_matrix = np.append(graph.t2_matrix, [row], axis=0)
            row_index += 1

def get_w_e_paths(graph, source, path):
    """Obtain west-east paths in the graph.

    Args:
        graph: An instance of InputGraph object.
        source: An integer representing the source vertex.
        path: A list containing paths.

    Returns:
        None
    """
    graph.t2longestdist[source] = max(graph.t2longestdist[source], len(path) - 1)
    graph.t2longestdistval = max(graph.t2longestdistval, graph.t2longestdist[source])
    if source == graph.east:
        path_deep_copy = [i for i in path]
        graph.wepaths.append(path_deep_copy)
        return
    ordered_children = get_t2_ordered_children(graph,source)
    for child in ordered_children:
        path.append(child)
        get_w_e_paths(graph,child, path)
        path.remove(child)

def get_t2_ordered_children(graph, centre):
    """Obtain children of the node in west-east direction for t1 matrix.

    Args:
        graph: An instance of InputGraph object.
        centre: An integer representing the source vertex.

    Returns:
        ordered_children: A list containing ordered children of the vertex.
    """
    ordered_nbrs = opr.order_nbrs(graph,centre, cw=True)
    index = 0
    ordered_children = []
    if centre == graph.west:
        return ordered_nbrs
    while graph.matrix[centre][ordered_nbrs[index]] != 2:
        index = (index + 1) % len(ordered_nbrs)
    while graph.matrix[centre][ordered_nbrs[index]] == 2:
        index = (index + 1) % len(ordered_nbrs)
    while graph.matrix[centre][ordered_nbrs[index]] == 3:
        ordered_children.append(ordered_nbrs[index])
        index = (index + 1) % len(ordered_nbrs)
    return ordered_children

def get_coordinates(graph,hor_dgph):
        
        def ismember(d, k):
            return [1 if (i == k) else 0 for i in d]

        def any(A):
            for i in A:
                if i != 0:
                    return 1
            return 0

        def find_sp(arr):
            for i in range(0,len(arr)):
                if arr[i]==1:
                    return [i+1]
            return [0]

        def find(arr):
            for i in range(0,len(arr)):
                if arr[i]==1:
                    return [i]
            return [0]

        hor_dgph=np.array(hor_dgph)
        hor_dgph=hor_dgph.transpose()
        xmin=float(0)
        ymin=float(0)
        B=np.array(graph.encoded_matrix)
        m=len(B[0])
        n=len(B)
        N=np.amax(B)+1
        rect_drawn=[]
        # C = np.zeros((n,m))
        # for i in range(0,m):
        #     temp = len(np.unique(np.transpose(B[i])))
        #     for j in range(0,temp):
        #         C[j][i] = np.unique(np.transpose(B[i]))[j]
        # print(C)


        j=0
        C=[[-1 for i in range(0,len(B[0]))] for i in range(0,len(B))]
        # print(C)
        while j<len(B[0]):
            rows=[]
            for i in range(0,len(B)):
                if B[i][j] not in rows:
                    rows.append(B[i][j])
            k=0
            for k in range(0,len(rows)):
                C[k][j]=rows[k]
            j+=1
        # print(C)


        # for i in range(0,len(C)):
        #     for j in range(0,len(C[0])):
        #         C[i][j] +=1
        xR=np.zeros((N),float)
        for i in range(0,m):
            xmax=np.zeros((N),float)
            ymin=0
            for j in range(0,n):
                if C[j][i]==-1:
                    break
                else:
                    if any(ismember(rect_drawn,C[j][i])):
                        ymin = ymin + graph.room_height[C[j][i]]
                        xmax=np.zeros((N),float)
                        xmax[0]=xR[C[j][i]]
                        continue
                    else:
                        if not any(find_sp(hor_dgph[C[j][i]])):
                            ymin=ymin
                        else:
                            l=find(hor_dgph[C[j][i]])
                            xmin=xR[l]
                    graph.room_x[C[j][i]],graph.room_y[C[j][i]]=xmin,ymin #-graph.room_height[C[j][i]]  #not subtracting height because code requires top left corner
                    rect_drawn.append(C[j][i])
                    xmax[C[j][i]]=xmin+graph.room_width[C[j][i]]
                    xR[C[j][i]]=xmax[C[j][i]]
                    ymin = ymin + graph.room_height[C[j][i]]
            xmax=xmax[xmax!=0]
            xmin=min(xmax)
