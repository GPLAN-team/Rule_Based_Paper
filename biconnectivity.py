import numpy as np
import networkx as nx

def isBiconnected(graph):
    h = nx.from_numpy_matrix(graph.matrix)
    return nx.is_biconnected(h)

def isBCUtil(graph, u, visited, parent, low, disc):

    children = 0

    visited[u] = True

    disc[u] = graph.Time
    low[u] = graph.Time
    graph.Time += 1
    for v in find_neighbors(graph,u):
        if graph.matrix[u][v] == 1:
            # If v is not visited yet, then make it a child of u
            # in DFS tree and recur for it
            if visited[v] == False:
                parent[v] = u
                children += 1
                if graph.isBCUtil(v, visited, parent, low, disc):
                    return True

                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u
                low[u] = min(low[u], low[v])

                # u is an articulation point in following cases
                # (1) u is root of DFS tree and has two or more children.
                if parent[u] == -1 and children > 1:
                    # self.articulation_points[u] = True
                    return True

                # (2) If u is not root and low value of one of its child is more
                # than discovery value of u.
                if parent[u] != -1 and low[v] >= disc[u]:
                    # self.articulation_points[u] = True
                    return True

            elif v != parent[u]:  # Update low value of u for parent function calls.
                low[u] = min(low[u], disc[v])
        else:
            continue

    return False

def isBC(graph):

    visited = [False] * (graph.node_count)
    disc = [float("Inf")] * (graph.node_count)
    low = [float("Inf")] * (graph.node_count)
    parent = [-1] * (graph.node_count)
    if isBCUtil(graph,0, visited, parent, low, disc):
        return False

    if any(i == False for i in visited):
        return False
    """
    for i in visited:
        if visited[i] is False:
            return False
        else:
            continue
    """
    return True

def BCCUtil(graph, u, parent, low, disc, st):

    # Count of children in current node
    children = 0
    #visited[u] = True
    # Initialize discovery time and low value
    disc[u] = graph.Time
    low[u] = graph.Time
    graph.Time += 1

    # Recur for all the vertices adjacent to this vertex
    for v in range(graph.node_count):
        if graph.matrix[u][v] == 1:
            # If v is not visited yet, then make it a child of u
            # in DFS tree and recur for it
            if disc[v] == -1:
                parent[v] = u
                children += 1
                st.append((u, v))  # store the edge in stack
                BCCUtil(graph,v, parent, low, disc, st)

                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u
                # Case 1 -- per Strongly Connected Components Article
                low[u] = min(low[u], low[v])

                # If u is an articulation point, pop
                # all edges from stack till (u, v)
                if parent[u] == -1 and children > 1 or parent[u] != -1 and low[v] >= disc[u]:
                    graph.no_of_bcc += 1  # increment count
                    graph.articulation_points[u] = True
                    w = -1
                    while w != (u, v):
                        w = st.pop()
                        # print("In bccutil no of bcc = " , graph.no_of_bcc)
                        graph.bcc_sets[0].add(w[0])
                        # self.bcc_sets[(self.no_of_bcc) - 1].add(w[1])
                        # print("Printing from bccutil")
                        # print(w[0])
                        print(w, "    ")
                    #print("")

            elif v != parent[u] and low[u] > disc[v]:
                '''Update low value of 'u' only of 'v' is still in stack 
                (i.e. it's a back edge, not cross edge). 
                Case 2 
                -- per Strongly Connected Components Article'''

                low[u] = min(low[u], disc[v])

                st.append((u, v))

def print_biconnected_components(graph):
    visited = [False] * (graph.node_count)
    disc = [-1] * (graph.node_count)
    low = [-1] * (graph.node_count)
    parent = [-1] * (graph.node_count)
    st = []
    # print("no of bcc = ", self.no_of_bcc)
    # print(self.articulation_points)
    for i in range(graph.node_count):
        if disc[i] == -1:
            BCCUtil(graph,i, parent, low, disc, st)

        if st:
            graph.no_of_bcc = graph.no_of_bcc + 1

            while st:
                w = st.pop()
                # print("printing from print_biconnected_components")
                # print(w[0])
                # print("printing from print_biconnected_components, no of bcc = ", self.no_of_bcc)
                # self.bcc_sets[(self.no_of_bcc) - 1].add(w[0])
                # self.bcc_sets[(self.no_of_bcc) - 1].add(w[1])
                print(w, "    ")
            #print("")

    # print(self.bcc_sets)

def utility_function_for_initialize_bcc_sets(graph, u, bcc_sets, parent, low, disc, st):
    children = 0
    # visited[u] = True
    # Initialize discovery time and low value
    disc[u] = graph.Time
    low[u] = graph.Time
    graph.Time += 1

    # Recur for all the vertices adjacent to this vertex
    for v in range(graph.node_count):
        if graph.matrix[u][v] == 1:
            # If v is not visited yet, then make it a child of u
            # in DFS tree and recur for it
            if disc[v] == -1:
                parent[v] = u
                children += 1
                st.append((u, v))  # store the edge in stack
                utility_function_for_initialize_bcc_sets(graph,v, bcc_sets, parent, low, disc, st)

                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u
                # Case 1 -- per Strongly Connected Components Article
                low[u] = min(low[u], low[v])

                # If u is an articulation point, pop
                # all edges from stack till (u, v)
                if parent[u] == -1 and children > 1 or parent[u] != -1 and low[v] >= disc[u]:
                    graph.no_of_bcc += 1  # increment count
                    graph.articulation_points[u] = True
                    w = -1
                    while w != (u, v):
                        w = st.pop()
                        # print("In utility_function_for_initialize_bcc_sets no of bcc = ", self.no_of_bcc)
                        bcc_sets[(graph.no_of_bcc) - 1].add(w[0])
                        bcc_sets[(graph.no_of_bcc) - 1].add(w[1])
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
    disc = [-1] * (graph.node_count)
    low = [-1] * (graph.node_count)
    parent = [-1] * (graph.node_count)
    st = []
    # self.bcc_sets = [set() for i in range(self.no_of_bcc)]
    graph.no_of_bcc = 0
    # print("no of bcc = ", self.no_of_bcc)
    # print(self.articulation_points)
    for i in range(graph.node_count):
        if disc[i] == -1:
            utility_function_for_initialize_bcc_sets(graph,i, graph.bcc_sets, parent, low, disc, st)

        if st:
            graph.no_of_bcc = graph.no_of_bcc + 1

            while st:
                w = st.pop()
                # print("printing from print_biconnected_components")
                # print(w[0])
                # print("printing from initialize_bcc_sets, no of bcc = ", self.no_of_bcc)
                graph.bcc_sets[(graph.no_of_bcc) - 1].add(w[0])
                graph.bcc_sets[(graph.no_of_bcc) - 1].add(w[1])
                # print(w)
            # print("")
    graph.bcc_sets = [x for x in graph.bcc_sets if x]
    # print(len(self.bcc_sets))
    # print(self.bcc_sets)
    # self.find_articulation_points()
    # self.remove_articulation_points_from_bcc_sets()
    # print(self.bcc_sets)

def find_articulation_points(graph):
    # self.no_of_articulation_points = 0
    for i in range(graph.node_count):
        if graph.articulation_points[i]:
            graph.no_of_articulation_points += 1
            graph.articulation_points_value.append(i)
            graph.articulation_point_sets[i].add(i)
    graph.articulation_point_sets = [x for x in graph.articulation_point_sets if x]

def find_neighbors(graph, v):
    h = nx.from_numpy_matrix(graph.matrix)
    nl = []
    for n in h.neighbors(v):
        nl.append(n)
    return nl

def make_biconnected(graph):
    for i in range(len(graph.articulation_points_value)):
        nl =find_neighbors(graph,graph.articulation_points_value[i])
        for j in range(0, (len(nl) - 1)):
            if not belong_in_same_block(graph,nl[j], nl[j+1]):

                graph.matrix[nl[j]][nl[j+1]] = 1
                graph.matrix[nl[j+1]][nl[j]] = 1
                graph.added_edges.add((nl[j], nl[j+1]))
                if (graph.articulation_points_value[i], nl[j]) in graph.added_edges or\
                        (nl[j], graph.articulation_points_value[i]) in graph.added_edges:
                    graph.matrix[graph.articulation_points_value[i]][nl[j]] = 0
                    graph.matrix[nl[j]][graph.articulation_points_value[i]] = 0
                    graph.removed_edges.add((graph.articulation_points_value[i], nl[j]))
                    graph.removed_edges.add((nl[j], graph.articulation_points_value[i]))
                if (graph.articulation_points_value[i], nl[j+1]) in graph.added_edges or\
                        (nl[j+1], graph.articulation_points_value[i]) in graph.added_edges:
                    graph.matrix[graph.articulation_points_value[i]][nl[j+1]] = 0
                    graph.matrix[nl[j+1]][graph.articulation_points_value[i]] = 0
                    graph.removed_edges.add((graph.articulation_points_value[i], nl[j+1]))
                    graph.removed_edges.add((nl[j+1], graph.articulation_points_value[i]))
    graph.final_added_edges = graph.added_edges - graph.removed_edges
    

def remove_articulation_points_from_bcc_sets(graph):
    for i in graph.articulation_points_value:
        for j in range(graph.no_of_articulation_points + 1):
            if i in graph.bcc_sets[j]:
                graph.bcc_sets[j].remove(i)

def belong_in_same_block(graph, a, b):
    for i in range(len(graph.bcc_sets)):
        if (a in graph.bcc_sets[i]) and (b in graph.bcc_sets[i]):
            return True
    return False



