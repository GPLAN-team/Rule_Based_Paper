# %%
# HEADER
import time
from turtle import pos
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import math
import numpy as np
from . import graph_crossings as gc
from . import septri as septri
import source.inputgraph as inputgraph
from . import dimensiongui as dimgui

# import triangularity as trg

# %%


def generate_graphs(ext_rooms, int_rooms):

    # GRAPH NODES

    G = nx.Graph()
    # n = int(input("Enter Outer Boundary Vertices: "))
    n = len(ext_rooms)
    # Outer boundary Convex Hull

    # m = int(input("Enter Interior Vertices: "))
    m = len(int_rooms)
    # Interior nodes

    rad = 1
    # Radius for plot

    e = (3*(n+m)-n)-3   # Edges for Triangular faces

    def _draw_regular_polygon(center, radius, n, m, angle, **kwargs):
        angle -= (math.pi/n)
        coord_list = [(center[0] + radius * math.sin((2*math.pi/n) * i - angle),
                       center[1] + radius * math.cos((2*math.pi/n) * i - angle)) for i in range(n)]
        for i in range(m):
            coord_list.append(
                (center[0]-radius + (i+1)*(2*radius)/(m+1), center[1]))
        return coord_list

    coord_list = _draw_regular_polygon((3, 3), rad, n, m, 0)

    for i in range(n+m):
        G.add_node(i, pos=coord_list[i])

    nodes = G.nodes
    nodecnt = len(nodes)

    pos = nx.get_node_attributes(G, 'pos')
    # nx.draw(G, with_labels=True, pos=pos)
    # plt.show()

    old_dims = [[0] * nodecnt, [0] * nodecnt, [0] * nodecnt,
                [0] * nodecnt, "", [0] * nodecnt, [0] * nodecnt]
    min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = dimgui.gui_fnc(
        old_dims, nodecnt)
    constraintsincbdry = [(i, i+1) for i in range(n-1)]
    constraintsincbdry.append((0, n-1))

    # Fixing Kitchen - 3, Master BR - 0 and Washroom - 1
    constraintsinc = [(3, n)]

    constraintsexc = [(1, 3)]

    listedges = []
    for i in range(0, n+m-1):
        for j in range(i+1, n+m):
            if(((i, j) not in constraintsincbdry) and ((i, j) not in constraintsexc) and ((i, j) not in constraintsinc)):
                listedges.append((i, j))

    listgraphs = []

    # %%
    # ALL Triangulated Graphs have same no of edges

    comb = combinations(listedges, e - len(constraintsinc) -
                        len(constraintsincbdry))
    for i in list(comb):
        H = nx.Graph()
        H.add_nodes_from(G)
        H.add_edges_from(constraintsinc)
        H.add_edges_from(constraintsincbdry)    # CONSTRAINT EDGES
        for source, target in i:
            H.add_edge(source, target)
        t = nx.is_planar(H)
        # t = nx.check_planarity(H, counterexample=False)
        if(t and nx.is_biconnected(H)):   # PLANARITY AND BICONNECTEDNESS
            listgraphs.append(H)

    print(len(listgraphs))
    # %%
    # APPLYING SWEEP LINE ALGO FOR ALL GRAPHS

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

        if(not flag):
            permgraphs.append(P)

    print(len(permgraphs))

    pos = nx.get_node_attributes(G, 'pos')

    # for P in permgraphs:
    #     nx.draw(P, with_labels=True, pos=pos)
    #     plt.show()

    # %%
    # Separating Triangles
    final_graphs = []
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
                    if(edge not in edge_to_faces):
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
                    if(edge not in separating_edge_to_triangles):
                        separating_edge_to_triangles[edge] = []
                    separating_edge_to_triangles[edge].append(
                        separating_triangle)

        if (separating_triangles != []):
            septri_info.append(True)
        else:
            septri_info.append(False)

    # for i in septri_info:
    #     print(i)

    print("Graphs without Separating Triangle: \n")
    count_non_septri = 0

    for i in range(0, len(permgraphs)):
        if septri_info[i] == False:
            # nx.draw(permgraphs[i], with_labels=True, pos=pos)
            # plt.show()
            count_non_septri += 1
            final_graphs.append(permgraphs[i])
    print(count_non_septri, "graphs without separating triangles")

    for P in final_graphs:
        edgecnt = nx.number_of_edges(P)
        edgeset = P.edges
        graph = inputgraph.InputGraph(
            nodecnt, edgecnt, edgeset, coord_list, [])

        # min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = dimgui.gui_fnc(
        #     old_dims, nodecnt)
        # start = time.time()
        # min_width = []
        # max_width = []
        # min_height = []
        # max_height = []
        # min_aspect = []
        # max_aspect = []
        # symmetric_text = []
        # for i in range(0, nodecnt):
        #     w[i].set(0)
        #     w1[i].set(99999)
        #     minA[i].set(0)
        #     maxA[i].set(99999)
        #     min_ar[i].set(0)
        #     max_ar[i].set(99999)
        graph.multiple_dual()
        graph.single_floorplan(min_width, min_height, max_width, max_height,
                               symm_string, min_aspect, max_aspect, plot_width, plot_height)
        print(graph.floorplan_exist)
        while(graph.floorplan_exist == False):
            old_dims = [min_width, max_width, min_height,
                        max_height, symm_string, min_aspect, max_aspect]
            min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = dimgui.gui_fnc(
                old_dims, nodecnt)
            graph.multiple_dual()
            graph.single_floorplan(min_width, min_height, max_width, max_height,
                                   symm_string, min_aspect, max_aspect, plot_width, plot_height)
        # end = time.time()
        # printe("Time taken: " + str((end-start)*1000) + " ms")
        graph_data = {
            'room_x': graph.room_x,
            'room_y': graph.room_y,
            'room_width': graph.room_width,
            'room_height': graph.room_height,
            'room_x_bottom_left': graph.room_x_bottom_left,
            'room_x_bottom_right': graph.room_x_bottom_right,
            'room_x_top_left': graph.room_x_top_left,
            'room_x_top_right': graph.room_x_top_right,
            'room_y_left_bottom': graph.room_y_left_bottom,
            'room_y_right_bottom': graph.room_y_right_bottom,
            'room_y_left_top': graph.room_y_left_top,
            'room_y_right_top': graph.room_y_right_top,
            'area': graph.area,
            'extranodes': graph.extranodes,
            'mergednodes': graph.mergednodes,
            'irreg_nodes': graph.irreg_nodes1
        }
        print("\n\n\n")
        print(graph_data['room_x'])
        print("\n\n\n")

    return final_graphs

# %%
