"""Main file of the projrct

"""

import warnings
import time
import tkinter as tk
import networkx as nx
import pythongui.gui as gui
import source.inputgraph as inputgraph
import pythongui.drawing as draw
import pythongui.dimensiongui as dimgui
# import circulation
# import checker
# from tkinter import messagebox
# import dimension_gui as dimgui
# import boundary_gui as bdygui

# import tests
# import triangularity as trng
origin = 50
def run():
    """Runs the GPLAN program.

    Args:
        None

    Returns:
        None
    """
    def printe(string):
        """Prints string on GUI console.

        Args:
            None

        Returns:
            None
        """
        gclass.textbox.insert('end',string)
        gclass.textbox.insert('end',"\n")

    warnings.filterwarnings("ignore")
    gclass = gui.gui_class() 

    while (gclass.command!="end"):
        if(gclass.command=="dissection"):
            make_dissection_corridor(gclass)
        # if ( gclass.command =="checker"):
        #     tests.tester(gclass.value,gclass.textbox)
        else:
            graph = inputgraph.InputGraph(gclass.value[0]
                ,gclass.value[1]
                ,gclass.value[2])
            origin = 0
            if(gclass.command == "single"):
                if(gclass.value[4] == 0):
                    start = time.time()
                    graph.single_dual()
                    end = time.time()
                    printe("Time taken: " + str((end-start)*1000) + " ms")
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
                    draw.draw_rdg(graph_data
                            ,1
                            ,gclass.pen
                            ,1
                            ,gclass.value[6]
                            ,[]
                            ,origin)
                else:
                    min_width,max_width,min_height,max_height= dimgui.gui_fnc(gclass.value[0])
                    start = time.time()
                    graph.single_dual()
                    graph.single_floorplan(min_width,min_height,max_width,max_height)
                    end = time.time()
                    printe("Time taken: " + str((end-start)*1000) + " ms")
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
                    draw.draw_rdg(graph_data
                            ,1
                            ,gclass.pen
                            ,1
                            ,gclass.value[6]
                            ,[]
                            ,origin)
            elif(gclass.command == "multiple"):
                if(gclass.value[4] == 0):
                    start = time.time()
                    graph.multiple_dual()
                    end = time.time()
                    printe("Time taken: " + str((end-start)*1000) + " ms")
                    for idx in range(len(graph.rel_matrix_list)):
                        graph_data = {
                            'room_x': graph.room_x[idx],
                            'room_y': graph.room_y[idx],
                            'room_width': graph.room_width[idx],
                            'room_height': graph.room_height[idx],
                            'room_x_bottom_left': graph.room_x_bottom_left[idx],
                            'room_x_bottom_right': graph.room_x_bottom_right[idx],
                            'room_x_top_left': graph.room_x_top_left[idx],
                            'room_x_top_right': graph.room_x_top_right[idx],
                            'room_y_left_bottom': graph.room_y_left_bottom[idx],
                            'room_y_right_bottom': graph.room_y_right_bottom[idx],
                            'room_y_left_top': graph.room_y_left_top[idx],
                            'room_y_right_top': graph.room_y_right_top[idx],
                            'area': graph.area,
                            'extranodes': graph.extranodes,
                            'mergednodes': graph.mergednodes,
                            'irreg_nodes': graph.irreg_nodes1
                        }
                        origin += 1000
                        draw.draw_rdg(graph_data
                            ,1
                            ,gclass.pen
                            ,1
                            ,gclass.value[6]
                            ,[]
                            ,origin)
                else:
                    min_width,max_width,min_height,max_height= dimgui.gui_fnc(gclass.value[0])
                    start = time.time()
                    graph.multiple_dual()
                    graph.multiple_floorplan(min_width,min_height,max_width,max_height)
                    end = time.time()
                    printe("Time taken: " + str((end-start)*1000) + " ms")
                    for idx in range(len(graph.rel_matrix_list)):
                        graph_data = {
                            'room_x': graph.room_x[idx],
                            'room_y': graph.room_y[idx],
                            'room_width': graph.room_width[idx],
                            'room_height': graph.room_height[idx],
                            'room_x_bottom_left': graph.room_x_bottom_left[idx],
                            'room_x_bottom_right': graph.room_x_bottom_right[idx],
                            'room_x_top_left': graph.room_x_top_left[idx],
                            'room_x_top_right': graph.room_x_top_right[idx],
                            'room_y_left_bottom': graph.room_y_left_bottom[idx],
                            'room_y_right_bottom': graph.room_y_right_bottom[idx],
                            'room_y_left_top': graph.room_y_left_top[idx],
                            'room_y_right_top': graph.room_y_right_top[idx],
                            'area': graph.area,
                            'extranodes': graph.extranodes,
                            'mergednodes': graph.mergednodes,
                            'irreg_nodes': graph.irreg_nodes1
                        }
                        origin += 1000
                        draw.draw_rdg(graph_data
                            ,1
                            ,gclass.pen
                            ,1
                            ,gclass.value[6]
                            ,[]
                            ,origin)
            #     if(not test_result[0]):
            #         messagebox.showerror("Invalid Graph", "Graph is not planar")
            #     # elif(not test_result[1]):
            #     #     messagebox.showerror("Invalid Graph", "Graph is not triangular")
            #     # elif(not test_result[2]):
            #     #     messagebox.showerror("Invalid Graph", "Graph is not biconnected")
            #     else:
            #         # try: 
            #         if(G.dimensioned == 0):
            #             G.create_single_dual(1,gclass.pen,gclass.textbox)
            #             draw.draw_rdg(G,1,gclass.pen,G.to_be_merged_vertices,G.rdg_vertices,1,gclass.value[6],[])
            #             W = ptpg.PTPG(gclass.value)
            #             if not trng.Check_Chordality(W.graph, 0) and W.triangulation_type == "wall":
            #                 # gclass.graph_ret()
            #                 gclass.ocan.add_tab()
            #                 # gclass.ocan.tscreen.resetscreen()
            #                 gclass.pen = gclass.ocan.getpen()
            #                 gclass.pen.speed(100000)

            #                 W.create_single_dual(1,gclass.pen,gclass.textbox, "wall")
            #                 # draw.draw_rdg(W,1,gclass.pen,W.to_be_merged_vertices,W.rdg_vertices,1,gclass.value[6],[])
            #                 W.make_walls(gclass.ocan.canvas)
            #             # else:
            #                 # G.create_single_dual(1,gclass.pen,gclass.textbox)
            #         else:
            #             # if(not checker.rfp_checker(G.matrix)):
            #             #     G.create_single_dual(2,gclass.pen,gclass.textbox)
            #             #     draw.draw_rdg(G,1,gclass.pen,G.to_be_merged_vertices,G.rdg_vertices,2,gclass.value[6],gclass.value[5])
            #             #     messagebox.showinfo("Orthogonal Floor Plan","The input graph has an orthogonal floorplan.Rooms with red boundary are the additional rooms which will be added but later merged.Please provide dimensions for the extra rooms as well.")
            #             #     G.width_min,G.width_max,G.height_min,G.height_max= dimgui.gui_fnc(G.original_node_count+len(G.to_be_merged_vertices))
            #             #     gclass.pen.clear()
            #             #     G.create_single_floorplan(gclass.pen,gclass.textbox,1)
            #             #     draw.draw_rdg(G,1,gclass.pen,G.to_be_merged_vertices,G.rdg_vertices,0,gclass.value[6],gclass.value[5])
            #             # else:
            #             G.width_min,G.width_max,G.height_min,G.height_max = dimgui.gui_fnc(G.node_count)
            #             G.create_single_floorplan(gclass.pen,gclass.textbox,0)
            #             draw.draw_rdg(G,1,gclass.pen,G.to_be_merged_vertices,G.rdg_vertices,0,gclass.value[6],gclass.value[5])
            #     # except:
            #             # printe("Biconnectivity and Triangularity led to non-K4 separating triangle")
            # elif(gclass.command == "multiple"):
            #     test_result = checker.gui_checker(G)
            #     if(not test_result[0]):
            #         messagebox.showerror("Invalid Graph", "Graph is not planar")
            #     # elif(not test_result[1]):
            #     #     messagebox.showerror("Invalid Graph", "Graph is not triangular")
            #     # elif(not test_result[2]):
            #     #     messagebox.showerror("Invalid Graph", "Graph is not biconnected")
            #     else:
            # #         print(G.original_node_count)
            # #         G.user_boundary_constraint,G.user_corner_constraint = bdygui.gui_fnc(G.node_count)
            #         if(G.dimensioned == 0):
            #             G.create_multiple_dual(1,gclass.pen,gclass.textbox)
            #         else:
            #             G.width_min,G.width_max,G.height_min,G.height_max = dimgui.gui_fnc(G.node_count)
            #             G.create_multiple_floorplan(gclass.pen,gclass.textbox,0)

        gclass.root.wait_variable(gclass.end)
        gclass.graph_ret()
        gclass.ocan.add_tab()

        # gclass.ocan.tscreen.resetscreen()
        gclass.pen = gclass.ocan.getpen()
        gclass.pen.speed(100000)




def make_dissection_corridor(gclass):
    dis =nx.Graph()
    dis = nx.from_numpy_matrix(gclass.dclass.mat)
    m = len(dis)
    spanned = circulation.BFS(dis,gclass.e1.get(),gclass.e2.get())
    gclass.cir_dim_mat = nx.to_numpy_matrix(spanned)
    # colors = ['#4BC0D9','#76E5FC','#6457A6','#5C2751','#7D8491','#BBBE64','#64F58D','#9DFFF9','#AB4E68','#C4A287','#6F9283','#696D7D','#1B1F3B','#454ADE','#FB6376','#6C969D','#519872','#3B5249','#A4B494','#CCFF66','#FFC800','#FF8427','#0F7173','#EF8354','#795663','#AF5B5B','#667761','#CF5C36','#F0BCD4','#ADB2D3','#FF1B1C','#6A994E','#386641','#8B2635','#2E3532','#124E78']*10
    colors = ['#4BC0D9']*10
    rnames = []
    for i in range(1,m+1):
        rnames.append('Room' + str(i))
    rnames.append("Corridor")
    for i in range(1,10):
        colors[m+i-1] = '#FF4C4C'
        rnames.append("")
    parameters= [len(spanned), spanned.size() , spanned.edges() , 0,0 ,rnames,colors]
    C = ptpg.PTPG(parameters)
    C.create_single_dual(1,gclass.pen,gclass.textbox)
    gclass.ocan.add_cir_tab()
    gclass.dclass.add_cir()

def make_graph_circulation(G,gclass):
    m =len(G.graph)
    spanned = circulation.BFS(G.graph,1,2)
    # plotter.plot(spanned,m)
    colors= gclass.value[6].copy()
    for i in range(0,100):
        colors.append('#FF4C4C')
    # print(colors)
    rnames = G.room_names
    rnames.append("Corridor")
    for i in range(0,100):
        rnames.append("")
    # print(rnames)
    
    parameters= [len(spanned), spanned.size() , spanned.edges() , 0,0 ,rnames,colors]
    C = ptpg.PTPG(parameters)
    # C.create_single_dual(1,gclass.pen,gclass.textbox)
    print(G.graph.edges())
    G.create_circulation_dual(1,gclass.pen,gclass.textbox)
    # draw.draw_rdg(G,1,gclass.pen,G.to_be_merged_vertices,G.rdg_vertices,0,gclass.value[6],gclass.value[5])
    G.circulation(gclass.pen,gclass.ocan.canvas, C, 1, 2)

if __name__ == "__main__":
    run()