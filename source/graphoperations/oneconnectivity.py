"""One-connected Module

This module allows the user to 

This module contains the following functions:
    * 
"""
import numpy as np
import copy
import networkx as nx

def get_biconnected_components(nxgraph):
    """Returns list of biconnected components in the graph.
    Args:
        nxgraph: an instance of NetworkX graph object.
    Returns:
        components: Set of biconnected components.
    """
    components = list(nx.biconnected_components(nxgraph))
    return components

def get_adj_matrix(matrix, component):
    """
    Args:
        
    Returns:
        
    """
    l = np.array(list(component))
    a = matrix[l][:,l]
    return a

def get_dict(component):
    """
    Args:
        
    Returns:
        
    """
    dict = {}
    cmpnt_lst = list(component)
    for i in range(0,len(cmpnt_lst)):
        dict[cmpnt_lst[i]] = i
    return dict

def recurse(list, i, final, individual):
    """
    Args:
        
    Returns:
        
    """
    if i == len(list):
        final.append(individual)
        return
    temp = list[i];
    for j in range(0, len(temp)):
        temp_individual = copy.deepcopy(individual)
        temp_individual.append(temp[j])
        recurse(list, i + 1, final, temp_individual)

def merge(em_list):
    """
    Args:
        
    Returns:
        
    """
    rowsEncodedMatrices = []  # variable stores the no. of rows in each encoded matrix after changing its orientation
    alignedEncodedMatrices = []  # stores encoded matrix in changed orientation
    equiDimensionedEncodedMatrices = []  # stores encoded matrix which are ready to be merged

    # Sample inputs
    # encodedMatrices = [np.array([[2,2],[1,0]]), np.array([[2,2, 2,2],[12,11,13,15], [5,5,5,5]]), np.array([[6,5],[7,5]])]
    encodedMatrices = em_list

    # loop changes the orientation of the received encoded matrices and stores them in alignedEncodedMatrices
    for i in range(len(encodedMatrices)):
        encodedMatrix = encodedMatrices[i]

        if i == 0:
            if len(np.unique(encodedMatrix[:, -1])) == 1:  # Last col
                val = encodedMatrix[0][-1]  # variable helps in checking the orientation of 1 to n-1 components
                alignedEncodedMatrices.append(encodedMatrix)
            if len(np.unique(encodedMatrix[:, 0])) == 1:  # First col
                val = encodedMatrix[0][0]
                alignedEncodedMatrices.append(np.fliplr(encodedMatrix))  # fliplr flips the matrix vertically
            if len(np.unique(encodedMatrix[0])) == 1:  # First row
                val = encodedMatrix[0][0]
                encodedMatrix = np.transpose(encodedMatrix)
                alignedEncodedMatrices.append(np.fliplr(encodedMatrix))
            if len(np.unique(encodedMatrix[-1])) == 1:  # Last row
                val = encodedMatrix[-1][0]
                encodedMatrix = np.transpose(encodedMatrix)
                alignedEncodedMatrices.append(encodedMatrix)

        elif i == len(encodedMatrices) - 1:
            if len(np.unique(encodedMatrix[:, -1])) == 1:  # Last col
                alignedEncodedMatrices.append(np.fliplr(encodedMatrix))
            if len(np.unique(encodedMatrix[:, 0])) == 1:  # First col
                alignedEncodedMatrices.append(encodedMatrix)
            if len(np.unique(encodedMatrix[0])) == 1:  # First row
                encodedMatrix = np.transpose(encodedMatrix)
                alignedEncodedMatrices.append(encodedMatrix)
            if len(np.unique(encodedMatrix[-1])) == 1:  # Last row
                encodedMatrix = np.transpose(encodedMatrix)
                alignedEncodedMatrices.append(np.fliplr(encodedMatrix))

        else:
            # Assuming both cut vertices occupy opposite row/column in encoded matrix
            if len(np.unique(encodedMatrix[:, -1])) == 1:
                if val == encodedMatrix[0][0]:
                    alignedEncodedMatrices.append(encodedMatrix)
                else:
                    encodedMatrix = np.fliplr(encodedMatrix)
                    alignedEncodedMatrices.append(encodedMatrix)
            elif len(np.unique(encodedMatrix[-1])) == 1:
                encodedMatrix = np.transpose(encodedMatrix)
                if val == encodedMatrix[0][0]:
                    alignedEncodedMatrices.append(encodedMatrix)
                else:
                    encodedMatrix = np.fliplr(encodedMatrix)
                    alignedEncodedMatrices.append(encodedMatrix)
            val = encodedMatrix[0][-1]

    for matrix in alignedEncodedMatrices:
        rowsEncodedMatrices.append(len(matrix))

    maxRows = max(rowsEncodedMatrices)

    # loop adds extra rows in encoded matrix to make all the EMs of the same height
    for i in range(len(rowsEncodedMatrices)):
        encodedMatrix = alignedEncodedMatrices[i]
        j = len(encodedMatrix)
        while j < maxRows:
            encodedMatrix = np.append(encodedMatrix, [encodedMatrix[-1]], axis=0)
            j = j + 1
        equiDimensionedEncodedMatrices.append(encodedMatrix)

    # finalEncodedMatrix stores the merged EM
    finalEncodedMatrix = equiDimensionedEncodedMatrices[0]

    # loop merges all the encoded matrices
    for i in range(1, len(equiDimensionedEncodedMatrices)):
        encodedMatrix = equiDimensionedEncodedMatrices[i]
        finalEncodedMatrix = np.concatenate((finalEncodedMatrix, encodedMatrix[:, 1:]), axis=1)


    return finalEncodedMatrix

def convert_to_rel(em,nodecnt):
    """
    Args:
        
    Returns:
        
    """
    rows = len(em)
    cols = len(em[0])
    row_start = nodecnt * np.ones(cols)
    row_end = (nodecnt + 2) * np.ones(cols)
    col_start = (nodecnt + 3) * np.ones(rows + 2)
    col_end = (nodecnt + 1) * np.ones(rows + 2)
    em = np.insert(em, 0, row_start, 0)
    em = np.insert(em, rows + 1, row_end, 0)
    em = np.insert(em, 0, col_start, 1)
    em = np.insert(em, cols + 1, col_end, 1)

    mat = np.zeros((nodecnt + 4, nodecnt + 4))

    for i in range(rows + 1, 0, -1):
        for j in range(1, cols + 1):
            if (em[i][j] != em[i - 1][j]):
                mat[em[i][j]][em[i - 1][j]] = 2

    for i in range(1, rows + 1):
        for j in range(0, cols + 1):
            if (em[i][j] != em[i][j + 1]):
                mat[em[i][j]][em[i][j + 1]] = 3

    mat[nodecnt][nodecnt + 1] = 1
    mat[nodecnt][nodecnt + 3] = 1
    mat[nodecnt + 1][nodecnt + 2] = 1
    mat[nodecnt + 1][nodecnt] = 1
    mat[nodecnt + 2][nodecnt + 1] = 1
    mat[nodecnt + 2][nodecnt + 3] = 1
    mat[nodecnt + 3][nodecnt] = 1
    mat[nodecnt + 3][nodecnt + 2] = 1

    return mat