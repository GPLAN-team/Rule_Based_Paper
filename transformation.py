import networkx as nx
import numpy as np

def transformEdges(graph,edge_to_be_transformed):
	nbd1= find_neighbour(graph,edge_to_be_transformed[0])
	nbd2 = find_neighbour(graph,edge_to_be_transformed[1])
	common_neighbours = nbd1.intersection(nbd2)
	graph.node_count +=1
	new_adjacency_matrix = np.zeros([graph.node_count, graph.node_count], int)
	for i in range(len(graph.matrix)):
		for j in range(len(graph.matrix)):
			new_adjacency_matrix[i][j] = graph.matrix[i][j]
	new_adjacency_matrix[edge_to_be_transformed[0]][edge_to_be_transformed[1]] = 0
	new_adjacency_matrix[edge_to_be_transformed[1]][edge_to_be_transformed[0]] = 0
	new_adjacency_matrix[graph.node_count-1][edge_to_be_transformed[0]] = 1
	new_adjacency_matrix[graph.node_count-1][edge_to_be_transformed[1]] = 1
	new_adjacency_matrix[edge_to_be_transformed[0]][graph.node_count-1] = 1
	new_adjacency_matrix[edge_to_be_transformed[1]][graph.node_count-1] = 1
	for vertex in common_neighbours:
		new_adjacency_matrix[vertex][graph.node_count-1]=1
		new_adjacency_matrix[graph.node_count-1][vertex]=1
	if(len(common_neighbours)==1):
		graph.edge_count+=2
	else:
		graph.edge_count+=3
	graph.matrix = new_adjacency_matrix
	graph.north +=1
	graph.east +=1
	graph.west +=1
	graph.south +=1 

def find_neighbour(graph,vertex):
	result = set()
	for i in range(0,graph.node_count):
		if(graph.matrix[vertex][i]==1):
			result.add(i)
	return result