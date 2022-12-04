# %%
from math import factorial
from turtle import pos
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import graph_crossings as gc
import itertools
print(nx.__version__)
G = nx.Graph()

G.add_nodes_from([0,1,2,3,4,5,6])
G.add_node(0, pos=(0, 2))
G.add_node(1, pos=(1, 3))
G.add_node(2, pos=(2, 0))
G.add_node(3, pos=(2.5, 1.8))
G.add_node(4, pos=(3.5, 2.8))
G.add_node(5, pos=(4.5, 0.4))
G.add_node(6, pos=(6, 2))
# G.add_node(7, pos=(4, 2))
# G.add_node(8, pos=(7, 2))
# G.add_node(8, pos=(0, 0))
# G.add_node(9, pos=(7, 2))
# G.add_node(10, pos=(8, 2))

# for i in range(0, factorial(6)):
# print(list(G.nodes.data("pos")))

G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (0,5), (1,4), (2,6)])

# print(check_crossings(G))   
# print(G.nodes)
# print(G.edges)
# print(list(G.nodes.data()))

nodes = G.nodes
edges = G.edges
nodecnt = len(nodes)
edgecnt = len(edges)
positions = [y for (x,y) in  G.nodes.data("pos")]

pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, with_labels=True, pos=pos)
# print(positions)
# print(nx.is_planar(G))
# %%
matrix = np.zeros((nodecnt, nodecnt), int)
for edge in (edges):
    matrix[edge[0]][edge[1]] = 1
    matrix[edge[1]][edge[0]] = 1
    
print(matrix)

xcoord = [x for x,y in positions]
ycoord = [y for x,y in positions]
print(xcoord)
print(ycoord)

print(gc.check_intersection(np.array(xcoord), np.array(ycoord), matrix))

# nx.draw(G, with_labels=True, font_weight='bold')
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, with_labels=True, pos=pos)

# newG = nx.PlanarEmbedding(G)
# nx.draw(newG, with_labels=True)

plt.show()
# %%