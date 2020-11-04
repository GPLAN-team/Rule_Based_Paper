"""PTPG Class.


"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import itertools as itr
import operations as opr
import warnings
import shortcutresolver as sr
import news
import time
from random import randint
import drawing as draw 
import tkinter as tk
import turtle
import ptpg
import contraction as cntr
import expansion as exp
import flippable as flp
import copy
import gui
from floorplan_to_st import floorplan_to_st
import dimension_gui as dimgui
import K4
import biconnectivity as bcn
import checker
import cip
import boundary_select as bdyslt
import triangularity as trng
import transformation
import math
colors = ['#4BC0D9','#76E5FC','#6457A6','#5C2751','#7D8491','#BBBE64','#64F58D','#9DFFF9','#AB4E68','#C4A287','#6F9283','#696D7D','#1B1F3B','#454ADE','#FB6376','#6C969D','#519872','#3B5249','#A4B494','#CCFF66','#FFC800','#FF8427','#0F7173','#EF8354','#795663','#AF5B5B','#667761','#CF5C36','#F0BCD4','#ADB2D3','#FF1B1C','#6A994E','#386641','#8B2635','#2E3532','#124E78']*10


def printe(string):
	box.insert('end',string)

class PTPG:
	
	# Attribute Initiallization
	def __init__(self,value):
		self.node_count=value[0] #Number of nodes in the graph
		self.edge_count=value[1] #Number of edges in the graph
		self.dimensioned = value[4] # True if dimensioned checkbox is active
		self.command = value[3]
		self.room_names = value[5]
		self.node_color = value[6]
		
		self.additional_adjacencies = None
		self.matrix = np.zeros((self.node_count, self.node_count), int) #Adjacency matrix for the graph
		self.triangulation_type = "wall" 	# Make option for "wall" or "space" and accordingly triangulate non-triangulated
		for i in (value[2]): #Populates the adjacency matrix on basis of edge input
			self.matrix[i[0]][i[1]] = 1
			self.matrix[i[1]][i[0]] = 1
		self.min_width = []  
		self.max_width= []
		self.min_height= []
		self.max_height = []
		self.graph = nx.Graph()
		self.graph.add_edges_from(value[2])
		self.north = self.node_count
		self.east = self.node_count + 1
		self.south = self.node_count + 2
		self.west = self.node_count + 3
		self.user_matrix = None
		self.edge_matrix = None
		self.edge_matrix1 = None
		self.colors= value[6]
		self.names= value[5]
		self.width_min=[]
		self.width_max=[]
		self.height_min=[]
		self.height_max=[]

		self.cip_list = []
		self.cip = []
		self.degrees = None
		self.good_vertices = None
		self.contractions = []
		self.rdg_vertices = []
		self.to_be_merged_vertices = []
		self.k4 = []
		self.rdg_vertices2 =[]

		self.t1_matrix = None
		self.t2_matrix = None
		self.t1_longest_distance = [-1] * (self.node_count + 4)
		self.t2_longest_distance = [-1] * (self.node_count + 4)
		self.t1_longest_distance_value = -1
		self.t2_longest_distance_value = -1
		self.n_s_paths = []
		self.w_e_paths = []

		self.original_north = self.north
		self.original_east = self.east
		self.original_south = self.south
		self.original_west = self.west


		self.rel_matrix =[]
		self.room_x = np.zeros(self.node_count)
		self.room_x_list = []
		self.room_y = np.zeros(self.node_count)
		self.room_y_list = []
		self.room_x_bottom_right = np.zeros(self.node_count)
		self.room_x_bottom_right_list = []
		self.room_x_bottom_left = np.zeros(self.node_count)
		self.room_x_bottom_left_list =[]
		self.room_x_top_right = np.zeros(self.node_count)
		self.room_x_top_right_list =[]
		self.room_x_top_left = np.zeros(self.node_count)
		self.room_x_top_left_list = []
		self.room_y_right_top = np.zeros(self.node_count)
		self.room_y_right_top_list =[]
		self.room_y_left_top = np.zeros(self.node_count)
		self.room_y_left_top_list =[]
		self.room_y_right_bottom = np.zeros(self.node_count)
		self.room_y_right_bottom_list = []
		self.room_y_left_bottom = np.zeros(self.node_count)
		self.room_y_left_bottom_list = []
		self.room_height = np.zeros(self.node_count)
		self.room_height_list = []
		self.room_width_list = []
		self.room_width = np.zeros(self.node_count)
		self.encoded_matrix = None
		self.area = []
		self.user_boundary_constraint = []
		self.user_corner_constraint = []
		self.directed = opr.get_directed(self)
		self.triangles = opr.get_all_triangles(self)
		self.outer_vertices = opr.get_outer_boundary_vertices(self)[0]
		self.outer_boundary = opr.get_outer_boundary_vertices(self)[1]
		self.shortcuts = None
		self.shortcut_list = []
		self.origin = 50
		self.boundaries = []
		
		self.Time = 0
		self.articulation_points = [False] * (self.node_count)
		self.no_of_articulation_points = 0
		self.articulation_points_value = []
		self.no_of_bcc = 0
		self.bcc_sets = [set() for i in range(self.node_count)]
		self.articulation_point_sets = [set() for i in range(self.node_count)]
		self.added_edges = set()
		self.removed_edges = set()
		self.final_added_edges = set()
		self.biconnected_vertices = []
		self.extra_vertices=[]

		self.original_edge_count = self.edge_count
		self.original_node_count = self.node_count
	

	
	def make_corridor(self,e1, e2,canvas,num):
			self.leaves = self.nodes
			leaves = self.leaves
			room1 = leaves[e1]
			room2 = leaves[e2]
			pts = self.common_points(room1, room2,num)
			if len(pts) != 4:
				pts = self.common_points(room2,room1,num)
			print(pts)
			if len(pts) == 4:
				canvas.create_rectangle(pts[0],pts[1],pts[2],pts[3],fill="white", outline = "white")

	def intersect(self,row1, row2, n):
		pt = []
		for i in range(0,n):
			if(row1[i]==1 and row2[i]==1):
				pt.append(i)

		return pt

	def common_points(self,leaf1, leaf2,num):
		pt = []
		if (leaf1.d1 == leaf2.d1 and leaf1.d4 == leaf2.d2):
			if num == 0:
				pt.append(leaf2.d1)
				pt.append(leaf2.d2-5)
			elif num == 1:
				pt.append(leaf2.d1-5)
				pt.append(leaf2.d2-5)
			if leaf1.width <= leaf2.width:
				pt.append(leaf1.d3+5)
				pt.append(leaf1.d4+5)
			else:
				pt.append(leaf2.d3+5)
				pt.append(leaf2.d2+5)
			
		elif (leaf1.d3 == leaf2.d1 and leaf1.d4 == leaf2.d4):
			if num == 0:
				pt.append(leaf1.d3-5)
				pt.append(leaf1.d4)
			elif num == 1:
				pt.append(leaf1.d3-5)
				pt.append(leaf1.d4+5)
			if leaf1.height <= leaf2.height:
				pt.append(leaf1.d3+5)
				pt.append(leaf1.d2-5)
			else:
				pt.append(leaf1.d3+5)
				pt.append(leaf2.d2-5)

		elif (leaf1.d3 == leaf2.d1 and leaf1.d2 == leaf2.d2):
			if num == 0:
				pt.append(leaf2.d1-5)
				pt.append(leaf2.d2)
			elif num == 1:
				pt.append(leaf2.d1-5)
				pt.append(leaf2.d2+5)
			if leaf1.height <= leaf2.height:
				pt.append(leaf1.d3+5)
				pt.append(leaf1.d4-5)
			else:
				pt.append(leaf1.d3+5)
				pt.append(leaf2.d4-5)

		elif (leaf1.d3 == leaf2.d3 and leaf1.d4 == leaf2.d2):
			if num ==0:
				pt.append(leaf1.d3)
				pt.append(leaf1.d4-5)
			elif num == 1:
				pt.append(leaf1.d3+5)
				pt.append(leaf1.d4-5)
			if leaf1.width <= leaf2.width:
				pt.append(leaf1.d1+5)
				pt.append(leaf1.d4+5)
			else:
				pt.append(leaf2.d1+5)
				pt.append(leaf2.d2+5)

		elif ((leaf1.d1 < leaf2.d1 and leaf1.d3 > leaf2.d1 and leaf1.d3 < leaf2.d3) and leaf1.d4 == leaf2.d2):
			pt.append(leaf2.d1-5)
			pt.append(leaf1.d4-5)
			pt.append(leaf1.d3)
			pt.append(leaf1.d4+5)
		elif ((leaf2.d1 < leaf1.d1 and leaf2.d3 > leaf1.d1 and leaf2.d3 < leaf1.d3) and leaf1.d4 == leaf2.d2):
			pt.append(leaf1.d1-5)
			pt.append(leaf1.d4-5)
			pt.append(leaf2.d3)
			pt.append(leaf1.d4+5)
		elif ((leaf1.d2 < leaf2.d2 and leaf1.d4 < leaf2.d4 and leaf2.d2 < leaf1.d4) and leaf1.d3 == leaf2.d1):
			pt.append(leaf2.d1-5)
			pt.append(leaf2.d2-5)
			pt.append(leaf2.d1+5)
			pt.append(leaf1.d4)
		elif ((leaf2.d2 < leaf1.d2 and leaf2.d4 < leaf1.d4 and leaf1.d2 < leaf2.d4) and leaf1.d3 == leaf2.d1):
			pt.append(leaf2.d1-5)
			pt.append(leaf1.d2-5)
			pt.append(leaf2.d1+5)
			pt.append(leaf2.d4)
		elif ((leaf1.d2 < leaf2.d2 and leaf1.d4 > leaf2.d4) and leaf1.d3 == leaf2.d1):
			pt.append(leaf2.d1-5)
			pt.append(leaf2.d2-5)
			pt.append(leaf2.d1+5)
			pt.append(leaf2.d4)
		elif ((leaf1.d1 > leaf2.d1 and leaf2.d3 > leaf1.d3) and leaf1.d4 == leaf2.d2):
			pt.append(leaf1.d1-5)
			pt.append(leaf1.d4-5)
			pt.append(leaf1.d3)
			pt.append(leaf1.d4+5)
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
			canvas.create_rectangle(room.d1,room.d2, room.d3, room.d4, fill = colors[i])
			canvas.create_text((room.d1+room.d3)/2,(room.d2+room.d4)/2,text=i)

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
		width= np.amax(self.room_width)
		height = np.amax(self.room_height)
		self.nodes = []
		origin = {'x': self.origin - 200, 'y': -50}
		scale = 100*(math.exp(-0.30*width+math.log(0.8)) + 0.1)
		for i in range(self.room_x.shape[0]):
			node = gui.treenode(None, None, None, self.room_height[i], self.room_width[i], None, (self.room_x[i]) * scale + origin['x'], (self.room_y[i]+ self.room_height[i]) * scale + origin['y'], (self.room_x[i] + self.room_width[i]) * scale + origin['x'], (self.room_y[i]) * scale + origin['y'] )
			print(node.d1, node.d2, node.d3, node.d4)
			self.nodes.append(node)
		
		self.add_cir(cir_class,canvas)

	def create_single_dual(self,mode,pen,textbox, triangulate_type="space"):
		
		start =time.time()
		if (not bcn.isBiconnected(self)):
			bcn.initialize_bcc_sets(self)
			bcn.find_articulation_points(self)
			bcn.make_biconnected(self)	
		self.edge_count += len(self.final_added_edges)
		additional_edges_for_triangulation = trng.Triangulate(self.graph)[2]
		self.additional_adjacencies = additional_edges_for_triangulation
		print(additional_edges_for_triangulation)
		print(self.edge_count)

		for edges in additional_edges_for_triangulation:
			print(edges[0],edges[1])
			if triangulate_type == "wall":
				trng.addEdges(self,edges, 1)
			else:
				trng.addEdges(self,edges,1)
		K4.find_K4(self)
		if(len(self.k4)!=0):
			for i in self.k4:
				print(i.edge_to_be_removed)
				K4.resolve_K4(self,i,i.edge_to_be_removed,self.rdg_vertices,self.rdg_vertices2,self.to_be_merged_vertices)
		# print("Edges: ",self.edge_count)
		if triangulate_type == "space":
			# Triangulate with empty spaces
			for edges in additional_edges_for_triangulation:
				self.extra_vertices.append(self.node_count)
				transformation.transformEdges(self,edges)
			for edges in self.final_added_edges:
				self.extra_vertices.append(self.node_count)
				transformation.transformEdges(self,edges)
		elif triangulate_type == "wall":
			for edges in self.final_added_edges:
				self.extra_vertices.append(self.node_count)
				transformation.transformEdges(self,edges)
			# Triangulate with walls or doors, done through drawing.py
		self.graph = nx.from_numpy_matrix(self.matrix)
		self.triangles = opr.get_all_triangles(self)
		print(self.graph.edges())
		print("Faces: ",len(self.triangles))
		print("Edges: ",self.edge_count)
		print("Vertices: ",self.node_count)
		print("Value: ",len(self.triangles)+self.node_count-self.edge_count)
		if not nx.check_planarity(self.graph) or (len(self.triangles)+self.node_count-self.edge_count)!=1:
			raise Exception("Error")
		self.directed = opr.get_directed(self)
		self.outer_vertices = opr.get_outer_boundary_vertices(self)[0]
		self.outer_boundary = opr.get_outer_boundary_vertices(self)[1]
		self.shortcuts = sr.get_shortcut(self)
		print(self.outer_boundary)
		if(self.edge_count==3 and self.node_count==3):
			self.cip = [[0],[0,1],[1,2],[2,0]]
		else:
			cips = cip.find_cip(self)
			if(len(cips)<=4):
				self.cip = news.boundary_path_single(news.find_boundary_single(cips),opr.ordered_outer_boundary(self))
			else:
				shortcut = sr.get_shortcut(self)
				while(len(shortcut)>4):
					index = randint(0,len(shortcut)-1)
					sr.remove_shortcut(shortcut[index],self,self.rdg_vertices,self.rdg_vertices2,self.to_be_merged_vertices)
					shortcut.pop(index)
				cips = cip.find_cip(self)
				self.cip = news.boundary_path_single(news.find_boundary_single(cips),opr.ordered_outer_boundary(self))
		news.add_news_vertices(self)

		print("North Boundary: ", self.cip[2])
		print("East Boundary: ", self.cip[1])
		print("South Boundary: ", self.cip[0])
		print("West Boundary: ",self.cip[3])
		cntr.initialize_degrees(self)
		cntr.initialize_good_vertices(self)
		v, u = cntr.contract(self)
		while v != -1:
			v, u = cntr.contract(self)
		exp.get_trivial_rel(self)
		while len(self.contractions) != 0:
			exp.expand(self)
		draw.construct_rdg(self,self.to_be_merged_vertices,self.rdg_vertices)
		end= time.time()
		textbox.insert('end',f"Time taken: {round(end-start,5)} seconds")
		textbox.insert('end',"\n")
	
	def create_single_floorplan(self,pen,textbox,mode):
		if(mode == 0):
			self.create_single_dual(0,pen,textbox)
		self.encoded_matrix = opr.get_encoded_matrix(self)
		B = copy.deepcopy(self.encoded_matrix)
		A = copy.deepcopy(self.encoded_matrix)
		# minimum_width = min(self.inp_min)
		for i in range(0,len(self.extra_vertices)):
			self.width_min.append(0)
			self.height_min.append(0)
		[width,height,hor_dgph] = floorplan_to_st(A,self.width_min,self.height_min)
		A=B
		# print(A)
		width = np.transpose(width)
		height = np.transpose(height)
		self.room_width = width.flatten()
		self.room_height = height.flatten()
		draw.construct_rfp(self,hor_dgph,self.to_be_merged_vertices,self.rdg_vertices)
		for i in range(0,len(self.room_x)):
			self.room_x[i]=round(self.room_x[i],3)
			# print(self.room_x[i])
		for i in range(0,len(self.room_y)):
			self.room_y[i]=round(self.room_y[i],3)
			# print(self.room_x[i],self.room_y[i],self.room_width[i],self.room_height[i],self.room_x_top_left[i],self.room_x_top_right[i],self.room_y_left_top[i],self.room_y_left_bottom[i],self.room_x_bottom_left[i],self.room_x_bottom_right[i],self.room_y_right_top[i],self.room_y_right_bottom[i])
		# print(self.room_x,self.room_y,self.room_width,self.room_height,self.room_x_top_left,self.room_x_top_right,self.room_y_left_top,self.room_y_left_bottom,self.room_x_bottom_left,self.room_x_bottom_right,self.room_y_right_top,self.room_y_right_bottom)
			# print(self.room_y[i])
		opr.calculate_area(self,self.to_be_merged_vertices,self.rdg_vertices)
		
	def create_multiple_dual(self,mode,pen,textbox):
		if (not bcn.isBiconnected(self)):
			bcn.initialize_bcc_sets(self)
			bcn.find_articulation_points(self)
			bcn.make_biconnected(self)	
		self.edge_count += len(self.final_added_edges)
		additional_edges_for_triangulation = trng.Triangulate(self.graph)[2]
		for edges in additional_edges_for_triangulation:
			print(edges[0],edges[1])
			trng.addEdges(self,edges)
		K4.find_K4(self)
		if(len(self.k4) == 0):
			start = time.time()
			for edges in additional_edges_for_triangulation:
				self.extra_vertices.append(self.node_count)
				transformation.transformEdges(self,edges)
				print(edges)
			for edges in self.final_added_edges:
				self.extra_vertices.append(self.node_count)
				transformation.transformEdges(self,edges)
				print(edges)
			self.graph = nx.from_numpy_matrix(self.matrix)
			self.triangles = opr.get_all_triangles(self)
			print("Faces: ",len(self.triangles))
			print("Edges: ",self.edge_count)
			print("Vertices: ",self.node_count)
			print("Value: ",len(self.triangles)+self.node_count-self.edge_count)
			if not nx.check_planarity(self.graph) or (len(self.triangles)+self.node_count-self.edge_count)!=1:
				raise Exception("Error")
			self.directed = opr.get_directed(self)
			self.outer_vertices = opr.get_outer_boundary_vertices(self)[0]
			self.outer_boundary = opr.get_outer_boundary_vertices(self)[1]
			self.shortcuts = sr.get_shortcut(self)
			if(self.edge_count==3 and self.node_count==3):
				self.cip_list = [[[0],[0,1],[1,2],[2,0]],[[0,1],[1],[1,2],[2,0]],[[0,1],[1,2],[2],[2,0]]]
			else:
				cip_test = cip.find_cip(self)
				if(len(cip_test)<=4):
					boundaries = news.multiple_boundaries(news.find_boundary_single(cip_test))
					self.cip_list= news.find_multiple_boundary(news.all_boundaries(boundaries,opr.ordered_outer_boundary(self)),opr.ordered_outer_boundary(self))
			self.edge_matrix = self.matrix.copy()
			self.original_edge_count = self.edge_count
			self.original_node_count = self.node_count
			if(len(self.cip_list) == 0):
				self.shortcut_list = list(itr.combinations(self.shortcuts,len(self.shortcuts)-4))
			no_of_boundaries = 0
			count = 0
			if(len(self.cip_list)== 0):
				for resolver in self.shortcut_list:
					rdg_vertices = []
					rdg_vertices2 = []
					to_be_merged_vertices = []
					for i in range(0,size):
						sr.remove_shortcut(resolver[i],self,rdg_vertices,rdg_vertices2,to_be_merged_vertices)
					cip_test = cip.find_cip(self)
					self.cip = news.boundary_path_single(news.find_boundary_single(cip_test),opr.ordered_outer_boundary(self))					
					print("North Boundary: ", self.cip[2])
					print("East Boundary: ", self.cip[1])
					print("South Boundary: ", self.cip[0])
					print("West Boundary: ",self.cip[3])
					news.add_news_vertices(self)
					cntr.initialize_degrees(self)
					cntr.initialize_good_vertices(self)
					v, u = cntr.contract(self)
					while v != -1:
						v, u = cntr.contract(self)
					exp.get_trivial_rel(self)
					while len(self.contractions) != 0:
						exp.expand(self)
					rel_matrix =[]
					rel_matrix.append(self.matrix)
					self.rdg_vertices.append(rdg_vertices)
					self.rdg_vertices2.append(rdg_vertices2)
					self.to_be_merged_vertices.append(to_be_merged_vertices)
					for i in rel_matrix:
						self.matrix = i
						flippable_edges = flp.get_flippable_edges(self,i)
						flippable_vertices = flp.get_flippable_vertices(self,i)[0]
						flippable_vertices_neighbours = flp.get_flippable_vertices(self,i)[1]
						for j in range(0,len(flippable_edges)):
							new_rel = flp.resolve_flippable_edge(flippable_edges[j],self,i)
							if(not any(np.array_equal(new_rel, i) for i in rel_matrix)):
								rel_matrix.append(new_rel)
								self.rdg_vertices.append(rdg_vertices)
								self.rdg_vertices2.append(rdg_vertices2)
								self.to_be_merged_vertices.append(to_be_merged_vertices)
						for j in range(0,len(flippable_vertices)):
							new_rel = flp.resolve_flippable_vertex(flippable_vertices[j],flippable_vertices_neighbours[j],self,i)
							if(not any(np.array_equal(new_rel, i) for i in rel_matrix)):
								rel_matrix.append(new_rel)
								self.rdg_vertices.append(rdg_vertices)
								self.rdg_vertices2.append(rdg_vertices2)
								self.to_be_merged_vertices.append(to_be_merged_vertices)
					count +=1
					if(count != len(self.shortcut_list)):
						self.node_count = self.original_node_count
						self.edge_count = self.original_edge_count
						self.matrix = self.edge_matrix.copy()
						self.north = self.original_north
						self.west = self.original_west
						self.east = self.original_east
						self.south = self.original_south
					for i in rel_matrix:
						self.rel_matrix.append(i)
					print("Number of different floor plans: ",len(rel_matrix)*2)
					print("\n")
					self.cip = self.original_cip.copy()
			else:
				self.cip = self.cip_list[0]
				self.original_cip = self.cip.copy()
				for k in self.cip_list:
					self.cip = k
					news.add_news_vertices(self)
					print("North Boundary: ", self.cip[2])
					print("East Boundary: ", self.cip[1])
					print("South Boundary: ", self.cip[0])
					print("West Boundary: ",self.cip[3])
					no_of_boundaries += 1
					cntr.initialize_degrees(self)
					cntr.initialize_good_vertices(self)
					v, u = cntr.contract(self)
					while v != -1:
						v, u = cntr.contract(self)
					exp.get_trivial_rel(self)
					while len(self.contractions) != 0:
						exp.expand(self)
					rel_matrix =[]
					rel_matrix.append(self.matrix)
					for i in rel_matrix:
						self.matrix = i
						flippable_edges = flp.get_flippable_edges(self,i)
						flippable_vertices = flp.get_flippable_vertices(self,i)[0]
						flippable_vertices_neighbours = flp.get_flippable_vertices(self,i)[1]
						for j in range(0,len(flippable_edges)):
							new_rel = flp.resolve_flippable_edge(flippable_edges[j],self,i)
							if(not any(np.array_equal(new_rel, i) for i in rel_matrix)):
								rel_matrix.append(new_rel)
						for j in range(0,len(flippable_vertices)):
							new_rel = flp.resolve_flippable_vertex(flippable_vertices[j],flippable_vertices_neighbours[j],self,i)
							if(not any(np.array_equal(new_rel, i) for i in rel_matrix)):
								rel_matrix.append(new_rel)
					count +=1
					if(count != len(self.cip_list)):
						self.node_count = self.original_node_count
						self.edge_count = self.original_edge_count
						self.matrix = self.edge_matrix.copy()
					for i in rel_matrix:
						self.rel_matrix.append(i)
					print("Number of different floor plans: ",len(rel_matrix))
					print("\n")
			textbox.insert('end',f"\n Total number of different floor plans: {len(self.rel_matrix)}")
			textbox.insert('end',"\n")
			textbox.insert('end',f"Total boundaries used:{no_of_boundaries}")
			textbox.insert('end',"\n")
			end = time.time()
			textbox.insert('end',f"Time taken per floorlan : {round((end-start)/len(self.rel_matrix),6)*1000} ms")
			textbox.insert('end',"\n")
			print(f"Runtime of the program is {end - start}")

		else:
			start = time.time()
			self.edge_matrix1 = self.matrix.copy()
			original_edge_count1 = self.edge_count
			original_node_count1 = self.node_count
			no_of_boundaries = 0
			count = 0
			check = 1
			for j in self.k4:
				if(j.case !=2 ):
					check = 0
					break
			for number in range(0,3):
				to_be_merged_vertices = []
				rdg_vertices = []
				rdg_vertices2 =[]
				
				for j in self.k4:
					if(j.case  == 2):
						K4.resolve_K4(self,j,j.edge_to_be_removed,rdg_vertices,rdg_vertices2,to_be_merged_vertices)
					else:
						K4.resolve_K4(self,j,j.all_edges_to_be_removed[number],rdg_vertices,rdg_vertices2,to_be_merged_vertices)
				for edges in additional_edges_for_triangulation:
					self.extra_vertices.append(self.node_count)
					transformation.transformEdges(self,edges)
					print(edges)
				for edges in self.final_added_edges:
					self.extra_vertices.append(self.node_count)
					transformation.transformEdges(self,edges)
					print(edges)
				self.graph = nx.from_numpy_matrix(self.matrix)
				self.triangles = opr.get_all_triangles(self)
				print("Faces: ",len(self.triangles))
				print("Edges: ",self.edge_count)
				print("Vertices: ",self.node_count)
				print("Value: ",len(self.triangles)+self.node_count-self.edge_count)
				if not nx.check_planarity(self.graph) or (len(self.triangles)+self.node_count-self.edge_count)!=1:
					self.node_count = original_node_count1
					self.edge_count = original_edge_count1
					self.matrix = self.edge_matrix1.copy()
					self.north = self.original_north
					self.west = self.original_west
					self.east = self.original_east
					self.south = self.original_south
					continue
				self.directed = opr.get_directed(self)
				self.triangles = opr.get_all_triangles(self)
				self.outer_vertices = opr.get_outer_boundary_vertices(self)[0]
				self.outer_boundary = opr.get_outer_boundary_vertices(self)[1]
				self.shortcuts = sr.get_shortcut(self)
				cip_test = cip.find_cip(self)
				if(len(cip_test)<=4):
					boundaries = news.multiple_boundaries(news.find_boundary_single(cip_test))
					self.cip_list= news.find_multiple_boundary(news.all_boundaries(boundaries,opr.ordered_outer_boundary(self)),opr.ordered_outer_boundary(self))
				self.edge_matrix = self.matrix.copy()
				self.original_edge_count = self.edge_count
				self.original_node_count = self.node_count
				if(len(self.cip_list) == 0):
					self.shortcut_list = list(itr.combinations(self.shortcuts,len(self.shortcuts)-4))
				no_of_boundaries = 0
				self.cip = self.cip_list[0]
				self.original_cip = self.cip.copy()
				for k in self.cip_list:
					self.cip = k
					news.add_news_vertices(self)
					print("North Boundary: ", self.cip[2])
					print("East Boundary: ", self.cip[1])
					print("South Boundary: ", self.cip[0])
					print("West Boundary: ",self.cip[3])
					no_of_boundaries += 1
					cntr.initialize_degrees(self)
					cntr.initialize_good_vertices(self)
					v, u = cntr.contract(self)
					while v != -1:
						v, u = cntr.contract(self)
					exp.get_trivial_rel(self)
					while len(self.contractions) != 0:
						exp.expand(self)
					rel_matrix =[]
					rel_matrix.append(self.matrix)
					self.rdg_vertices.append(rdg_vertices)
					self.rdg_vertices2.append(rdg_vertices2)
					self.to_be_merged_vertices.append(to_be_merged_vertices)
					for i in rel_matrix:
						self.matrix = i
						flippable_edges = flp.get_flippable_edges(self,i)
						flippable_vertices = flp.get_flippable_vertices(self,i)[0]
						flippable_vertices_neighbours = flp.get_flippable_vertices(self,i)[1]
						for j in range(0,len(flippable_edges)):
							new_rel = flp.resolve_flippable_edge(flippable_edges[j],self,i)
							if(not any(np.array_equal(new_rel, i) for i in rel_matrix)):
								self.rdg_vertices.append(rdg_vertices)
								self.rdg_vertices2.append(rdg_vertices2)
								self.to_be_merged_vertices.append(to_be_merged_vertices)
								rel_matrix.append(new_rel)
						for j in range(0,len(flippable_vertices)):
							new_rel = flp.resolve_flippable_vertex(flippable_vertices[j],flippable_vertices_neighbours[j],self,i)
							if(not any(np.array_equal(new_rel, i) for i in rel_matrix)):
								rel_matrix.append(new_rel)
								self.rdg_vertices.append(rdg_vertices)
								self.rdg_vertices2.append(rdg_vertices2)
								self.to_be_merged_vertices.append(to_be_merged_vertices)

					count +=1
					if(count != len(self.cip_list)):
						self.node_count = self.original_node_count
						self.edge_count = self.original_edge_count
						self.matrix = self.edge_matrix.copy()
					for i in rel_matrix:
						self.rel_matrix.append(i)
					print("Number of different floor plans: ",len(rel_matrix))
					print("\n")
					# end = time.time()
					# print(f"Runtime of the program is {end - start}")
					# start = time.time()
				if(number!=2 and check == 0):
					self.node_count = original_node_count1
					self.edge_count = original_edge_count1
					self.matrix = self.edge_matrix1.copy()
					self.north = self.original_north
					self.west = self.original_west
					self.east = self.original_east
					self.south = self.original_south
					for j in self.k4:
						j.identified = 0
				elif(check == 1):
					break
				print("Yeah")
			print("Total number of different floor plans: ",len(self.rel_matrix))
			print("Total boundaries used:", no_of_boundaries)
			end = time.time()
			print(f"Runtime of the program is {end - start}")
			textbox.insert('end',f"Total number of different floor plans: {len(self.rel_matrix)}")
			textbox.insert('end',"\n")
			textbox.insert('end',f"Total boundaries used:{no_of_boundaries}")
			textbox.insert('end',"\n")
			textbox.insert('end',f"Time taken per floorlan : {round((end-start)/len(self.rel_matrix),6)*1000} ms")
			textbox.insert('end',"\n")
		if(mode == 1):
			count = 0
			origin_count = 1
			for i in self.rel_matrix:
				self.matrix = i
				if(len(self.to_be_merged_vertices)!= 0):
					draw.construct_rdg(self,self.to_be_merged_vertices[count],self.rdg_vertices[count])
					if(origin_count != 1):
						self.origin += 1000
					draw.draw_rdg(self,origin_count,pen,self.to_be_merged_vertices[count],self.rdg_vertices[count],mode,self.colors,self.names)
					origin_count +=1
					draw.construct_rdg(self,self.to_be_merged_vertices[count],self.rdg_vertices2[count])
					if(origin_count != 1):
						self.origin += 1000
					draw.draw_rdg(self,origin_count,pen,self.to_be_merged_vertices[count],self.rdg_vertices2[count],mode,self.colors,self.names)
					origin_count +=1
					count +=1
					
				else:
					draw.construct_rdg(self,self.to_be_merged_vertices,self.rdg_vertices)
					if(origin_count != 1):
						self.origin += 1000
					draw.draw_rdg(self,origin_count,pen,self.to_be_merged_vertices,self.rdg_vertices,mode,self.colors,self.names)
					origin_count +=1

	def create_circulation_dual(self,mode,pen,textbox):
		global box
		box = textbox
		self.original_edge_count = self.edge_count
		self.original_node_count = self.node_count
		self.triangles = opr.get_all_triangles(self)
		K4.find_K4(self)
		for i in self.k4:
			K4.resolve_K4(self,i,i.edge_to_be_removed,self.rdg_vertices,self.rdg_vertices2,self.to_be_merged_vertices)
		self.directed = opr.get_directed(self)
		self.triangles = opr.get_all_triangles(self)
		self.outer_vertices = opr.get_outer_boundary_vertices(self)[0]
		self.outer_boundary = opr.get_outer_boundary_vertices(self)[1]
		self.shortcuts = sr.get_shortcut(self)
		self.cip = news.find_cip_single(self)
		# self.cip =[ [0,1,2,3,4,5,6],[6,7,8,9,10,11,12],[12,13,14,15],[15,16,17,18,19,0]]
		news.add_news_vertices(self)
		print("North Boundary: ", self.cip[0])
		print("East Boundary: ", self.cip[1])
		print("South Boundary: ", self.cip[2])
		print("West Boundary: ",self.cip[3])
		for i in range(0,len(self.to_be_merged_vertices)):
			self.node_color.append(self.node_color[self.rdg_vertices[i]])
		self.node_position = nx.planar_layout(nx.from_numpy_matrix(self.matrix))
		cntr.initialize_degrees(self)
		cntr.initialize_good_vertices(self)
		v, u = cntr.contract(self)
		while v != -1:
			v, u = cntr.contract(self)
			# draw.draw_undirected_graph(self,pen)
			# input()
		# print(self.contractions)
		exp.get_trivial_rel(self)
		while len(self.contractions) != 0:
			exp.expand(self)
		draw.construct_rdg(self,self.to_be_merged_vertices,self.rdg_vertices)
		# for i  in range(0,len(self.to_be_merged_vertices)):
		#   print(self.room_x[self.to_be_merged_vertices[i]],self.room_y[self.to_be_merged_vertices[i]],self.room_width[self.to_be_merged_vertices[i]],self.room_height[self.to_be_merged_vertices[i]],self.room_x_top_left[self.to_be_merged_vertices[i]],self.room_x_top_right[self.to_be_merged_vertices[i]],self.room_y_left_top[self.to_be_merged_vertices[i]],self.room_y_left_bottom[self.to_be_merged_vertices[i]],self.room_x_bottom_left[self.to_be_merged_vertices[i]],self.room_x_bottom_right[self.to_be_merged_vertices[i]],self.room_y_right_top[self.to_be_merged_vertices[i]],self.room_y_right_bottom[self.to_be_merged_vertices[i]])
		#   print(self.room_x[self.rdg_vertices[i]],self.room_y[self.rdg_vertices[i]],self.room_width[self.rdg_vertices[i]],self.room_height[self.rdg_vertices[i]],self.room_x_top_left[self.rdg_vertices[i]],self.room_x_top_right[self.rdg_vertices[i]],self.room_y_left_top[self.rdg_vertices[i]],self.room_y_left_bottom[self.rdg_vertices[i]],self.room_x_bottom_left[self.rdg_vertices[i]],self.room_x_bottom_right[self.rdg_vertices[i]],self.room_y_right_top[self.rdg_vertices[i]],self.room_y_right_bottom[self.rdg_vertices[i]]) 
		# print(self.room_x,self.room_y,self.room_width,self.room_height,self.room_x_top_left,self.room_x_top_right,self.room_y_left_top,self.room_y_left_bottom,self.room_x_bottom_left,self.room_x_bottom_right,self.room_y_right_top,self.room_y_right_bottom)
		

	def create_multiple_floorplan(self,pen,textbox,mode):
		global box
		box = textbox
		self.create_multiple_dual(0,pen,textbox)
		count = 0
		origin_count = 1
		minimum_width = min(self.width_min)
		minimum_height = min(self.height_min)
		if(len(self.to_be_merged_vertices)!=0):
			for i in range(0,len(self.to_be_merged_vertices[0])):
				self.width_min.append(minimum_width)
				self.height_min.append(minimum_height)
		for i in range(0,len(self.extra_vertices)):
			self.width_min.append(0)
			self.height_min.append(0)
		for i in range(0,len(self.rel_matrix)):
			self.matrix = self.rel_matrix[i]
			if(len(self.to_be_merged_vertices)!= 0):
				draw.construct_rdg(self,self.to_be_merged_vertices[count],self.rdg_vertices[count])
				self.encoded_matrix = opr.get_encoded_matrix(self)
				B = copy.deepcopy(self.encoded_matrix)
				A = copy.deepcopy(self.encoded_matrix)
				[width,height,hor_dgph] = floorplan_to_st(A,self.width_min,self.height_min)
				A=B
				width = np.transpose(width)
				height = np.transpose(height)
				self.room_width = width.flatten()
				self.room_height = height.flatten()
				draw.construct_rfp(self,hor_dgph,self.to_be_merged_vertices[count],self.rdg_vertices[count])
				for i in range(0,len(self.room_x)):
					self.room_x[i]=round(self.room_x[i],3)
				for i in range(0,len(self.room_y)):
					self.room_y[i]=round(self.room_y[i],3)
					print(self.room_x[i],self.room_y[i],self.room_width[i],self.room_height[i],self.room_x_top_left[i],self.room_x_top_right[i],self.room_y_left_top[i],self.room_y_left_bottom[i],self.room_x_bottom_left[i],self.room_x_bottom_right[i],self.room_y_right_top[i],self.room_y_right_bottom[i])
				opr.calculate_area(self,self.to_be_merged_vertices[count],self.rdg_vertices[count])
				draw.draw_rdg(self,count+1,pen,self.to_be_merged_vertices[count],self.rdg_vertices[count],mode,self.colors,self.names)
				self.area =[]
				origin_count +=1
				if(origin_count != 1):
					self.origin += 1000
				draw.construct_rfp(self,hor_dgph,self.to_be_merged_vertices[count],self.rdg_vertices2[count])
				for i in range(0,len(self.room_x)):
					self.room_x[i]=round(self.room_x[i],3)
					# print(self.room_x[i])
				for i in range(0,len(self.room_y)):
					self.room_y[i]=round(self.room_y[i],3)
				opr.calculate_area(self,self.to_be_merged_vertices[count],self.rdg_vertices2[count])
				raw.draw_rdg(self,count+1,pen,self.to_be_merged_vertices[count],self.rdg_vertices[count],mode,self.colors,self.names)
				self.area =[]
				origin_count+=1
				if(origin_count != 1):
					self.origin += 500
				
				count+=1
			else:
				draw.construct_rdg(self,self.to_be_merged_vertices,self.rdg_vertices)
				self.encoded_matrix = opr.get_encoded_matrix(self)
				B = copy.deepcopy(self.encoded_matrix)
				A = copy.deepcopy(self.encoded_matrix)
				[width,height,hor_dgph] = floorplan_to_st(A,self.width_min,self.height_min)
				A=B
				# print(A)
				width = np.transpose(width)
				height = np.transpose(height)
				self.room_width = width.flatten()
				self.room_height = height.flatten()
				draw.construct_rfp(self,hor_dgph,self.to_be_merged_vertices,self.rdg_vertices)
				for i in range(0,len(self.room_x)):
					self.room_x[i]=round(self.room_x[i],3)
				for i in range(0,len(self.room_y)):
					self.room_y[i]=round(self.room_y[i],3)
				if(origin_count != 1):
					self.origin += 500
				opr.calculate_area(self,self.to_be_merged_vertices,self.rdg_vertices)
				draw.draw_rdg(self,count+1,pen,self.to_be_merged_vertices,self.rdg_vertices,mode,self.colors,self.names)
				self.area =[]
				origin_count +=1
				count+=1