import networkx as nx
import matplotlib.pyplot as plt
from networkx.classes import graph
import numpy as np
from networkx.readwrite.json_graph import adjacency

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Edge:
    def __init__(self, room, left, right):
        self.room = room
        self.left = left
        self.right = right

class Room:
    def __init__(self, name, tl_x, tl_y, br_x, br_y):
        self.label = name
        # self.color = color
        self.top_left_x = tl_x
        self.top_left_y = tl_y
        self.bottom_right_x = br_x
        self.bottom_right_y = br_y
        self.height = abs(self.bottom_right_y - self.top_left_y)
        self.width = abs(self.bottom_right_x - self.top_left_x)

class RFP:
    def __init__(self,graph,rooms):
        self.graph = graph
        self.rooms = rooms


    #Functions to create RFP from the graph

class circulation:
    def __init__(self,graph,room1, room2):
        self.graph = graph
        self.adjacency = {}
        self.circulation_graph = nx.Graph()
        # self.room1 = room1 #For testing common_edges
        # self.room2 = room2 #For testing common_edges
        # self.RFP = RFP

    def circulation_algorithm(self,v1=1,v2=2):
        """
        Applies the circulation algorithm on the PTPG graph
        
        Args:
            v1 (int, optional): First endpoint of the exterior edge to start the circulation algorithm. Defaults to 1.
            v2 (int, optional): Second endpoint of the exterior edge to start the circulation algorithm. Defaults to 2.
        """
        graph = self.graph
        print(nx.to_numpy_matrix(graph))
        # n is the number of vertices in the initial graph
        n = len(graph)
        m = n
        s = (v1-1 ,v2-1 , -1)

        # print("choose a door")
        # i ,j = map(int, input().split())
        # s[0] = i
        # s[1] = j

        # This dictionary tracks the pair of rooms each corridor is adjacent to
        # (key is vertex corresponding to corridor and values are a pair of rooms)
        adjacency = {}
        corridor_counter = 0
        queue = []
        queue.append(s)

        # Start of circulation algorithm
        while ( queue ):
            # Pops out the first element of the queue to subdivide the edge for V_n+1
            s = queue.pop(0)  
            for ne in list(nx.common_neighbors(graph,s[0],s[1])):
                if ne < m :
                    graph.add_edge(s[0],n)
                    graph.add_edge(s[1],n)
                    graph.remove_edge(s[0],s[1])
                    if s[2]>0:
                        # If condition satisfied this adds edge between current corridor vertex and previous one
                        graph.add_edge(n,s[2])
                    graph.add_edge(n,ne)
                    n+=1
                    # Adds the two tuples corresponding to the two triangles formed in the face considered
                    adjacency[corridor_counter] = [s[0],s[1]]
                    corridor_counter += 1
                    queue.append((ne,s[0],n-1))
                    queue.append((ne,s[1],n-1))
        
        # Change the key values to corridor vertex number
        corridor_vertices = [x+m for x in range(len(adjacency))]
        final_adjacency = dict(zip(corridor_vertices, list(adjacency.values())))

        # Now the final_adjacency dictionary contains the pair of rooms adjacent to each corridor

        A = nx.adjacency_matrix(graph, nodelist=range(m))
        # Now A stores the adjacency matrix of the graph, the nodelist parameter ensures the proper order of rows
        # corresponding to the node label
        print(A.todense())
        #todense prints the matrix in proper format along with the data type
        self.circulation_graph = graph
        self.adjacency = final_adjacency

    def corridor_boundary_rooms(self,corridor_vertex):
        """For a given corridor, this function outputs the two rooms it connects

        Args:
            corridor_vertex (Networkx node): Node corresponding to the corridor for which we need to find the neighbors
            # v1 (int, optional): First endpoint of the exterior edge to start the circulation algorithm. Defaults to 1.
            # v2 (int, optional): Second endpoint of the exterior edge to start the circulation algorithm. Defaults to 2.

        Returns:
            [a,b]: pair of rooms that the corridor_vertex is adjacent to
        """
        # input_graph = self.circulation_graph        
        # Gets the tuple corresponding to the key value (key = corridor_vertex)
        [a,b] = self.adjacency.get(corridor_vertex)
        
        return [a,b]

    def adjust_RFP_to_circulation(self):
        """
        Adjusts the RFP to form the circulation

        Args:
            None

        Returns:
            None
        """       
        for corridor in range(len(self.graph), len(self.circulation_graph)):
            [room1, room2] = self.corridor_boundary_rooms(corridor)
            self.add_corridor_between_2_rooms(room1,room2)
    
    def add_corridor_between_2_rooms(self,room1,room2):
        """Adds corridors between 2 given rooms

        Args:
            room1 (int): Room index of first room 
            room2 (int): Room index of second room
        """

        common_edges = self.find_common_edges(room1, room2)

    def find_common_edges(self,room1,room2):
        """Given two rooms this function finds the common edges between the two rooms

        Args:
            room1 (int): Room index of first room 
            room2 (imt): Room index of second room 

        Returns:
            [tuple]: This tuple has 5 elements, namely the x and y of left end of common edge, x and y of right end of common edge
                     and the direction of common edge with respect to room1 (N/S/E/W)
        """

        common_edge = (0,0,0,0,(room1.label,"Null"))
        # Case1: The rooms are vertically (same y coordinates)
        # Room1 is below Room2
        if room1.top_left_y == room2.bottom_right_y:
            common_edge = (max(room1.top_left_x, room2.top_left_x), room1.top_left_y, min(room1.bottom_right_x, room2.bottom_right_x), room2.bottom_right_y, (room1.label, "N"))
        
        # Room1 is above Room2
        elif room1.bottom_right_y == room2.top_left_y:
            common_edge = (max(room1.top_left_x, room2.top_left_x), room2.top_left_y, min(room1.bottom_right_x, room2.bottom_right_x), room1.bottom_right_y, (room1.label, "S"))

        # Case2: The rooms are horizontally adjacent (same x coordinates)
        # Room1 is to right of Room2 
        elif room1.top_left_x == room2.bottom_right_x:
            common_edge = (room1.top_left_x, max(room1.bottom_right_y, room2.bottom_right_y), room2.bottom_right_x, min(room1.top_left_y,room2.top_left_y), (room1.label, "W"))
        
        # Room1 is to left of Room2
        elif room1.bottom_right_x == room2.top_left_x:
            common_edge = (room2.top_left_x, max(room1.bottom_right_y, room2.bottom_right_y), room1.bottom_right_x, min(room1.top_left_y,room2.top_left_y), (room1.label, "E"))
        
        return common_edge

    def find_common_neighbors(self,room1,room2):
        common_edge = self.find_common_edge(room1, room2)
        neighbors = []
        orientation = 'x'
        height = 0
        if(common_edge[1] == common_edge[3]):
            height = common_edge[1]
            orientation = 'x' #Common edge is parallel to x axis
        
        elif(common_edge[0] == common_edge[2]):
            height = common_edge[1]
            orientation = 'y' #Common edge is parallel to y axis
        
        # The axis wrt which we shift the room edges to form corridor
        axis = (orientation, height)

        for room in list(nx.common_neighbors(self.graph, room1.label, room2.label))

    # def find_neighboring_edges_other_than_one(edge, exclude_vertex):
    # def find_directions_for_common_edges(room1,room2):
    # def Move_edge(room, shift_by, direction, shift_edge):
    # def remove_corridor_between_2_rooms(room1,room2):

def plot(graph,m):
    """Plots thr graph using matplotlib

    Args:
        graph (Networkx graph): The graph to plot
        m (integer): Number of vertices in the graph
    """
    pos=nx.spring_layout(graph) # positions for all nodes
    nx.draw_networkx(graph,pos, labels=None,node_size=400 ,node_color='#4b8bc8',font_size=12, font_color='k', font_family='sans-serif', font_weight='normal', alpha=1, bbox=None, ax=None)
    nx.draw_networkx_edges(graph,pos)
    nx.draw_networkx_nodes(graph,pos,
                        nodelist=list(range(m,len(graph))),
                        node_color='r',
                        node_size=500,
                    alpha=1)
    plt.show()

def main():
    def make_graph():
        g = nx.Graph()
        g.add_edge(0,1)
        g.add_edge(0,2)
        g.add_edge(2,1)
        n = len(g)
        return g
    
    def test_circ():
        g = make_graph()
        circulation_obj = circulation(g)
        rooms = []
        circulation_obj.circulation_algorithm()
        plot(circulation_obj.circulation_graph,n)
        rooms = circulation_obj.corridor_boundary_rooms(n)
        print("Adjacency: ", circulation_obj.adjacency)
        print("Rooms that corridor 6 connects: ", rooms)

    def test_comm_edges():
        # Case1 test:
        g1 = make_graph()
        tl_x1 = 10
        br_x1 = 20
        br_y1 = 0
        tl_y1 = 10
        tl_x2 = 0
        tl_y2 = 20
        br_x2 = 30
        br_y2 = 10
        room1 = Room("0", tl_x1, tl_y1, br_x1, br_y1)
        room2 = Room("1", tl_x2, tl_y2, br_x2, br_y2)

        circulation_obj1 = circulation(g1, room1, room2)
        common_edge1 = circulation_obj1.find_common_edges(room1, room2)
        print("Common edge case1:", common_edge1)

        # Case2 test:
        g2 = make_graph()
        tl_x3 = 10
        br_x3 = 20
        br_y3 = 10
        tl_y3 = 20
        tl_x4 = 0
        tl_y4 = 10
        br_x4 = 30
        br_y4 = 0
        room3 = Room("0", tl_x3, tl_y3, br_x3, br_y3)
        room4 = Room("1", tl_x4, tl_y4, br_x4, br_y4)

        circulation_obj2 = circulation(g2, room3, room4)
        common_edge2 = circulation_obj2.find_common_edges(room3, room4)
        print("Common edge case2:", common_edge2)

        # Case3 test:
        g3 = make_graph()
        tl_x5 = 10
        br_x5 = 20
        br_y5 = 5
        tl_y5 = 15
        tl_x6 = 0
        tl_y6 = 20
        br_x6 = 10
        br_y6 = 0
        room5 = Room("0", tl_x5, tl_y5, br_x5, br_y5)
        room6 = Room("1", tl_x6, tl_y6, br_x6, br_y6)

        circulation_obj3 = circulation(g3, room5, room6)
        common_edge3 = circulation_obj3.find_common_edges(room5, room6)
        print("Common edge case3:", common_edge3)

        # Case4 test:
        g4 = make_graph()
        tl_x7= 0
        br_x7 = 10
        br_y7 = 5
        tl_y7 = 15 
        tl_x8 = 10
        tl_y8 = 20
        br_x8 = 20
        br_y8 = 0
        room7 = Room("0", tl_x7, tl_y7, br_x7, br_y7)
        room8 = Room("1", tl_x8, tl_y8, br_x8, br_y8)

        circulation_obj4 = circulation(g4, room7, room8)
        common_edge4 = circulation_obj4.find_common_edges(room7, room8)
        print("Common edge case4:", common_edge4)

    # test_comm_edges()

if __name__ == "__main__":
    main()
