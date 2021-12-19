"""
Get quick floorplans for required house plans.
Current conditions:
    1. Kitchen is NOT adjacent to bathroom.

    Functions in this module: (The most imp function is getRandomGraphlist())
        1. planner() - Returns dictionary containing names of the rooms and their respective count and the total number of rooms.
        2. getCustomRooms() - Works like planner(), except it allows user to have custom rooms.
        3. createGraph() - Creates the basic networkX graph with room names added to each vertex as an attribute. 
                           (look into vertex attributes on networkx:https://networkx.org/documentation/stable/tutorial.html#adding-attributes-to-graphs-nodes-and-edges)
        4. getRandomGraphlist() - MAIN function to get list of random graphs which is to be made into floorplans
        5. getRandomGraph() - function to generate a random graph as required in the module, after which the constraints are applied.
                              Can change probabilities here to experiment on new possibilities. 
        6. data_from_json() - Parses the inputgraph.json file to get the default graph.
        7. runner() - API Function to be called from other files to use generation of a list of graphs.
        8. my_plot(), driver(), runner_test() - testing functions to test the above functions by running this file independently. 
                                 (inputs need to be given from console)
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import json
from random import randint
from FastPLAN_constraints import applyConstraints

JSON_PATH = ('inputgraph.json')

def planner(str="1BHK", store_rooms = 0, custom = False, distinct_rooms = 4):
    """
    Input: Room plan, if storeroom is required, if user is entering custom rooms and the number of distinct rooms.
    Returns: Room dictionary, Total Rooms
    """
    try:
        assert(len(str)==4), "Invalid Input. You can only enter n-BHK as an input."
    except Exception as e:
        print(e)
    if(not custom):
        room_dict = {"bedroom": int(str[0]), "bathroom": int(str[0]), "kitchen": 1, "hall": 1, "storeroom": int(store_rooms) }
        total_rooms = sum((room_dict.values()))
        return room_dict, total_rooms
    if(custom):
        room_dict, total_rooms = getCustomRooms(distinct_rooms)
        return room_dict, total_rooms    

def getCustomRooms(distinct_rooms):
    """
    Allows user to add custom plans.
    Returns: 
        room_dict - a dictionary with {room_name: number of rooms}
        total_rooms - Total number of rooms in the plan.
    """
    room_dict = {}
    total_rooms = 0
    for i in range(distinct_rooms):
        room = input("Enter room name")
        number = input("Enter number of " + room + "you want")
        room_dict.update({room: number})
        total_rooms += number
    return room_dict, total_rooms

def createGraph(room_dict,total_rooms):
    """
    Creates a default graph with vertex attributes.
    Returns:
        1. G_default - The default graph.
        2. vertex_dictlist - list of tuples which contains the vertex of the graph and its attributes. (here in the form: ((1,{'name':'bedroom'}), (2,{'name':'bathroom'}))
    """
    if(room_dict["storeroom"]==0):
        room_dict.pop("storeroom")
    g_default = nx.Graph()
    node_list = range(total_rooms)
    g_default.add_nodes_from(node_list)
    rooms = list(room_dict.keys())
    # print(rooms)          #Uncomment to see the list of rooms.
    i = 0   #first iterator
    j = 0   #second iterator
    while(i<total_rooms):
        room = rooms[j]
        while(room_dict[room]):
            g_default.nodes[i]["name"] = room
            room_dict[room] -= 1
            i += 1
        j += 1
    vertex_dictlist = (g_default.nodes.data())
    print(g_default.nodes.data())  #Uncomment to see vertices with room names as the attribute.
    # nx.draw_kamada_kawai(G_default, node_size = 100, with_labels = True, node_color = 'orange', font_size = 10) #Uncomment to see default graph.
    return g_default, vertex_dictlist

def getRandomGraphlist(room_dict, total_rooms, number = 50, defaultGraph = False, default_components = None, is_biconnected = True):
    """Returns required list of graphs.
        Inputs:
            1. room_dict - a dictionary with {room_name: number of rooms}
            2. total_rooms - total number of rooms in the plan
            3. number - (fixed) Number of random graphs to generate
            4. defaultGraph - Is default graph given?(False by default)
            5. default_components - Tuple containing default graph and its vertex dictlist.
            6. is_biconnected - Do you want the graph list to be biconnected graphs? (True by default)
        Output:
            1. graphs - list of required random networkx graphs
    """
    if(defaultGraph == False):
        g_def, vertex_dictlist = createGraph(room_dict, total_rooms)
    else:
        g_def, vertex_dictlist = default_components
    
    graphs = []
    for i in range(number):
        g = nx.Graph()
        g = getRandomGraph(g_def, total_rooms)
        # print(g.edges())        #uncomment to print edges in the random graph.
        g = applyConstraints(g,vertex_dictlist,is_biconnected)
        if (is_biconnected):
            if(nx.is_biconnected(g) and nx.check_planarity(g)[0]):
                graphs.append(g)
        else:
            if(nx.is_connected(g) and nx.check_planarity(g)[0]):
                graphs.append(g)
    # We now have a list of graphs
    return graphs


def getRandomGraph(defaultGraph,total_rooms):
    """Used to generate a random graph.
        Inputs:
            1. defaultGraph - The graph to start the random generation with.
            2. total_rooms - total number of rooms in the plan
        Output:
            1. rnd_g - random graph generated
    """
    rnd_g = nx.Graph(defaultGraph)
    i = 0   # first iterator
    j = 0   # second iterator
    while(i<total_rooms):
        j=0
        while(j<total_rooms):
            if(i==j):
                j+=1
                continue
            if(randint(0,3)==0):           #Can change probabilities here to manipulate the results
                rnd_g.add_edge(i,j)
                if not nx.check_planarity(rnd_g)[0]:
                    rnd_g.remove_edge(i,j)
            j+=1
        i+=1
    return rnd_g

def data_from_json():
    """
    Makes a room dictionary from inputgraph.json
    Returns:
        1. room_dict - a dictionary with {room_name: number of rooms}
        2. total_rooms - Total number of rooms in the plan. 
    """
    roomdict = {}
    total_rooms = 0
    f = open(JSON_PATH)
    data = json.load(f)
    total_rooms = len(data["nodes"])
    for room in data["nodes"]:
        roomdict.update({room : data["nodes"].count(room)})
    g_default = nx.Graph()
    node_list = range(total_rooms)
    g_default.add_nodes_from(node_list)
    for edge in data["edges"]:
        g_default.add_edge(int(edge[0]),int(edge[1]))
    temp_roomdict = roomdict
    rooms = list(roomdict.keys())
    i = 0   #first iterator
    j = 0   #second iterator
    while(i<total_rooms):
        room = rooms[j]
        while(temp_roomdict[room]):
            g_default.nodes[i]["name"] = room
            temp_roomdict[room] -= 1
            i += 1
        j += 1
    vertex_dictlist = (g_default.nodes.data())
    defaultComponents = g_default, vertex_dictlist

    f.close()
    return roomdict, total_rooms, defaultComponents

def runner(is_biconnected):
    """
    Input: 
        nxgraph: A networkx Graph object
        non_adjacent_list: A list representing what to vertices SHOULD NOT be adjacent.
    Output:
        graphs: A list of networkx Graphs.
    """
    #Function might be needed to be updated acc to above i/p o/p conditions.

    graphs = []
    roomdict, total_rooms, defaultComponents = data_from_json()
    graphs = getRandomGraphlist(roomdict, total_rooms, number = 50, defaultGraph = True, default_components = defaultComponents, is_biconnected = is_biconnected)

    return graphs



###Testing Functions ahead###

def my_plot(graphs, figsize = 14 , dotsize = 20):
    num = len(graphs)
    fig = plt.figure()

    k = int(np.sqrt(num)) #for sub-plotting
    i = 1                 #for sub-plotting
    
    for g in graphs:
        # print("The Graph is planar: " + str(nx.check_planarity(g)[0]))
        plt.subplot(k+1,k+1,i+1)
        gnx = nx.Graph(g)
        nx.draw_kamada_kawai(gnx, node_size = 100, with_labels = True, node_color = 'orange', font_size = 10)
        print('.', end='')
        i+=1

def driver():
    """
    To test the working of normal functions, independent of the json file.
    """
    print("You can enter the type of plan you want(nBHK format). To enter a custom plan, type 'custom' ")
    plan = input("Enter your plan: ")
    if(plan == "custom" or plan == "Custom"):
        distinct_rooms = input("Enter number of distinct rooms: ")
        room_dict, total_rooms = planner(str="1BHK", store_rooms = 0, custom = True, distinct_rooms = distinct_rooms)
    else:
        store_rooms = input("Enter number of storerooms you want: ")
        room_dict, total_rooms = planner(plan, store_rooms,False, 4)
    graphs = getRandomGraphlist(room_dict,total_rooms)
    my_plot(graphs)
    plt.show()

def runner_test():
    """
    Tests runner API function.
    (pass is_biconnected = True to get biconnected graphlist, false to also allow one-connected graphs in graph list.)
    """
    graphs = runner(False)
    my_plot(graphs)
    plt.show()

if __name__ == "__main__":
    # driver()
    runner_test()