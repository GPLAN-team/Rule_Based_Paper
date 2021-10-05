"""InputGraph class

This module provides Ptpg class to the user and allows to 
create multiple dimensioned floorplans.

"""
import copy
import numpy as np
import networkx as nx
from random import randint
import source.graphoperations.biconnectivity as bcn
import source.graphoperations.operations as opr
import source.separatingtriangle.shortcutresolver as sr
import source.boundary.cip as cip
import source.boundary.news as news
import source.floorplangen.contraction as cntr
import source.floorplangen.expansion as exp
import source.floorplangen.rdg as rdg
import source.separatingtriangle.k4 as k4
import source.graphoperations.triangularity as trng
import source.floorplangen.transformation as transform
import source.dimensioning.floorplan_to_st as fpts
import source.floorplangen.flippable as flp
import source.separatingtriangle.gen_septri as gst
# import itertools as itr
# import warnings

# import time


# import flippable as flp


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
        bdy_nodes: A list containing all boundary nodes in the graph.
        bdy_edges: A list contaning all boundary edges in the graph.
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
        self.bdy_nodes = []
        self.bdy_edges = []
        self.irreg_nodes1 = []
        self.irreg_nodes2 = []
        self.mergednodes = []
        self.degrees = None
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
        self.nodecnt_list=[]
        self.nonrect = False
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
        self.area = []
        self.rel_matrix_list = []
        self.floorplan_exist = False
        self.fpcnt = 0
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
    
    def single_dual(self):
        """Generates a single dual for a given input graph.

        Args:
            None

        Returns:
            None
        """
        bcn_edges = []
        if (not bcn.isBiconnected(self)):
            bcn.initialize_bcc_sets(self)
            bcn.find_articulation_points(self)
            bcn_edges = bcn.make_biconnected(self)
        trng_edges = trng.triangulate(self.matrix)
        if(len(bcn_edges) != 0 or len(trng_edges) != 0):
            self.nonrect = True
        for edge in bcn_edges:
            self.matrix[edge[0]][edge[1]] = 1
            self.matrix[edge[1]][edge[0]] = 1
            self.edgecnt += 1 #Extra edge added
        for edge in trng_edges:
            self.matrix[edge[0]][edge[1]] = 1
            self.matrix[edge[1]][edge[0]] = 1
            self.edgecnt += 1 #Extra edge added
        if(self.nodecnt - self.edgecnt + len(opr.get_trngls(self.matrix)) != 1):
            origin_pos = nx.planar_layout(nx.from_numpy_matrix(self.matrix))
            pos = [origin_pos[i] for i in range(0,self.nodecnt)]
            ptpg_matrices, extra_nodes = gst.handle_STs(self.matrix, pos, 1)
            self.matrix = ptpg_matrices[0]
            self.nodecnt = self.matrix.shape[0]
            self.edgecnt = int(np.count_nonzero(self.matrix == 1)/2)
            for key in extra_nodes[0]:
                self.mergednodes.append(key)
                self.irreg_nodes1.append(extra_nodes[0][key][0])
                self.irreg_nodes2.append(extra_nodes[0][key][1])
        for edge in bcn_edges:
            self.extranodes.append(self.nodecnt)
            self.matrix,extra_edges_cnt = transform.transform_edges(self.matrix,edge)
            self.nodecnt += 1 #Extra node added
            self.edgecnt += extra_edges_cnt
        for edge in trng_edges:
            self.extranodes.append(self.nodecnt)
            self.matrix,extra_edges_cnt = transform.transform_edges(self.matrix,edge)
            self.nodecnt += 1 #Extra node added
            self.edgecnt += extra_edges_cnt          
        print("After triangulation and biconnectivity: ", self.matrix)
        triangular_cycles = opr.get_trngls(self.matrix)
        digraph = opr.get_directed(self.matrix)
        self.bdy_nodes,self.bdy_edges = opr.get_bdy(triangular_cycles, digraph)
        print(self.bdy_nodes,self.bdy_edges)
        shortcuts = sr.get_shortcut(self.matrix,self.bdy_nodes, self.bdy_edges)
        bdys = []
        if(self.edgecnt == 3 and self.nodecnt == 3):
            bdys = [[0],[0,1],[1,2],[2,0]]
        else:
            bdy_ordered = opr.ordered_bdy(self.bdy_nodes, self.bdy_edges)
            cips = cip.find_cip(bdy_ordered, shortcuts)
            if(len(cips) <= 4):
                bdys = news.bdy_path(news.find_bdy(cips)
                                        , bdy_ordered)
            else:
                while(len(shortcuts) > 4):
                    index = randint(0,len(shortcuts)-1)
                    self.matrix = sr.remove_shortcut(shortcuts[index]
                        , triangular_cycles
                        , self.matrix)
                    self.irreg_nodes1.append(shortcuts[index][0])
                    self.irreg_nodes2.append(shortcuts[index][1])
                    self.mergednodes.append(self.nodecnt)
                    self.nodecnt += 1 #Extra vertex added to remove shortcut
                    self.edgecnt += 3 #Extra edges added to remove shortcut
                    shortcuts.pop(index)
                    triangular_cycles = opr.get_trngls(self.matrix)
                bdy_ordered = opr.ordered_bdy(self.bdy_nodes, self.bdy_edges)
                cips = cip.find_cip(bdy_ordered, shortcuts)
                bdys = news.bdy_path(news.find_bdy(cips)
                                    , bdy_ordered)

        self.matrix, self.edgecnt = news.add_news(bdys, self.matrix, self.nodecnt, self.edgecnt)
        self.nodecnt += 4

        self.degrees = cntr.degrees(self.matrix)
        goodnodes = cntr.goodnodes(self.matrix, self.degrees)
        self.matrix, self.degrees, goodnodes,cntrs = cntr.contract(self.matrix
                                                            , goodnodes
                                                            , self.degrees)

        self.matrix = exp.basecase(self.matrix, self.nodecnt)
        while len(cntrs) != 0:
            self.matrix = exp.expand(self.matrix, self.nodecnt, cntrs)
        [self.room_x
        , self.room_y
        , self.room_width
        , self.room_height
        , self.room_x_bottom_left
        , self.room_x_bottom_right
        , self.room_x_top_left
        , self.room_x_top_right
        , self.room_y_left_bottom
        , self.room_y_right_bottom
        , self.room_y_left_top
        , self.room_y_right_top] = rdg.construct_dual(self.matrix
                                                        , self.nodecnt
                                                        , self.mergednodes
                                                        , self.irreg_nodes1)
    
    def single_floorplan(self, min_width, min_height, max_width, max_height, symm_rooms, min_ar, max_ar, plot_width, plot_height):
        for i in range(len(self.rel_matrix_list)):
            rel_matrix = self.rel_matrix_list[i]
            encoded_matrix = opr.get_encoded_matrix(rel_matrix.shape[0]-4
                                    , self.room_x[i]
                                    , self.room_y[i]
                                    , self.room_width[i]
                                    , self.room_height[i])
            encoded_matrix_deepcopy = copy.deepcopy(encoded_matrix)
            [width,height,hor_dgph,status] = fpts.floorplan_to_st(encoded_matrix_deepcopy
                                                , min_width
                                                , min_height
                                                , max_width
                                                , max_height
                                                , symm_rooms
                                                , min_ar
                                                , max_ar
                                                , plot_width
                                                , plot_height)
            if(status==False):
                continue
            else:
                self.floorplan_exist = True
            width = np.transpose(width)
            height = np.transpose(height)
            self.room_width = width.flatten()
            self.room_height = height.flatten()
            [self.room_x
                , self.room_y
                , self.room_width
                , self.room_height
                , self.room_x_bottom_left
                , self.room_x_bottom_right
                , self.room_x_top_left
                , self.room_x_top_right
                , self.room_y_left_bottom
                , self.room_y_right_bottom
                , self.room_y_left_top
                , self.room_y_right_top] = rdg.construct_floorplan(encoded_matrix
                                                            , self.nodecnt + 4
                                                            , self.room_width
                                                            , self.room_height
                                                            , hor_dgph
                                                            , self.mergednodes
                                                            , self.irreg_nodes1)
            for j in range(0,len(self.room_x)):
                self.room_x[j]=round(self.room_x[j],3)
            for j in range(0,len(self.room_y)):
                self.room_y[j]=round(self.room_y[j],3)
            self.area = opr.calculate_area(self.room_x.shape[0]
                                    , self.room_width
                                    , self.room_height
                                    , self.extranodes
                                    , self.mergednodes
                                    , self.irreg_nodes1)
            break

    def multiple_dual(self):
        bcn_edges = []
        if (not bcn.isBiconnected(self)):
            bcn.initialize_bcc_sets(self)
            bcn.find_articulation_points(self)
            bcn_edges = bcn.make_biconnected(self)
        trng_edges = trng.triangulate(self.matrix)
        if(len(bcn_edges) != 0 or len(trng_edges) != 0):
            self.nonrect = True
        for edge in bcn_edges:
            self.matrix[edge[0]][edge[1]] = 1
            self.matrix[edge[1]][edge[0]] = 1
            self.edgecnt += 1 #Extra edge added
        for edge in trng_edges:
            self.matrix[edge[0]][edge[1]] = 1
            self.matrix[edge[1]][edge[0]] = 1
            self.edgecnt += 1
        if(self.nodecnt - self.edgecnt + len(opr.get_trngls(self.matrix)) != 1):
            origin_pos = nx.planar_layout(nx.from_numpy_matrix(self.matrix))
            pos = [origin_pos[i] for i in range(0,self.nodecnt)]
            ptpg_matrices, extra_nodes = gst.handle_STs(self.matrix, pos, 20)

            for cnt in range(len(ptpg_matrices)):
                self.matrix = ptpg_matrices[cnt]
                self.nodecnt = self.matrix.shape[0]
                self.edgecnt = int(np.count_nonzero(self.matrix == 1)/2)
                mergednodes = []
                irreg_nodes1 = []
                irreg_nodes2 = []
                for key in extra_nodes[cnt]:
                    mergednodes.append(key)
                    irreg_nodes1.append(extra_nodes[cnt][key][0])
                    irreg_nodes2.append(extra_nodes[cnt][key][1])
                self.matrix, cip_list, self.nodecnt, self.edgecnt, extranodes = generate_multiple_bdy(self.matrix, self.nodecnt, self.edgecnt, bcn_edges, trng_edges)
                for bdys in cip_list:
                    matrix = copy.deepcopy(self.matrix)
                    rel_matrices = generate_multiple_rel(bdys,matrix,self.nodecnt,self.edgecnt)
                    for i in rel_matrices:
                        self.fpcnt +=1
                        self.rel_matrix_list.append(i)
                        self.mergednodes.append(mergednodes)
                        self.irreg_nodes1.append(irreg_nodes1)
                        self.irreg_nodes2.append(irreg_nodes2)
                        self.extranodes.append(extranodes)
                        self.nodecnt_list.append(self.nodecnt)
        else: 
            self.matrix, cip_list, self.nodecnt, self.edgecnt, extranodes = generate_multiple_bdy(self.matrix, self.nodecnt, self.edgecnt, bcn_edges, trng_edges)
            for bdys in cip_list:
                matrix = copy.deepcopy(self.matrix)
                rel_matrices = generate_multiple_rel(bdys,matrix,self.nodecnt,self.edgecnt)
                for i in rel_matrices:
                    self.fpcnt +=1
                    self.rel_matrix_list.append(i)
                    self.mergednodes.append([])
                    self.irreg_nodes1.append([])
                    self.irreg_nodes2.append([])
                    self.extranodes.append(extranodes)
                    self.nodecnt_list.append(self.nodecnt)

        self.room_x = []
        self.room_y = []
        self.room_width = []
        self.room_height = []
        self.room_x_bottom_left = []
        self.room_x_bottom_right = []
        self.room_x_top_left = []
        self.room_x_top_right = []
        self.room_y_left_bottom = []
        self.room_y_right_bottom = []
        self.room_y_left_top = []
        self.room_y_right_top = []
        self.area = []
        for cnt in range(self.fpcnt):
            [room_x
                , room_y
                , room_width
                , room_height
                , room_x_bottom_left
                , room_x_bottom_right
                , room_x_top_left
                , room_x_top_right
                , room_y_left_bottom
                , room_y_right_bottom
                , room_y_left_top
                , room_y_right_top] = rdg.construct_dual(self.rel_matrix_list[cnt]
                                                            ,self.nodecnt_list[cnt] + 4
                                                            ,self.mergednodes[cnt]
                                                            ,self.irreg_nodes1[cnt])
            self.room_x.append(room_x)
            self.room_y.append(room_y)
            self.room_width.append(room_width)
            self.room_height.append(room_height)
            self.room_x_bottom_left.append(room_x_bottom_left)
            self.room_x_bottom_right.append(room_x_bottom_right)
            self.room_x_top_left.append(room_x_top_left)
            self.room_x_top_right.append(room_x_top_right)
            self.room_y_left_bottom.append(room_y_left_bottom)
            self.room_y_right_bottom.append(room_y_right_bottom)
            self.room_y_left_top.append(room_y_left_top)
            self.room_y_right_top.append(room_y_right_top)
            self.area.append([])

    def multiple_floorplan(self, min_width, min_height, max_width, max_height, symm_rooms, min_ar, max_ar, plot_width, plot_height):
        status_list = []
        for i in range(len(self.rel_matrix_list)):
            rel_matrix = self.rel_matrix_list[i]
            encoded_matrix = opr.get_encoded_matrix(rel_matrix.shape[0]-4
                                    , self.room_x[i]
                                    , self.room_y[i]
                                    , self.room_width[i]
                                    , self.room_height[i])
            encoded_matrix_deepcopy = copy.deepcopy(encoded_matrix)
            [width,height,hor_dgph,status] = fpts.floorplan_to_st(encoded_matrix_deepcopy
                                                , min_width
                                                , min_height
                                                , max_width
                                                , max_height
                                                , symm_rooms
                                                , min_ar
                                                , max_ar
                                                , plot_width
                                                , plot_height)
            status_list.append(status)
            if(status==False):
                continue
            else:
                self.floorplan_exist = True
            width = np.transpose(width)
            height = np.transpose(height)
            self.room_width[i] = width.flatten()
            self.room_height[i] = height.flatten()
            [self.room_x[i]
                , self.room_y[i]
                , self.room_width[i]
                , self.room_height[i]
                , self.room_x_bottom_left[i]
                , self.room_x_bottom_right[i]
                , self.room_x_top_left[i]
                , self.room_x_top_right[i]
                , self.room_y_left_bottom[i]
                , self.room_y_right_bottom[i]
                , self.room_y_left_top[i]
                , self.room_y_right_top[i]] = rdg.construct_floorplan(encoded_matrix
                                                            , self.nodecnt + 4
                                                            , self.room_width[i]
                                                            , self.room_height[i]
                                                            , hor_dgph
                                                            , self.mergednodes
                                                            , self.irreg_nodes1)
            for j in range(0,len(self.room_x[i])):
                self.room_x[i][j]=round(self.room_x[i][j],3)
            for j in range(0,len(self.room_y[i])):
                self.room_y[i][j]=round(self.room_y[i][j],3)
            self.area.append(opr.calculate_area(self.room_x[i].shape[0]
                                    , self.room_width[i]
                                    , self.room_height[i]
                                    , self.extranodes
                                    , self.mergednodes
                                    , self.irreg_nodes1))
    
        room_x = []
        room_y = []
        room_width = []
        room_height = []
        room_x_bottom_left = []
        room_x_bottom_right = []
        room_x_top_left = []
        room_x_top_right = []
        room_y_left_bottom = []
        room_y_right_bottom = []
        room_y_left_top = []
        room_y_right_top = []
        for i in range(len(status_list)):
            if status_list[i] == True:
                room_x.append(self.room_x[i])
                room_y.append(self.room_y[i])
                room_width.append(self.room_width[i])
                room_height.append(self.room_height[i])
                room_x_bottom_left.append(self.room_x_bottom_left[i])
                room_x_bottom_right.append(self.room_x_bottom_right[i])
                room_x_top_left.append(self.room_x_top_left[i])
                room_x_top_right.append(self.room_x_top_right[i])
                room_y_left_bottom.append(self.room_y_left_bottom[i])
                room_y_right_bottom.append(self.room_y_right_bottom[i])
                room_y_left_top.append(self.room_y_left_top[i])
                room_y_right_top.append(self.room_y_right_top[i])
        self.room_x = room_x
        self.room_y = room_y
        self.room_width = room_width
        self.room_height = room_height
        self.room_x_bottom_left = room_x_bottom_left
        self.room_x_bottom_right = room_x_bottom_right
        self.room_x_top_left = room_x_top_left
        self.room_x_top_right = room_x_top_right 
        self.room_y_left_bottom = room_y_left_bottom 
        self.room_y_right_bottom = room_y_right_bottom 
        self.room_y_left_top = room_y_left_top 
        self.room_y_right_top = room_y_right_top 

def generate_multiple_rel(bdys,matrix,nodecnt,edgecnt):
    matrix,edgecnt = news.add_news(bdys,matrix,nodecnt,edgecnt)
    news_matrix = copy.deepcopy(matrix)
    nodecnt += 4
    degrees = cntr.degrees(news_matrix)
    goodnodes = cntr.goodnodes(news_matrix,degrees)
    news_matrix,degrees,goodnodes,cntrs = cntr.contract(news_matrix
                                                    ,goodnodes
                                                    ,degrees)

    news_matrix = exp.basecase(news_matrix,nodecnt)
    while len(cntrs) != 0:
        news_matrix = exp.expand(news_matrix,nodecnt,cntrs)
    rel_matrix = []
    rel_matrix.append(news_matrix)
    for mat in rel_matrix:
        flippable_edges = flp.get_flippable_edges(matrix,mat,nodecnt-4)
        flippable_vertices, flippable_vertices_neighbours = flp.get_flippable_vertices(matrix,mat,nodecnt-4)
        print("Flippable edges: ",len(flippable_edges))
        print("Flippable vertices: ",len(flippable_vertices))
        for j in range(0,len(flippable_edges)):
            new_rel = flp.resolve_flippable_edge(flippable_edges[j],mat)
            if(not any(np.array_equal(new_rel, i) for i in rel_matrix)):
                rel_matrix.append(new_rel)
        for j in range(0,len(flippable_vertices)):
            new_rel = flp.resolve_flippable_vertex(flippable_vertices[j],flippable_vertices_neighbours[j],mat)
            if(not any(np.array_equal(new_rel, i) for i in rel_matrix)):
                rel_matrix.append(new_rel)
    return rel_matrix

    

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
        
def generate_multiple_bdy(matrix, nodecnt, edgecnt, bcn_edges, trng_edges):
    extranodes = []
    for edge in bcn_edges:
        extranodes.append(nodecnt)
        matrix,extra_edges_cnt = transform.transform_edges(matrix,edge)
        nodecnt += 1 #Extra node added
        edgecnt += extra_edges_cnt
    for edge in trng_edges:
        extranodes.append(nodecnt)
        matrix,extra_edges_cnt = transform.transform_edges(matrix,edge)
        nodecnt += 1 #Extra node added
        edgecnt += extra_edges_cnt 
    triangular_cycles = opr.get_trngls(matrix)
    digraph = opr.get_directed(matrix)
    bdy_nodes,bdy_edges = opr.get_bdy(triangular_cycles,digraph)
    shortcuts = sr.get_shortcut(matrix,bdy_nodes,bdy_edges)
    if(edgecnt==3 and nodecnt==3):
        cip_list = [[[0],[0,1],[1,2],[2,0]],[[0,1],[1],[1,2],[2,0]],[[0,1],[1,2],[2],[2,0]]]
    else:
        bdy_ordered = opr.ordered_bdy(bdy_nodes,bdy_edges)
        cips = cip.find_cip(bdy_ordered,shortcuts)
        corner_pts = news.multiple_corners(news.find_bdy(cips))
        outer_boundary = opr.ordered_bdy(bdy_nodes,bdy_edges)
        cip_list= news.find_multiple_boundary(news.all_boundaries(corner_pts,outer_boundary),outer_boundary)
    print("Number of boundaries: ",len(cip_list))
    return matrix, cip_list, nodecnt, edgecnt, extranodes

    