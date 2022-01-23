"""InputGraph class

This module provides InputGraph class to the user and allows to 
create single/multiple dimensionless/dimensioned floorplans.

This module contains the following functions:

    * generate_multiple_rel - generates multiple RELs for given matrix and boundary.
    * generate_multiple_bdy - generates multiple boundary for given matrix and extra edges.
"""
import copy
import numpy as np
import networkx as nx
from random import randint
from .graphoperations import biconnectivity as bcn
from .graphoperations import oneconnectivity as onc
from .graphoperations import operations as opr
from .irregular import shortcutresolver as sr
from .boundary import cip as cip
from .boundary import news as news
from .floorplangen import contraction as cntr
from .floorplangen import expansion as exp
from .floorplangen import rdg as rdg
from .graphoperations import triangularity as trng
from .floorplangen import transformation as transform
from .dimensioning import floorplan_to_st as fpts
from .floorplangen import flippable as flp
from .irregular import septri as st
from .dimensioning import block_checker as bc

class OCError(Exception):
    pass
class InputGraph:
    """A InputGraph class for graph input by the user.
    This class provides methods to generate single or
     multiple dimensioned/dimensionless floorplans.

    This module contains the following functions:

    * single_dual - generates a single dual for a given input graph.
    * single_floorplan - generates a single floorplan for a given input graph.
    * multiple_dual - generates multiple duals for a given input graph.
    * multiple_floorplan - generates multiple floorplans for a given input graph.

    Attributes:
        nodecnt: An integer count of the number of nodes in the graph.
        edgecnt: An integer count of the number of edges in the graph.
        matrix: An adjacency matrix of the graph.
        bdy_nodes: A list containing all boundary nodes in the graph.
        bdy_edges: A list contaning all boundary edges in the graph.
        cip: A list containing all cips in the graph.
        irreg_nodes1: A list containing irregular room nodes 1. 
                        (list of list for multiple floorplans)
        irreg_nodes2: A list containing irregular room nodes 2. 
                        (list of list for multiple floorplans)
        mergednodes: A list containing nodes to be merged.
                        (list of list for multiple floorplans)
        degrees: A list containing degree of each node.
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
        nodecnt_list: A list containing node count for each rel matrix.
        nonrect: A boolean indicating if non rectangular floor plans exist.
        extranodes: A list containing extra nodes added for biconnectivity 
                    and triangularity. (list of list for multiple floorplans)
        area: A list containing the area of each room.
                (list of list for multiple floorplans)
        rel_matrix_list: A list containing multiple rel_matrices.
        floorplan_exist: A boolean indicating floorplan exists.
        fpcnt: An integer indicating the count of floorplans.
        coordinates: A list containing the coordinates of each node.
    """

    def __init__(self, nodecnt, edgecnt, edgeset, node_coordinates, matrix):
        self.nodecnt = nodecnt
        self.edgecnt = edgecnt
        self.matrix = np.zeros((self.nodecnt, self.nodecnt), int)
        if (matrix == []):
            self.matrix = np.zeros((self.nodecnt, self.nodecnt), int)
            for edges in (edgeset):
                self.matrix[edges[0]][edges[1]] = 1
                self.matrix[edges[1]][edges[0]] = 1
        else:
            self.matrix = matrix
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
        self.nodecnt_list = []
        self.nonrect = False
        self.extranodes = []
        self.area = []
        self.rel_matrix_list = []
        self.floorplan_exist = False
        self.fpcnt = 0
        self.coordinates = [np.array(x) for x in node_coordinates]

    def irreg_single_dual(self):
        """Generates an irregular single dual for a given input graph.

        Args:
            None

        Returns:
            None
        """
        #Biconnectivity Augmentation
        bcn_edges = []
        if (not bcn.is_biconnected(self.matrix)):
            bcn_edges = bcn.biconnect(self.matrix)
        for edge in bcn_edges:
            self.matrix[edge[0]][edge[1]] = 1
            self.matrix[edge[1]][edge[0]] = 1
            self.edgecnt += 1  # Extra edge added
        
        #Triangularity
        trng_edges = trng.triangulate(self.matrix)
        for edge in trng_edges:
            self.matrix[edge[0]][edge[1]] = 1
            self.matrix[edge[1]][edge[0]] = 1
            self.edgecnt += 1  # Extra edge added
        
        if(len(bcn_edges) != 0 or len(trng_edges) != 0):
            self.nonrect = True
        
        #Separating Triangle Elimination
        if(self.nodecnt - self.edgecnt + len(opr.get_trngls(self.matrix)) != 1):
            ptpg_matrices, extra_nodes = st.handle_STs(
                self.matrix, self.coordinates, 1)
            self.matrix = ptpg_matrices[0]
            self.nodecnt = self.matrix.shape[0]
            self.edgecnt = int(np.count_nonzero(self.matrix == 1)/2)
            for key in extra_nodes[0]:
                self.mergednodes.append(key)
                self.irreg_nodes1.append(extra_nodes[0][key][0])
                self.irreg_nodes2.append(extra_nodes[0][key][1])

        #Edge Transformation        
        for edge in bcn_edges:
            self.extranodes.append(self.nodecnt)
            self.matrix, extra_edges_cnt = transform.transform_edges(
                self.matrix, edge)
            self.nodecnt += 1  # Extra node added
            self.edgecnt += extra_edges_cnt
        for edge in trng_edges:
            self.extranodes.append(self.nodecnt)
            self.matrix, extra_edges_cnt = transform.transform_edges(
                self.matrix, edge)
            self.nodecnt += 1  # Extra node added
            self.edgecnt += extra_edges_cnt
        
        #Boundary Identification
        triangular_cycles = opr.get_trngls(self.matrix)
        digraph = opr.get_directed(self.matrix)
        self.bdy_nodes, self.bdy_edges = opr.get_bdy(
            triangular_cycles, digraph)
        shortcuts = sr.get_shortcut(
            self.matrix, self.bdy_nodes, self.bdy_edges)
        bdys = []
        if(self.edgecnt == 3 and self.nodecnt == 3):
            bdys = [[0], [0, 1], [1, 2], [2, 0]]
        else:
            bdy_ordered = opr.ordered_bdy(self.bdy_nodes, self.bdy_edges)
            cips = cip.find_cip(bdy_ordered, shortcuts)
            if(len(cips) <= 4):
                bdys = news.bdy_path(news.find_bdy(cips), bdy_ordered)
            else:
                while(len(shortcuts) > 4):
                    index = randint(0, len(shortcuts)-1)
                    self.matrix = sr.remove_shortcut(
                        shortcuts[index], triangular_cycles, self.matrix)
                    self.irreg_nodes1.append(shortcuts[index][0])
                    self.irreg_nodes2.append(shortcuts[index][1])
                    self.mergednodes.append(self.nodecnt)
                    self.nodecnt += 1  # Extra vertex added to remove shortcut
                    self.edgecnt += 3  # Extra edges added to remove shortcut
                    shortcuts.pop(index)
                    triangular_cycles = opr.get_trngls(self.matrix)
                bdy_ordered = opr.ordered_bdy(self.bdy_nodes, self.bdy_edges)
                cips = cip.find_cip(bdy_ordered, shortcuts)
                bdys = news.bdy_path(news.find_bdy(cips), bdy_ordered)

        #4-completion
        self.matrix, self.edgecnt = news.add_news(
            bdys, self.matrix, self.nodecnt, self.edgecnt)
        self.nodecnt += 4

        #Contraction
        self.degrees = cntr.degrees(self.matrix)
        goodnodes = cntr.goodnodes(self.matrix, self.degrees)
        self.matrix, self.degrees, goodnodes, cntrs = cntr.contract(
            self.matrix, goodnodes, self.degrees)

        #Expansion
        self.matrix = exp.basecase(self.matrix, self.nodecnt)
        while len(cntrs) != 0:
            self.matrix = exp.expand(self.matrix, self.nodecnt, cntrs)
        [self.room_x, self.room_y, self.room_width, self.room_height, self.room_x_bottom_left, self.room_x_bottom_right, self.room_x_top_left, self.room_x_top_right,
            self.room_y_left_bottom, self.room_y_right_bottom, self.room_y_left_top, self.room_y_right_top] = rdg.construct_dual(self.matrix, self.nodecnt, self.mergednodes, self.irreg_nodes1)

    def single_floorplan(self, min_width, min_height, max_width, max_height, symm_rooms, min_ar, max_ar, plot_width, plot_height):
        """Generates a single floorplan for a given input graph.

        Args:
            min_width: A list containing the minimum width constraint of each room.
            min_height: A list containing the minimum height constraint of each room.
            max_width: A list containing the maximum width constraint of each room.
            max_height: A list containing the maximum height constraint of each room.
            symm_rooms: A string representing symmetric room constraint.
            min_ar: A list containing the minimum aspect ratio constraint of each room.
            max_ar: A list containing the maximum aspect ratio constraint of each room.
            plot_width: An integer representing plot width constraint.
            plot_height: An integer representing plot height constraint

        Returns:
            None
        """
        for i in range(0, len(self.mergednodes[0])):
            min_width.append(0)
            min_height.append(0)
            max_width.append(10)
            max_height.append(10)
            min_ar.append(0)
            max_ar.append(10000)
        for i in range(0, len(self.extranodes[0])):
            min_width.append(0)
            min_height.append(0)
            max_height.append(10000)
            max_width.append(10000)
            min_ar.append(0)
            max_ar.append(10000)
        for i in range(len(self.rel_matrix_list)):
            rel_matrix = self.rel_matrix_list[i]
            encoded_matrix = opr.get_encoded_matrix(
                rel_matrix.shape[0]-4, self.room_x[i], self.room_y[i], self.room_width[i], self.room_height[i])
            encoded_matrix_deepcopy = copy.deepcopy(encoded_matrix)
            [boolean, ver_list, hor_list] = bc.block_checker(
                encoded_matrix_deepcopy, symm_rooms)
            if boolean:
                [width, height, hor_dgph, status] = fpts.floorplan_to_st(
                    encoded_matrix_deepcopy, min_width, min_height, max_width, max_height, ver_list, hor_list, min_ar, max_ar, plot_width, plot_height)
            else:
                status = False
            if(status == False):
                continue
            else:
                self.floorplan_exist = True
            width = np.transpose(width)
            height = np.transpose(height)
            self.room_width = width.flatten()
            self.room_height = height.flatten()
            self.extranodes, self.mergednodes, self.irreg_nodes1 = self.extranodes[i], self.mergednodes[i], self.irreg_nodes1[i]
            [self.room_x, self.room_y, self.room_width, self.room_height, self.room_x_bottom_left, self.room_x_bottom_right, self.room_x_top_left, self.room_x_top_right, self.room_y_left_bottom, self.room_y_right_bottom,
                self.room_y_left_top, self.room_y_right_top] = rdg.construct_floorplan(encoded_matrix, self.nodecnt + 4, self.room_width, self.room_height, hor_dgph, self.mergednodes, self.irreg_nodes1)
            for j in range(0, len(self.room_x)):
                self.room_x[j] = round(self.room_x[j], 3)
            for j in range(0, len(self.room_y)):
                self.room_y[j] = round(self.room_y[j], 3)
            self.area = opr.calculate_area(
                self.room_x.shape[0], self.room_width, self.room_height, self.extranodes, self.mergednodes, self.irreg_nodes1)
            
            break

    def irreg_multiple_dual(self):
        """Generates multiple irregular duals for a given input graph.

        Args:
            None

        Returns:
            None
        """
        #Biconnectivity Augmentation
        bcn_edges = []
        if (not bcn.is_biconnected(self.matrix)):
            bcn_edges = bcn.biconnect(self.matrix)
        for edge in bcn_edges:
            self.matrix[edge[0]][edge[1]] = 1
            self.matrix[edge[1]][edge[0]] = 1
            self.edgecnt += 1  # Extra edge added

        #Triangulation
        trng_edges = trng.triangulate(self.matrix)
        for edge in trng_edges:
            self.matrix[edge[0]][edge[1]] = 1
            self.matrix[edge[1]][edge[0]] = 1
            self.edgecnt += 1
        
        if(len(bcn_edges) != 0 or len(trng_edges) != 0):
            self.nonrect = True
        
        if(self.nodecnt - self.edgecnt + len(opr.get_trngls(self.matrix)) != 1):
            origin_pos = nx.planar_layout(nx.from_numpy_matrix(self.matrix))
            pos = [origin_pos[i] for i in range(0, self.nodecnt)]
            ptpg_matrices, extra_nodes = st.handle_STs(self.matrix, pos, 20)

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
                self.matrix, cip_list, self.nodecnt, self.edgecnt, extranodes = generate_multiple_bdy(
                    self.matrix, self.nodecnt, self.edgecnt, bcn_edges, trng_edges)
                for bdys in cip_list:
                    matrix = copy.deepcopy(self.matrix)
                    rel_matrices = generate_multiple_rel(
                        bdys, matrix, self.nodecnt, self.edgecnt)
                    for i in rel_matrices:
                        self.fpcnt += 1
                        self.rel_matrix_list.append(i)
                        self.mergednodes.append(mergednodes)
                        self.irreg_nodes1.append(irreg_nodes1)
                        self.irreg_nodes2.append(irreg_nodes2)
                        self.extranodes.append(extranodes)
                        self.nodecnt_list.append(self.nodecnt)
        else:
            self.matrix, cip_list, self.nodecnt, self.edgecnt, extranodes = generate_multiple_bdy(
                self.matrix, self.nodecnt, self.edgecnt, bcn_edges, trng_edges)
            for bdys in cip_list:
                matrix = copy.deepcopy(self.matrix)
                rel_matrices = generate_multiple_rel(
                    bdys, matrix, self.nodecnt, self.edgecnt)
                for i in rel_matrices:
                    self.fpcnt += 1
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
            [room_x, room_y, room_width, room_height, room_x_bottom_left, room_x_bottom_right, room_x_top_left, room_x_top_right, room_y_left_bottom, room_y_right_bottom,
                room_y_left_top, room_y_right_top] = rdg.construct_dual(self.rel_matrix_list[cnt], self.nodecnt_list[cnt] + 4, self.mergednodes[cnt], self.irreg_nodes1[cnt])
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

    def multiple_floorplan(self, min_width, min_height, max_width, max_height, symm_rooms, min_ar, max_ar, plot_width, plot_height):
        """Generates multiple floorplans for a given input graph.

        Args:
            min_width: A list containing the minimum width constraint of each room.
            min_height: A list containing the minimum height constraint of each room.
            max_width: A list containing the maximum width constraint of each room.
            max_height: A list containing the maximum height constraint of each room.
            symm_rooms: A string representing symmetric room constraint.
            min_ar: A list containing the minimum aspect ratio constraint of each room.
            max_ar: A list containing the maximum aspect ratio constraint of each room.
            plot_width: An integer representing plot width constraint.
            plot_height: An integer representing plot height constraint.

        Returns:
            None
        """
        for i in range(0, len(self.mergednodes[0])):
            min_width.append(0)
            min_height.append(0)
            max_width.append(10000)
            max_height.append(10000)
            min_ar.append(0)
            max_ar.append(10000)
        for i in range(0, len(self.extranodes[0])):
            min_width.append(0)
            min_height.append(0)
            max_height.append(10000)
            max_width.append(10000)
            min_ar.append(0)
            max_ar.append(10000)
        status_list = []
        for i in range(len(self.rel_matrix_list)):
            rel_matrix = self.rel_matrix_list[i]
            encoded_matrix = opr.get_encoded_matrix(
                rel_matrix.shape[0]-4, self.room_x[i], self.room_y[i], self.room_width[i], self.room_height[i])
            encoded_matrix_deepcopy = copy.deepcopy(encoded_matrix)
            [boolean, ver_list, hor_list] = bc.block_checker(
                encoded_matrix_deepcopy, symm_rooms)
            if boolean:
                [width, height, hor_dgph, status] = fpts.floorplan_to_st(
                    encoded_matrix_deepcopy, min_width, min_height, max_width, max_height, ver_list, hor_list, min_ar, max_ar, plot_width, plot_height)
            else:
                status = False
            status_list.append(status)
            if(status == False):
                continue
            else:
                self.floorplan_exist = True
            width = np.transpose(width)
            height = np.transpose(height)
            self.room_width[i] = width.flatten()
            self.room_height[i] = height.flatten()
            [self.room_x[i], self.room_y[i], self.room_width[i], self.room_height[i], self.room_x_bottom_left[i], self.room_x_bottom_right[i], self.room_x_top_left[i], self.room_x_top_right[i], self.room_y_left_bottom[i],
                self.room_y_right_bottom[i], self.room_y_left_top[i], self.room_y_right_top[i]] = rdg.construct_floorplan(encoded_matrix, self.nodecnt + 4, self.room_width[i], self.room_height[i], hor_dgph, self.mergednodes[i], self.irreg_nodes1[i])
            for j in range(0, len(self.room_x[i])):
                self.room_x[i][j] = round(self.room_x[i][j], 3)
            for j in range(0, len(self.room_y[i])):
                self.room_y[i][j] = round(self.room_y[i][j], 3)
            self.area.append(opr.calculate_area(
                self.room_x[i].shape[0], self.room_width[i], self.room_height[i], self.extranodes[i], self.mergednodes[i], self.irreg_nodes1[i]))

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

    def oneconnected_dual(self, string):
        """Generates oneconnected rectangular duals for a given input graph.

        Args:
            string: A string representing single or multiple dual.

        Returns:
            None
        """
        #Identifying cut-vertices
        matrix = copy.deepcopy(self.matrix)
        matrix = np.array(matrix)
        nodes = len(matrix)
        nxgraph = nx.from_numpy_matrix(matrix)
        cutvertices = bcn.get_cutvertices(nxgraph)
        components = onc.get_biconnected_components(nxgraph)
        adj_mats = []
        dicts = []
        corners = []

        #Creating dictionary map
        for i in range(0, len(components)):
            adj_mats.append(onc.get_adj_matrix(matrix, components[i]))
            dicts.append(onc.get_dict(components[i]))
        ems = []

        #Generating multiple floorplans for each component
        for i in range(0, len(components)):
            matrix1 = adj_mats[i]
            nodecnt = len(matrix1[0])
            edgecnt = int(np.sum(matrix1) / 2)
            graph = InputGraph(nodecnt
                                   , edgecnt
                                   ,[],[], matrix1)

            corners = []
            graph.irreg_multiple_dual()
            #Identifying corners
            for j in range(len(graph.rel_matrix_list)):
                m = graph.rel_matrix_list[j]
                n = len(m)
                for x in range(0, n):
                    if (m[n - 1][x] == 3 and m[x][n - 4] == 2):
                        nw = x
                    if (m[x][n - 4] == 2 and m[x][n - 3] == 3):
                        ne = x
                    if (m[x][n - 3] == 3 and m[n - 2][x] == 2):
                        se = x
                    if (m[n - 2][x] == 2 and m[n - 1][x] == 3):
                        sw = x
                corners.append([nw, ne, se, sw])

            #Checking if the floorplan matches the requirement
            idx = []
            em = []
            cmpt_cv = {}

            for key in dicts[i].keys():
                if key in cutvertices:
                    cmpt_cv[dicts[i][key]] = 0
            for j in range(0, len(corners)):
                for key in cmpt_cv.keys():
                    cmpt_cv[key] = 0
                for k in range(0, 4):
                    if corners[j][k] in cmpt_cv:
                        cmpt_cv[corners[j][k]] = cmpt_cv[corners[j][k]] + 1
                flag = 1
                for value in cmpt_cv.values():
                    if value != 2:
                        flag = 0
                        break
                if flag:
                    idx.append(j)


            res = dict((v, k) for k, v in dicts[i].items())

            for i in range(len(idx)):
                rel_matrix = graph.rel_matrix_list[idx[i]]
                encoded_matrix = opr.get_encoded_matrix(rel_matrix.shape[0] - 4
                                                        , graph.room_x[idx[i]]
                                                        , graph.room_y[idx[i]]
                                                        , graph.room_width[idx[i]]
                                                        , graph.room_height[idx[i]])
                rows = encoded_matrix.shape[0]
                cols = encoded_matrix.shape[1]

                for x in range(0, rows):
                    for y in range(0, cols):
                        encoded_matrix[x][y] = res[encoded_matrix[x][y]]

                em.append(encoded_matrix)
            ems.append(em)

        #Error condition: No encoded matrix present for any component        
        for i in range(0, len(ems)):
            if len(ems[i])== 0:
                raise OCError

        #Merging encoded matrices to form multiple rels
        final = []
        individual = []
        onc.recurse(ems, 0, final, individual)
        final_em = []
        for i in range(0, len(final)):
            final_em.append(onc.merge(final[i]))
        for i in range(len(final_em)):
            rel = onc.convert_to_rel(final_em[i], nodes)
            self.rel_matrix_list.append(rel)

        #Returning floorplans as per string
        if(string == "single"):
            [self.room_x, self.room_y, self.room_width, self.room_height, self.room_x_bottom_left, self.room_x_bottom_right,
            self.room_x_top_left, self.room_x_top_right,
            self.room_y_left_bottom, self.room_y_right_bottom, self.room_y_left_top,
            self.room_y_right_top] = rdg.construct_dual(self.rel_matrix_list[0], nodes + 4, [], [])
        elif(string == "multiple"):
            self.fpcnt = len(self.rel_matrix_list)
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
            self.extranodes = []
            self.mergednodes = []
            self.irreg_nodes1 = []
            self.irreg_nodes2 = []
            
            
            for cnt in range(self.fpcnt):
                [room_x, room_y, room_width, room_height, room_x_bottom_left, room_x_bottom_right, room_x_top_left, room_x_top_right, room_y_left_bottom, room_y_right_bottom,
                    room_y_left_top, room_y_right_top] = rdg.construct_dual(self.rel_matrix_list[cnt], nodes + 4, [], [])
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
                self.mergednodes.append([])
                self.irreg_nodes1.append([])
                self.irreg_nodes2.append([])
                self.extranodes.append([])

    def single_dual(self):
        """Generates a single dual for a given input graph.

        Args:
            None

        Returns:
            None
        """
        if (not bcn.is_biconnected(self.matrix)):
            try:
                self.oneconnected_dual("single")
            except OCError:
                self.irreg_single_dual()
        else:
            self.irreg_single_dual()
    
    def multiple_dual(self):
        """Generates multiple duals for a given input graph.

        Args:
            None

        Returns:
            None
        """
        if (not bcn.is_biconnected(self.matrix)):
            try:
                self.oneconnected_dual("multiple")
            except OCError:
                self.irreg_multiple_dual()
        else:
            self.irreg_multiple_dual()

def generate_multiple_rel(bdys, matrix, nodecnt, edgecnt):
    """Generates multiple RELs for given matrix and boundary.

    Args:
        bdys: A list representing the boundary of the graph.
        matrix: A matrix representing the adjacency matrix of the graph.
        nodecnt: An integer representing the node count of the graph.
        edgecnt: An integer representing the edge count of the graph.
    Returns:
        rel_matrix: A list containing rel_matrix for given boundary
                    and adjacency matrix.
    """
    matrix, edgecnt = news.add_news(bdys, matrix, nodecnt, edgecnt)
    news_matrix = copy.deepcopy(matrix)
    nodecnt += 4
    degrees = cntr.degrees(news_matrix)
    goodnodes = cntr.goodnodes(news_matrix, degrees)
    news_matrix, degrees, goodnodes, cntrs = cntr.contract(
        news_matrix, goodnodes, degrees)

    news_matrix = exp.basecase(news_matrix, nodecnt)
    while len(cntrs) != 0:
        news_matrix = exp.expand(news_matrix, nodecnt, cntrs)
    rel_matrix = []
    rel_matrix.append(news_matrix)
    for mat in rel_matrix:
        flippable_edges = flp.get_flippable_edges(matrix, mat, nodecnt-4)
        flippable_vertices, flippable_vertices_neighbours = flp.get_flippable_vertices(
            matrix, mat, nodecnt-4)
        for j in range(0, len(flippable_edges)):
            new_rel = flp.resolve_flippable_edge(flippable_edges[j], mat)
            if(not any(np.array_equal(new_rel, i) for i in rel_matrix)):
                rel_matrix.append(new_rel)
        for j in range(0, len(flippable_vertices)):
            new_rel = flp.resolve_flippable_vertex(
                flippable_vertices[j], flippable_vertices_neighbours[j], mat)
            if(not any(np.array_equal(new_rel, i) for i in rel_matrix)):
                rel_matrix.append(new_rel)
    return rel_matrix

def generate_multiple_bdy(matrix, nodecnt, edgecnt, bcn_edges, trng_edges):
    """Generates multiple boundary for given matrix and extra edges.

    Args:
        matrix: A matrix representing the adjacency matrix of the graph.
        nodecnt: An integer representing the node count of the graph.
        edgecnt: An integer representing the edge count of the graph.
        bcn_edges: A list containing extra edges added for biconnectivity.
        trng_edges: A list containing extra edges added for triangularity.
    Returns:
        matrix: A matrix representing the adjacency matrix of the graph.
        cip_list: A list containing differemt possible boundaries.
        nodecnt: An integer representing the node count of the graph.
        edgecnt: An integer representing the edge count of the graph.
        extranodes: A list containing the extra nodes added to the graph.
    """
    extranodes = []
    for edge in bcn_edges:
        extranodes.append(nodecnt)
        matrix, extra_edges_cnt = transform.transform_edges(matrix, edge)
        nodecnt += 1  # Extra node added
        edgecnt += extra_edges_cnt
    for edge in trng_edges:
        extranodes.append(nodecnt)
        matrix, extra_edges_cnt = transform.transform_edges(matrix, edge)
        nodecnt += 1  # Extra node added
        edgecnt += extra_edges_cnt
    triangular_cycles = opr.get_trngls(matrix)
    digraph = opr.get_directed(matrix)
    bdy_nodes, bdy_edges = opr.get_bdy(triangular_cycles, digraph)
    shortcuts = sr.get_shortcut(matrix, bdy_nodes, bdy_edges)
    if(edgecnt == 3 and nodecnt == 3):
        cip_list = [[[0], [0, 1], [1, 2], [2, 0]], [
            [0, 1], [1], [1, 2], [2, 0]], [[0, 1], [1, 2], [2], [2, 0]]]
    else:
        bdy_ordered = opr.ordered_bdy(bdy_nodes, bdy_edges)
        cips = cip.find_cip(bdy_ordered, shortcuts)
        corner_pts = news.multiple_corners(news.find_bdy(cips))
        outer_boundary = opr.ordered_bdy(bdy_nodes, bdy_edges)
        cip_list = news.find_multiple_boundary(
            news.all_boundaries(corner_pts, outer_boundary), outer_boundary)
    return matrix, cip_list, nodecnt, edgecnt, extranodes
