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

def populate_t1_matrix(matrix, nodecnt):
    """Populates t1_matrix attribute of InputGraph object.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        None
    """
    nspaths = []
    t1longestdistval = -1
    t1longestdist = [-1] * (nodecnt)
    t1longestdistval = get_n_s_paths(matrix, nodecnt, nodecnt - 2, [nodecnt - 2],nspaths, t1longestdist,t1longestdistval)
    t1_matrix = np.empty((0, t1longestdistval + 1), int)
    row_index = 0
    for path in nspaths:
        is_valid_path = True
        row = [-1] * (t1longestdistval + 1)
        path_index = 0
        current_vertex = path[path_index]
        for distance in range(t1longestdistval + 1):
            if path_index + 1 < len(path) and t1longestdist[path[path_index + 1]] <= distance:
                path_index += 1
                current_vertex = path[path_index]
            if row_index != 0 and t1_matrix[row_index - 1][distance] != current_vertex \
                    and current_vertex in t1_matrix[:, distance]:
                is_valid_path = False
                break
            row[distance] = current_vertex
        if is_valid_path:
            t1_matrix = np.append(t1_matrix, [row], axis=0)
            row_index += 1
    t1_matrix = t1_matrix.transpose()
    return t1_matrix

# while populating the t1_matrix we need N-S paths such that they are obtained in a DFS ordered manner with children
# obtained in anticlockwise direction..... but in the REL we have S-N paths... so we construct the S-N path with
# children obtained in clockwise direction and reverse the path when we reach N.
def get_n_s_paths(matrix, nodecnt, source, path, nspaths, t1longestdist,t1longestdistval):
    """Obtain north-south paths in the graph.

    Args:
        graph: An instance of InputGraph object.
        source: An integer representing the source vertex.
        path: A list containing paths.

    Returns:
        None
    """
    if source == nodecnt - 4: # base case of this recursive function as every S-N ends at N

        # making a deep copy of the path array as it changes during the recursive calls and we want to save the
        # current state of this array
        path_deep_copy = [i for i in path]

        path_deep_copy.reverse() # reversing the array to get N-S path from the S-N path

        #iterating over the nodes in path and updating their longest distance from north
        for i in range(len(path_deep_copy)):
            node = path_deep_copy[i]
            t1longestdist[node] = max(t1longestdist[node], i) # index i represent the distance of node from north
            # updating the length of the longest N-S path
            t1longestdistval = max(t1longestdistval, t1longestdist[node])

        # adding this path in the n_s_paths
        nspaths.append(path_deep_copy)
        return t1longestdistval

    # if we have not reached north yet then we get the children of the current source node and continue this DFS
    # to reach N from each children
    ordered_children = get_t1_ordered_children(matrix,nodecnt,source)
    for child in ordered_children:
        path.append(child)
        t1longestdistval = get_n_s_paths(matrix
                                        ,nodecnt
                                        ,child
                                        , path
                                        ,nspaths
                                        ,t1longestdist
                                        ,t1longestdistval)
        path.remove(child)
    return t1longestdistval

def get_t1_ordered_children(matrix, nodecnt, centre):
    """Obtain children of the node in south-north direction for t1 matrix.

    Args:
        graph: An instance of InputGraph object.
        centre: An integer representing the source vertex.

    Returns:
        ordered_children: A list containing ordered children of the vertex.
    """
    ordered_nbrs = opr.order_nbrs(matrix, nodecnt, centre, cw=True)
    index = 0
    ordered_children = []
    if centre == nodecnt - 2: #south
        return ordered_nbrs
    while matrix[ordered_nbrs[index]][centre] != 3:
        index = (index + 1) % len(ordered_nbrs)
    while matrix[ordered_nbrs[index]][centre] == 3:
        index = (index + 1) % len(ordered_nbrs)
    while matrix[centre][ordered_nbrs[index]] == 2:
        ordered_children.append(ordered_nbrs[index])
        index = (index + 1) % len(ordered_nbrs)
    return ordered_children

def populate_t2_matrix(matrix,nodecnt):
    """Populates t2_matrix attribute of InputGraph object.

    Args:
        graph: An instance of InputGraph object.

    Returns:
        None
    """
    wepaths = []
    t2longestdistval = -1
    t2longestdist = [-1] * (nodecnt)
    t2longestdistval = get_w_e_paths(matrix, nodecnt, nodecnt - 1, [nodecnt - 1], wepaths, t2longestdist, t2longestdistval)
    t2_matrix = np.empty((0, t2longestdistval + 1), int)
    row_index = 0
    for path in wepaths:
        is_valid_path = True
        row = [-1] * (t2longestdistval + 1)
        path_index = 0
        current_vertex = path[path_index]
        for distance in range(t2longestdistval + 1):
            if path_index + 1 < len(path) and t2longestdist[path[path_index + 1]] <= distance:
                path_index += 1
                current_vertex = path[path_index]
            if row_index != 0 and t2_matrix[row_index - 1][distance] != current_vertex \
                    and current_vertex in t2_matrix[:, distance]:
                is_valid_path = False
                break
            row[distance] = current_vertex
        if is_valid_path:
            t2_matrix = np.append(t2_matrix, [row], axis=0)
            row_index += 1
    return t2_matrix

def get_w_e_paths(matrix, nodecnt, source, path, wepaths, t2longestdist, t2longestdistval):
    """Obtain west-east paths in the graph.

    Args:
        graph: An instance of InputGraph object.
        source: An integer representing the source vertex.
        path: A list containing paths.

    Returns:
        None
    """
    t2longestdist[source] = max(t2longestdist[source], len(path) - 1)
    t2longestdistval = max(t2longestdistval, t2longestdist[source])
    if source == nodecnt - 3:
        path_deep_copy = [i for i in path]
        wepaths.append(path_deep_copy)
        return t2longestdistval
    ordered_children = get_t2_ordered_children(matrix, nodecnt, source)
    for child in ordered_children:
        path.append(child)
        t2longestdistval = get_w_e_paths(matrix, nodecnt, child, path, wepaths, t2longestdist, t2longestdistval)
        path.remove(child)
    return t2longestdistval

def get_t2_ordered_children(matrix, nodecnt, centre): 
    """Obtain children of the node in west-east direction for t1 matrix.

    Args:
        graph: An instance of InputGraph object.
        centre: An integer representing the source vertex.

    Returns:
        ordered_children: A list containing ordered children of the vertex.
    """
    ordered_nbrs = opr.order_nbrs(matrix, nodecnt, centre, cw=True)
    index = 0
    ordered_children = []
    if centre == nodecnt - 1:
        return ordered_nbrs
    while matrix[centre][ordered_nbrs[index]] != 2:
        index = (index + 1) % len(ordered_nbrs)
    while matrix[centre][ordered_nbrs[index]] == 2:
        index = (index + 1) % len(ordered_nbrs)
    while matrix[centre][ordered_nbrs[index]] == 3:
        ordered_children.append(ordered_nbrs[index])
        index = (index + 1) % len(ordered_nbrs)
    return ordered_children

def get_coordinates(encoded_matrix, nodecnt, room_width, room_height, hor_dgph):
    room_x = np.zeros(nodecnt-4)
    room_y = np.zeros(nodecnt-4)
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
    B=np.array(encoded_matrix)
    m=len(B[0])
    n=len(B)
    N=np.amax(B)+1
    rect_drawn=[]

    j=0
    C=[[-1 for i in range(0,len(B[0]))] for i in range(0,len(B))]
    while j<len(B[0]):
        rows=[]
        for i in range(0,len(B)):
            if B[i][j] not in rows:
                rows.append(B[i][j])
        k=0
        for k in range(0,len(rows)):
            C[k][j]=rows[k]
        j+=1

    xR=np.zeros((N),float)
    for i in range(0,m):
        xmax=np.zeros((N),float)
        ymin=0
        for j in range(0,n):
            if C[j][i]==-1:
                break
            else:
                if any(ismember(rect_drawn,C[j][i])):
                    ymin = ymin + room_height[C[j][i]]
                    xmax=np.zeros((N),float)
                    xmax[0]=xR[C[j][i]]
                    continue
                else:
                    if not any(find_sp(hor_dgph[C[j][i]])):
                        ymin=ymin
                    else:
                        l=find(hor_dgph[C[j][i]])
                        xmin=xR[l]
                room_x[C[j][i]],room_y[C[j][i]]=xmin,ymin #-room_height[C[j][i]]  #not subtracting height because code requires top left corner
                rect_drawn.append(C[j][i])
                xmax[C[j][i]]=xmin+room_width[C[j][i]]
                xR[C[j][i]]=xmax[C[j][i]]
                ymin = ymin + room_height[C[j][i]]
        xmax=xmax[xmax!=0]
        xmin=min(xmax)
    return room_x, room_y
