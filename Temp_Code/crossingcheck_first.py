# %%
from operator import truediv
from sys import api_version
# from turtle import pos
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from math import factorial, perm
import numpy as np
import graph_crossings as gc

G = nx.Graph()
G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7])
G.add_node(0, pos=(2, 4))
G.add_node(1, pos=(4, 4))
G.add_node(2, pos=(5, 2))
G.add_node(3, pos=(4, 0))
G.add_node(4, pos=(2, 0))
G.add_node(5, pos=(1, 2)) 
G.add_node(6, pos=(2, 2))
G.add_node(7, pos=(4, 2))
# G.add_node(1, pos=(1, 3))  # Master BR
# G.add_node(2, pos=(5, 3))  # WR
# G.add_node(3, pos=(1, 1.5))  # Kitchen
# G.add_node(4, pos=(2, 2.5))  # Dining
# G.add_node(5, pos=(4, 2.5))  # Store
# G.add_node(0, pos=(5, 1.5))

G.add_edges_from([(0,1), (1,2), (2,3), (3,4), (4,5), (0,5)])

pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, with_labels=True, pos=pos)

# H = G.copy()
# H.add_edges_from([(0,6)])
# pos = nx.get_node_attributes(H, 'pos')
# nx.draw(H, with_labels=True, pos=pos)

print(nx.__version__)
# %%
nodes = G.nodes
listedges = []

# ALL POSSIBLE EDGES WHICH DOESNT HAVE ANY CONSTRAINTS

for i in range(0, 7):
    for j in range(i+1, 8):
        if((i, j) not in [(6,7), (0,1), (1,2), (2,3), (3,4), (4,5), (0,5)]):
            listedges.append((i, j))

print(len(listedges))
listgraphs = []
# %%
# USING COMBINATION OF THOSE EDGES AND ADDING EDGES CORRESPONDING TO THE CONSTRAINTS TO GENERATE GRAPHS AND CHECK PLANARITY AND BI-CONNECTEDNESS
# Biconnectedness : no of nodes - constraints - 1
# Planarity - Eulers formula: 3*no of nodes - 6 - constraints
# No of edges already added = 6 -> subtract from each condition
for i in range(8 - 6 - 1, 3*8 - 6 - 6):  
    comb = combinations(listedges, i+1)
    for i in list(comb):
        H = G.copy()
        # H.add_nodes_from(G)
        # H.add_edges_from([(1, 2), (3, 4)])    # CONSTRAINT EDGES
        for source, target in i:
            H.add_edge(source, target)
        t = nx.check_planarity(H, counterexample=False)
        if(t[0] and nx.is_biconnected(H)):   # PLANARITY AND BICONNECTEDNESS
            listgraphs.append(H)

print(len(listgraphs))
# %%
pos_test = nx.get_node_attributes(listgraphs[10], 'pos')
# nx.draw(G, with_labels=True, pos=pos)
nx.draw(listgraphs[10], with_labels=True, pos=pos_test)

# pos = nx.get_node_attributes(listgraphs[100], 'pos')
# nx.draw(listgraphs[-11], with_labels=True, pos=pos)

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

# pos = nx.get_node_attributes(G, 'pos')
# nx.draw(permgraphs[-1], with_labels=True, pos=pos)

# plt.show()
# %%
coordinates = []