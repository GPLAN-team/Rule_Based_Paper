"""
Dimensioning Module
This module allows user to obtain optimised dimensions for height and width of each room from their inputs. This module handles symmetry constraints,
aspect ratio constraints as well as plot size constraints.

This module contains the following functions stored in seperate files:
    * floorplan_to_st - Takes user inputs and converts them into encoded matrix form of horizontal and vertical st graphs. Calls solve_linear and
    					convert_adj_equ_sym.
	* convert_adj_equ_sym - Converts encoded st graphs into linear equations.
    * solve_linear - Takes few user inputs along with the encoded horizontal and vertical st graphs to give optimized dimensions .

"""
import numpy as np

def convert_adj_equ_sym(DGPH, symm_rooms,plot_dimension):
    """
       Args:
           DGPH: Encoded matrix form of vertical/horizontal adjacencies including the north/west node
    	   symm_rooms: String of symmetric room constraints
       Attributes:
    	   LINEQ: Matrix showing an edge, where 1 denotes the starting node and -1 denotes the ending node.
       Returns:
           f: The coefficients of the linear objective function to be minimized.
           A: The inequality constraint matrix. Each row of A specifies the coefficients of a linear
              inequality constraints on widths/heights.
           Aeq: The equality constraint matrix. Each row of Aeq specifies the coefficients of a
                equality constraint on widths/heights.
           Beq: The equality constraint vector. Each element of Aeq @ width/height must equal
                the corresponding element of Beq.
       """
    N = len(DGPH)
    lineq_temp = np.zeros([N, N ** 2])

    symm_rooms = symm_rooms.split(',')
    symm_num = len(symm_rooms)
    for i in range(0,symm_num):
        symm_rooms[i] = symm_rooms[i].replace( '+', ' ')
        symm_rooms[i] = symm_rooms[i].replace('(', '' )
        symm_rooms[i] = symm_rooms[i].replace(')', '')

    # starting Liner equalities as a matrix; 1 indicates starting vertex and -1 indicates the end vertex of an edge.
    for i in range(0, N):
        for j in range(0, N):
            if DGPH[i][j] == 1:
                lineq_temp[i][N * i + j] = 1
                lineq_temp[j][N * i + j] = -1

    # starting removing extra variables from matrix
    LINEQ = []
    count = 0
    LINEQ = np.array(LINEQ)
    for i in range(0, N):
        for j in range(0, N):
            if DGPH[i][j] == 1:
                LINEQ = np.append(LINEQ,lineq_temp[:, (N*i)+j])
                count = count+1

    LINEQ = np.reshape(LINEQ,(count,N))
    LINEQ = np.transpose(LINEQ)

    # Starting Objective function
    n = len(LINEQ[0])
    f = np.zeros([1, n])
    z = np.sum(DGPH[0], dtype=int)

    for i in range(0, z):
        f[0][i] = 1


    # Linear inequalities (Dimensional Constraints)
    def ismember(d, k):
        return [1 if (i == k) else 0 for i in d]

    A = []
    for i in range(0, N):
        A.append(ismember(LINEQ[i], -1))
    A = np.array(A)
    A_min = np.dot(A, -1)
    A_max = A
    A_min = np.delete(A_min, 0, 0)
    A_max = np.delete(A_max, 0, 0)
    A = np.vstack((A_min, A_max))

    #symm
    symm_eq_mat = np.zeros((int(symm_num/2),n))

    for i in range(0,int(symm_num/2)):
        temp1 = (symm_rooms[2 * i])
        temp1 = temp1.split(' ')
        temp1_sz = len(temp1);
        temp1 = [int(i) for i in temp1]
        add_mat = np.zeros((int(symm_num / 2), n))
        if temp1_sz > 1:
            if DGPH[temp1[0], temp1[1]] == 1:
                temp1 = [temp1[0]]

        temp1_sz = len(temp1)
        for j in range(0,temp1_sz):
            add_mat[i] = add_mat[i] + A[temp1[j]]

        temp2 = (symm_rooms[2 *i + 1]);
        temp2 = temp2.split(' ')
        temp2_sz = len(temp2);
        temp2 = [int(i) for i in temp2]

        subt_mat = np.zeros((int(symm_num/2),n))
        if temp2_sz > 1:
            if DGPH[temp2[0], temp2[1]] == 1:
                temp2 = [temp2[0]]

        temp2_sz = len(temp2)
        for k in range(0,temp2_sz):
            subt_mat[i] = subt_mat[i] + A[temp2[k]];

        symm_eq_mat[i] = add_mat[i] - subt_mat[i]

    def any(A):
        for i in A:
            if i == 1:
                return 1
        return 0
    #Linear Equality Constraints (Network flow)
    Aeq = []
    for i in range(0, N):
        if any(ismember(LINEQ[i], 1)) != 0 and any(ismember(LINEQ[i], -1)) != 0:
            Aeq.append(LINEQ[i])

    o = len(Aeq[0])

    #symm
    for i in range(0,int(symm_num / 2)):
       Aeq = np.vstack((Aeq,symm_eq_mat[i]));

    # arr = np.reshape(arr, (-1, o))
    Aeq = np.array(Aeq)
    Beq = np.zeros([1, len(Aeq)])
    if(plot_dimension!=-1):
        plt_dim_equ = f
        Aeq = np.vstack((plt_dim_equ, Aeq))
        dim = np.zeros([1, 1])
        dim[0][0] = plot_dimension
        Beq = np.hstack((dim, Beq))

    return [f, A, Aeq, Beq]