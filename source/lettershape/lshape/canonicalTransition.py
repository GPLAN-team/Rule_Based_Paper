import source.graphoperations.operations as opr
import numpy as np
import copy


# step 1: write the output manually for north, east and NE vertices.
# uske baaad algo go brr


def process_edge(node, edge_list):
    # print("processing: ", node, ": ", edge_list)
    min_element = edge_list[0]
    for i in edge_list:
        if i < min_element:
            min_element = i
    while edge_list[-1] != min_element:
        edge_list.insert(0, edge_list.pop())
    final_list = []
    for i in edge_list:
        if i > node:
            final_list.append(i)
    # print("Processed: ", node, ": ", final_list)
    return final_list


def vector_prod(p1, p2, p3, nodes_data, canonical_order):
    pos_p1 = nodes_data[int(canonical_order[int(p1)])]
    pos_p2 = nodes_data[int(canonical_order[int(p2)])]
    pos_p3 = nodes_data[int(canonical_order[int(p3)])]
    x1 = pos_p2.pos_x - pos_p1.pos_x
    y1 = pos_p2.pos_y - pos_p1.pos_y
    x2 = pos_p3.pos_x - pos_p2.pos_x
    y2 = pos_p3.pos_y - pos_p2.pos_y
    return x1 * y2 - x2 * y1


def get_edge_order(graph, node, nodes_data, canonical_order):
    node_cnt = graph.nodecnt
    node_cnt -= 2
    node -= 1
    node_nums = []
    adj = graph.matrix[node]
    for i in range(len(adj)):
        if adj[i] == 1:
            node_nums.append(i)
    node_set = set(node_nums)
    # if node == 7:
    #     print("first: ", node_set)
    curr = node_nums[0]
    node_nums.remove(curr)
    node_set.remove(curr)
    ordered_list = [curr]
    while len(node_set) != 0:
        for i in node_set:
            if graph.matrix[curr][i] == 1:
                curr = i
                ordered_list.append(i)
                node_set.remove(i)
                break
    while not (ordered_list[-1] > node > ordered_list[0]) and not (ordered_list[-1] < node < ordered_list[0]):
        ordered_list.insert(0, ordered_list.pop())
    print("curr node: ", node)
    print("ordered list: ", ordered_list)
    p1 = -1
    p2 = -1
    for i in range(len(ordered_list) - 1):
        if 1 < ordered_list[i] < node_cnt and 1 < ordered_list[i + 1] < node_cnt:
            p1 = ordered_list[i]
            p2 = ordered_list[i + 1]
            break
    if node == 1:
        while ordered_list[0] != 0:
            ordered_list.insert(0, ordered_list.pop())
        if graph.matrix[ordered_list[0]][ordered_list[1]] == 0:
            ordered_list.reverse()
            while ordered_list[0] != 0:
                ordered_list.insert(0, ordered_list.pop())
        ordered_list = process_edge(node, ordered_list)
        ordered_list = [x + 1 for x in ordered_list]
        return ordered_list
    if p1 == -1:
        ordered_list.insert(0, ordered_list.pop())
        print("gone for checking node: ", node, ordered_list)
        if vector_prod(node, ordered_list[0], ordered_list[1], nodes_data, canonical_order) < 0:
            print("fail!")
            ordered_list.reverse()
    else:
        if vector_prod(node, p1, p2, nodes_data, canonical_order) < 0:
            ordered_list.reverse()
    # for i in ordered_list:
    #     if i < node:
    #         ordered_list.remove(i)
    ordered_list = process_edge(node, ordered_list)
    ordered_list = [x + 1 for x in ordered_list]
    return ordered_list


def create_canonical_matrix(canonical_order, matrix):
    new_matrix = matrix.copy()
    mat_size = len(canonical_order)
    print("old matrix", matrix)
    for i in range(mat_size):
        for j in range(mat_size):
            new_matrix[canonical_order[i]][canonical_order[j]] = 0
            if matrix[i][j] == 1:
                new_matrix[canonical_order[i]][canonical_order[j]] = 1
    print("new matrix", new_matrix)
    return new_matrix


def Update_Graph(graph, matrix, canonical_order):
    graph.matrix = matrix

    triangular_cycles = opr.get_trngls(graph.matrix)
    digraph = opr.get_directed(graph.matrix)
    graph.bdy_nodes, graph.bdy_edges = opr.get_bdy(triangular_cycles, digraph)
    new_outer_boundary = opr.ordered_bdy(graph.bdy_nodes, graph.bdy_edges)
    wst = canonical_order[graph.west]
    sth = canonical_order[graph.south]
    while not ((new_outer_boundary[0] == wst and new_outer_boundary[-1] == sth) or (
            new_outer_boundary[0] == sth and new_outer_boundary[-1] == wst)):
        new_outer_boundary.insert(0, new_outer_boundary.pop())
    if new_outer_boundary[0] == sth:
        new_outer_boundary.reverse()
    return new_outer_boundary


def Canonical_L_Shaped(canonical_order, graph, nodes_data, triplet):
    can_ord_origin = copy.deepcopy(canonical_order)
    canonical_order = (np.ceil(canonical_order)).astype(int)
    can_ord_final = copy.deepcopy(canonical_order)
    for i in range(len(canonical_order)):
        can_ord_final[canonical_order[i]] = i
    print("my order:", can_ord_final)
    canonical_order = can_ord_final
    adj_matrix = create_canonical_matrix(canonical_order, graph.matrix)
    dummy_graph = copy.deepcopy(graph)
    dummy_graph.matrix = adj_matrix
    triangular_cycles = opr.get_trngls(dummy_graph.matrix)
    digraph = opr.get_directed(dummy_graph.matrix)
    dummy_graph.bdy_nodes, dummy_graph.bdy_edges = opr.get_bdy(triangular_cycles, digraph)
    outer_boundary = opr.ordered_bdy(dummy_graph.bdy_nodes, dummy_graph.bdy_edges)
    dummy_graph_constant = copy.deepcopy(dummy_graph)
    print("old outer boundary", outer_boundary)
    basis_edge = []
    point_order = []
    edge_order = []

    # taking care of every node
    n_cnt = dummy_graph.nodecnt
    n_cnt_constant = n_cnt
    curr_basis = []
    while n_cnt > 3:
        for i in range(n_cnt):  # this takes care of basis edge for max node IE north
            if adj_matrix[n_cnt - 1][i] == 1:
                basis_edge.append([i + 1, n_cnt])
                curr_basis = [i + 1, n_cnt]
                break

        adj_n_cnt = adj_matrix[n_cnt - 1]
        adj_matrix = np.delete(adj_matrix, n_cnt - 1, axis=0)
        adj_matrix = np.delete(adj_matrix, n_cnt - 1, axis=1)

        new_outer_boundary = Update_Graph(dummy_graph, adj_matrix, canonical_order)

        curr_pnt_ord = []
        for i in new_outer_boundary:
            if adj_n_cnt[i] == 1:
                curr_pnt_ord.append(i)
        curr_pnt_ord = [x + 1 for x in curr_pnt_ord]
        point_order.append(curr_pnt_ord)

        # Get positions of nodes. First 3 are trivial. For rest of nodes use any 2 nodes??
        if n_cnt == n_cnt_constant:
            curr_edge = []
        elif n_cnt == n_cnt_constant - 1:
            curr_edge = [n_cnt_constant]
        elif n_cnt == n_cnt_constant - 2:
            curr_edge = [n_cnt_constant, n_cnt_constant - 1]
        else:
            curr_edge = get_edge_order(dummy_graph_constant, n_cnt, nodes_data, can_ord_origin)
        edge_order.append(curr_edge)
        # print("removed last node:", adj_matrix)
        # print("new outer boundary", new_outer_boundary)

        # print("After Itr: ", n_cnt, basis_edge, point_order, edge_order)
        # print(n_cnt, '\t\t', curr_basis, '\t\t', curr_pnt_ord, '\t\t', curr_edge)
        n_cnt = n_cnt - 1  # or n_cnt = n_cnt - 1
    basis_edge.append([1, 3])
    basis_edge.append([1, 2])
    point_order.append([1, 2])
    point_order.append([1])
    edge_order.append(get_edge_order(dummy_graph_constant, 3, nodes_data, can_ord_origin))
    edge_order.append(get_edge_order(dummy_graph_constant, 2, nodes_data, can_ord_origin))
    # print('3', '\t\t', [1, 3], '\t\t', [1, 2], '\t\t', get_edge_order(dummy_graph_constant, 3, nodes_data, can_ord_origin))
    # print('2', '\t\t', [1, 2], '\t\t', [1], '\t\t', get_edge_order(dummy_graph_constant, 2, nodes_data, can_ord_origin))

    for i in basis_edge:
        i[0] = i[0] - 1
        i[1] = i[1] - 1
    for i in point_order:
        for j in range(len(i)):
            i[j] = i[j] - 1
    for i in edge_order:
        for j in range(len(i)):
            i[j] = i[j] - 1
    print("Finals: ", basis_edge, point_order, edge_order)

    for i in range(len(basis_edge)):
        print(len(basis_edge) - i, '\t\t', basis_edge[i], '\t\t', point_order[i], '\t\t', edge_order[i])

    print("Added vertices", graph.north, canonical_order[graph.north], graph.west, canonical_order[graph.west],
          graph.south, canonical_order[graph.south], graph.east, canonical_order[graph.east])

    if edge_order[2][0] < edge_order[2][1]:
        edge_order[2].reverse()
    if edge_order[-1][0] > edge_order[-1][-1]:
        edge_order[len(edge_order) - 1].reverse()
    left_edges, right_edges = calculateEdges(basis_edge, point_order, edge_order, can_ord_origin)
    rel = generate_rel(graph, left_edges, right_edges)
    return rel


def calculateEdges(basis_edge, point_order, edge_order, can_ord_origin):
    right_edges = []
    left_edges = []
    numberOfVertices = len(basis_edge)
    print("checking order: ", edge_order)
    print("num count: ", numberOfVertices)
    for i in range(2, len(edge_order)):
        left_edge = [numberOfVertices - i, edge_order[i][0]]
        right_edge = [numberOfVertices - i, edge_order[i][len(edge_order[i]) - 1]]
        left_edges.append(left_edge)
        right_edges.append(right_edge)
    for i in range(0, len(basis_edge)):
        x = basis_edge[i][0]
        if x == point_order[i][0]:
            right_edges.append(copy.deepcopy(basis_edge[i]))
        else:
            left_edges.append(copy.deepcopy(basis_edge[i]))

    print("left edges", left_edges)
    print("right edges", right_edges)

    for i in left_edges:
        i[0] = int(can_ord_origin[i[0]])
        i[1] = int(can_ord_origin[i[1]])
    for i in right_edges:
        i[0] = int(can_ord_origin[i[0]])
        i[1] = int(can_ord_origin[i[1]])
    print("left edges", left_edges)
    print("right edges", right_edges)
    return left_edges, right_edges


def generate_rel(graph, left_edges, right_edges):
    rel = copy.deepcopy(graph.matrix)
    numberOfVertices = len(graph.matrix[0])
    for edge in left_edges:
        if edge[0] > numberOfVertices - 5 and edge[1] > numberOfVertices - 5:
            print("ignored: ", edge[0], edge[1])
            continue
        rel[edge[0]][edge[1]] = 2
        rel[edge[1]][edge[0]] = 0

    for edge in right_edges:
        if edge[0] > numberOfVertices - 5 and edge[1] > numberOfVertices - 5:
            print("ignored: ", edge[0], edge[1])
            continue
        rel[edge[0]][edge[1]] = 3
        rel[edge[1]][edge[0]] = 0

    print("rel", rel)
    return rel
