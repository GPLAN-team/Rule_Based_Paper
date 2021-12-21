"""
Constraints for the FastPLAN module.

Contains the main function applyConstraints() followed by various constraint functions:
    1. applyKitchenBath() - Constraint stating kitchen and bathroom mustn't be adjacent.
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def applyConstraints(graph, vertex_dictlist, biconnected = True):
    updated_graph = nx.Graph(graph)
    
    #Applying Biconnectivity (could be done better)
    if (biconnected):
        updated_graph.add_edges_from(nx.k_edge_augmentation(updated_graph, k = 3))
    # else:
        # updated_graph.add_edges_from(nx.k_edge_augmentation(updated_graph, k = 1))
    #Applying constraints:
    updated_graph = applyKitchenBath(updated_graph, vertex_dictlist)
    
    
    return updated_graph

def applyKitchenBath(graph, vertex_dictlist):
    """Constraint stating kitchen and bathroom mustn't be adjacent.
    """
    updated_graph = nx.Graph(graph)
    kitchenlist = []
    bathroomlist = []
    for i in vertex_dictlist:
        if i[1]["name"] == "kitchen":
            kitchenlist.append(int(i[0]))

        if i[1]["name"] == "bathroom":
            bathroomlist.append(int(i[0]))
    
    for kitchen in kitchenlist:
        for bathroom in bathroomlist:
            if updated_graph.has_edge(kitchen,bathroom):
                updated_graph.remove_edge(kitchen,bathroom)
    
    return updated_graph
