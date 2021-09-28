"""Biconnectivity Augmentation Module

This module allows user to check if the graph is biconnected and can
make it biconnected.

This module contains the following functions:

    * is_biconnected - returns a boolean representing whether the graph
        is biconnected or not.
    * biconnect - checks if a graph needs to be biconnected 
        and returns edges to be added to make it biconnected
"""
import numpy as np
import networkx as nx

def isBiconnected(graph):
    h = nx.from_numpy_matrix(graph.matrix)
    return nx.is_biconnected(h)

def utility_function_for_initialize_bcc_sets(graph, u, bccsets, parent, low, disc, st):
    children = 0
    # visited[u] = True
    # Initialize discovery time and low value
    disc[u] = graph.time
    low[u] = graph.time
    graph.time += 1

    # Recur for all the vertices adjacent to this vertex
    for v in range(graph.nodecnt):
        if graph.matrix[u][v] == 1:
            # If v is not visited yet, then make it a child of u
            # in DFS tree and recur for it
            if disc[v] == -1:
                parent[v] = u
                children += 1
                st.append((u, v))  # store the edge in stack
                utility_function_for_initialize_bcc_sets(graph,v, bccsets, parent, low, disc, st)

                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u
                # Case 1 -- per Strongly Connected Components Article
                low[u] = min(low[u], low[v])

                # If u is an articulation point, pop
                # all edges from stack till (u, v)
                if parent[u] == -1 and children > 1 or parent[u] != -1 and low[v] >= disc[u]:
                    graph.bcccnt += 1  # increment count
                    graph.articulationpts[u] = True
                    w = -1
                    while w != (u, v):
                        w = st.pop()
                        # print("In utility_function_for_initialize_bcc_sets no of bcc = ", self.bcccnt)
                        bccsets[(graph.bcccnt) - 1].add(w[0])
                        bccsets[(graph.bcccnt) - 1].add(w[1])
                        # print("Printing from bccutil")
                        # print(w[0])
                        # print(w)
                    # print("")

            elif v != parent[u] and low[u] > disc[v]:
                '''Update low value of 'u' only of 'v' is still in stack 
                (i.e. it's a back edge, not cross edge). 
                Case 2 
                -- per Strongly Connected Components Article'''

                low[u] = min(low[u], disc[v])

                st.append((u, v))

def initialize_bcc_sets(graph):
    disc = [-1] * (graph.nodecnt)
    low = [-1] * (graph.nodecnt)
    parent = [-1] * (graph.nodecnt)
    st = []
    # self.bccsets = [set() for i in range(self.bcccnt)]
    graph.bcccnt = 0
    # print("no of bcc = ", self.bcccnt)
    # print(self.articulationpts)
    for i in range(graph.nodecnt):
        if disc[i] == -1:
            utility_function_for_initialize_bcc_sets(graph,i, graph.bccsets, parent, low, disc, st)

        if st:
            graph.bcccnt = graph.bcccnt + 1

            while st:
                w = st.pop()
                # print("printing from print_biconnected_components")
                # print(w[0])
                # print("printing from initialize_bcc_sets, no of bcc = ", self.bcccnt)
                graph.bccsets[(graph.bcccnt) - 1].add(w[0])
                graph.bccsets[(graph.bcccnt) - 1].add(w[1])
                # print(w)
            # print("")
    graph.bccsets = [x for x in graph.bccsets if x]
    # print(len(self.bccsets))
    # print(self.bccsets)
    # self.find_articulation_points()
    # self.remove_articulation_points_from_bcc_sets()
    # print(self.bccsets)

def find_articulation_points(graph):
    # self.articulationptscnt = 0
    for i in range(graph.nodecnt):
        if graph.articulationpts[i]:
            graph.articulationptscnt += 1
            graph.articulationpts_val.append(i)
            graph.articulationpts_sets[i].add(i)
    graph.articulationpts_sets = [x for x in graph.articulationpts_sets if x]

def find_neighbors(graph, v):
    h = nx.from_numpy_matrix(graph.matrix)
    nl = []
    for n in h.neighbors(v):
        nl.append(n)
    return nl

def make_biconnected(graph):
    for i in range(len(graph.articulationpts_val)):
        nl = find_neighbors(graph,graph.articulationpts_val[i])
        for j in range(0, (len(nl) - 1)):
            if not belong_in_same_block(graph,nl[j], nl[j+1]):

                graph.matrix[nl[j]][nl[j+1]] = 1
                graph.matrix[nl[j+1]][nl[j]] = 1
                graph.added_edges.add((nl[j], nl[j+1]))
                if (graph.articulationpts_val[i], nl[j]) in graph.added_edges or\
                        (nl[j], graph.articulationpts_val[i]) in graph.added_edges:
                    graph.matrix[graph.articulationpts_val[i]][nl[j]] = 0
                    graph.matrix[nl[j]][graph.articulationpts_val[i]] = 0
                    graph.removed_edges.add((graph.articulationpts_val[i], nl[j]))
                    graph.removed_edges.add((nl[j], graph.articulationpts_val[i]))
                if (graph.articulationpts_val[i], nl[j+1]) in graph.added_edges or\
                        (nl[j+1], graph.articulationpts_val[i]) in graph.added_edges:
                    graph.matrix[graph.articulationpts_val[i]][nl[j+1]] = 0
                    graph.matrix[nl[j+1]][graph.articulationpts_val[i]] = 0
                    graph.removed_edges.add((graph.articulationpts_val[i], nl[j+1]))
                    graph.removed_edges.add((nl[j+1], graph.articulationpts_val[i]))
    return graph.added_edges - graph.removed_edges

def belong_in_same_block(graph, a, b):
    for i in range(len(graph.bccsets)):
        if (a in graph.bccsets[i]) and (b in graph.bccsets[i]):
            return True
    return False