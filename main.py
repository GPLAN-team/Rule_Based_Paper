"""Main file of the project

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
origin = 0
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
        else:
            graph = inputgraph.InputGraph(gclass.value[0]
                ,gclass.value[1]
                ,gclass.value[2]
                ,gclass.value[7])
            origin = 0
            if(gclass.command == "single"): #Single Irregular Dual/Floorplan
                if(gclass.value[4] == 0): #Non-Dimensioned single dual
                    start = time.time()
                    graph.irreg_single_dual()
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
                else: #Dimensioned single floorplan
                    old_dims = [[0] * gclass.value[0]
                                , [0] * gclass.value[0]
                                , [0] * gclass.value[0]
                                , [0] * gclass.value[0]
                                , ""
                                , [0] * gclass.value[0]
                                , [0] * gclass.value[0]]
                    min_width,max_width,min_height,max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height  = dimgui.gui_fnc(old_dims, gclass.value[0])
                    start = time.time()
                    graph.irreg_multiple_dual()
                    graph.single_floorplan(min_width,min_height,max_width,max_height,symm_string, min_aspect, max_aspect, plot_width, plot_height)
                    while(graph.floorplan_exist == False):
                        old_dims = [min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect]
                        min_width,max_width,min_height,max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height  = dimgui.gui_fnc(old_dims, gclass.value[0])
                        graph.multiple_dual()
                        graph.single_floorplan(min_width,min_height,max_width,max_height,symm_string, min_aspect, max_aspect, plot_width, plot_height)
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
            elif(gclass.command == "multiple"):#Multiple Irregular Dual/Floorplan
                if(gclass.value[4] == 0):#Non-Dimensioned multiple dual
                    start = time.time()
                    graph.irreg_multiple_dual()
                    end = time.time()
                    printe("Average Time taken: " + str(((end-start)*1000)/graph.fpcnt) + " ms")
                    printe("Number of floorplans: " +  str(graph.fpcnt))
                    for idx in range(graph.fpcnt):
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
                            'extranodes': graph.extranodes[idx],
                            'mergednodes': graph.mergednodes[idx],
                            'irreg_nodes': graph.irreg_nodes1[idx]
                        }
                        draw.draw_rdg(graph_data
                            ,idx+1
                            ,gclass.pen
                            ,1
                            ,gclass.value[6]
                            ,[]
                            ,origin)
                        # origin += 1000
                        
                        gclass.ocan.add_tab()
                        gclass.pen = gclass.ocan.getpen()
                        gclass.pen.speed(0)
                else:#Dimensioned multiple floorplans
                    old_dims = [[0] * gclass.value[0]
                                , [0] * gclass.value[0]
                                , [0] * gclass.value[0]
                                , [0] * gclass.value[0]
                                , ""
                                , [0] * gclass.value[0]
                                , [0] * gclass.value[0]]
                    min_width,max_width,min_height,max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height  = dimgui.gui_fnc(old_dims, gclass.value[0])
                    start = time.time()
                    graph.irreg_multiple_dual()
                    graph.multiple_floorplan(min_width,min_height,max_width,max_height,symm_string, min_aspect, max_aspect, plot_width, plot_height)
                    end = time.time()
                    printe("Time taken: " + str((end-start)*1000) + " ms")
                    printe("Number of floorplans: " +  str(len(graph.room_x)))
                    for idx in range(len(graph.room_x)):
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
                            'area': graph.area[idx],
                            'extranodes': graph.extranodes[idx],
                            'mergednodes': graph.mergednodes[idx],
                            'irreg_nodes': graph.irreg_nodes1[idx]
                        }
                        # origin += 1000
                        draw.draw_rdg(graph_data
                            ,idx+1
                            ,gclass.pen
                            ,1
                            ,gclass.value[6]
                            ,[]
                            ,origin)
                        
                        gclass.ocan.add_tab()
                        gclass.pen = gclass.ocan.getpen()
                        gclass.pen.speed(0)
            elif(gclass.command == "single_oc"):
                if(gclass.value[4] == 0): #Non-Dimensioned single rectangular dual
                    start = time.time()
                    try:
                        graph.oneconnected_dual("single")
                    except inputgraph.OCError:
                        gclass.show_warning("Can not generate rectangular floorplan.")
                        graph.irreg_single_dual()
                    except inputgraph.BCNError:
                        graph.irreg_single_dual()
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
                else: #Dimensioned single floorplan
                    old_dims = [[0] * gclass.value[0]
                                , [0] * gclass.value[0]
                                , [0] * gclass.value[0]
                                , [0] * gclass.value[0]
                                , ""
                                , [0] * gclass.value[0]
                                , [0] * gclass.value[0]]
                    min_width,max_width,min_height,max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height  = dimgui.gui_fnc(old_dims, gclass.value[0])
                    start = time.time()
                    try:
                        graph.oneconnected_dual("multiple")
                    except inputgraph.OCError:
                        gclass.show_warning("Can not generate rectangular floorplan.")
                        graph.irreg_multiple_dual()
                    except inputgraph.BCNError:
                        graph.irreg_multiple_dual()
                    graph.single_floorplan(min_width,min_height,max_width,max_height,symm_string, min_aspect, max_aspect, plot_width, plot_height)
                    while(graph.floorplan_exist == False):
                        old_dims = [min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect]
                        min_width,max_width,min_height,max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height  = dimgui.gui_fnc(old_dims, gclass.value[0])
                        graph.multiple_dual()
                        graph.single_floorplan(min_width,min_height,max_width,max_height,symm_string, min_aspect, max_aspect, plot_width, plot_height)
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
            elif(gclass.command == "multiple_oc"):
                if(gclass.value[4] == 0):#Non-Dimensioned multiple dual
                    start = time.time()
                    try:
                        graph.oneconnected_dual("multiple")
                    except inputgraph.OCError:
                        gclass.show_warning("Can not generate rectangular floorplan.")
                        graph.irreg_multiple_dual()
                    except inputgraph.BCNError:
                        graph.irreg_multiple_dual()
                    end = time.time()
                    printe("Average Time taken: " + str(((end-start)*1000)/graph.fpcnt) + " ms")
                    printe("Number of floorplans: " +  str(graph.fpcnt))
                    for idx in range(graph.fpcnt):
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
                            'extranodes': graph.extranodes[idx],
                            'mergednodes': graph.mergednodes[idx],
                            'irreg_nodes': graph.irreg_nodes1[idx]
                        }
                        draw.draw_rdg(graph_data
                            ,idx+1
                            ,gclass.pen
                            ,1
                            ,gclass.value[6]
                            ,[]
                            ,origin)
                        # origin += 1000
                        
                        gclass.ocan.add_tab()
                        gclass.pen = gclass.ocan.getpen()
                        gclass.pen.speed(0)
                else:#Dimensioned multiple floorplans
                    old_dims = [[0] * gclass.value[0]
                                , [0] * gclass.value[0]
                                , [0] * gclass.value[0]
                                , [0] * gclass.value[0]
                                , ""
                                , [0] * gclass.value[0]
                                , [0] * gclass.value[0]]
                    min_width,max_width,min_height,max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height  = dimgui.gui_fnc(old_dims, gclass.value[0])
                    start = time.time()
                    try:
                        graph.oneconnected_dual("multiple")
                    except inputgraph.OCError:
                        gclass.show_warning("Can not generate rectangular floorplan.")
                        graph.irreg_multiple_dual()
                    except inputgraph.BCNError:
                        graph.irreg_multiple_dual()
                    graph.multiple_floorplan(min_width,min_height,max_width,max_height,symm_string, min_aspect, max_aspect, plot_width, plot_height)
                    end = time.time()
                    printe("Time taken: " + str((end-start)*1000) + " ms")
                    printe("Number of floorplans: " +  str(len(graph.room_x)))
                    for idx in range(len(graph.room_x)):
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
                            'area': graph.area[idx],
                            'extranodes': graph.extranodes[idx],
                            'mergednodes': graph.mergednodes[idx],
                            'irreg_nodes': graph.irreg_nodes1[idx]
                        }
                        # origin += 1000
                        draw.draw_rdg(graph_data
                            ,idx+1
                            ,gclass.pen
                            ,1
                            ,gclass.value[6]
                            ,[]
                            ,origin)
                        
                        gclass.ocan.add_tab()
                        gclass.pen = gclass.ocan.getpen()
                        gclass.pen.speed(0)
        gclass.root.wait_variable(gclass.end)
        gclass.graph_ret()
        gclass.ocan.add_tab()
        gclass.pen = gclass.ocan.getpen()
        gclass.pen.speed(0)
        # gclass.ocan.tscreen.resetscreen()

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
    G.create_circulation_dual(1,gclass.pen,gclass.textbox)
    # draw.draw_rdg(G,1,gclass.pen,G.to_be_merged_vertices,G.rdg_vertices,0,gclass.value[6],gclass.value[5])
    G.circulation(gclass.pen,gclass.ocan.canvas, C, 1, 2)

if __name__ == "__main__":
    run()