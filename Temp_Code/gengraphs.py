# %%
# INITIAL NODES
from turtle import pos
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations, permutations
import math
import numpy as np
from . import graph_crossings as gc
from . import triangularity as trg
from . import septri as septri
import source.inputgraph as inputgraph
import pythongui.dimensiongui as dimgui


def generate_graphs(ext_rooms, int_rooms, rooms, rect_floorplans=True, adjacencies=[], non_adjacencies=[]):

    G = nx.Graph()
    # n = input("Enter Outer Boundary Vertices")
    # n = 5   # Outer boundary Convex Hull
    n = len(ext_rooms)
    graph_param = []
    print("PARAMS")
    print(ext_rooms)
    print(int_rooms)
    print(rooms)
    print(adjacencies)
    print(non_adjacencies)
    print("PARAMS END")

    # m =input("Enter Inner Boundary Vertices")
    # m = 3   # Inner nodes
    m = len(int_rooms)

    rad = 1

    e = (3*(n+m)-n)-3   # Edges for Triangular faces

    def _draw_regular_polygon(center, radius, n, m, angle, **kwargs):
        angle -= (math.pi/n)
        coord_list = [(center[0] + radius * math.sin((2*math.pi/n) * i - angle),
                       center[1] + radius * math.cos((2*math.pi/n) * i - angle)) for i in range(n)]
        for i in range(m):
            coord_list.append(
                (center[0]-radius + (i+1)*(2*radius)/(m+1), center[1]))
        return coord_list

    angle = math.pi/n

    if (n % 4 == 0):
        angle = 0

    coord_list = _draw_regular_polygon((3, 3), rad, n, m, 0)
    # print(coord_list)

    for i in range(n+m):
        G.add_node(i, pos=coord_list[i])

    constraints_incbdry = [(i, i+1) for i in range(n-1)]
    if (n > 3):
        constraints_incbdry.append((0, n-1))
    else:
        raise ValueError('value of n is not in permissible limits!')

    # nx.draw(G, with_labels=True, pos=pos)
    # plt.show()

    # if n == 5:
    #     constraints_incbdry.append((0,4))
    # elif n  == 6:
    #     constraints_incbdry.append((0,5))
    # elif n  == 4:
    #     constraints_incbdry.append((0,3))
    # else:
    #     raise ValueError('value of n is not in permissible limits!')

    # print(constraints_incbdry)
    constraints_inc = []
    constraints_exc = []

    # Adding adjacency and non-adjacency constraints
    for rule in adjacencies:
        a = min(rule[0], rule[1])
        b = max(rule[0], rule[1])
        if a == b:
            continue
        constraints_inc.append((a, b))

    for rule in non_adjacencies:
        a = min(rule[0], rule[1])
        b = max(rule[0], rule[1])
        if a == b:
            continue
        constraints_exc.append((a, b))

    print(f"Constraints_inc: {constraints_inc}")
    print(f"Constraints_exc: {constraints_exc}")

    # if n == 4:
    # # Fixing Master BR - 0, WC1 - 1, BR2 - 2, WC2 - 3  Kitchen - 4, Dining - 5, Living - 6, Store - 7
    #     constraints_inc = [(4,5), (5,6)]
    #     constraints_exc = [(3,4)]
    # elif n == 5:
    # # Fixing Master BR - 0, WC1 - 1, WC2 - 2, BR2 - 3, Kitchen - 4, Dining - 5, Living - 6, Store - 7  (5 outer vertices)
    #     constraints_inc = [(4, 5), (5,6)]

    #     constraints_exc = [(2,4), (1,4)]
    # elif n == 6:
    # # Fixing Master BR - 0, WC1 - 1, BR2 - 2, WC2 - 3, Living - 4, Kitchen - 5, Dining - 6, Store - 7
    #     constraints_inc = [(5,6), (4,6)]

    #     constraints_exc = [(1, 5)]

    # --------------------------PERMUTATION-----------------------
    def map_constraints(perm):
        new_constraints_inc = []
        new_constraints_exc = []
        for rule in constraints_inc:
            a = None
            b = None
            if rule[0] in perm:
                a = perm.index(rule[0])
            else:
                # a = rule[0]
                a = n + int_rooms.index(rule[0])

            if rule[1] in perm:
                b = perm.index(rule[1])
            else:
                # b = rule[1]
                b = n + int_rooms.index(rule[1])

            new_constraints_inc.append((min(a, b), max(a, b)))

        for rule in constraints_exc:
            a = None
            b = None
            if rule[0] in perm:
                a = perm.index(rule[0])
            else:
                # a = rule[0]
                a = n + int_rooms.index(rule[0])

            if rule[1] in perm:
                b = perm.index(rule[1])
            else:
                # b = rule[1]
                b = n + int_rooms.index(rule[1])

            new_constraints_exc.append((min(a, b), max(a, b)))

        return new_constraints_inc, new_constraints_exc

    def check_validity_of_permutation(perm):
        new_constraints_inc, new_constraints_exc = map_constraints(perm)

        # if n == 6:
        #     if (4, 7) in new_constraints_inc or (1, 6) in new_constraints_inc:
        #         return new_constraints_inc, new_constraints_exc, False

        for i in range(0, n):
            # if i == n-1:
            #     if (perm[0], perm[n-1]) in new_constraints_exc or (perm[n-1], perm[0]) in new_constraints_exc:
            #         return new_constraints_inc, new_constraints_exc, False

            # elif (perm[i], perm[i+1]) in new_constraints_exc or (perm[i+1], perm[i]) in new_constraints_exc:
            #     return new_constraints_inc, new_constraints_exc, False

            if i == n-1:
                if (0, n-1) in new_constraints_exc or (n-1, 0) in new_constraints_exc:
                    return new_constraints_inc, new_constraints_exc, False

            elif (i, i+1) in new_constraints_exc or (i+1, i) in new_constraints_exc:
                return new_constraints_inc, new_constraints_exc, False

        return new_constraints_inc, new_constraints_exc, True

    # %%

    # %%
    new_constraints_inc = []
    new_constraints_exc = []
    valid_perm = []
    perm = permutations(ext_rooms, n)
    for p in perm:
        new_constraints_inc, new_constraints_exc, valid = check_validity_of_permutation(
            p)
        if valid == True:
            print("Found valid permutation ", p)
            valid_perm = list(p)
            break
        else:
            continue

    print(new_constraints_inc)
    print(new_constraints_exc)
    # %%
    valid_perm.extend(int_rooms)

    # MAPPING BETWEEN ROOM NUMBERS AND ROOM NAMES
    perm_mapping = [rooms[i] for i in valid_perm]
    print(perm_mapping)
    # %%
    constraints_incbdry = [(i, i+1) for i in range(n-1)]
    if n >= 4:
        constraints_incbdry.append((0, n-1))
    else:
        raise ValueError('value of n is not in permissible limits!')

    new_constraints_inc_unmodified = new_constraints_inc

    new_constraints_inc = list(
        set(new_constraints_inc).difference(set(constraints_incbdry)))
    print("Inclusion constraints: ", new_constraints_inc)
    print("Exclusion constraints: ", new_constraints_exc)

    # ----------------------------PERMUTATION END ---------------------------

    pos = nx.get_node_attributes(G, 'pos')
    # nx.draw(G, with_labels=True, pos=pos)
    # plt.show()
    # plt.savefig('nodes_positioning')

    listedges = []
    for i in range(0, n+m-1):
        for j in range(i+1, n+m):
            if (((i, j) not in constraints_incbdry) and ((i, j) not in new_constraints_exc) and ((i, j) not in new_constraints_inc)):
                listedges.append((i, j))
    print(listedges)

    listgraphs = []

    # %%
    # USING COMBINATION OF THOSE EDGES AND ADDING EDGES CORRESPONDING TO THE CONSTRAINTS TO GENERATE GRAPHS AND CHECK PLANARITY AND BI-CONNECTEDNESS

    # for i in range(1, 10):
    #     comb = combinations(listedges, i+1)
    #     for i in list(comb):
    #         H = nx.Graph()
    #         H.add_nodes_from(G)
    #         H.add_edges_from(constraints_inc)
    #         H.add_edges_from(constraints_incbdry)    # CONSTRAINT EDGES
    #         for source, target in i:
    #             H.add_edge(source, target)
    #         t = nx.check_planarity(H, counterexample=False)
    #         if(t[0] and nx.is_biconnected(H)):   # PLANARITY AND BICONNECTEDNESS
    #             listgraphs.append(H)

    # ALL Triangulated Graphs have same no of edges

    comb = combinations(
        listedges, e - len(new_constraints_inc) - len(constraints_incbdry))
    for i in list(comb):
        H = nx.Graph()
        H.add_nodes_from(G)
        H.add_edges_from(new_constraints_inc)
        H.add_edges_from(constraints_incbdry)    # CONSTRAINT EDGES
        for source, target in i:
            H.add_edge(source, target)
        t = nx.check_planarity(H, counterexample=False)
        if (t[0] and nx.is_biconnected(H)):   # PLANARITY AND BICONNECTEDNESS
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

        flag = gc.check_intersection(
            np.array(xcoord), np.array(ycoord), matrix)
        # print(flag)

        if (not flag):
            permgraphs.append(P)

    print(len(permgraphs))

    pos = nx.get_node_attributes(G, 'pos')
    # %%
    # nx.draw(permgraphs[2], with_labels=True, pos=pos)

    # plt.show()

    # %%
    # TRIANGULATION
    positions = nx.get_node_attributes(G, 'pos')
    tri_graphs = []  # list of trinagulated graphs - PTGs
    # flag of triangulated or not for all the permgraphs (just for testing)
    tri_flag = []
    i = 1
    maxi = 0
    mini = 20
    for P in permgraphs:
        non_tri_faces = trg.get_nontriangular_face(positions, P)
        tri_edges = trg.get_tri_edges(non_tri_faces, positions)

        if tri_edges == []:
            maxi = max(maxi, len(P.edges()))
            mini = min(mini, len(P.edges()))
            tri_graphs.append(P)
            tri_flag.append(True)
            # plt.figure(i)
            i += 1
            # nx.draw(P, with_labels=True, pos = pos)
        else:
            tri_flag.append(False)

    # print(len(tri_graphs))
    # print(maxi)
    # print(mini)
    # for P in tri_graphs:
    #     nx.draw(P, with_labels=True, pos=pos)
    #     plt.show()

    # %%
    print(f" Tri Flag: {tri_flag}")
    # %%
    # # ROOM PERMUTATION
    # permutegraphs = []
    # # 4 - Dining    5 - Store
    # G.nodes[4]['name'] = 'Dining'
    # G.nodes[5]['name'] = 'Store'
    # for P in tri_graphs:
    #     graphs = []
    #     edges = P.edges
    #     P.nodes[4]['name'] = 'Dining'
    #     P.nodes[5]['name'] = 'Store'
    #     edgecnt = len(edges)
    #     matrix = np.zeros((nodecnt, nodecnt), int)
    #     for edge in (edges):
    #         matrix[edge[0]][edge[1]] = 1
    #         matrix[edge[1]][edge[0]] = 1
    #     nameattr = nx.get_node_attributes(G, 'name')
    #     diningnode = list(nameattr.keys())[list(nameattr.values()).index('Dining')]
    #     # print(diningnode)
    # %%
    # SEPARATING TRIANGLES
    # Get all cycles of length 3
    septri_info = []
    for P in permgraphs:
        all_cliques = list(nx.enumerate_all_cliques(P))
        all_triangles = [sorted(i) for i in all_cliques if len(i) == 3]
        all_triangles = [list(triangle)
                         for triangle in np.unique(all_triangles, axis=0)]

        origin_pos = positions

        trianlular_faces = []
        separating_triangles = []
        separating_edges = []  # edges of separating triangles
        separating_edge_to_triangles = dict()
        edge_to_faces = dict()

        for face in all_triangles:
            flag = False
            for NodeID in range(n+m):
                if NodeID in face:
                    continue

                # Search for node within triangle
                if (septri.point_in_triangle(origin_pos[face[0]][0], origin_pos[face[0]][1], origin_pos[face[1]][0],
                                             origin_pos[face[1]
                                                        ][1], origin_pos[face[2]][0],
                                             origin_pos[face[2]][1], origin_pos[NodeID][0], origin_pos[NodeID][1])):
                    flag = True
                    break

            if not flag:
                # Add face information to edge_to_faces
                trianlular_faces.append(face)
                for edge in septri.get_edges(face):
                    if (edge not in edge_to_faces):
                        edge_to_faces[edge] = []
                    edge_to_faces[edge].append(face)

            else:
                # Add ST information to separating_triangles, separating_edges and separating_edge_to_triangles
                separating_triangle = tuple(
                    sorted([face[0], face[1], face[2]]))
                separating_triangles.append(separating_triangle)

                edges = septri.get_edges(face)
                separating_edges.extend(edges)

                for edge in edges:
                    if (edge not in separating_edge_to_triangles):
                        separating_edge_to_triangles[edge] = []
                    separating_edge_to_triangles[edge].append(
                        separating_triangle)

        if (separating_triangles != []):
            septri_info.append(True)
        else:
            septri_info.append(False)

    # for i in septri_info:
    #     print(i)

    # print("Graphs without Separating Triangle: \n")
    print(f"Septri Info is {septri_info}")
    final_graphs = []
    count_non_septri = 0

    if rect_floorplans == True:
        for i in range(0, len(permgraphs)):
            if septri_info[i] == False:
                # nx.draw(permgraphs[i], with_labels=True, pos=pos)
                # plt.show()
                # plt.savefig('RFP_'+str(i))
                count_non_septri += 1
                final_graphs.append(permgraphs[i])
                graph_param.append([nodecnt, nx.number_of_edges(
                    permgraphs[i]), permgraphs[i].edges, coord_list])
        print(count_non_septri, "graphs without separating triangles")

    else:
        for i in range(0, len(permgraphs)):
            if septri_info[i] == True:
                # nx.draw(permgraphs[i], with_labels=True, pos=pos)
                # plt.show()
                # plt.savefig('OFP_'+str(i))
                count_non_septri += 1
                final_graphs.append(permgraphs[i])
                graph_param.append([nodecnt, nx.number_of_edges(
                    permgraphs[i]), permgraphs[i].edges, coord_list])

        print(count_non_septri, "graphs with separating triangles")

    # # DIMENSIONING PART

    # for P in final_graphs:
    # P = final_graphs[1]
    # edgecnt = nx.number_of_edges(P)
    # edgeset = P.edges
    # graph = inputgraph.InputGraph(
    #     nodecnt, edgecnt, edgeset, coord_list, [])
    # old_dims = [[0] * nodecnt, [0] * nodecnt, [0] * nodecnt,
    #             [0] * nodecnt, "", [0] * nodecnt, [0] * nodecnt]
    # min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = dimgui.gui_fnc(
    #     old_dims, nodecnt)
    # # start = time.time()
    # # min_width = []
    # # max_width = []
    # # min_height = []
    # # max_height = []
    # # min_aspect = []
    # # max_aspect = []
    # # symmetric_text = []
    # # for i in range(0, nodecnt):
    # #     w[i].set(0)
    # #     w1[i].set(99999)
    # #     minA[i].set(0)
    # #     maxA[i].set(99999)
    # #     min_ar[i].set(0)
    # #     max_ar[i].set(99999)
    # graph.multiple_dual()
    # graph.single_floorplan(min_width, min_height, max_width, max_height,
    #                        symm_string, min_aspect, max_aspect, plot_width, plot_height)
    # print(graph.floorplan_exist)
    # while(graph.floorplan_exist == False):
    #     old_dims = [min_width, max_width, min_height,
    #                 max_height, symm_string, min_aspect, max_aspect]
    #     min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = dimgui.gui_fnc(
    #         old_dims, nodecnt)
    #     graph.multiple_dual()
    #     graph.single_floorplan(min_width, min_height, max_width, max_height,
    #                            symm_string, min_aspect, max_aspect, plot_width, plot_height)
    # # end = time.time()
    # # printe("Time taken: " + str((end-start)*1000) + " ms")
    # graph_data = {
    #     'room_x': graph.room_x,
    #     'room_y': graph.room_y,
    #     'room_width': graph.room_width,
    #     'room_height': graph.room_height,
    #     'room_x_bottom_left': graph.room_x_bottom_left,
    #     'room_x_bottom_right': graph.room_x_bottom_right,
    #     'room_x_top_left': graph.room_x_top_left,
    #     'room_x_top_right': graph.room_x_top_right,
    #     'room_y_left_bottom': graph.room_y_left_bottom,
    #     'room_y_right_bottom': graph.room_y_right_bottom,
    #     'room_y_left_top': graph.room_y_left_top,
    #     'room_y_right_top': graph.room_y_right_top,
    #     'area': graph.area,
    #     'extranodes': graph.extranodes,
    #     'mergednodes': graph.mergednodes,
    #     'irreg_nodes': graph.irreg_nodes1
    # }
    # print("\n\n\n")
    # print(graph_data['area'])
    # print("\n\n\n")

    return final_graphs, coord_list, perm_mapping, new_constraints_inc_unmodified, new_constraints_exc, graph_param
    # %%
