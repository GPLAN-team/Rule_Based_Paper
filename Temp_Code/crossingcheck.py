# %%
from operator import truediv
from sys import api_version
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from math import factorial, perm
import numpy as np
import graph_crossings as gc
import triangularity as trg

G = nx.Graph()
G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7])
G.add_node(0, pos=(2, 4))  #BR1
G.add_node(1, pos=(4, 4))  #WC1
G.add_node(2, pos=(5, 2))  #BR2
G.add_node(3, pos=(4, 0))  #WC2
G.add_node(4, pos=(2, 0))  #Living room
G.add_node(5, pos=(1, 2))  #Kitchen
G.add_node(6, pos=(2, 2))  #Dining room
G.add_node(7, pos=(4, 2))  #Store room



# %%
nodes = G.nodes
listedges = []

# ALL POSSIBLE EDGES WHICH DOESNT HAVE ANY CONSTRAINTS

constraintsinc = [(0,1), (1,2), (2,3), (3,4), (4,5), (0,5), (5,6), (4,6)]
constraintsexc = [(1,5),(3,5)]

G.add_edges_from(constraintsinc)

pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, with_labels=True, pos=pos)
# %%
for i in range(0, 7):
    for j in range(i+1, 8):
        if(((i, j) not in constraintsinc) and ((i, j) not in constraintsexc)):
            listedges.append((i, j))

listgraphs = []
# %%
# USING COMBINATION OF THOSE EDGES AND ADDING EDGES CORRESPONDING TO THE CONSTRAINTS TO GENERATE GRAPHS AND CHECK PLANARITY AND BI-CONNECTEDNESS

for i in range(1, 10):
    comb = combinations(listedges, i+1)
    for i in list(comb):
        H = G.copy()
        # H.add_nodes_from(G)
        # H.add_edges_from(constraintsinc)    # CONSTRAINT EDGES
        for source, target in i:
            H.add_edge(source, target)
        t = nx.check_planarity(H, counterexample=False)
        if(t[0] and nx.is_biconnected(H)):   # PLANARITY AND BICONNECTEDNESS
            listgraphs.append(H)

print(len(listgraphs))
# %%
# APPLYING SWEEP LINE ALGO FOR ALL GRAPHS

nodes = G.nodes
nodecnt = len(nodes)
positions = [y for (x, y) in G.nodes.data("pos")]
permgraphs = []
for P in listgraphs:
    edges = P.edges
    edgecnt = len(edges)
    matrix = np.zeros((nodecnt, nodecnt), int)
    for edge in (edges):
        matrix[edge[0]][edge[1]] = 1
        matrix[edge[1]][edge[0]] = 1
    xcoord = [x for x, y in positions]
    ycoord = [y for x, y in positions]

    flag = gc.check_intersection(np.array(xcoord), np.array(ycoord), matrix)
    # print(flag)

    if(not flag):
        permgraphs.append(P)

print(len(permgraphs))
# %%
pos = nx.get_node_attributes(G, 'pos')
nx.draw(permgraphs[5], with_labels=True, pos=pos)

plt.show()
# %%

# nxgraph = nx.from_numpy_matrix(matrix)
positions = nx.get_node_attributes(G, 'pos')
print(positions)
# %%
positions = nx.get_node_attributes(G, 'pos')
tri_graphs = []  #list of triangulated graphs - PTGs
tri_flag = []  #flag of triangulated or not for all the permgraphs (just for testing)
# i = 1
for P in permgraphs:
    non_tri_faces = trg.get_nontriangular_face(positions, P)
    tri_edges = trg.get_tri_edges(non_tri_faces, positions)
    
    if tri_edges == []:
        tri_graphs.append(P)
        tri_flag.append(True)
        # plt.figure(i)
        # i += 1
        # nx.draw(P, with_labels=True, pos = pos)
    else:
        tri_flag.append(False)
    
print(len(tri_graphs))
# %%
nx.draw(tri_graphs[0], with_labels=True, pos = positions)
# %%
i = 1
mapping = {0: "BR1", 1: "WC1", 2: "BR2", 3: "WC2", 4: "Living", 5: "Kitchen", 6: "Dining", 7: "Store"}
for  P in tri_graphs:
    P = nx.relabel_nodes(P, mapping, copy=False)
    print(P)
    plt.figure(i)
    i += 1
    positions = nx.get_node_attributes(P, 'pos')
    nx.draw(P, with_labels=True, pos=positions)
# %%
print(tri_graphs)
# %%