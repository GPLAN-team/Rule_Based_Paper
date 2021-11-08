import networkx as nx
import numpy as np
import source.separatingtriangle.septri as gst
nodcnt = 4
matrix = np.array([[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]])
print("Node count: ", matrix.shape[0])
print("Edge Count: ", int(np.count_nonzero(matrix == 1)/2))
origin_pos = nx.planar_layout(nx.from_numpy_matrix(matrix))
pos = [origin_pos[i] for i in range(0,nodcnt)]
outputs, extra_nodes = gst.handle_STs(matrix, pos, 1)
print(outputs, extra_nodes)