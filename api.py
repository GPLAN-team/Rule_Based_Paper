
"""API

Generates floorplans for given graph data as input.
Current support only for rectangular floorplans.
A running example is available.

"""
from source import inputgraph as inputgraph
import json
import networkx as nx
import matplotlib.pyplot as plt

from pythongui import dimensiongui as dimgui

def multigraph_to_rfp(input_graph_list):
    output_rfps = []
    for each_graph in input_graph_list:
        print("each graph = "  + str(each_graph.edges()))
        output_rfps.append(graph_to_rfp(convert_nxgraph_to_input_data(each_graph))[0])
        # output_rfps.append(graph_to_rfp(each_graph))

    return output_rfps

def convert_nxgraph_to_input_data(nxgraph: nx.Graph):
    
    input_data = {}
    nodes = []
    edges = []

    rooms = list(nxgraph.nodes())
    edges_list = list(nxgraph.edges())
    # adjacency_constraints = list(nxgraph.edges())
    # edges_list = []
    # for each_edge in adjacency_constraints:
    #     l, r = int(each_edge[0]), int(each_edge[1])
    #     edges_list.append((l,r))

    # nxgraph = nx.Graph()
    # nxgraph.add_edges_from(edges_list)
    # nx.draw(nxgraph)
    # plt.show()

    try:
        pos = nx.planar_layout(nxgraph)
    except:
        pos = nx.spring_layout(nxgraph)



    for i, each_room in enumerate(rooms):
        node = {}
        node["id"] = i
        node["label"] = each_room
        node["x"] = pos[i][0]
        node["y"] = pos[i][1]
        node["color"] = "#e7e7e7"
        nodes.append(node)

    for each_edge in edges_list:
        st_edge = {}
        st_edge["source"] = each_edge[0]
        st_edge["target"] = each_edge[1]
        edges.append(st_edge)


    input_data["nodes"] = nodes
    input_data["edges"] = edges

    # print(input_data)
    return input_data

def convert_json_to_input_data(graph):
    input_data = {}
    nodes = []
    edges = []

    rooms = graph["rooms"]
    adjacency_constraints = graph["adjacency_constraints"]
    edges_list = []
    for each_edge in adjacency_constraints:
        l, r = int(each_edge[0]), int(each_edge[1])
        edges_list.append((l,r))

    nxgraph = nx.Graph()
    nxgraph.add_edges_from(edges_list)
    nx.draw(nxgraph)
    plt.show()

    try:
        pos = nx.planar_layout(nxgraph)
    except:
        pos = nx.spring_layout(nxgraph)



    for i, each_room in enumerate(rooms):
        node = {}
        node["id"] = i
        node["label"] = each_room
        node["x"] = pos[i][0]
        node["y"] = pos[i][1]
        node["color"] = "#e7e7e7"
        nodes.append(node)

    for each_edge in edges_list:
        st_edge = {}
        st_edge["source"] = each_edge[0]
        st_edge["target"] = each_edge[1]
        edges.append(st_edge)


    input_data["nodes"] = nodes
    input_data["edges"] = edges

    # print(input_data)
    return input_data

def test_one_BHK_to_input_data():
    one_BHK_file = open("two_bhk.json")
    json_data = json.load(one_BHK_file)
    input_data =  convert_json_to_input_data(json_data)
    print(input_data)
    output_data = graph_to_rfp(input_data)
    print(output_data)

def graph_to_rfp(input_data, normalize_const=40, limit=100000):
    """Generates a rfp for given graph data

    Args:
        input_data: A dictionary containing keys:
            nodes: Node data of the graph.
            edges: Edge data of the graph.
        normalize_const: (optional) Normalize height, width, top, left to this
        limit: (optional) Limit no. of RFPs to these many

    Returns:
        output_data: A list containing multiple or single floorplan.
            Each floorplan is a list of dictionary where each dictionary denotes a room.
    """
    nodecnt = len(input_data['nodes'])
    edgecnt = len(input_data['edges'])
    edgedata = []
    for edge in input_data['edges']:
        edgedata.append([edge['source'], edge['target']])
    node_coordinates = []
    for node in input_data['nodes']:
        node_coordinates.append([node['x'], node['y']])
    graph = inputgraph.InputGraph(nodecnt, edgecnt, edgedata, node_coordinates, [])
    output_data = []
    graph.irreg_multiple_dual()
    for idx in range(min(graph.fpcnt, limit)):
        output_fp = []
        for node in input_data['nodes']:
            output_fp.append({
                "id": node["id"],
                "label": node["label"],
                "color": node["color"],
                "left": int(graph.room_x[idx][node["id"]] * normalize_const),
                "top": int(graph.room_y[idx][node["id"]] * normalize_const),
                "width": int(graph.room_width[idx][node["id"]] * normalize_const),
                "height": int(graph.room_height[idx][node["id"]] * normalize_const)
                })
        for cnt in range(len(graph.mergednodes[idx])):
            output_fp.append({
                "id": graph.mergednodes[idx][cnt],
                "label": input_data['nodes'][graph.irreg_nodes1[idx][cnt]]["label"],
                "color": input_data['nodes'][graph.irreg_nodes1[idx][cnt]]["color"],
                "left": int(graph.room_x[idx][graph.mergednodes[idx][cnt]] * normalize_const),
                "top": int( graph.room_y[idx][graph.mergednodes[idx][cnt]] * normalize_const),
                "width": int(graph.room_width[idx][graph.mergednodes[idx][cnt]] * normalize_const),
                "height": int(graph.room_height[idx][graph.mergednodes[idx][cnt]] * normalize_const)
                })
        output_data.append(output_fp)
    return output_data

def dimensioning_part(graphs, coord_list):
    P = graphs[0]
    nodecnt = len(P.nodes)
    edgecnt = nx.number_of_edges(P)
    edgeset = P.edges
    graph = inputgraph.InputGraph(
        nodecnt, edgecnt, edgeset, coord_list, [])
    old_dims = [[0] * nodecnt, [0] * nodecnt, [0] * nodecnt,
                [0] * nodecnt, "", [0] * nodecnt, [0] * nodecnt]
    min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = dimgui.gui_fnc(
        old_dims, nodecnt)
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
    print(graph_data['area'])
    print("\n\n\n")
    
    return graph_data


if __name__ == "__main__":
    test_one_BHK_to_input_data()
    input_data = {
        "nodes": [
            {"id": 0, "label": "kitchen", "x": 14, "y": 20, "color":  "#e7e7e7"},
            {"id": 1, "label": "living room", "x": 25, "y": 20, "color":  "#e7e7e7"},
            {"id": 2, "label": "rotunda", "x": 20, "y": 30, "color":  "#e7e7e7"}],
        "edges": [
            {"source": 0, "target": 1},
            {"source": 1, "target": 2},
            {"source": 2, "target": 0}],
    }
    # print(graph_to_rfp(input_data))

    input_data = {
        "nodes": [
            {"id": 0, "label": "kitchen", "x": 14, "y": 20, "color":  "#e7e7e7"},
            {"id": 1, "label": "living room", "x": 25, "y": 20, "color":  "#e7e7e7"},
            {"id": 2, "label": "rotunda", "x": 20, "y": 30, "color":  "#e7e7e7"}],
        "edges": [
            {"source": 0, "target": 1},
            {"source": 1, "target": 2},
            {"source": 2, "target": 0}],
    }
    # print(graph_to_rfp(input_data))

    input_data = {
        "nodes": [
            {"id": 0, "label": "kitchen", "x": 14, "y": 20, "color":  "#e7e7e7"},
            {"id": 1, "label": "living room", "x": 25, "y": 20, "color":  "#e7e7e7"},
            {"id": 2, "label": "rotunda", "x": 20, "y": 30, "color":  "#e7e7e7"},
            {"id": 3, "label": "rotunda", "x": 20, "y": 25, "color":  "#e7e7e7"}],
        "edges": [
            {"source": 0, "target": 1},
            {"source": 1, "target": 2},
            {"source": 2, "target": 0},
            {"source": 0, "target": 3},
            {"source": 1, "target": 3},
            {"source": 2, "target": 3}],
    }
