#%%
from math import factorial
# from turtle import pos
import networkx as nx
import matplotlib.pyplot as plt
import itertools

def ccw(a,b,c):
    return (c[1]-a[1]) * (b[0]-a[0]) > (b[1]-a[1]) * (c[0]-a[0])

def intersect(a,b,c,d):
    return ccw(a,c,d) != ccw(b,c,d) and ccw(a,b,c) != ccw(a,b,d)
    
def check_crossings(G):
    nodes = G.nodes.data("pos")
    # print(nodes)
    edges = [e for e in G.edges]
    # print(edges)
    for e in edges:
        for v in edges:
            if e == v:
                continue
            res = intersect(nodes[e[0]], nodes[e[1]], nodes[v[0]], nodes[v[1]])
            if res:
                print("Edge crossing detected between edges ", e," and ",v)
                return True
    return False
    
G = nx.Graph()

G.add_nodes_from([1,2,3,4,5,6])
G.add_node(1, pos=(2, 4))
G.add_node(2, pos=(4, 4))
G.add_node(3, pos=(5, 2))
G.add_node(4, pos=(4, 0))
G.add_node(5, pos=(2, 0))
G.add_node(6, pos=(1, 2))
G.add_node(7, pos=(2, 2))
G.add_node(8, pos=(4, 2))

# for i in range(0, factorial(6)):
# print(list(G.nodes.data("pos")))

G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1)])
# pos = nx.planar_layout(G)
# print(check_crossings(G))   

# print(nx.is_planar(G))

# nx.draw(G, with_labels=True, font_weight='bold')
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, with_labels=True, pos=pos)

# newG = nx.PlanarEmbedding(G)
# nx.draw(newG, with_labels=True)

plt.show()
# %%
mapping = {1: "BR1", 2: "WC1", 3: "BR2", 4: "WC2", 5: "Living", 6: "Kitchen", 7: "Dining", 8: "Store"}
G = nx.relabel_nodes(G, mapping)
positions = pos = nx.get_node_attributes(G, 'pos')

nx.draw(G, with_labels=True, pos=positions)
# %%