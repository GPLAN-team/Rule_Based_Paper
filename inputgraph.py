"""InputGraph class

This module provides Ptpg class to the user and allows to 
create multiple dimensioned floorplans.

"""
import numpy as np
import networkx as nx
from random import randint
import biconnectivity as bcn
import operations as opr
import shortcutresolver as sr
import cip
import news
import contraction as cntr
import expansion as exp
import rdg
import k4
import triangularity as trng
import transformation as transform
# import itertools as itr
# import warnings

# import time


# import flippable as flp
# import copy

# from floorplan_to_st import floorplan_to_st
# import dimension_gui as dimgui
# import K4
# import biconnectivity as bcn
# import checker
# import cip
# import boundary_select as bdyslt
# import triangularity as trng
# import transformation
# import math

class InputGraph:
    """A InputGraph class for graph input by the user.
    This class provides methods to generate single or
     multiple dimensioned/dimensionless floorplans.

    Attributes:
        nodecnt: An integer count of the number of nodes in the graph.
        edgecnt: An integer count of the number of edges in the graph.
        matrix: An adjacency matrix of the graph.
        north: An integer indicating the node number
               of the North vertex. (Default value: nodecnt)
        east: An integer indicating the node number
              of the North vertex. (Default value: nodecnt+1)
        south: An integer indicating the node number 
               of the North vertex. (Default value: nodecnt+2)
        west: An integer indicating the node number 
              of the North vertex. (Default value: nodecnt+3)
        trngls: A list containing all triangular cycles in the graph.
        digraph: A networkx digraph of the graph.
        bdy_nodes: A list containing all boundary nodes in the graph.
        bdy_edges: A list contaning all boundary edges in the graph.
        shortcuts: A list containing all shortcuts in the graph.
        cip: A list containing all cips in the graph.
        irreg_nodes1: A list containing irregular room nodes.
        irreg_nodes2: A list containing irregular room nodes.
        mergednodes: A list containing nodes to be merged.
        degrees: A list containing degree of each node.
        goodnodes: A list containing good vertices.
        cntrs: A list containing contractions in defined order.
        t1_matrix: A matrix representing t1 matrix of the graph.
        t2_matrix: A matrix representing t2 matrix of the graph.
        t1longestdist: A matrix represent longest distance
                      in t1 matrix for each node.
        t2longestdist: A matrix represent longest distance 
                      in t2 matrix for each node.
        t1longestdistval: An integer representing longest
                         distance in t1 matrix.
        t2longestdistval: An integer representing longest
                          distance in t2 matrix.
        nspaths: A list representng north-south paths.
        wepaths: A list representing west-east paths.
        room_x: A list containing bottom-left x coordinate
                of each room.
        room_y: A list containing bottom-left y coordinate
               of each room.
        room_x_bottom_right: A list containing rightmost-middle
                             x coordinate in bottom edge.
        room_x_bottom_left: A list containing leftmost-middle
                            x coordinate in bottom edge.
        room_x_top_right: A list containing rightmost-middle
                          x coordinate in top edge.
        room_x_top_left: A list containing leftmost-middle
                         x coordinate in top edge.
        room_y_right_top: A list containing topmost-middle
                          x coordinate in right edge.
        room_y_left_top: A list containing topmost-middle
                         x coordinate in left edge.
        room_y_right_bottom: A list containing bottommost-middle
                             x coordinate in right edge.
        room_y_left_bottom: A list containing bottommost-middle
                            x coordinate in left edge.
        room_height: A list containing height of each room.
        room_width: A list containing width of each room.
        k4: A list containing k4 cycles in the graph.
        nonrect:  A boolean representing if the graph
                  has rectangular floorplan.
        trng_edges: A list containing edges to be added in
                    triangulation.
        extranodes: A list representing extra nodes added.
    """
    
    def __init__(self,nodecnt,edgecnt,edgeset):
        self.nodecnt=nodecnt 
        self.edgecnt=edgecnt
        self.matrix = np.zeros((self.nodecnt, self.nodecnt), int) 
        for edges in (edgeset): 
            self.matrix[edges[0]][edges[1]] = 1
            self.matrix[edges[1]][edges[0]] = 1
        self.north = self.nodecnt
        self.east = self.nodecnt + 1
        self.south = self.nodecnt + 2
        self.west = self.nodecnt + 3
        self.trngls = opr.get_trngls(self)
        self.digraph = opr.get_directed(self)
        self.bdy_nodes = []
        self.bdy_edges = []
        self.shortcuts = []
        self.cip = []
        self.irreg_nodes1 = []
        self.irreg_nodes2 = []
        self.mergednodes = []
        self.degrees = None
        self.goodnodes = None
        self.cntrs = []
        self.t1_matrix = None
        self.t2_matrix = None
        self.t1longestdist = [-1] * (self.nodecnt + 4)
        self.t2longestdist = [-1] * (self.nodecnt + 4)
        self.t1longestdistval = -1
        self.t2longestdistval = -1
        self.nspaths = []
        self.wepaths = []
        self.room_x = np.zeros(self.nodecnt)
        self.room_y = np.zeros(self.nodecnt)
        self.room_x_bottom_right = np.zeros(self.nodecnt)
        self.room_x_bottom_left = np.zeros(self.nodecnt)
        self.room_x_top_right = np.zeros(self.nodecnt)
        self.room_x_top_left = np.zeros(self.nodecnt)
        self.room_y_right_top = np.zeros(self.nodecnt)
        self.room_y_left_top = np.zeros(self.nodecnt)
        self.room_y_right_bottom = np.zeros(self.nodecnt)
        self.room_y_left_bottom = np.zeros(self.nodecnt)
        self.room_height = np.zeros(self.nodecnt)
        self.room_width = np.zeros(self.nodecnt)
        self.k4=[]
        self.nonrect = False
        self.trng_edges = []
        self.extranodes = []
        self.time = 0
        self.articulationpts = [False] * (self.nodecnt)
        self.articulationptscnt = 0
        self.articulationpts_val = []
        self.bcccnt = 0
        self.bccsets = [set() for i in range(self.nodecnt)]
        self.articulationpts_sets = [set() for i in range(self.nodecnt)]
        self.added_edges = set()
        self.removed_edges = set()
        self.bcn_edges = set()
        # self.rdg_vertices = []
        # self.to_be_merged_vertices = []
        # self.k4 = []
        # self.rdg_vertices2 =[]
        # self.user_matrix = None
        # self.edge_matrix = None
        # self.edge_matrix1 = None
        # self.colors= value[6]
        # self.names= value[5]
        # self.width_min=[]
        # self.width_max=[]
        # self.height_min=[]
        # self.height_max=[]

        # self.cip_list = []
        # self.cip = []
        # self.rdg_vertices = []
        # self.to_be_merged_vertices = []
        # self.k4 = []
        # self.rdg_vertices2 =[]

        
        
        

        # self.original_north = self.north
        # self.original_east = self.east
        # self.original_south = self.south
        # self.original_west = self.west


        # self.rel_matrix =[]
        # self.room_x = np.zeros(self.node_count)
        # self.room_x_list = []
        # self.room_y = np.zeros(self.node_count)
        # self.room_y_list = []
        # self.room_x_bottom_right = np.zeros(self.node_count)
        # self.room_x_bottom_right_list = []
        # self.room_x_bottom_left = np.zeros(self.node_count)
        # self.room_x_bottom_left_list =[]
        # self.room_x_top_right = np.zeros(self.node_count)
        # self.room_x_top_right_list =[]
        # self.room_x_top_left = np.zeros(self.node_count)
        # self.room_x_top_left_list = []
        # self.room_y_right_top = np.zeros(self.node_count)
        # self.room_y_right_top_list =[]
        # self.room_y_left_top = np.zeros(self.node_count)
        # self.room_y_left_top_list =[]
        # self.room_y_right_bottom = np.zeros(self.node_count)
        # self.room_y_right_bottom_list = []
        # self.room_y_left_bottom = np.zeros(self.node_count)
        # self.room_y_left_bottom_list = []
        # self.room_height = np.zeros(self.node_count)
        # self.room_height_list = []
        # self.room_width_list = []
        # self.room_width = np.zeros(self.node_count)
        # self.encoded_matrix = None
        # self.area = []
        # self.user_boundary_constraint = []
        # self.user_corner_constraint = []
        # self.directed = opr.get_directed(self)
        # self.triangles = opr.get_all_triangles(self)
        # self.outer_vertices = opr.get_outer_boundary_vertices(self)[0]
        # self.outer_boundary = opr.get_outer_boundary_vertices(self)[1]
        # self.shortcuts = None
        # self.shortcut_list = []
        # self.boundaries = []
        
        # self.Time = 0
        # self.articulation_points = [False] * (self.node_count)
        # self.no_of_articulation_points = 0
        # self.articulation_points_value = []
        # self.no_of_bcc = 0
        # self.bcc_sets = [set() for i in range(self.node_count)]
        # self.articulation_point_sets = [set() for i in range(self.node_count)]
        # self.added_edges = set()
        # self.removed_edges = set()
        # self.final_added_edges = set()
        # self.biconnected_vertices = []
        # self.extra_vertices=[]

        # self.original_edge_count = self.edge_count
        # self.original_node_count = self.node_count
    

    
    def make_corridor(self,e1, e2,canvas,num, color = "white",  wide = 0):
        self.leaves = self.nodes
        leaves = self.leaves
        room1 = leaves[e1]
        room2 = leaves[e2]
        pts = self.common_points(room1, room2,num, 2)
        if len(pts) != 4:
            pts = self.common_points(room2,room1,num, 2)
        print(pts)
        if len(pts) == 4:
            
            if wide >0:
                if( abs( pts[0]- pts[2] )  > abs ( pts[1] - pts[3] ) ):             # hor
                    print("hor")
                    if pts[0] < pts[2] :
                        canvas.create_rectangle(pts[0] + wide,pts[1],pts[2] - wide,pts[3],fill= cyan, outline = cyan)
                    else:                        
                        canvas.create_rectangle(pts[0] - wide,pts[1],pts[2] + wide,pts[3],fill= cyan, outline = cyan)
                else :
                    print("ver")
                    if pts[1] < pts[3]:
                        canvas.create_rectangle(pts[0],pts[1] + wide ,pts[2],pts[3] - wide,fill= cyan, outline = cyan)
                    else :
                        canvas.create_rectangle(pts[0],pts[1]  ,pts[2],pts[3],fill= cyan, outline = cyan)
    
            else :
                canvas.create_rectangle(pts[0],pts[1],pts[2],pts[3],fill=color, outline = color)

    def make_space(self,e1, e2,canvas,num):
        self.leaves = self.nodes
        leaves = self.leaves
        room1 = leaves[e1]
        room2 = leaves[e2]
        print(vars(room1))

        print(vars(room2))
        pts = self.common_points(room1, room2,num, 2)
        if len(pts) != 4:
            pts = self.common_points(room2,room1, num, 2)
        print(pts)
        if len(pts) == 4:
            # canvas.create_rectangle(pts[0],pts[1],pts[2],pts[3],fill="black", outline = "black")
            if( abs( pts[0]- pts[2] )  > abs ( pts[1] - pts[3] ) ):             # hor
                var1 = pts[0]/2 + pts[2]/2
                canvas.create_rectangle(var1 - 5,pts[1],var1 + 5,pts[3],fill="white",outline="white")
                print("hor")
            else :
                print("ver")
                var1 = pts[1]/2 + pts[3] / 2
                canvas.create_rectangle(pts[0],var1 -5 ,pts[2],var1 + 5,fill="white",outline="white")
                
    def intersect(self,row1, row2, n):
        pt = []
        for i in range(0,n):
            if(row1[i]==1 and row2[i]==1):
                pt.append(i)

        return pt

    # d1 = topx; d2 = topleft y;d3 = botrig x; d4 = botrig y
    def common_points(self,leaf1, leaf2,num, wide):
        pt = []
        if ( leaf1.d4 == leaf2.d2):
            print("commonpt11")
            pt.append( max(leaf1.d1,leaf2.d1) -wide)
            pt.append(leaf1.d4-wide)
            pt.append(min(leaf1.d3,leaf2.d3 ) )
            pt.append(leaf1.d4+wide)
        elif ( leaf1.d3 == leaf2.d1):
            print("commonpt9")
            pt.append(leaf2.d1-wide)
            pt.append(min( leaf1.d2,leaf2.d2)-wide)
            pt.append(leaf2.d1+wide)
            pt.append(max(leaf1.d4,leaf2.d4))
        return pt

    def add_cir(self,cir_class,canvas):
        mat = cir_class.matrix
        e1 = 1
        e2 = 2
        print(e1,e2)
        print("hi")
        i = 0
        self.leaves = self.nodes
        leaves = self.leaves
        for room in leaves: # drawing all 
            i+=1
            canvas.create_rectangle(room.d1,room.d2, room.d3, room.d4, fill = colors[i], width = 5)
            canvas.create_text((room.d1+room.d3)/2,(room.d2+room.d4)/2,text=i - 1)

        num_corridors = len(mat) - len(leaves)
        print("No of corridors are ",num_corridors)
        n = len(leaves)
        self.make_corridor(e1 - 1 ,e2 - 1,canvas,0)
        mat = np.squeeze(np.asarray(mat))

        for cor in range(n+1,len(mat)):
            print(cor, "row", len(mat[cor]), "sz")
            for itr in range(n,cor):
                print(itr,"col")
                if( mat[cor][itr] == 1):
                    rms = self.intersect(mat[cor], mat[itr], n)
                    print(rms , "rms")
                    self.make_corridor(rms[0] , rms[1], canvas,1)
                    break

    def circulation(self,pen,canvas, cir_class, door1, door2):
        print("Make corrdor start")
        num_cor = cir_class.node_count - self.node_count
        print(num_cor)
        self.create_treenodes()
        
        self.add_cir(cir_class,canvas)

    def create_treenodes(self):
        width= np.amax(self.room_width)
        height = np.amax(self.room_height)
        self.nodes = []
        origin = {'x': 50 - 200, 'y': -50}
        scale = 100*(math.exp(-0.30*width+math.log(0.8)) + 0.1)
        for i in range(self.room_x.shape[0]):
            node = gui.treenode(None, None, None, self.room_height[i], self.room_width[i], None, (self.room_x[i]) * scale + origin['x'], (self.room_y[i]+ self.room_height[i]) * scale + origin['y'], (self.room_x[i] + self.room_width[i]) * scale + origin['x'], (self.room_y[i]) * scale + origin['y'] )
            print(node.d1, node.d2, node.d3, node.d4)
            self.nodes.append(node)

    def make_walls(self, canvas, connectivity = []):  # additional edges , create tree nodes , pen, canvas, part of make corridor in a for loop with additional edges
        self.create_treenodes()
        self.leaves = self.nodes
        leaves = self.leaves
        i = 0
        print( "rdg", self.rdg_vertices)

        for room in leaves: # drawing all 
            
            if i not in self.extra_v:
                canvas.create_rectangle(room.d1,room.d2, room.d3, room.d4, width = 5, fill = colors[i])
                if len(self.to_be_merged_vertices) is 0 or i < (self.to_be_merged_vertices[0]):
                    canvas.create_text((room.d1+room.d3)/2,(room.d2+room.d4)/2,text= i)
                i+=1
        i= 0
        print("Room No {x1,y1,x2,y2} ")
        for room in leaves :
            if room in self.rdg_vertices:
                print("Room ",i,"{",room.d1,room.d2,room.d3,room.d4,"}")
                i+=1

        print("--------------------------")
        print(self.graph.edges())
        # nx.draw(self.graph, labels=None, font_size=12, font_color='k', font_family='sans-serif', font_weight='normal', alpha=1.0, bbox=None, ax=None)
        # plt.show()
        con = [] 
        print()
        for edge in connectivity:
            con.append((edge[0],edge[1]))
        print("con", con)
        self.connectivity_graph = con
        print("conn", self.connectivity_graph)
        for edge in self.graph.edges():
            # i = input()
            print(edge)
            if ( edge in con) or ((edge[1],edge[0]) in con):
                self.make_space(edge[0], edge[1], canvas, 1)

        # nx.draw(self.graph, labels=None, font_size=12, font_color='k', font_family='sans-serif', font_weight='normal', alpha=1.0, bbox=None, ax=None)
        # plt.show()
        

        for edge in self.additional_adjacencies:
            print("make_walls")
            print(edge)
            self.make_corridor(edge[0], edge[1], canvas, 1, "black")
        
        for edge in self.final_added_edges:
            print("make_walls")
            print(edge)
            self.make_corridor(edge[0], edge[1], canvas, 1, "black")

    def merge_orthogonal_walls(self, canvas):
        for i in range(len(self.to_be_merged_vertices)):
            self.make_corridor(self.to_be_merged_vertices[i], self.rdg_vertices[i], canvas, 1, cyan, 5)
        
        # for edge in self.graph.edges():
        #     print(edge)
        #     if( edge[0] in self.to_be_merged_vertices and edge[1] in self.to_be_merged_vertices):
                # print(edge)
                # self.make_corridor(edge[0], edge[1], canvas, 1, cyan, 5)

    def single_dual(self):
        """Creates a single dimensionless floorplan for given graph"""
        
        if (not nx.is_biconnected(nx.from_numpy_matrix(self.matrix))):
            bcn.init_bccsets(self)
            bcn.find_articulationpnts(self)
            bcn.makebcn(self)  
        trng.triangulate(self)
        for edge in self.trng_edges:
            trng.addedge(self,edge)
        k4.findk4(self)
        if(len(self.k4)!=0):
            self.nonrect = True
            for k4s in self.k4:
                k4.removek4(self
                    , k4s
                    , k4s.edge
                    , self.irreg_nodes1
                    , self.irreg_nodes2
                    , self.mergednodes)
        for edge in self.trng_edges:
            self.extranodes.append(self.nodecnt)
            transform.transform(self,edge)
            self.nonrect = True
        for edge in self.bcn_edges:
            self.extranodes.append(self.nodecnt)
            transform.transform(self,edge)
            self.nonrect = True
        # if triangulate_type == "space":
        #     # Triangulate with empty spaces
        #     for edges in additional_edges_for_triangulation:
        #         self.extra_vertices.append(self.node_count)
        #         transformation.transformEdges(self,edges)
        #     for edges in self.final_added_edges:
        #         self.extra_vertices.append(self.node_count)
        #         transformation.transformEdges(self,edges)
        # elif triangulate_type == "wall":
        #     for edges in self.final_added_edges:
        #         self.extra_vertices.append(self.node_count)
        #         transformation.transformEdges(self,edges)
        #     # Triangulate with walls or doors, done through drawing.py
        # self.graph = nx.from_numpy_matrix(self.matrix)
        if self.nonrect:
            self.trngls = opr.get_trngls(self)
            self.digraph = opr.get_directed(self)
        # if not nx.check_planarity(self.graph) or (len(self.triangles)+self.node_count-self.edge_count)!=1:
        #     raise Exception("Error")
        
        self.bdy_nodes = opr.get_bdy(self)[0]
        self.bdy_edges = opr.get_bdy(self)[1]
        self.shortcuts = sr.get_shortcut(self)
        if(self.edgecnt==3 and self.nodecnt==3):
            self.cip = [[0],[0,1],[1,2],[2,0]]
        else:
            cips = cip.find_cip(self)
            print(cips)
            if(len(cips)<=4):
                self.cip = news.bdy_path(news.find_bdy(cips),
                    opr.ordered_bdy(self))
            else:
                shortcut = sr.get_shortcut(self)
                while(len(shortcut)>4):
                    index = randint(0,len(shortcut)-1)
                    sr.remove_shortcut(shortcut[index]
                        ,self,self.irreg_nodes1
                        ,self.irreg_nodes2
                        ,self.mergednodes)
                    shortcut.pop(index)
                cips = cip.find_cip(self)
                self.cip = news.bdy_path(news.find_bdy(cips)
                    ,opr.ordered_bdy(self))
        news.add_news(self)

        cntr.init_degrees(self)
        cntr.init_goodnodes(self)
        v, u = cntr.contract(self)
        while v != -1:
            v, u = cntr.contract(self)

        exp.basecase(self)
        while len(self.cntrs) != 0:
            exp.expand(self)

        rdg.construct_dual(self,self.mergednodes,self.irreg_nodes1)
    
    # def create_single_floorplan(self,pen,textbox,mode):
    #     if(mode == 0):
    #         self.create_single_dual(0,pen,textbox)
    #     self.encoded_matrix = opr.get_encoded_matrix(self)
    #     B = copy.deepcopy(self.encoded_matrix)
    #     A = copy.deepcopy(self.encoded_matrix)
    #     # minimum_width = min(self.inp_min)
    #     for i in range(0,len(self.extra_vertices)):
    #         self.width_min.append(0)
    #         self.height_min.append(0)
    #     [width,height,hor_dgph,status] = floorplan_to_st(A,self.width_min,self.height_min,self.width_max,self.height_max)
    #     A=B
    #     # print(A)
    #     width = np.transpose(width)
    #     height = np.transpose(height)
    #     self.room_width = width.flatten()
    #     self.room_height = height.flatten()
    #     draw.construct_rfp(self,hor_dgph,self.to_be_merged_vertices,self.rdg_vertices)
    #     for i in range(0,len(self.room_x)):
    #         self.room_x[i]=round(self.room_x[i],3)
    #         # print(self.room_x[i])
    #     for i in range(0,len(self.room_y)):
    #         self.room_y[i]=round(self.room_y[i],3)
    #         # print(self.room_x[i],self.room_y[i],self.room_width[i],self.room_height[i],self.room_x_top_left[i],self.room_x_top_right[i],self.room_y_left_top[i],self.room_y_left_bottom[i],self.room_x_bottom_left[i],self.room_x_bottom_right[i],self.room_y_right_top[i],self.room_y_right_bottom[i])
    #     # print(self.room_x,self.room_y,self.room_width,self.room_height,self.room_x_top_left,self.room_x_top_right,self.room_y_left_top,self.room_y_left_bottom,self.room_x_bottom_left,self.room_x_bottom_right,self.room_y_right_top,self.room_y_right_bottom)
    #         # print(self.room_y[i])
    #     opr.calculate_area(self,self.to_be_merged_vertices,self.rdg_vertices)
        
    # def create_multiple_dual(self,mode,pen,textbox):
    #     if (not bcn.isBiconnected(self)):
    #         bcn.initialize_bcc_sets(self)
    #         bcn.find_articulation_points(self)
    #         bcn.make_biconnected(self)    
    #     self.edge_count += len(self.final_added_edges)
    #     additional_edges_for_triangulation = trng.Triangulate(self.graph)[2]
    #     for edges in additional_edges_for_triangulation:
    #         print(edges[0],edges[1])
    #         trng.addEdges(self,edges)
    #     K4.find_K4(self)
    #     if(len(self.k4) == 0):
    #         start = time.time()
    #         for edges in additional_edges_for_triangulation:
    #             self.extra_vertices.append(self.node_count)
    #             transformation.transformEdges(self,edges)
    #             print(edges)
    #         for edges in self.final_added_edges:
    #             self.extra_vertices.append(self.node_count)
    #             transformation.transformEdges(self,edges)
    #             print(edges)
    #         self.graph = nx.from_numpy_matrix(self.matrix)
    #         self.triangles = opr.get_all_triangles(self)
    #         print("Faces: ",len(self.triangles))
    #         print("Edges: ",self.edge_count)
    #         print("Vertices: ",self.node_count)
    #         print("Value: ",len(self.triangles)+self.node_count-self.edge_count)
    #         if not nx.check_planarity(self.graph) or (len(self.triangles)+self.node_count-self.edge_count)!=1:
    #             raise Exception("Error")
    #         self.directed = opr.get_directed(self)
    #         self.outer_vertices = opr.get_outer_boundary_vertices(self)[0]
    #         self.outer_boundary = opr.get_outer_boundary_vertices(self)[1]
    #         self.shortcuts = sr.get_shortcut(self)
    #         if(self.edge_count==3 and self.node_count==3):
    #             self.cip_list = [[[0],[0,1],[1,2],[2,0]],[[0,1],[1],[1,2],[2,0]],[[0,1],[1,2],[2],[2,0]]]
    #         else:
    #             cip_test = cip.find_cip(self)
    #             if(len(cip_test)<=4):
    #                 boundaries = news.multiple_boundaries(news.find_boundary_single(cip_test))
    #                 self.cip_list= news.find_multiple_boundary(news.all_boundaries(boundaries,opr.ordered_outer_boundary(self)),opr.ordered_outer_boundary(self))
    #         self.edge_matrix = self.matrix.copy()
    #         self.original_edge_count = self.edge_count
    #         self.original_node_count = self.node_count
    #         if(len(self.cip_list) == 0):
    #             self.shortcut_list = list(itr.combinations(self.shortcuts,len(self.shortcuts)-4))
    #         no_of_boundaries = 0
    #         count = 0
    #         if(len(self.cip_list)== 0):
    #             for resolver in self.shortcut_list:
    #                 rdg_vertices = []
    #                 rdg_vertices2 = []
    #                 to_be_merged_vertices = []
    #                 for i in range(0,size):
    #                     sr.remove_shortcut(resolver[i],self,rdg_vertices,rdg_vertices2,to_be_merged_vertices)
    #                 cip_test = cip.find_cip(self)
    #                 self.cip = news.boundary_path_single(news.find_boundary_single(cip_test),opr.ordered_outer_boundary(self))                    
    #                 print("North Boundary: ", self.cip[2])
    #                 print("East Boundary: ", self.cip[1])
    #                 print("South Boundary: ", self.cip[0])
    #                 print("West Boundary: ",self.cip[3])
    #                 news.add_news_vertices(self)
    #                 cntr.initialize_degrees(self)
    #                 cntr.initialize_good_vertices(self)
    #                 v, u = cntr.contract(self)
    #                 while v != -1:
    #                     v, u = cntr.contract(self)
    #                 exp.get_trivial_rel(self)
    #                 while len(self.contractions) != 0:
    #                     exp.expand(self)
    #                 rel_matrix =[]
    #                 rel_matrix.append(self.matrix)
    #                 self.rdg_vertices.append(rdg_vertices)
    #                 self.rdg_vertices2.append(rdg_vertices2)
    #                 self.to_be_merged_vertices.append(to_be_merged_vertices)
    #                 for i in rel_matrix:
    #                     self.matrix = i
    #                     flippable_edges = flp.get_flippable_edges(self,i)
    #                     flippable_vertices = flp.get_flippable_vertices(self,i)[0]
    #                     flippable_vertices_neighbours = flp.get_flippable_vertices(self,i)[1]
    #                     for j in range(0,len(flippable_edges)):
    #                         new_rel = flp.resolve_flippable_edge(flippable_edges[j],self,i)
    #                         if(not any(np.array_equal(new_rel, i) for i in rel_matrix)):
    #                             rel_matrix.append(new_rel)
    #                             self.rdg_vertices.append(rdg_vertices)
    #                             self.rdg_vertices2.append(rdg_vertices2)
    #                             self.to_be_merged_vertices.append(to_be_merged_vertices)
    #                     for j in range(0,len(flippable_vertices)):
    #                         new_rel = flp.resolve_flippable_vertex(flippable_vertices[j],flippable_vertices_neighbours[j],self,i)
    #                         if(not any(np.array_equal(new_rel, i) for i in rel_matrix)):
    #                             rel_matrix.append(new_rel)
    #                             self.rdg_vertices.append(rdg_vertices)
    #                             self.rdg_vertices2.append(rdg_vertices2)
    #                             self.to_be_merged_vertices.append(to_be_merged_vertices)
    #                 count +=1
    #                 if(count != len(self.shortcut_list)):
    #                     self.node_count = self.original_node_count
    #                     self.edge_count = self.original_edge_count
    #                     self.matrix = self.edge_matrix.copy()
    #                     self.north = self.original_north
    #                     self.west = self.original_west
    #                     self.east = self.original_east
    #                     self.south = self.original_south
    #                 for i in rel_matrix:
    #                     self.rel_matrix.append(i)
    #                 print("Number of different floor plans: ",len(rel_matrix)*2)
    #                 print("\n")
    #                 self.cip = self.original_cip.copy()
    #         else:
    #             self.cip = self.cip_list[0]
    #             self.original_cip = self.cip.copy()
    #             for k in self.cip_list:
    #                 self.cip = k
    #                 news.add_news_vertices(self)
    #                 print("North Boundary: ", self.cip[2])
    #                 print("East Boundary: ", self.cip[1])
    #                 print("South Boundary: ", self.cip[0])
    #                 print("West Boundary: ",self.cip[3])
    #                 no_of_boundaries += 1
    #                 cntr.initialize_degrees(self)
    #                 cntr.initialize_good_vertices(self)
    #                 v, u = cntr.contract(self)
    #                 while v != -1:
    #                     v, u = cntr.contract(self)
    #                 exp.get_trivial_rel(self)
    #                 while len(self.contractions) != 0:
    #                     exp.expand(self)
    #                 rel_matrix =[]
    #                 rel_matrix.append(self.matrix)
    #                 for i in rel_matrix:
    #                     self.matrix = i
    #                     flippable_edges = flp.get_flippable_edges(self,i)
    #                     flippable_vertices = flp.get_flippable_vertices(self,i)[0]
    #                     flippable_vertices_neighbours = flp.get_flippable_vertices(self,i)[1]
    #                     for j in range(0,len(flippable_edges)):
    #                         new_rel = flp.resolve_flippable_edge(flippable_edges[j],self,i)
    #                         if(not any(np.array_equal(new_rel, i) for i in rel_matrix)):
    #                             rel_matrix.append(new_rel)
    #                     for j in range(0,len(flippable_vertices)):
    #                         new_rel = flp.resolve_flippable_vertex(flippable_vertices[j],flippable_vertices_neighbours[j],self,i)
    #                         if(not any(np.array_equal(new_rel, i) for i in rel_matrix)):
    #                             rel_matrix.append(new_rel)
    #                 count +=1
    #                 if(count != len(self.cip_list)):
    #                     self.node_count = self.original_node_count
    #                     self.edge_count = self.original_edge_count
    #                     self.matrix = self.edge_matrix.copy()
    #                 for i in rel_matrix:
    #                     self.rel_matrix.append(i)
    #                 print("Number of different floor plans: ",len(rel_matrix))
    #                 print("\n")
    #         textbox.insert('end',f"\n Total number of different floor plans: {len(self.rel_matrix)}")
    #         textbox.insert('end',"\n")
    #         textbox.insert('end',f"Total boundaries used:{no_of_boundaries}")
    #         textbox.insert('end',"\n")
    #         end = time.time()
    #         textbox.insert('end',f"Time taken per floorlan : {round((end-start)/len(self.rel_matrix),6)*1000} ms")
    #         textbox.insert('end',"\n")
    #         print(f"Runtime of the program is {end - start}")

    #     else:
    #         start = time.time()
    #         self.edge_matrix1 = self.matrix.copy()
    #         original_edge_count1 = self.edge_count
    #         original_node_count1 = self.node_count
    #         no_of_boundaries = 0
    #         count = 0
    #         check = 1
    #         for j in self.k4:
    #             if(j.case !=2 ):
    #                 check = 0
    #                 break
    #         for number in range(0,3):
    #             to_be_merged_vertices = []
    #             rdg_vertices = []
    #             rdg_vertices2 =[]
                
    #             for j in self.k4:
    #                 if(j.case  == 2):
    #                     K4.resolve_K4(self,j,j.edge_to_be_removed,rdg_vertices,rdg_vertices2,to_be_merged_vertices)
    #                 else:
    #                     K4.resolve_K4(self,j,j.all_edges_to_be_removed[number],rdg_vertices,rdg_vertices2,to_be_merged_vertices)
    #             for edges in additional_edges_for_triangulation:
    #                 self.extra_vertices.append(self.node_count)
    #                 transformation.transformEdges(self,edges)
    #                 print(edges)
    #             for edges in self.final_added_edges:
    #                 self.extra_vertices.append(self.node_count)
    #                 transformation.transformEdges(self,edges)
    #                 print(edges)
    #             self.graph = nx.from_numpy_matrix(self.matrix)
    #             self.triangles = opr.get_all_triangles(self)
    #             print("Faces: ",len(self.triangles))
    #             print("Edges: ",self.edge_count)
    #             print("Vertices: ",self.node_count)
    #             print("Value: ",len(self.triangles)+self.node_count-self.edge_count)
    #             if not nx.check_planarity(self.graph) or (len(self.triangles)+self.node_count-self.edge_count)!=1:
    #                 self.node_count = original_node_count1
    #                 self.edge_count = original_edge_count1
    #                 self.matrix = self.edge_matrix1.copy()
    #                 self.north = self.original_north
    #                 self.west = self.original_west
    #                 self.east = self.original_east
    #                 self.south = self.original_south
    #                 continue
    #             self.directed = opr.get_directed(self)
    #             self.triangles = opr.get_all_triangles(self)
    #             self.outer_vertices = opr.get_outer_boundary_vertices(self)[0]
    #             self.outer_boundary = opr.get_outer_boundary_vertices(self)[1]
    #             self.shortcuts = sr.get_shortcut(self)
    #             cip_test = cip.find_cip(self)
    #             if(len(cip_test)<=4):
    #                 boundaries = news.multiple_boundaries(news.find_boundary_single(cip_test))
    #                 self.cip_list= news.find_multiple_boundary(news.all_boundaries(boundaries,opr.ordered_outer_boundary(self)),opr.ordered_outer_boundary(self))
    #             self.edge_matrix = self.matrix.copy()
    #             self.original_edge_count = self.edge_count
    #             self.original_node_count = self.node_count
    #             if(len(self.cip_list) == 0):
    #                 self.shortcut_list = list(itr.combinations(self.shortcuts,len(self.shortcuts)-4))
    #             no_of_boundaries = 0
    #             self.cip = self.cip_list[0]
    #             self.original_cip = self.cip.copy()
    #             for k in self.cip_list:
    #                 self.cip = k
    #                 news.add_news_vertices(self)
    #                 print("North Boundary: ", self.cip[2])
    #                 print("East Boundary: ", self.cip[1])
    #                 print("South Boundary: ", self.cip[0])
    #                 print("West Boundary: ",self.cip[3])
    #                 no_of_boundaries += 1
    #                 cntr.initialize_degrees(self)
    #                 cntr.initialize_good_vertices(self)
    #                 v, u = cntr.contract(self)
    #                 while v != -1:
    #                     v, u = cntr.contract(self)
    #                 exp.get_trivial_rel(self)
    #                 while len(self.contractions) != 0:
    #                     exp.expand(self)
    #                 rel_matrix =[]
    #                 rel_matrix.append(self.matrix)
    #                 self.rdg_vertices.append(rdg_vertices)
    #                 self.rdg_vertices2.append(rdg_vertices2)
    #                 self.to_be_merged_vertices.append(to_be_merged_vertices)
    #                 for i in rel_matrix:
    #                     self.matrix = i
    #                     flippable_edges = flp.get_flippable_edges(self,i)
    #                     flippable_vertices = flp.get_flippable_vertices(self,i)[0]
    #                     flippable_vertices_neighbours = flp.get_flippable_vertices(self,i)[1]
    #                     for j in range(0,len(flippable_edges)):
    #                         new_rel = flp.resolve_flippable_edge(flippable_edges[j],self,i)
    #                         if(not any(np.array_equal(new_rel, i) for i in rel_matrix)):
    #                             self.rdg_vertices.append(rdg_vertices)
    #                             self.rdg_vertices2.append(rdg_vertices2)
    #                             self.to_be_merged_vertices.append(to_be_merged_vertices)
    #                             rel_matrix.append(new_rel)
    #                     for j in range(0,len(flippable_vertices)):
    #                         new_rel = flp.resolve_flippable_vertex(flippable_vertices[j],flippable_vertices_neighbours[j],self,i)
    #                         if(not any(np.array_equal(new_rel, i) for i in rel_matrix)):
    #                             rel_matrix.append(new_rel)
    #                             self.rdg_vertices.append(rdg_vertices)
    #                             self.rdg_vertices2.append(rdg_vertices2)
    #                             self.to_be_merged_vertices.append(to_be_merged_vertices)

    #                 count +=1
    #                 if(count != len(self.cip_list)):
    #                     self.node_count = self.original_node_count
    #                     self.edge_count = self.original_edge_count
    #                     self.matrix = self.edge_matrix.copy()
    #                 for i in rel_matrix:
    #                     self.rel_matrix.append(i)
    #                 print("Number of different floor plans: ",len(rel_matrix))
    #                 print("\n")
    #                 # end = time.time()
    #                 # print(f"Runtime of the program is {end - start}")
    #                 # start = time.time()
    #             if(number!=2 and check == 0):
    #                 self.node_count = original_node_count1
    #                 self.edge_count = original_edge_count1
    #                 self.matrix = self.edge_matrix1.copy()
    #                 self.north = self.original_north
    #                 self.west = self.original_west
    #                 self.east = self.original_east
    #                 self.south = self.original_south
    #                 for j in self.k4:
    #                     j.identified = 0
    #             elif(check == 1):
    #                 break
    #             print("Yeah")
    #         print("Total number of different floor plans: ",len(self.rel_matrix))
    #         print("Total boundaries used:", no_of_boundaries)
    #         end = time.time()
    #         print(f"Runtime of the program is {end - start}")
    #         textbox.insert('end',f"Total number of different floor plans: {len(self.rel_matrix)}")
    #         textbox.insert('end',"\n")
    #         textbox.insert('end',f"Total boundaries used:{no_of_boundaries}")
    #         textbox.insert('end',"\n")
    #         textbox.insert('end',f"Time taken per floorlan : {round((end-start)/len(self.rel_matrix),6)*1000} ms")
    #         textbox.insert('end',"\n")
    #     if(mode == 1):
    #         count = 0
    #         origin_count = 1
    #         for i in self.rel_matrix:
    #             self.matrix = i
    #             if(len(self.to_be_merged_vertices)!= 0):
    #                 draw.construct_rdg(self,self.to_be_merged_vertices[count],self.rdg_vertices[count])
    #                 if(origin_count != 1):
    #                     self.origin += 1000
    #                 draw.draw_rdg(self,origin_count,pen,self.to_be_merged_vertices[count],self.rdg_vertices[count],mode,self.colors,self.names)
    #                 origin_count +=1
    #                 draw.construct_rdg(self,self.to_be_merged_vertices[count],self.rdg_vertices2[count])
    #                 if(origin_count != 1):
    #                     self.origin += 1000
    #                 draw.draw_rdg(self,origin_count,pen,self.to_be_merged_vertices[count],self.rdg_vertices2[count],mode,self.colors,self.names)
    #                 origin_count +=1
    #                 count +=1
                    
    #             else:
    #                 draw.construct_rdg(self,self.to_be_merged_vertices,self.rdg_vertices)
    #                 if(origin_count != 1):
    #                     self.origin += 1000
    #                 draw.draw_rdg(self,origin_count,pen,self.to_be_merged_vertices,self.rdg_vertices,mode,self.colors,self.names)
    #                 origin_count +=1

    # def create_circulation_dual(self,mode,pen,textbox):
    #     global box
    #     box = textbox
    #     self.original_edge_count = self.edge_count
    #     self.original_node_count = self.node_count
    #     self.triangles = opr.get_all_triangles(self)
    #     K4.find_K4(self)
    #     for i in self.k4:
    #         K4.resolve_K4(self,i,i.edge_to_be_removed,self.rdg_vertices,self.rdg_vertices2,self.to_be_merged_vertices)
    #     self.directed = opr.get_directed(self)
    #     self.triangles = opr.get_all_triangles(self)
    #     self.outer_vertices = opr.get_outer_boundary_vertices(self)[0]
    #     self.outer_boundary = opr.get_outer_boundary_vertices(self)[1]
    #     self.shortcuts = sr.get_shortcut(self)
    #     self.cip = news.find_cip_single(self)
    #     # self.cip =[ [0,1,2,3,4,5,6],[6,7,8,9,10,11,12],[12,13,14,15],[15,16,17,18,19,0]]
    #     news.add_news_vertices(self)
    #     print("North Boundary: ", self.cip[0])
    #     print("East Boundary: ", self.cip[1])
    #     print("South Boundary: ", self.cip[2])
    #     print("West Boundary: ",self.cip[3])
    #     for i in range(0,len(self.to_be_merged_vertices)):
    #         self.node_color.append(self.node_color[self.rdg_vertices[i]])
    #     self.node_position = nx.planar_layout(nx.from_numpy_matrix(self.matrix))
    #     cntr.initialize_degrees(self)
    #     cntr.initialize_good_vertices(self)
    #     v, u = cntr.contract(self)
    #     while v != -1:
    #         v, u = cntr.contract(self)
    #         # draw.draw_undirected_graph(self,pen)
    #         # input()
    #     # print(self.contractions)
    #     exp.get_trivial_rel(self)
    #     while len(self.contractions) != 0:
    #         exp.expand(self)
    #     draw.construct_rdg(self,self.to_be_merged_vertices,self.rdg_vertices)
    #     # for i  in range(0,len(self.to_be_merged_vertices)):
    #     #   print(self.room_x[self.to_be_merged_vertices[i]],self.room_y[self.to_be_merged_vertices[i]],self.room_width[self.to_be_merged_vertices[i]],self.room_height[self.to_be_merged_vertices[i]],self.room_x_top_left[self.to_be_merged_vertices[i]],self.room_x_top_right[self.to_be_merged_vertices[i]],self.room_y_left_top[self.to_be_merged_vertices[i]],self.room_y_left_bottom[self.to_be_merged_vertices[i]],self.room_x_bottom_left[self.to_be_merged_vertices[i]],self.room_x_bottom_right[self.to_be_merged_vertices[i]],self.room_y_right_top[self.to_be_merged_vertices[i]],self.room_y_right_bottom[self.to_be_merged_vertices[i]])
    #     #   print(self.room_x[self.rdg_vertices[i]],self.room_y[self.rdg_vertices[i]],self.room_width[self.rdg_vertices[i]],self.room_height[self.rdg_vertices[i]],self.room_x_top_left[self.rdg_vertices[i]],self.room_x_top_right[self.rdg_vertices[i]],self.room_y_left_top[self.rdg_vertices[i]],self.room_y_left_bottom[self.rdg_vertices[i]],self.room_x_bottom_left[self.rdg_vertices[i]],self.room_x_bottom_right[self.rdg_vertices[i]],self.room_y_right_top[self.rdg_vertices[i]],self.room_y_right_bottom[self.rdg_vertices[i]]) 
    #     # print(self.room_x,self.room_y,self.room_width,self.room_height,self.room_x_top_left,self.room_x_top_right,self.room_y_left_top,self.room_y_left_bottom,self.room_x_bottom_left,self.room_x_bottom_right,self.room_y_right_top,self.room_y_right_bottom)
        

    # def create_multiple_floorplan(self,pen,textbox,mode):
    #     global box
    #     box = textbox
    #     self.create_multiple_dual(0,pen,textbox)
    #     count = 0
    #     origin_count = 1
    #     minimum_width = min(self.width_min)
    #     minimum_height = min(self.height_min)
    #     if(len(self.to_be_merged_vertices)!=0):
    #         for i in range(0,len(self.to_be_merged_vertices[0])):
    #             self.width_min.append(minimum_width)
    #             self.height_min.append(minimum_height)
    #     for i in range(0,len(self.extra_vertices)):
    #         self.width_min.append(0)
    #         self.height_min.append(0)
    #     for i in range(0,len(self.rel_matrix)):
    #         self.matrix = self.rel_matrix[i]
    #         if(len(self.to_be_merged_vertices)!= 0):
    #             draw.construct_rdg(self,self.to_be_merged_vertices[count],self.rdg_vertices[count])
    #             self.encoded_matrix = opr.get_encoded_matrix(self)
    #             B = copy.deepcopy(self.encoded_matrix)
    #             A = copy.deepcopy(self.encoded_matrix)
    #             [width,height,hor_dgph,status] = floorplan_to_st(A,self.width_min,self.height_min,self.width_max,self.height_max)
    #             A=B
    #             width = np.transpose(width)
    #             height = np.transpose(height)
    #             self.room_width = width.flatten()
    #             self.room_height = height.flatten()
    #             draw.construct_rfp(self,hor_dgph,self.to_be_merged_vertices[count],self.rdg_vertices[count])
    #             for i in range(0,len(self.room_x)):
    #                 self.room_x[i]=round(self.room_x[i],3)
    #             for i in range(0,len(self.room_y)):
    #                 self.room_y[i]=round(self.room_y[i],3)
    #                 print(self.room_x[i],self.room_y[i],self.room_width[i],self.room_height[i],self.room_x_top_left[i],self.room_x_top_right[i],self.room_y_left_top[i],self.room_y_left_bottom[i],self.room_x_bottom_left[i],self.room_x_bottom_right[i],self.room_y_right_top[i],self.room_y_right_bottom[i])
    #             opr.calculate_area(self,self.to_be_merged_vertices[count],self.rdg_vertices[count])
    #             draw.draw_rdg(self,count+1,pen,self.to_be_merged_vertices[count],self.rdg_vertices[count],mode,self.colors,self.names)
    #             self.area =[]
    #             origin_count +=1
    #             if(origin_count != 1):
    #                 self.origin += 1000
    #             draw.construct_rfp(self,hor_dgph,self.to_be_merged_vertices[count],self.rdg_vertices2[count])
    #             for i in range(0,len(self.room_x)):
    #                 self.room_x[i]=round(self.room_x[i],3)
    #                 # print(self.room_x[i])
    #             for i in range(0,len(self.room_y)):
    #                 self.room_y[i]=round(self.room_y[i],3)
    #             opr.calculate_area(self,self.to_be_merged_vertices[count],self.rdg_vertices2[count])
    #             raw.draw_rdg(self,count+1,pen,self.to_be_merged_vertices[count],self.rdg_vertices[count],mode,self.colors,self.names)
    #             self.area =[]
    #             origin_count+=1
    #             if(origin_count != 1):
    #                 self.origin += 500
                
    #             count+=1
    #         else:
    #             draw.construct_rdg(self,self.to_be_merged_vertices,self.rdg_vertices)
    #             self.encoded_matrix = opr.get_encoded_matrix(self)
    #             B = copy.deepcopy(self.encoded_matrix)
    #             A = copy.deepcopy(self.encoded_matrix)
    #             [width,height,hor_dgph,status] = floorplan_to_st(A,self.width_min,self.height_min,self.width_max,self.height_max)
    #             A=B
    #             # print(A)
    #             width = np.transpose(width)
    #             height = np.transpose(height)
    #             self.room_width = width.flatten()
    #             self.room_height = height.flatten()
    #             draw.construct_rfp(self,hor_dgph,self.to_be_merged_vertices,self.rdg_vertices)
    #             for i in range(0,len(self.room_x)):
    #                 self.room_x[i]=round(self.room_x[i],3)
    #             for i in range(0,len(self.room_y)):
    #                 self.room_y[i]=round(self.room_y[i],3)
    #             if(origin_count != 1):
    #                 self.origin += 500
    #             opr.calculate_area(self,self.to_be_merged_vertices,self.rdg_vertices)
    #             draw.draw_rdg(self,count+1,pen,self.to_be_merged_vertices,self.rdg_vertices,mode,self.colors,self.names)
    #             self.area =[]
    #             origin_count +=1
    #             count+=1