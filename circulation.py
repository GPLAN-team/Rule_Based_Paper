import networkx as nx

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Edge:
    def __init__(self, room, left, right):
        self.room = room
        self.left = left
        self.right = right
        

def circulaion_algorithm(graph,v1=1,v2=2):
    """
    Applies the circulation algorithm on the PTPG graph

    Args:
        graph (NetworkX graph): The output graph after applying triangulation and other algorithms to get a Properly
                      Triangulated Planar Graph (PTPG).
        v1 (int, optional): First endpoint of the exterior edge to start the circulation algorithm. Defaults to 1.
        v2 (int, optional): Second endpoint of the exterior edge to start the circulation algorithm. Defaults to 2.

    Returns:
        graph: The final graph after adding the vertices and edges corresponding to corridors
        final_adjacency: The dictionary that contains the pair of rooms adjacent to each corridor
    """

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
    return graph, final_adjacency

def corridor_boundary_rooms(input_graph,corridor_vertex,v1=1,v2=2):
    """For a given corridor, this function outputs the two rooms it connects

    Args:
        input_graph (NetworkX graph): The graph input by the user
        corridor_vertex (Networkx node): Node corresponding to the corridor for which we need to find the neighbors
        v1 (int, optional): First endpoint of the exterior edge to start the circulation algorithm. Defaults to 1.
        v2 (int, optional): Second endpoint of the exterior edge to start the circulation algorithm. Defaults to 2.

    Returns:
        [a,b]: pair of rooms that the corridor_vertex is adjacent to
    """
    # Get the circulation graph and the adjacency dictionary
    circulation_graph, adjacency = circulaion_algorithm(input_graph,v1,v2)

    # Gets the tuple corresponding to the key value (key = corridor_vertex)
    [a,b] = adjacency.get(corridor_vertex)

    return [a,b]


# def adjust_RFP_to_circulation():
# def add_corridor_between_2_rooms(room1,room2):
# def find_common_edges(room1,room2):
# def find_directions_for_common_edges(room1,room2):
# def find_neighboring_edges_other_than_one(edge, exclude_vertex):
# def Move_edge(room, shift_by, direction, shift_edge):
# def remove_corridor_between_2_rooms(room1,room2):