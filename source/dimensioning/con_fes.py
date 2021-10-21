import numpy as np

def con_fes(A,B,Aeq,Beq):
    p = A.shape[0]
    q = A.shape[1]
    surpA = np.identity(p)
    r = Aeq.shape[0]
    s = Aeq.shape[1]
    surpAeq = np.zeros((r,p))
    Beq = np.zeros((1,r))
    A = np.concatenate((A,surpA),axis = 1)
    Aeq = np.concatenate((Aeq,surpAeq),axis=1)
    A_cat = np.concatenate((A,Aeq),axis=0)
    B = np.array(B)
    Beq = Beq.flatten()
    B_cat = np.concatenate((B, Beq), axis=0)
    #augmenting the matrix
    B_cat = B_cat.reshape(1,B_cat.shape[0])
    aug = np.concatenate((A_cat,B_cat.transpose()),axis=1)
    #consistancy check for A_cat=B_cat
    '''
        -A is assumued to be the augmented matrix
        -All rows of A, and all the columns but the last shall be the coefficient matrix
        -we can define consistency based on the rank of matrix. If the ranks of augmented
        matrix and coefficient matrix are same, we can say that the system is consistent.
    '''
    if np.linalg.matrix_rank(aug) == np.linalg.matrix_rank(aug[:, :-1]):
        return True
    else:
        return False



