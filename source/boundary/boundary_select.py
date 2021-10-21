import networkx as nx
import warnings
import numpy as np

def boundary_populate(boundary_list):
	answer = []
	for boundary in boundary_list:
		answer.append(boundary)
		temp = [boundary[1],boundary[2],boundary[3],boundary[0]]
		answer.append(temp)
		temp = [boundary[2],boundary[3],boundary[0],boundary[1]]
		answer.append(temp)
		temp = [boundary[3],boundary[0],boundary[1],boundary[2]]
		answer.append(temp)
		temp = [boundary[0],boundary[3],boundary[2],boundary[1]]
		answer.append(temp)
		temp = [boundary[3],boundary[2],boundary[1],boundary[0]]
		answer.append(temp)
		temp = [boundary[2],boundary[1],boundary[0],boundary[3]]
		answer.append(temp)
		temp = [boundary[1],boundary[0],boundary[3],boundary[2]]
		answer.append(temp)
	return answer

def possible_boundary(boundary_list,user_constraint,corner_constraint):
	answer = []
	for boundary in boundary_list:
		# boundary[0].reverse()
		# boundary[1].reverse()
		# boundary[2].reverse()
		# boundary[3].reverse()

		possible = True
		for room in user_constraint[0]:
			if(room not in boundary[0]):
				possible = False
			if(not possible):
				break
		if(not possible):
			continue
		for room in corner_constraint[0]:
			if(room != boundary[1][len(boundary[1])-1]):
				possible = False
		if(not possible):
			continue
		for room in user_constraint[1]:
			if(room not in boundary[1]):
				possible = False
			if(not possible):
				break
		if(not possible):
			continue
		for room in corner_constraint[1]:
			if(room != boundary[2][len(boundary[2])-1]):
				possible = False
		if(not possible):
			continue
		for room in user_constraint[2]:
			if(room not in boundary[2]):
				possible = False
			if(not possible):
				break
		if(not possible):
			continue
		for room in corner_constraint[2]:
			if(room != boundary[3][len(boundary[3])-1]):
				possible = False
		if(not possible):
			continue
		for room in user_constraint[3]:
			if(room not in boundary[3]):
				possible = False
			if(not possible):
				break
		if(not possible):
			continue
		for room in corner_constraint[3]:
			if(room != boundary[0][len(boundary[0])-1]):
				possible = False
		if(not possible):
			continue
		else:
			print(boundary)
			print("Hello")
			answer.append(boundary)
	return answer