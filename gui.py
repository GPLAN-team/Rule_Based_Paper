import math
import tkinter as tk
from FastPLAN import FastPLAN
from input import Input
import json
from FastPLAN.FastPLAN import runner
from FastPLAN.FastPLAN import my_plot
import matplotlib.pyplot as plt
from api import multigraph_to_rfp, dimensioning_part
import networkx as nx
import sys
import turtle
import numpy as np
import pythongui.drawing as draw
import Temp_Code.gengraphs as gengraphs
import source.inputgraph as inputgraph
from pythongui import dimensiongui as dimgui
import circulation as cir
from os.path import exists
import source.lettershape.lshape.Lshaped as Lshaped

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


helv15 = ("Helvetica", 15, "bold")
helv8 = ("Helvetica", 8, "bold")
colors = [
    "#7B68EE",  # medium slate blue
    "#40E0D0",  # turqouise
    "#FF7F50",  # coral
    "#FF69B4",  # hot pink
    "#E6E6FA",  # lavender
    "#FA8072",  # salmon
    "#98FB98",  # pale green
    "#BA55D3",  # medium orchid
    "#B0C4DE",  # light steel blue
    "#FFA500",  # orange
    "#FFDAB9",  # peach puff
    "#6495ED",  # corn flower blue
] * 10
INPUTGRAPH_JSON_PATH = ("./FastPLAN/inputgraph.json")

rgb_colors = [
    (123, 104, 238),  # medium slate blue
    (64, 224, 208),  # turqouise
    (255, 127, 80),  # coral
    (255, 105, 180),  # hot pink
    (230, 230, 250),  # lavender
    (250, 128, 114),  # salmon
    (152, 251, 152),  # pale green
    (186, 85, 211),  # medium orchid
    (176, 196, 222),  # light steel blue
    (255, 165, 0),  # orange
    (255, 218, 185),  # peach puff
    (100, 149, 237),  # corn flower blue
]*10

hex_colors = [
    "#7B68EE",  # medium slate blue
    "#40E0D0",  # turqouise
    "#FF7F50",  # coral
    "#FF69B4",  # hot pink
    "#E6E6FA",  # lavender
    "#FA8072",  # salmon
    "#98FB98",  # pale green
    "#BA55D3",  # medium orchid
    "#B0C4DE",  # light steel blue
    "#FFA500",  # orange
    "#FFDAB9",  # peach puff
    "#6495ED",  # corn flower blue
]*10


class App:
    def __init__(self) -> None:
        self.input = Input()
        self.initialise_root()
        self.add_logo()
        self.custom_rfp_section()
        # self.properties_section()
        self.modification_section()
        self.rfp_draw_section()
        self.room_check = []
        self.room_checkobj = []
        self.room_freq = []
        self.value = []
        self.freqbox = []
        self.output_found = False
        self.curr_rfp = -1
        self.colors_map = {}
        self.irreg_check = 0
        self.graph_objs = []
        self.grid_scale = 0
        self.grid_coord = []
        self.circ_val = 0
        self.floorplan_graphs = []
        self.current_graphs = []

    def initialise_root(self):
        self.root = tk.Tk()
        self.root.title("Rule Based GPLAN")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(str(str(self.screen_width) +
                           'x' + str(self.screen_height)))

    def add_logo(self):
        self.logo_frame = tk.Frame(self.root)
        self.logo_frame.grid(row=0, column=0)
        logo_canvas = tk.Canvas(self.logo_frame, width=100, height=100)
        logo_canvas.pack()
        logo_canvas.create_text(50, 50, text="GPLAN", font=helv15)

    def custom_rfp_section(self):
        self.custom_rfp_choice_frame = tk.Frame(self.root)
        # master = self.custom_rfp_choice_frame
        self.custom_rfp_choice_frame.grid(row=0, column=1, padx=10, pady=10)
        self.oneBHK_Button = tk.Button(self.custom_rfp_choice_frame, text="1 BHK", font=helv15,
                                       command=self.oneBHK_Button_click)
        self.oneBHK_Button.grid(row=0, column=0, padx=10, pady=10)
        self.twoBHK_Button = tk.Button(self.custom_rfp_choice_frame, text="2 BHK", font=helv15,
                                       command=self.twoBHK_Button_click)
        self.twoBHK_Button.grid(row=0, column=1, padx=10, pady=10)
        self.threeBHK_Button = tk.Button(self.custom_rfp_choice_frame, text="3 BHK", font=helv15,
                                         command=self.threeBHK_Button_click)
        self.threeBHK_Button.grid(row=0, column=2, padx=10, pady=10)
        self.reset_Button = tk.Button(self.custom_rfp_choice_frame, text="Reset", font=helv15,
                                      command=self.reset_Button_click)
        self.reset_Button.grid(row=0, column=3, padx=10, pady=10)

        self.dimCheckVar = tk.IntVar(value=1)
        self.gridCheckVar = tk.IntVar()
        self.circCheckVar = tk.IntVar()
        # self.dimCheckVar = 1
        # self.dim_Button = tk.Checkbutton(self.custom_rfp_choice_frame, text="Dimensioned", font=helv15,
        #                                  command=self.dimensioned_checkbox_click, variable=self.dimCheckVar, onvalue=1, offvalue=0)

        # self.dim_Button.grid(row=0, column=4, padx=10, pady=10)

        self.grid_Button = tk.Checkbutton(self.custom_rfp_choice_frame, text="Grid", font=helv15,
                                          command=self.grid_checkbox_click, variable=self.gridCheckVar, onvalue=1, offvalue=0)

        self.grid_Button.grid(row=0, column=4, padx=10, pady=10)

        self.circ_Button = tk.Checkbutton(self.custom_rfp_choice_frame, text="Circulation", font=helv15,
                                          command=self.circ_checkbox_click, variable=self.circCheckVar, onvalue=1, offvalue=0)

        self.circ_Button.grid(row=0, column=5, padx=10, pady=10)

        self.showGraph_Button = tk.Button(self.custom_rfp_choice_frame, text="Show Current Graph", font=helv15,
                                          command=self.showGraph_Button_click)
        self.showGraph_Button.grid(row=0, column=6, padx=10, pady=10)

    # def properties_section(self):
        # self.properties_frame = tk.Frame(self.root)
        # self.properties_frame.grid(row=1, column=11, padx=10, pady=10)

        # self.colors_table_frame = tk.Frame(self.properties_frame)
        # self.colors_table_frame.grid()
        # self.colors_table_canvas = tk.Canvas(
        #     self.colors_table_frame, width=300, height=500)
        # self.colors_table_canvas.grid()

        # self.update_colors_table()

    def modification_section(self):
        self.modify_frame = tk.Frame(self.root)
        self.modify_frame.grid(row=1, column=0, padx=10, pady=10)

        self.modify_rooms_button = tk.Button(self.modify_frame, text="Modify Rooms", font=helv15,
                                             command=self.modify_rooms_Button_click)
        self.modify_rooms_button.grid(row=2, column=0, padx=10, pady=10)

        self.modify_doors_button = tk.Button(self.modify_frame, text="Adjacencies", font=helv15,
                                             command=self.modify_doors_Button_click)
        self.modify_doors_button.grid(row=3, column=0, padx=10, pady=10)

        self.modify_doors_button = tk.Button(self.modify_frame, text="Non-Adjacencies", font=helv15,
                                             command=self.modify_non_adj_Button_click)
        self.modify_doors_button.grid(row=4, column=0, padx=10, pady=10)

        self.run_button = tk.Button(self.modify_frame, text="Rectangular floorplan", font=helv15,
                                    command=self.run_Rect_Button_click)
        self.run_button.grid(row=5, column=0, padx=10, pady=10)

        self.run_button = tk.Button(self.modify_frame, text="Irregular floorplan", font=helv15,
                                    command=self.run_Irreg_Button_click)
        self.run_button.grid(row=6, column=0, padx=10, pady=10)

        self.run_button = tk.Button(self.modify_frame, text="L-Shaped floorplan", font=helv15,
                                    command=self.run_Lshaped_Button_click)
        self.run_button.grid(row=7, column=0, padx=10, pady=10)

        self.prev_btn = tk.Button(
            self.modify_frame, text="Previous", font=helv15, command=self.handle_prev_btn)
        self.prev_btn.grid(row=8, column=0, padx=10, pady=10)

        self.next_btn = tk.Button(
            self.modify_frame, text="Next", font=helv15, command=self.handle_next_btn)
        self.next_btn.grid(row=9, column=0, padx=10, pady=10)

        self.exit_btn = tk.Button(
            self.modify_frame, text="Exit", font=helv15, command=self.handle_exit_btn)
        self.exit_btn.grid(row=10, column=0, padx=11, pady=10)

        # self.circ_button = tk.Button(self.modify_frame, text="Circulation floorplan", font=helv15,
        #                              command=self.run_Circ_Button_click)
        # self.circ_button.grid(row=10, column=0, padx=10, pady=10)

    def rfp_draw_section(self):
        self.rfp_draw_frame = tk.Frame(self.root)
        self.rfp_draw_frame.grid(
            row=1, column=1, padx=10, pady=10, rowspan=10, columnspan=10)

        # self.rfp_canvas = tk.Canvas(
        #     self.rfp_draw_frame, width=800, height=800, background="red", border=10)
        # self.rfp_canvas.grid(row=0, column=0, rowspan=10, columnspan=10)

        self.rfp_canvas = turtle.ScrolledCanvas(
            self.rfp_draw_frame, width=900, height=550)
        self.rfp_canvas.bind("<Double-Button-1>", self.zoom)
        self.rfp_canvas.grid(row=0, column=0, rowspan=10, columnspan=10)
        self.tscreen = turtle.TurtleScreen(self.rfp_canvas)
        self.tscreen.screensize(50000, 1000)
        # self.tscreen.bgcolor(col[3])
        self.pen = turtle.RawTurtle(self.tscreen)
        self.pen.speed(10000000)

    def zoom(self, event):
        self.canvas.config(width=self.root.winfo_screenwidth(),
                           height=self.root.winfo_screenheight())

    def handle_prev_btn(self):

        if self.curr_rfp == 0:
            tk.messagebox.showwarning("The Start", "Please try new options")
            return

        if self.gridCheckVar.get() == 1:
            self.grid_Button.deselect()
        if self.circCheckVar.get() == 1:
            self.circ_Button.deselect()

        self.curr_rfp -= 1
        graph_data = self.graph_objs[self.curr_rfp]

        # graph = inputgraph.InputGraph(
        #     self.graphs_param[self.curr_rfp][0], self.graphs_param[self.curr_rfp][1], self.graphs_param[self.curr_rfp][2], self.graphs_param[self.curr_rfp][3])

        # if (self.circ_val == 1):
        #     print("Condition : Circulation Irregular")
        #     graph_data = {
        #         'room_x': graph.room_x,
        #         'room_y': graph.room_y,
        #         'room_width': graph.room_width,
        #         'room_height': graph.room_height,
        #         'area': graph.area,
        #         'extranodes': graph.extranodes,
        #         'mergednodes': graph.mergednodes,
        #         'irreg_nodes': graph.irreg_nodes1
        #     }

        # elif (self.dimCheckVar.get() == 1 and self.irreg_check == 1):
        #     print("Condition : Dimensioned Irregular")
        #     # try:
        #     #     graph.oneconnected_dual("multiple")
        #     # except inputgraph.OCError:
        #     #     print("Can not generate rectangular floorplan.")
        #     #     graph.irreg_multiple_dual()
        #     # except inputgraph.BCNError:
        #     # graph.irreg_multiple_dual()
        #     # graph.single_floorplan(self.dim_params[0], self.dim_params[2], self.dim_params[1], self.dim_params[3],
        #     #                        self.dim_params[4], self.dim_params[5], self.dim_params[6], self.dim_params[7], self.dim_params[8])
        #     graph_data = {
        #         'room_x': graph.room_x,
        #         'room_y': graph.room_y,
        #         'room_width': graph.room_width,
        #         'room_height': graph.room_height,
        #         'area': graph.area,
        #         'extranodes': graph.extranodes,
        #         'mergednodes': graph.mergednodes,
        #         'irreg_nodes': graph.irreg_nodes1
        #     }
        # # elif (self.irreg_check == 1):
        # #     print("Condition : Non dimensioned Irregular")
        # #     # try:
        # #     #     graph.oneconnected_dual("multiple")
        # #     # except inputgraph.OCError:
        # #     #     print("Can not generate rectangular floorplan.")
        # #     #     graph.irreg_multiple_dual()
        # #     # except inputgraph.BCNError:
        # #     graph.irreg_single_dual()
        # #     graph_data = {
        # #         'room_x': graph.room_x,
        # #         'room_y': graph.room_y,
        # #         'room_width': graph.room_width,
        # #         'room_height': graph.room_height,
        # #         'area': graph.area,
        # #         'extranodes': graph.extranodes,
        # #         'mergednodes': graph.mergednodes,
        # #         'irreg_nodes': graph.irreg_nodes1
        # #     }

        # elif (self.dimCheckVar.get() == 1 and self.irreg_check == 0):
        #     # graph.irreg_multiple_dual()
        #     # graph.single_floorplan(self.dim_params[0], self.dim_params[2], self.dim_params[1], self.dim_params[3],
        #     #                        self.dim_params[4], self.dim_params[5], self.dim_params[6], self.dim_params[7], self.dim_params[8])
        #     # print(graph.floorplan_exist)
        #     # while(graph.floorplan_exist == False):
        #     #     old_dims = [min_width, max_width, min_height,
        #     #                 max_height, symm_string, min_aspect, max_aspect]
        #     #     min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = dimgui.gui_fnc(
        #     #         old_dims, nodecnt)
        #     #     graph.multiple_dual()
        #     #     graph.single_floorplan(min_width, min_height, max_width, max_height,
        #     #                         symm_string, min_aspect, max_aspect, plot_width, plot_height)
        #     # end = time.time()
        #     # printe("Time taken: " + str((end-start)*1000) + " ms")
        #     graph_data = {
        #         'room_x': graph.room_x,
        #         'room_y': graph.room_y,
        #         'room_width': graph.room_width,
        #         'room_height': graph.room_height,
        #         'area': graph.area,
        #         'extranodes': graph.extranodes,
        #         'mergednodes': graph.mergednodes,
        #         'irreg_nodes': graph.irreg_nodes1
        #     }

        # # else:
        # #     graph.irreg_single_dual()
        # #     graph_data = {
        # #         'room_x': graph.room_x,
        # #         'room_y': graph.room_y,
        # #         'room_width': graph.room_width,
        # #         'room_height': graph.room_height,
        # #         'area': graph.area,
        # #         'extranodes': graph.extranodes,
        # #         'mergednodes': graph.mergednodes,
        # #         'irreg_nodes': graph.irreg_nodes1
        # #     }

        self.draw_one_rfp(graph_data)

    def handle_next_btn(self):
        if self.curr_rfp == len(self.graph_objs) - 1:
            tk.messagebox.showwarning(
                "The End", "You have exhausted all the options")
            return

        if self.gridCheckVar.get() == 1:
            self.grid_Button.deselect()
        if self.circCheckVar.get() == 1:
            self.circ_Button.deselect()

        self.curr_rfp += 1
        graph_data = self.graph_objs[self.curr_rfp]
        # cir.plot(self.circ_graphs[self.curr_rfp], len(self.circ_graphs[self.curr_rfp]))

        # graph = inputgraph.InputGraph(
        #     self.graphs_param[self.curr_rfp][0], self.graphs_param[self.curr_rfp][1], self.graphs_param[self.curr_rfp][2], self.graphs_param[self.curr_rfp][3])

        # if (self.circ_val == 1):
        #     print("Condition : Circulation Irregular")
        #     graph_data = {
        #         'room_x': graph.room_x,
        #         'room_y': graph.room_y,
        #         'room_width': graph.room_width,
        #         'room_height': graph.room_height,
        #         'area': graph.area,
        #     }

        # elif (self.dimCheckVar.get() == 1 and self.irreg_check == 1):
        #     print("Condition : Dimensioned Irregular")
        #     # try:
        #     #     graph.oneconnected_dual("multiple")
        #     # except inputgraph.OCError:
        #     #     print("Can not generate rectangular floorplan.")
        #     #     graph.irreg_multiple_dual()
        #     # except inputgraph.BCNError:
        #     # graph.irreg_multiple_dual()
        #     # graph.single_floorplan(self.dim_params[0], self.dim_params[2], self.dim_params[1], self.dim_params[3],
        #     #                        self.dim_params[4], self.dim_params[5], self.dim_params[6], self.dim_params[7], self.dim_params[8])

        #     graph_data = {
        #         'room_x': graph.room_x,
        #         'room_y': graph.room_y,
        #         'room_width': graph.room_width,
        #         'room_height': graph.room_height,
        #         'area': graph.area,
        #         'extranodes': graph.extranodes,
        #         'mergednodes': graph.mergednodes,
        #         'irreg_nodes': graph.irreg_nodes1
        #     }
        # # elif (self.irreg_check == 1):
        # #     print("Condition : Non dimensioned Irregular")
        # #     # try:
        # #     #     graph.oneconnected_dual("multiple")
        # #     # except inputgraph.OCError:
        # #     #     print("Can not generate rectangular floorplan.")
        # #     #     graph.irreg_multiple_dual()
        # #     # except inputgraph.BCNError:
        # #     graph.irreg_single_dual()
        # #     graph_data = {
        # #         'room_x': graph.room_x,
        # #         'room_y': graph.room_y,
        # #         'room_width': graph.room_width,
        # #         'room_height': graph.room_height,
        # #         'area': graph.area,
        # #         'extranodes': graph.extranodes,
        # #         'mergednodes': graph.mergednodes,
        # #         'irreg_nodes': graph.irreg_nodes1
        # #     }

        # elif (self.dimCheckVar.get() == 1 and self.irreg_check == 0):
        #     # graph.irreg_multiple_dual()
        #     # graph.single_floorplan(self.dim_params[0], self.dim_params[2], self.dim_params[1], self.dim_params[3],
        #     #                        self.dim_params[4], self.dim_params[5], self.dim_params[6], self.dim_params[7], self.dim_params[8])
        #     # print(f"FloorPlan Exist: {graph.floorplan_exist}")
        #     # while(graph.floorplan_exist == False):
        #     #     old_dims = [min_width, max_width, min_height,
        #     #                 max_height, symm_string, min_aspect, max_aspect]
        #     #     min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = dimgui.gui_fnc(
        #     #         old_dims, nodecnt)
        #     #     graph.multiple_dual()
        #     #     graph.single_floorplan(min_width, min_height, max_width, max_height,
        #     #                         symm_string, min_aspect, max_aspect, plot_width, plot_height)
        #     # end = time.time()
        #     # printe("Time taken: " + str((end-start)*1000) + " ms")

        #     graph_data = {
        #         'room_x': graph.room_x,
        #         'room_y': graph.room_y,
        #         'room_width': graph.room_width,
        #         'room_height': graph.room_height,
        #         'area': graph.area,
        #         'extranodes': graph.extranodes,
        #         'mergednodes': graph.mergednodes,
        #         'irreg_nodes': graph.irreg_nodes1
        #     }

        # # else:
        # #     graph.irreg_single_dual()
        # #     graph_data = {
        # #         'room_x': graph.room_x,
        # #         'room_y': graph.room_y,
        # #         'room_width': graph.room_width,
        # #         'room_height': graph.room_height,
        # #         'area': graph.area,
        # #         'extranodes': graph.extranodes,
        # #         'mergednodes': graph.mergednodes,
        # #         'irreg_nodes': graph.irreg_nodes1
        # #     }

        # # print(graph_data['room_x'].shape[0])
        self.draw_one_rfp(graph_data)

    def handle_exit_btn(self):
        self.root.destroy()
        exit()

    # def update_colors_table(self):

    #     self.colors_table_canvas.delete("all")
    #     for i, each_room in enumerate(self.input.rooms.values()):
    #         self.colors_table_canvas.create_rectangle(
    #             100, 100 + i*30, 120, 120 + i*30, fill=self.colors_map[each_room])
    #         self.colors_table_canvas.create_text(
    #             200, 105 + i*30, text=each_room)

    def draw_one_rfp(self, graph_data, origin=(0, 0), scale=1):
        x, y = origin
        if self.gridCheckVar.get() == 1:
            self.grid_Button.deselect()
        self.rfp_canvas.delete("all")

        # draw.draw_rdg(graph_data, 1, self.pen, 1,
        #               colors[:self.graphs_param[self.curr_rfp][0]], [], 250)

        for i, each_room in enumerate(self.input.rooms.values()):
            #     print(f"each room {each_room}")
            self.colors_map[self.input.rooms[i]
                            ] = hex_colors[i]
            # if self.irreg_check == 1:
            #     self.rfp_canvas.create_rectangle(x + scale * each_room['left'], y + scale * each_room['top'], x + scale * (
            #         each_room['left'] + each_room['width']), y + scale * (each_room['top'] + each_room['height']), fill=hex_colors[each_room['label']])
            #     # self.rfp_canvas.create_text( x + scale*(each_room['left'] + each_room['width']/2), y + scale * (each_room['top'] + each_room['height']/2), text=self.input.rooms[each_room['label']], font= helv8)

        # self.update_colors_table()
        # if self.irreg_check != 1:
        self.grid_scale, self.grid_coord = draw.draw_rdg(graph_data, 1, self.pen, 1,
                                                         list(self.colors_map.values()), self.input.rooms, 200)
        # draw.drawgrid(self.pen)

    def default_dim(self):
        min_width = []
        max_width = []
        min_height = []
        max_height = []
        symm_string = "()"
        min_aspect = []
        max_aspect = []
        plot_width = -1
        plot_height = -1
        for i, room in self.input.rooms.items():
            if (room == "Living"):
                min_width.append(9)
                min_height.append(11)
                max_width.append(14)
                max_height.append(18)
                min_aspect.append(0.5)
                max_aspect.append(2)
            elif (room == "Kitchen"):
                min_width.append(6)
                min_height.append(8)
                max_width.append(10)
                max_height.append(13)
                min_aspect.append(0.7)
                max_aspect.append(2.2)
            elif (room == "Bed 2"):
                min_width.append(7)
                min_height.append(7)
                max_width.append(12)
                max_height.append(11)
                min_aspect.append(0.7)
                max_aspect.append(2.2)
            elif (room == "Bed 1"):
                min_width.append(8)
                min_height.append(9)
                max_width.append(13)
                max_height.append(14)
                min_aspect.append(.7)
                max_aspect.append(2.2)
            elif (room == "WC 1"):
                min_width.append(6)
                min_height.append(4)
                max_width.append(10)
                max_height.append(7)
                min_aspect.append(0.7)
                max_aspect.append(2.2)
            elif (room == "WC 2"):
                min_width.append(4)
                min_height.append(3)
                max_width.append(8)
                max_height.append(7)
                min_aspect.append(0.7)
                max_aspect.append(2.2)
            elif (room == "Store"):
                min_width.append(4)
                min_height.append(4)
                max_width.append(8)
                max_height.append(8)
                min_aspect.append(0.7)
                max_aspect.append(2.2)
            elif (room == "Dining"):
                min_width.append(5)
                min_height.append(4)
                max_width.append(9)
                max_height.append(8)
                min_aspect.append(0.7)
                max_aspect.append(2.2)
            elif (room == "Office"):
                min_width.append(5)
                min_height.append(4)
                max_width.append(9)
                max_height.append(8)
                min_aspect.append(0.7)
                max_aspect.append(2.2)
            else:
                min_width.append(0)
                min_height.append(0)
                max_width.append(9999)
                max_height.append(9999)
                min_aspect.append(0.5)
                max_aspect.append(2)
        self.dim_constraints = [
            min_width, max_width, min_height, max_height, min_aspect, max_aspect]
        return min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height

    def filename(self):
        s = ""
        t = ""
        if ("Dining" in self.input.rooms.values() and "Store" in self.input.rooms.values()):
            if (len(self.interior_rooms) == 2):
                s = "Dint"
                t = "Sint"
            elif (len(self.interior_rooms) == 1 and self.input.rooms[self.interior_rooms[0]] == "Dining"):
                s = "Dint"
                t = "S"
            elif (len(self.interior_rooms) == 1 and self.input.rooms[self.interior_rooms[0]] == "Store"):
                s = "D"
                t = "Sint"
            else:
                s = "D"
                t = "S"
        elif ("Dining" in self.input.rooms.values()):
            if (len(self.interior_rooms) == 1 and self.input.rooms[self.interior_rooms[0]] == "Dining"):
                s = "Dint"
            else:
                s = "D"
        elif ("Store" in self.input.rooms.values()):
            if (len(self.interior_rooms) == 1 and self.input.rooms[self.interior_rooms[0]] == "Store"):
                t = "Sint"
            else:
                t = "S"
        self.filename = f"graphs/{s}{t}.pkl"

    # def showGraph_Button_click(self):
    #     print("Showing Graph of current floor plan")
    #     # print(len(self.currentGraph))
    #     self.my_plot_current(self.floorplan_graphs[self.curr_rfp])
    #     plt.show()

    # def my_plot_current(self, current, figsize=14, dotsize=20):
    #     num = 1
    #     fig = plt.figure()
    #     k = int(np.sqrt(num))
    #     i = 1
    #     # making graph
    #     plt.subplot(k+1, k+1, i+1)
    #     gnx = nx.Graph(current)
    #     nx.draw_kamada_kawai(
    #         gnx, node_size=100, with_labels=True, node_color='orange', font_size=10)
    #     print('.', end='')


    def showGraph_Button_click(self):
        print("Showing Graph of current floor plan")
        # create a new window
        graph_window = tk.Toplevel()
        graph_window.title("Floor Plan Graph")

        # create a matplotlib figure and plot the graph
        fig = Figure(figsize=(6, 4), dpi=100)
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        ax = fig.add_subplot(111)

        # create the initial graph
        self.draw_graph(ax)

        # bind the edge click event to a callback function
        canvas.mpl_connect('button_press_event', lambda event: self.on_edge_click(event, ax, graph_window))

        # add a button to close the window
        button = tk.Button(master=graph_window, text="Close", command=graph_window.destroy)
        button.pack(side=tk.BOTTOM)

    def draw_graph(self, ax):
        gnx = nx.Graph(self.current_graphs[self.curr_rfp])
        nx.draw_kamada_kawai(
            gnx, node_size=100, with_labels=True, node_color='orange', font_size=10, ax=ax)
        ax.set_title("Floor Plan Graph")
    

    

    # def on_edge_click(self, event, ax, graph_window):
    #     # get the mouse coordinates and the graph layout
    #     x, y = event.xdata, event.ydata
    #     pos = nx.kamada_kawai_layout(self.current_graphs[self.curr_rfp])

    #     # compute the maximum spanning tree of the graph and get its edges in order of increasing weight
    #     mst_edges = list(nx.algorithms.tree.mst.maximum_spanning_edges(self.current_graphs[self.curr_rfp], algorithm='kruskal', data=False))

    #     # find the closest edge to the mouse click among the edges in the maximum spanning tree
    #     min_dist = float('inf')
    #     closest_edge = None
    #     for u, v in mst_edges:
    #         # iterate over each edge segment
    #         for i in range(len(pos[u])-1):
    #             p1 = np.array([pos[u][i], pos[u][i+1]])
    #             p2 = np.array([pos[v][i], pos[v][i+1]])

    #             # calculate the distance from the mouse click to the edge segment
    #             dist = np.linalg.norm(np.cross(p2-p1, p1-np.array([x, y])))/np.linalg.norm(p2-p1)

    #             if dist < min_dist:
    #                 min_dist = dist
    #                 closest_edge = (u, v)
    #     def traingulated(G):
    #         for cycle in nx.cycle_basis(G):
    #             if len(cycle) >= 4 and not nx.chordal.is_chordal(nx.Graph(G.subgraph(cycle))):
    #                 return False
    #         return True

    #     # remove the closest edge and redraw the graph
    #     self.current_graphs[self.curr_rfp].remove_edge(*closest_edge)
    #     is_triangulate = traingulated(nx.Graph(self.current_graphs[self.curr_rfp]))
    #     if is_triangulate:
    #         ax.clear()
    #         self.draw_graph(ax)
    #         ax.set_title("Floor Plan Graph (click an edge to remove it)")

    #     else:
    #         # show an error message if the graph is not triangulated
    #         print("Error: Graph is not triangulated.")

    #     ax.figure.canvas.draw()

    def on_edge_click(self, event, ax, graph_window):
        # get the mouse coordinates and the graph layout
        x, y = event.xdata, event.ydata
        pos = nx.kamada_kawai_layout(self.current_graphs[self.curr_rfp])

        # find the clicked edge, if any
        clicked_edge = None
        min_dist = float('inf')
        for u, v in self.current_graphs[self.curr_rfp].edges():
            # iterate over each edge segment
            for i in range(len(pos[u])-1):
                p1 = np.array([pos[u][i], pos[u][i+1]])
                p2 = np.array([pos[v][i], pos[v][i+1]])

                # calculate the distance from the mouse click to the edge segment
                dist = np.linalg.norm(np.cross(p2-p1, p1-np.array([x, y])))/np.linalg.norm(p2-p1)

                if dist < min_dist and dist < 0.05:  # check if the distance is small enough to be considered a click on the edge
                    min_dist = dist
                    clicked_edge = (u, v)
        def traingulated(G):
            for cycle in nx.cycle_basis(G):
                if len(cycle) >= 4 and not nx.chordal.is_chordal(nx.Graph(G.subgraph(cycle))):
                    return False
            return True

        if clicked_edge is not None:
            # remove the clicked edge and redraw the graph

            self.current_graphs[self.curr_rfp].remove_edge(*clicked_edge)
            is_triangulate = traingulated(nx.Graph(self.current_graphs[self.curr_rfp]))
            if is_triangulate:
                ax.clear()
                self.draw_graph(ax)
                ax.set_title("Floor Plan Graph (click an edge to remove it)")
            else:
                # show an error message if the graph is not triangulated
                ax.set_title("Floor Plan Graph - Cannot remove edge because graph is not triangulated")
                print("Error: Graph is not triangulated.")
        else:
            # do nothing if the click is on white space
            pass

        ax.figure.canvas.draw()

    def run_Rect_Button_click(self):
        self.filename()
        if (not (exists(self.filename))):
            print("File exists")
        print("[LOG] Rectangular Floorplans Button Clicked")

        self.graph_objs = []

        print(f"Room List is {list(self.input.rooms.values())}")
        print(f"Doors List is {self.input.adjacencies}")
        print(f"Non-Adjacencies List is {self.input.non_adjacencies}")
        self.create_inputgraph_json()
        # graphs = runner(False)
        self.interior_rooms.sort()
        print("Exterior rooms: ", self.exterior_rooms,
              "  Interior rooms: ", self.interior_rooms)
        self.graphs, coord_list, self.room_mapping, adjacencies_modified, non_adjacencies_modified, self.graphs_param = gengraphs.generate_graphs(
            self.exterior_rooms, self.interior_rooms, list(self.input.rooms.values()), rect_floorplans=True, adjacencies=self.input.adjacencies, non_adjacencies=self.input.non_adjacencies, )
        graphs = self.graphs
        self.input.add_rooms_from(self.room_mapping)
        self.input.add_doors_from(adjacencies_modified)
        self.input.add_non_adjacencies_from(non_adjacencies_modified)

        min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = self.default_dim()
        self.dim_params = [min_width, max_width, min_height, max_height,
                           symm_string, min_aspect, max_aspect, plot_width, plot_height]

        for i in range(len(self.graphs)):
            graph = inputgraph.InputGraph(
                self.graphs_param[i][0], self.graphs_param[i][1], self.graphs_param[i][2], self.graphs_param[i][3])
            graph.irreg_multiple_dual()
            graph.single_floorplan(self.dim_params[0], self.dim_params[2], self.dim_params[1], self.dim_params[3],
                                   self.dim_params[4], self.dim_params[5], self.dim_params[6], self.dim_params[7], self.dim_params[8])
            print(graph.floorplan_exist)
            if (graph.floorplan_exist):
                graph_data = {
                    'room_x': graph.room_x,
                    'room_y': graph.room_y,
                    'room_width': graph.room_width,
                    'room_height': graph.room_height,
                    'area': graph.area,
                    'extranodes': graph.extranodes,
                    'mergednodes': graph.mergednodes,
                    'irreg_nodes': graph.irreg_nodes1
                }

                self.graph_objs.append(graph_data)
                self.current_graphs.append(self.graphs[i])
                self.floorplan_graphs.append(self.graphs[i])

        print("[LOG] Dimensioned selected")

        # print(graphs)
        my_plot(graphs)
        plt.show()
        # nodecnt = len(graphs[0].nodes)
        print("[LOG] Now will wait for dimensions input")

        # old_dims = [[0] * nodecnt, [0] * nodecnt, [0] * nodecnt,
        #             [0] * nodecnt, "", [0] * nodecnt, [0] * nodecnt]
        # min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = dimgui.gui_fnc(
        #     old_dims, nodecnt)

        # dim_graphdata = dimensioning_part(graphs, coord_list)
        print("[LOG] Dimensioned floorplan object\n")
        # print(dim_graphdata)

        print(f"{len(graphs)} output_graphs = {str(graphs)}")

        # self.draw_one_rfp(dim_graphdata)

        # output_rfps = multigraph_to_rfp(graphs, rectangular=True)
        # print(f"number of rfps = {len(output_rfps)}")
        # self.output_rfps = output_rfps

        self.output_found = True
        self.curr_rfp = -1

        # print(f"{len(output_rfps)} output rfps = {str(output_rfps)}")

        # print(f"one rfp = {output_rfps[0]}")

        # else:
        #     # print(graphs)
        #     my_plot(graphs)
        #     plt.show()

        #     print(f"{len(graphs)} output_graphs = {str(graphs)}")

        #     # output_rfps = multigraph_to_rfp(graphs, rectangular=True)
        #     # print(f"number of rfps = {len(output_rfps)}")
        #     # self.output_rfps = output_rfps

        #     self.output_found = True
        #     self.curr_rfp = -1

        #     # print(f"{len(output_rfps)} output rfps = {str(output_rfps)}")

        #     # print(f"one rfp = {output_rfps[0]}")
        print(f"Number of Floor Plans : {len(self.graph_objs)}")
        self.handle_next_btn()

    def run_Irreg_Button_click(self):
        print("[LOG] Irregular Floorplans Button Clicked")

        self.graph_objs = []

        print(f"Room List is {list(self.input.rooms.values())}")
        print(f"Doors List is {self.input.adjacencies}")
        self.create_inputgraph_json()
        # graphs = runner(False)
        self.irreg_check = 1
        self.interior_rooms.sort()
        print("Exterior rooms: ", self.exterior_rooms,
              "  Interior rooms: ", self.interior_rooms)
        self.graphs, coord_list, self.room_mapping, adjacencies_modified, non_adjacencies_modified, self.graphs_param = gengraphs.generate_graphs(
            self.exterior_rooms, self.interior_rooms, list(self.input.rooms.values()), rect_floorplans=False, adjacencies=self.input.adjacencies, non_adjacencies=self.input.non_adjacencies)
        graphs = self.graphs
        self.input.add_rooms_from(self.room_mapping)
        self.input.add_doors_from(adjacencies_modified)
        self.input.add_non_adjacencies_from(non_adjacencies_modified)

        min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = self.default_dim()
        self.dim_params = [min_width, max_width, min_height, max_height,
                           symm_string, min_aspect, max_aspect, plot_width, plot_height]

        for i in range(len(self.graphs)):
            graph = inputgraph.InputGraph(
                self.graphs_param[i][0], self.graphs_param[i][1], self.graphs_param[i][2], self.graphs_param[i][3])
            graph.irreg_multiple_dual()
            graph.single_floorplan(self.dim_params[0], self.dim_params[2], self.dim_params[1], self.dim_params[3],
                                   self.dim_params[4], self.dim_params[5], self.dim_params[6], self.dim_params[7], self.dim_params[8])
            print(graph.floorplan_exist)
            if (graph.floorplan_exist):
                graph_data = {
                    'room_x': graph.room_x,
                    'room_y': graph.room_y,
                    'room_width': graph.room_width,
                    'room_height': graph.room_height,
                    'area': graph.area,
                    'extranodes': graph.extranodes,
                    'mergednodes': graph.mergednodes,
                    'irreg_nodes': graph.irreg_nodes1
                }
                print(
                    f"\nIrregular nodes1: {graph.irreg_nodes1}\nMerged Nodes : {graph.mergednodes}\nIrregular nodes2: {graph.irreg_nodes2}\n")
                self.graph_objs.append(graph_data)
                self.floorplan_graphs.append(self.graphs[i])

        # if self.dimCheckVar.get() == 1:
        print("[LOG] Dimensioned selected")

        # print(graphs)
        my_plot(graphs)
        plt.show()

        # nodecnt = len(graphs[0].nodes)
        print("[LOG] Now will wait for dimensions input")

        # old_dims = [[0] * nodecnt, [0] * nodecnt, [0] * nodecnt,
        #             [0] * nodecnt, "", [0] * nodecnt, [0] * nodecnt]
        # min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = dimgui.gui_fnc(
        #     old_dims, nodecnt)

        # dim_graphdata = dimensioning_part(graphs, coord_list)
        print("[LOG] Dimensioned floorplan object\n")
        # print(dim_graphdata)

        print(f"{len(graphs)} output_graphs = {str(graphs)}")

        # self.draw_one_rfp(dim_graphdata)

        # output_rfps = multigraph_to_rfp(graphs, rectangular=False)
        # print(f"number of rfps = {len(output_rfps)}")
        # self.output_rfps = output_rfps

        self.output_found = True
        self.curr_rfp = -1

        # print(f"{len(output_rfps)} output rfps = {str(output_rfps)}")

        # print(f"one rfp = {output_rfps[0]}")

        # else:
        #     # print(graphs)
        #     my_plot(graphs)
        #     plt.show()

        #     print(f"{len(graphs)} output_graphs = {str(graphs)}")

        #     # output_rfps = multigraph_to_rfp(graphs, rectangular=False)
        #     # print(f"number of irfps = {len(output_rfps)}")
        #     # self.output_rfps = output_rfps

        #     self.output_found = True
        #     self.curr_rfp = -1

        #     # print(f"{len(output_rfps)} output irfps = {str(output_rfps)}")

        #     # print(f"one irfp = {output_rfps[0]}")

        print(f"Number of Floor Plans : {len(self.graph_objs)}")

        self.handle_next_btn()

    def run_Lshaped_Button_click(self):
        print("[LOG] L-Shaped Floorplans Button Clicked")

        self.graph_objs = []

        print(f"Room List is {list(self.input.rooms.values())}")
        print(f"Doors List is {self.input.adjacencies}")
        print(f"Non-Adjacencies List is {self.input.non_adjacencies}")
        self.create_inputgraph_json()
        # graphs = runner(False)
        self.interior_rooms.sort()
        print("Exterior rooms: ", self.exterior_rooms,
              "  Interior rooms: ", self.interior_rooms)
        self.graphs, coord_list, self.room_mapping, adjacencies_modified, non_adjacencies_modified, self.graphs_param = gengraphs.generate_graphs(
            self.exterior_rooms, self.interior_rooms, list(self.input.rooms.values()), rect_floorplans=True, adjacencies=self.input.adjacencies, non_adjacencies=self.input.non_adjacencies, )
        graphs = self.graphs
        self.input.add_rooms_from(self.room_mapping)
        self.input.add_doors_from(adjacencies_modified)
        self.input.add_non_adjacencies_from(non_adjacencies_modified)

        min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = self.default_dim()
        self.dim_params = [min_width, max_width, min_height, max_height,
                           symm_string, min_aspect, max_aspect, plot_width, plot_height]

        for i in range(len(self.graphs)):
            graph = inputgraph.InputGraph(
                self.graphs_param[i][0], self.graphs_param[i][1], self.graphs_param[i][2], self.graphs_param[i][3])

            Lshaped.LShapedFloorplan(graph, gclass.app.nodes_data)

            # All rels are in it. Currently we have only 1.
            graph.rel_matrix_list.append(graph.matrix)

            # Since multiple rfp are generated before calling single_floorplan, all the parameters need to be
            # converted list of lists
            temp_lst = []
            temp_lst.append(graph.extranodes)
            graph.extranodes = temp_lst
            temp_lst = []
            temp_lst.append(graph.mergednodes)
            graph.mergednodes = temp_lst
            temp_lst = []
            temp_lst.append(graph.irreg_nodes1)
            graph.irreg_nodes1 = temp_lst
            temp_lst = []
            temp_lst.append(graph.room_x)
            graph.room_x = temp_lst
            temp_lst = []
            temp_lst.append(graph.room_y)
            graph.room_y = temp_lst
            temp_lst = []
            temp_lst.append(graph.room_width)
            graph.room_width = temp_lst
            temp_lst = []
            temp_lst.append(graph.room_height)
            graph.room_height = temp_lst

            graph.nodecnt -= 4  # Because Lshaped was counting NESW as well

            graph.single_floorplan(self.dim_params[0], self.dim_params[2], self.dim_params[1], self.dim_params[3],
                                   self.dim_params[4], self.dim_params[5], self.dim_params[6], self.dim_params[7], self.dim_params[8])
            print(graph.floorplan_exist)
            if (graph.floorplan_exist):
                graph_data = {
                    'room_x': graph.room_x,
                    'room_y': graph.room_y,
                    'room_width': graph.room_width,
                    'room_height': graph.room_height,
                    'area': graph.area,
                    'extranodes': graph.extranodes,
                    'mergednodes': graph.mergednodes,
                    'irreg_nodes': graph.irreg_nodes1
                }
                self.graph_objs.append(graph_data)
                self.floorplan_graphs.append(self.graphs[i])

        print("[LOG] Dimensioned selected")

        # print(graphs)
        my_plot(graphs)
        plt.show()
        # nodecnt = len(graphs[0].nodes)
        print("[LOG] Now will wait for dimensions input")

        # old_dims = [[0] * nodecnt, [0] * nodecnt, [0] * nodecnt,
        #             [0] * nodecnt, "", [0] * nodecnt, [0] * nodecnt]
        # min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = dimgui.gui_fnc(
        #     old_dims, nodecnt)

        # dim_graphdata = dimensioning_part(graphs, coord_list)
        print("[LOG] Dimensioned floorplan object\n")
        # print(dim_graphdata)

        print(f"{len(graphs)} output_graphs = {str(graphs)}")

        # self.draw_one_rfp(dim_graphdata)

        # output_rfps = multigraph_to_rfp(graphs, rectangular=True)
        # print(f"number of rfps = {len(output_rfps)}")
        # self.output_rfps = output_rfps

        self.output_found = True
        self.curr_rfp = -1

        # print(f"{len(output_rfps)} output rfps = {str(output_rfps)}")

        # print(f"one rfp = {output_rfps[0]}")

        # else:
        #     # print(graphs)
        #     my_plot(graphs)
        #     plt.show()

        #     print(f"{len(graphs)} output_graphs = {str(graphs)}")

        #     # output_rfps = multigraph_to_rfp(graphs, rectangular=True)
        #     # print(f"number of rfps = {len(output_rfps)}")
        #     # self.output_rfps = output_rfps

        #     self.output_found = True
        #     self.curr_rfp = -1

        #     # print(f"{len(output_rfps)} output rfps = {str(output_rfps)}")

        #     # print(f"one rfp = {output_rfps[0]}")
        print(f"Number of Floor Plans : {len(self.graph_objs)}")
        self.handle_next_btn()

    # def run_Circ_Button_click(self):

    #     self.circ_val = 1

    #     is_dimensioned = True
    #     remove_corridor = False
    #     dim_constraints = []

    #     print("[LOG] Circulation Floorplans Button Clicked")

    #     self.graph_objs = []

    #     print(f"Room List is {list(self.input.rooms.values())}")
    #     print(f"Doors List is {self.input.adjacencies}")
    #     print(f"Non-Adjacencies List is {self.input.non_adjacencies}")
    #     self.create_inputgraph_json()
    #     self.interior_rooms.sort()
    #     print("Exterior rooms: ", self.exterior_rooms,
    #           "  Interior rooms: ", self.interior_rooms)
    #     self.graphs, coord_list, self.room_mapping, adjacencies_modified, non_adjacencies_modified, self.graphs_param = gengraphs.generate_graphs(
    #         self.exterior_rooms, self.interior_rooms, list(self.input.rooms.values()), rect_floorplans=True, adjacencies=self.input.adjacencies, non_adjacencies=self.input.non_adjacencies, )
    #     graphs = self.graphs
    #     self.input.add_rooms_from(self.room_mapping)
    #     self.input.add_doors_from(adjacencies_modified)
    #     self.input.add_non_adjacencies_from(non_adjacencies_modified)

    #     min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = self.default_dim()
    #     self.dim_params = [min_width, max_width, min_height, max_height,
    #                        symm_string, min_aspect, max_aspect, plot_width, plot_height]
    #     # Non-dimensioned single circulation
    #     #    if (gclass.value[8] == 0 and gclass.value[9] == 0):
    #     #         start = time.time()
    #     #         graph.irreg_single_dual()
    #     #         end = time.time()
    #     #         printe("Time taken: " + str((end-start)*1000) + " ms")
    #     #         print("type of roomx " + str(type(graph.room_x)))
    #     #         graph_data = {
    #     #             'room_x': graph.room_x,
    #     #             'room_y': graph.room_y,
    #     #             'room_width': graph.room_width,
    #     #                 'room_height': graph.room_height,
    #     #                 # 'room_x_bottom_left': graph.room_x_bottom_left,
    #     #                 # 'room_x_bottom_right': graph.room_x_bottom_right,
    #     #                 # 'room_x_top_left': graph.room_x_top_left,
    #     #                 # 'room_x_top_right': graph.room_x_top_right,
    #     #                 # 'room_y_left_bottom': graph.room_y_left_bottom,
    #     #                 # 'room_y_right_bottom': graph.room_y_right_bottom,
    #     #                 # 'room_y_left_top': graph.room_y_left_top,
    #     #                 # 'room_y_right_top': graph.room_y_right_top,
    #     #                 'area': graph.area,
    #     #                 'extranodes': graph.extranodes,
    #     #                 'mergednodes': graph.mergednodes,
    #     #                 'irreg_nodes': graph.irreg_nodes1
    #     #         }

    #     #         # new_graph_data = call_circulation(graph_data, gclass.value[2], gclass.entry_door, gclass.corridor_thickness)
    #     #         (new_graph_data, success) = call_circulation(graph_data, gclass,
    #     #                                                      node_coord, is_dimensioned, dim_constraints, remove_corridor)
    #     #         # If there was some error in algorithm execution new_graph_data will be empty
    #     #         # we display the pop-up error message
    #     #         if new_graph_data == None:
    #     #             tk.messagebox.showerror(
    #     #                 "Error", "ERROR!! THE INITIAL CHOSEN ENTRY EDGE MUST BE EXTERIOR EDGE")

    #     #         # If no issues we continue to draw the corridor
    #     #         else:
    #     #             # draw_circulation(new_graph_data, gclass.ocan.canvas, gclass.value[6], gclass.entry_door)
    #     #             # draw_circulation(new_graph_data, gclass.pen, gclass.ocan.canvas, gclass.value[6])
    #     #             draw.draw_rdg(new_graph_data, 1, gclass.pen,
    #     #                           1, gclass.value[6], [], origin)

    #     # Dimensioned single circulation
    #     if (self.dimCheckVar.get()):
    #         is_dimensioned = True
    #         feasible_dim = 0
    #         # old_dims = [[0] * gclass.value[0], [0] * gclass.value[0], [0] * gclass.value[0],
    #         #             [0] * gclass.value[0], "", [0] * gclass.value[0], [0] * gclass.value[0]]
    #         # min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = dimgui.gui_fnc(
    #         #     old_dims, gclass.value[0])
    #         # dimensional_constraints = [min_width, max_width, min_height, max_height,
    #         #                            symm_string, min_aspect, max_aspect, plot_width, plot_height]
    #         # start = time.time()
    #         for i in range(len(self.graphs)):
    #             graph = inputgraph.InputGraph(
    #                 self.graphs_param[i][0], self.graphs_param[i][1], self.graphs_param[i][2], self.graphs_param[i][3])
    #             graph.irreg_multiple_dual()
    #             graph.single_floorplan(self.dim_params[0], self.dim_params[2], self.dim_params[1], self.dim_params[3],
    #                                    self.dim_params[4], self.dim_params[5], self.dim_params[6], self.dim_params[7], self.dim_params[8])
    #             print(graph.floorplan_exist)

    #             if (not (graph.floorplan_exist)):
    #                 continue
    #             # self.graph_objs.append(graph)

    #         # try:
    #         #     graph.oneconnected_dual("multiple")
    #         # except inputgraph.OCError:
    #         #     gclass.show_warning(
    #         #         "Can not generate rectangular floorplan.")
    #         #     graph.irreg_multiple_dual()
    #         # except inputgraph.BCNError:
    #         #     graph.irreg_multiple_dual()

    #         # graph.single_floorplan(min_width, min_height, max_width, max_height,
    #         #                        symm_string, min_aspect, max_aspect, plot_width, plot_height)
    #         # while (graph.floorplan_exist == False):
    #         #     old_dims = [min_width, max_width, min_height,
    #         #                 max_height, symm_string, min_aspect, max_aspect]
    #         #     min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = dimgui.gui_fnc(
    #         #         old_dims, gclass.value[0])
    #         #     graph.irreg_multiple_dual()
    #         #     graph.single_floorplan(min_width, min_height, max_width, max_height,
    #         #                            symm_string, min_aspect, max_aspect, plot_width, plot_height)
    #         # end = time.time()
    #         # printe("Time taken: " + str((end-start)*1000) + " ms")
    #             # for idx in range(len(graph.room_x)):
    #             graph_data = {
    #                 'room_x': graph.room_x,
    #                 'room_y': graph.room_y,
    #                 'room_width': graph.room_width,
    #                 'room_height': graph.room_height,
    #                 'area': graph.area,
    #                 'extranodes': graph.extranodes,
    #                 'mergednodes': graph.mergednodes,
    #                 'irreg_nodes': graph.irreg_nodes1
    #             }

    #             # new_graph_data = call_circulation(graph_data, gclass.value[2], gclass.entry_door, gclass.corridor_thickness)

    #             # new_graph_data, success
    #             try:
    #                 (new_graph_data, success) = self.call_circulation(
    #                     graph_data, self.graphs[i].edges, is_dimensioned, self.dim_constraints, remove_corridor)
    #             except:
    #                 continue
    #             print("Constraints: ", self.dim_constraints)
    #             print("New graph data: ", new_graph_data)
    #             print("success: ", success)
    #             # If there was some error in algorithm execution new_graph_data will be empty
    #             # we display the pop-up error message

    #             print(f"NEW GRAPH DATA : {new_graph_data}")
    #             if new_graph_data == None:
    #                 tk.messagebox.showerror(
    #                     "Error", "ERROR!! THE INITIAL CHOSEN ENTRY EDGE MUST BE EXTERIOR EDGE")

    #             # If no issues we continue to draw the corridor
    #             else:
    #                 if (success == False):
    #                     continue
    #                 # draw_circulation(new_graph_data, gclass.ocan.canvas, gclass.value[6], gclass.entry_door)
    #                 # draw_circulation(new_graph_data, gclass.pen, gclass.ocan.canvas, gclass.value[6])
    #                 # draw.draw_rdg(new_graph_data, 1, self.pen,
    #                 #               1, gclass.value[6], [], origin)

    #                 # graph.room_x = new_graph_data['room_x']
    #                 # graph.room_y = new_graph_data['room_y']
    #                 # graph.room_width = new_graph_data['room_width']
    #                 # graph.room_height = new_graph_data['room_height']
    #                 # graph.area = new_graph_data['area']
    #                 self.graph_objs.append(new_graph_data)

    #                 feasible_dim = 1
    #                 # break

    #             if (feasible_dim == 0):
    #                 tk.messagebox.showerror(
    #                     "Error", "ERROR!! NO CIRCULATION POSSIBLE FOR GIVEN DIMENSIONS")

    #     # elif (gclass.value[8] == 0 and gclass.value[9] == 1):  # Add/remove
    #         # remove_corridor = True
    #         # start = time.time()
    #         # graph.irreg_single_dual()
    #         # end = time.time()
    #         # printe("Time taken: " + str((end-start)*1000) + " ms")
    #         # print("type of roomx " + str(type(graph.room_x)))
    #         # graph_data = {
    #         #     'room_x': graph.room_x,
    #         #     'room_y': graph.room_y,
    #         #     'room_width': graph.room_width,
    #         #     'room_height': graph.room_height,
    #         #     'area': graph.area,
    #         #     'extranodes': graph.extranodes,
    #         #     'mergednodes': graph.mergednodes,
    #         #     'irreg_nodes': graph.irreg_nodes1
    #         # }

    #         # (new_graph_data, success) = call_circulation(graph_data, gclass,
    #         #                                              node_coord, is_dimensioned, dim_constraints, remove_corridor)

    #         # # If there was some error in algorithm execution new_graph_data will be empty
    #         # # we display the pop-up error message
    #         # if new_graph_data == None:
    #         #     tk.messagebox.showerror(
    #         #         "Error", "ERROR!! THE INITIAL CHOSEN ENTRY EDGE MUST BE EXTERIOR EDGE")

    #         # # If no issues we continue to draw the corridor
    #         # else:
    #         #     # draw_circulation(new_graph_data, gclass.ocan.canvas, gclass.value[6], gclass.entry_door)
    #         #     # draw_circulation(new_graph_data, gclass.pen, gclass.ocan.canvas, gclass.value[6])
    #         #     draw.draw_rdg(new_graph_data, 1, gclass.pen,
    #         #                   1, gclass.value[6], [], origin)

    #     my_plot(graphs)
    #     plt.show()

    #     # nodecnt = len(graphs[0].nodes)
    #     # print("[LOG] Now will wait for dimensions input")

    #     # old_dims = [[0] * nodecnt, [0] * nodecnt, [0] * nodecnt,
    #     #             [0] * nodecnt, "", [0] * nodecnt, [0] * nodecnt]
    #     # min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = dimgui.gui_fnc(
    #     #     old_dims, nodecnt)

    #     # dim_graphdata = dimensioning_part(graphs, coord_list)
    #     print("[LOG] Dimensioned floorplan object\n")
    #     # print(dim_graphdata)

    #     print(f"{len(graphs)} output_graphs = {str(graphs)}")

    #     # self.draw_one_rfp(dim_graphdata)

    #     # output_rfps = multigraph_to_rfp(graphs, rectangular=False)
    #     # print(f"number of rfps = {len(output_rfps)}")
    #     # self.output_rfps = output_rfps

    #     self.output_found = True
    #     self.curr_rfp = -1

    #     # print(f"{len(output_rfps)} output rfps = {str(output_rfps)}")

    #     # print(f"one rfp = {output_rfps[0]}")

    #     # else:
    #     #     # print(graphs)
    #     #     my_plot(graphs)
    #     #     plt.show()

    #     #     print(f"{len(graphs)} output_graphs = {str(graphs)}")

    #     #     # output_rfps = multigraph_to_rfp(graphs, rectangular=False)
    #     #     # print(f"number of irfps = {len(output_rfps)}")
    #     #     # self.output_rfps = output_rfps

    #     #     self.output_found = True
    #     #     self.curr_rfp = -1

    #     #     # print(f"{len(output_rfps)} output irfps = {str(output_rfps)}")

    #     #     # print(f"one irfp = {output_rfps[0]}")

    #     print(f"Number of Floor Plans : {len(self.graph_objs)}")

    #     self.handle_next_btn()

    def call_circulation(self, graph_data, edges, is_dimensioned, dim_constraints, remove_corridor):

        # print("PARAMS START: \n")
        # print(graph_data, edges, is_dimensioned,
        #       dim_constraints, remove_corridor)
        # print(f"ROOM MAPPING : {self.room_mapping}")
        # print("PARAMS END: \n")
        g = nx.Graph()
        remove_corridor = False
        edge_set = edges

        # scale = self.grid_scale

        corridor_thickness = 1

        for x in edge_set:
            g.add_edge(x[0], x[1])

        n = len(g)

        rooms = []
        for i in range(len(g.nodes())):
            rooms.append(cir.Room(i, graph_data.get("room_x")[i], graph_data.get("room_y")[i] + graph_data.get(
                "room_height")[i], graph_data.get("room_x")[i] + graph_data.get("room_width")[i], graph_data.get("room_y")[i]))

        # cir.plot(g,n)
        rfp = cir.RFP(g, rooms)

        i = self.room_mapping.index('WC 1')
        entry0 = self.room_mapping.index('Living')
        entry1 = self.room_mapping.index('Kitchen')

        circulation_obj = cir.circulation(g, corridor_thickness, rfp)

        # circulation_obj = cir.circulation(g, rfp)
        if is_dimensioned == True:
            circulation_obj.is_dimensioned = True
            circulation_obj.dimension_constraints = dim_constraints
        # circulation_result = circulation_obj.circulation_algorithm(entry[0], entry[1])
        # circulation_result = circulation_obj.multiple_circulation(coord)
        circulation_result = circulation_obj.circulation_algorithm(
            entry0+1, entry1+1)
        if circulation_result == 0:
            return None

        # print("ADJACENCIES: ",circulation_obj.adjacency)

        # Else do not include WC1
        circulation_obj.donot_include(
            len(g), circulation_obj.circulation_graph, i)

        # if remove_corridor == True:
        #     # Created a deepcopy of object to display circulation before
        #     # we display GUI for removing corridor
        #     circ = copy.deepcopy(circulation_obj)
        #     circ.adjust_RFP_to_circulation()

        #     # Printing how much shift was done for each room
        #     for room in circ.RFP.rooms:
        #         print("Room ", room.id, ":")
        #         print("Push top edge by: ", room.rel_push_T)
        #         print("Push bottom edge by: ", room.rel_push_B)
        #         print("Push left edge by: ", room.rel_push_L)
        #         print("Push right edge by: ", room.rel_push_R)
        #         print(room.target)
        #         print('\n')

        #     room_x1 = []
        #     room_y1 = []
        #     room_height1 = []
        #     room_width1 = []

        #     # Getting the required values
        #     for room in circ.RFP.rooms:
        #         room_x1.append(room.top_left_x)
        #         room_y1.append(room.bottom_right_y)
        #         room_height1.append(abs(room.top_left_y - room.bottom_right_y))
        #         room_width1.append(abs(room.top_left_x - room.bottom_right_x))

        #     graph_data1 = {}
        #     graph_data1['room_x'] = np.array(room_x1)
        #     graph_data1['room_y'] = np.array(room_y1)
        #     graph_data1['room_height'] = np.array(room_height1)
        #     graph_data1['room_width'] = np.array(room_width1)
        #     graph_data1['area'] = np.array(circulation_obj.room_area)
        #     graph_data1['extranodes'] = graph_data['extranodes']
        #     graph_data1['mergednodes'] = graph_data['mergednodes']
        #     graph_data1['irreg_nodes'] = graph_data['irreg_nodes']
        #     draw.draw_rdg(graph_data1, 1, gclass.pen, 1,
        #                   gclass.value[6], [], origin)

        #     # Now going back to flow of removing circulation
        #     corridors = circulation_obj.adjacency
        #     rem_edges = gclass.remove_corridor_gui(corridors)

        #     for x in rem_edges:
        #         circulation_obj.remove_corridor(
        #             circulation_obj.circulation_graph, x[0], x[1])

        # To remove entry corridor alone we are just shifting rooms by looking at second corridor vertex
        # Done by shifting the range left bound in for loop of adjust_RFP_to_circulation()
        circulation_obj.adjust_RFP_to_circulation()

        # Printing how much shift was done for each room
        # for room in circulation_obj.RFP.rooms:
        #     print("Room ", room.id, ":")
        #     print("Push top edge by: ", room.rel_push_T)
        #     print("Push bottom edge by: ", room.rel_push_B)
        #     print("Push left edge by: ", room.rel_push_L)
        #     print("Push right edge by: ", room.rel_push_R)
        #     print(room.target)
        #     print('\n')

        room_x = []
        room_y = []
        room_height = []
        room_width = []
        new_graph_data = dict()
        # Getting the required values
        for room in circulation_obj.RFP.rooms:
            room_x.append(room.top_left_x)
            room_y.append(room.bottom_right_y)
            room_height.append(abs(room.top_left_y - room.bottom_right_y))
            room_width.append(abs(room.top_left_x - room.bottom_right_x))

        new_graph_data['room_x'] = np.array(room_x)
        new_graph_data['room_y'] = np.array(room_y)
        new_graph_data['room_height'] = np.array(room_height)
        new_graph_data['room_width'] = np.array(room_width)
        new_graph_data['area'] = np.array(circulation_obj.room_area)
        new_graph_data['extranodes'] = graph_data['extranodes']
        new_graph_data['mergednodes'] = graph_data['mergednodes']
        new_graph_data['irreg_nodes'] = graph_data['irreg_nodes']
        return (new_graph_data, circulation_obj.is_dimensioning_successful)

    def create_inputgraph_json(self):
        input = {}
        input["nodes"] = list(self.input.rooms.values())
        input["edges"] = self.input.adjacencies

        inputgraph_object = json.dumps(input, indent=4)

        with open(INPUTGRAPH_JSON_PATH, "w") as outfile:
            outfile.write(inputgraph_object)

    def oneBHK_Button_click(self):
        print("[LOG] One BHK Button Clicked")

        self.input.reset()
        with open('./one_bhk.json') as one_file:
            one_bhk_data = json.load(one_file)

        new_rooms = one_bhk_data['rooms']
        new_adj_list = one_bhk_data['adjacency_constraints']

        self.input.add_rooms_from(room_list=new_rooms)
        self.input.add_doors_from(adjcancy_list=new_adj_list)

        print(self.input.rooms)
        print(self.input.adjacencies)

    def twoBHK_Button_click(self):
        print("[LOG] two BHK Button Clicked")

        self.input.reset()
        with open('./two_bhk.json') as one_file:
            one_bhk_data = json.load(one_file)

        new_rooms = one_bhk_data['rooms']
        new_adj_list = one_bhk_data['adjacency_constraints']
        new_non_adj_list = one_bhk_data['non_adjacency_constraints']

        self.input.add_rooms_from(room_list=new_rooms)
        self.input.add_doors_from(adjcancy_list=new_adj_list)
        self.input.add_non_adjacencies_from(
            non_adjacency_list=new_non_adj_list)

        print(self.input.rooms)
        print(self.input.adjacencies)
        print(self.input.non_adjacencies)

    def threeBHK_Button_click(self):
        print("[LOG] three BHK Button Clicked")

        self.input.reset()
        with open('./three_bhk.json') as one_file:
            one_bhk_data = json.load(one_file)

        new_rooms = one_bhk_data['rooms']
        new_adj_list = one_bhk_data['adjacency_constraints']

        self.input.add_rooms_from(room_list=new_rooms)
        self.input.add_doors_from(adjcancy_list=new_adj_list)

        print(self.input.rooms)
        print(self.input.adjacencies)

    def reset_Button_click(self):
        print("[LOG] Reset Button Clicked")
        self.input.reset()

    def dimensioned_checkbox_click(self):
        check = "Checked" if self.dimCheckVar.get() == 1 else "Unchecked"
        print("[LOG] Dimensioned checkbox ", check)

    def grid_checkbox_click(self):
        check = "Checked" if self.gridCheckVar.get() == 1 else "Unchecked"
        print("[LOG] Grid checkbox ", check)
        if self.grid_scale == 0:
            tk.messagebox.showwarning(
                "The End", "You need to draw the floor plan first")
            self.grid_Button.deselect()
            return
        else:
            draw.draw_grid(self.pen, self.grid_scale, self.grid_coord)

    def circ_checkbox_click(self):
        check = "Checked" if self.circCheckVar.get() == 1 else "Unchecked"
        print("[LOG] Circ checkbox ", check)
        # print(f"SELF.GRAPH_OBJ Length: {len(self.graph_objs)}\n")
        try:
            feasible_dim = 0
            print(f"OLD GRAPH DATA: {self.graph_objs[self.curr_rfp]}")
            (new_graph_data, success) = self.call_circulation(
                self.graph_objs[self.curr_rfp], self.floorplan_graphs[self.curr_rfp].edges, True, self.dim_constraints, False)
            print(f"NEW GRAPH DATA: {new_graph_data}")
            if (success == False):
                tk.messagebox.showwarning(
                    "The End", "Success False, Circulation not possible")
                return
            self.draw_one_rfp(new_graph_data)

            feasible_dim = 1
            # break

            if (feasible_dim == 0):
                tk.messagebox.showerror(
                    "Error", "ERROR!! NO CIRCULATION POSSIBLE FOR GIVEN DIMENSIONS")
        except:
            tk.messagebox.showwarning(
                "The End", "Circulation not possible")

    def recall_room_list_frame(self, frame):

        head = tk.Label(frame, text="Room List")
        head.grid(row=0, column=0, padx=5, pady=5)

        self.room_label_list = []
        self.remove_room_btn_list = []
        self.interior_rooms = []
        self.exterior_rooms = []
        self.interior_rooms_btn_list = dict()
        for i, each_room in self.input.rooms.items():
            self.exterior_rooms.append(i)
            each_room_label = tk.Label(frame, text=each_room)
            each_room_label.grid(row=i+1, column=0, padx=5, pady=5)
            self.room_label_list.append(each_room_label)
            if (each_room == "Dining" or each_room == "Store"):
                each_remove_room_btn = tk.Button(
                    frame, text="Remove", command=lambda i=i: self.handle_remove_room_btn(i, self.mod_room_win))
                each_remove_room_btn.grid(row=i+1, column=1, padx=5, pady=5)

                each_intext_room_btn = tk.Button(
                    frame, text="Interior", command=lambda i=i: self.handle_intext_room_btn(i))
                each_intext_room_btn.grid(row=i+1, column=2, padx=5, pady=5)

                self.interior_rooms_btn_list[each_room] = each_intext_room_btn

                self.remove_room_btn_list.append(each_remove_room_btn)

    def modify_rooms_Button_click(self):
        print("[LOG] Modify Rooms Button Clicked")

        self.possible_rooms = ["Office"]

        for i, each_room in self.input.rooms.items():
            if (each_room in self.possible_rooms):
                self.possible_rooms.remove(each_room)
        room_win = tk.Toplevel(self.root)
        self.mod_room_win = room_win

        room_win.title("Room Modifier")
        # room_win.geometry(str(1000) + 'x' + str(400))
        prev_room_list_frame = tk.Frame(room_win)

        prev_room_list_frame.grid()

        self.recall_room_list_frame(prev_room_list_frame)

        new_room_frame = tk.Frame(room_win)
        new_room_frame.grid(row=1, column=0)

        for i in range(len(self.possible_rooms)):
            each_room_label = tk.Label(
                new_room_frame, text=self.possible_rooms[i])
            # each_room_label.insert(index='1.0', chars=self.possible_rooms[i])
            each_room_label.grid(row=i, column=0, padx=5, pady=5)
            add_new_room_btn = tk.Button(new_room_frame, text="Add Room",
                                         command=lambda i=each_room_label: self.handle_add_new_room_btn(i, prev_room_list_frame))
            add_new_room_btn.grid(row=i, column=1)

        new_room_text = tk.Text(new_room_frame, height=1, width=8)
        new_room_text.grid(row=len(self.possible_rooms),
                           column=0, padx=5, pady=5)

        add_new_room_btn = tk.Button(new_room_frame, text="Add Room",
                                     command=lambda i=new_room_text: self.handle_add_new_room_btn(i, prev_room_list_frame))
        add_new_room_btn.grid(row=len(self.possible_rooms), column=1)

        room_win.wait_window()

    def handle_add_new_room_btn(self, new_room, prev_room_list_frame):
        idx = len(self.input.rooms)
        try:
            self.input.rooms[idx] = new_room.get("1.0", "end")
        except:
            self.input.rooms[idx] = new_room.cget("text")
            # new_room.destroy()
            # add_new_room_btn.destroy()
        print(self.input.rooms)
        self.mod_room_win.destroy()
        self.modify_rooms_Button_click()
        # self.recall_room_list_frame(prev_room_list_frame)

    def handle_remove_room_btn(self, room_id, room_win):
        print(f"room to remove is {room_id}")
        self.input.rooms.pop(room_id)
        # self.room_label_list[room_id].destroy()
        # self.remove_room_btn_list[room_id].destroy()
        # self.interior_rooms_btn_list[room_id].destroy()
        self.input.add_rooms_from(room_list=list(self.input.rooms.values()))
        print(f"current room list = {self.input.rooms}")
        # self.recall_room_list_frame(prev_room_list_frame)
        room_win.destroy()
        self.modify_rooms_Button_click()

    def handle_intext_room_btn(self, room_id, ):
        # print(f"room is {room_id}")
        self.exterior_rooms.remove(room_id)
        self.interior_rooms.append(room_id)
        self.interior_rooms_btn_list[self.input.rooms[room_id]].configure(
            highlightbackground='blue')
        print("Exterior Rooms: ")
        print(self.exterior_rooms)
        # print(f"current room list = {self.input.rooms}")

    def modify_doors_Button_click(self):
        print("[LOG] Adjacencies Button Clicked")

        doors_win = tk.Toplevel(self.root)

        doors_win.title("Adjacencies")
        # doors_win.geometry(str(1000) + 'x' + str(400))

        adj_frame = tk.Frame(doors_win)
        adj_frame.grid(row=0)

        self.recall_adj_constraints_frame(adj_frame)

        add_new_adj_frame = tk.Frame(doors_win)
        add_new_adj_frame.grid(row=1)

        cur_new_adj_frame_row = 0

        add_new_adj_label = tk.Label(
            add_new_adj_frame, text="Add New Adjacency")
        add_new_adj_label.grid(row=cur_new_adj_frame_row, columnspan=5)

        self.new_adj_text_left = tk.StringVar()
        self.new_adj_text_right = tk.StringVar()

        cur_new_adj_frame_row += 1

        new_adj_option_left = tk.OptionMenu(
            add_new_adj_frame, self.new_adj_text_left, *list(self.input.rooms.values()))
        new_adj_option_left.grid(
            row=cur_new_adj_frame_row, column=0, padx=5, pady=5)

        new_adj_door_sign = tk.Label(add_new_adj_frame, text="<=>")
        new_adj_door_sign.grid(row=cur_new_adj_frame_row,
                               column=1, padx=5, pady=5)

        new_adj_option_right = tk.OptionMenu(
            add_new_adj_frame, self.new_adj_text_right, *list(self.input.rooms.values()))
        new_adj_option_right.grid(
            row=cur_new_adj_frame_row, column=2, padx=5, pady=5)

        add_new_adj_btn = tk.Button(
            add_new_adj_frame, text="Add Rule", command=lambda: self.handle_add_new_adj_btn(adj_frame))
        add_new_adj_btn.grid(row=cur_new_adj_frame_row,
                             column=3, padx=5, pady=5)

        doors_win.wait_variable()

    def modify_non_adj_Button_click(self):
        print("[LOG] Modify Non-Adjacencies Button Clicked")

        doors_win = tk.Toplevel(self.root)

        doors_win.title("Non-Adjacencies Modifier")
        # doors_win.geometry(str(1000) + 'x' + str(400))

        non_adj_frame = tk.Frame(doors_win)
        non_adj_frame.grid(row=0)

        self.recall_non_adj_constraints_frame(non_adj_frame)

        add_new_non_adj_frame = tk.Frame(doors_win)
        add_new_non_adj_frame.grid(row=1)

        cur_new_non_adj_frame_row = 0

        add_new_non_adj_label = tk.Label(
            add_new_non_adj_frame, text="Add New Non-Adjacencies")
        add_new_non_adj_label.grid(row=cur_new_non_adj_frame_row, columnspan=5)

        self.new_non_adj_text_left = tk.StringVar()
        self.new_non_adj_text_right = tk.StringVar()

        cur_new_non_adj_frame_row += 1

        new_non_adj_option_left = tk.OptionMenu(
            add_new_non_adj_frame, self.new_non_adj_text_left, *list(self.input.rooms.values()))
        new_non_adj_option_left.grid(
            row=cur_new_non_adj_frame_row, column=0, padx=5, pady=5)

        new_non_adj_door_sign = tk.Label(add_new_non_adj_frame, text="<=>")
        new_non_adj_door_sign.grid(
            row=cur_new_non_adj_frame_row, column=1, padx=5, pady=5)

        new_non_adj_option_right = tk.OptionMenu(
            add_new_non_adj_frame, self.new_non_adj_text_right, *list(self.input.rooms.values()))
        new_non_adj_option_right.grid(
            row=cur_new_non_adj_frame_row, column=2, padx=5, pady=5)

        add_new_non_adj_btn = tk.Button(
            add_new_non_adj_frame, text="Add Rule", command=lambda: self.handle_add_new_non_adj_btn(non_adj_frame))
        add_new_non_adj_btn.grid(
            row=cur_new_non_adj_frame_row, column=3, padx=5, pady=5)

        doors_win.wait_variable()

    def handle_add_new_adj_btn(self, frame):
        right = self.new_adj_text_right.get()
        left = self.new_adj_text_left.get()
        rule_dict = self.input.rooms
        rev_dict = dict(zip(rule_dict.values(), rule_dict.keys()))
        self.input.adjacencies.append([rev_dict[left], rev_dict[right]])
        self.recall_adj_constraints_frame(frame)

    def handle_add_new_non_adj_btn(self, frame):
        right = self.new_non_adj_text_right.get()
        left = self.new_non_adj_text_left.get()
        rule_dict = self.input.rooms
        rev_dict = dict(zip(rule_dict.values(), rule_dict.keys()))
        self.input.non_adjacencies.append([rev_dict[left], rev_dict[right]])
        self.recall_non_adj_constraints_frame(frame)

    def handle_remove_adj_rule_btn(self, frame: tk.Frame, rule):
        print(f"rule to remove {rule}")
        print(f"current adjs is {self.input.adjacencies}")
        self.input.adjacencies.remove(rule)
        self.recall_adj_constraints_frame(frame)

    def handle_remove_non_adj_rule_btn(self, frame: tk.Frame, rule):
        print(f"rule to remove {rule}")
        print(f"current non-adjs is {self.input.adjacencies}")
        self.input.non_adjacencies.remove(rule)
        self.recall_non_adj_constraints_frame(frame)

    def recall_adj_constraints_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        adj_cons_label = tk.Label(frame, text="Adjacencies")
        adj_cons_label.grid(row=0, padx=5, pady=5)

        self.adj_cons_frame_list = []

        for i, each_rule in enumerate(self.input.adjacencies):
            each_frame = tk.Frame(frame)
            each_frame.grid(row=i+1)

            if each_rule[0] in self.input.rooms.keys() and each_rule[1] in self.input.rooms.keys():
                left_label = tk.Label(
                    each_frame, text=self.input.rooms[each_rule[0]])
                left_label.grid(row=i+1, column=0, padx=5, pady=5)

                door_sign = tk.Label(each_frame, text="<=>")
                door_sign.grid(row=i+1, column=1, padx=5, pady=5)

                right_label = tk.Label(
                    each_frame, text=self.input.rooms[each_rule[1]])
                right_label.grid(row=i+1, column=2, padx=5, pady=5)

                remove_adj_btn = tk.Button(each_frame, text="Remove Rule", command=lambda lframe=frame,
                                           lrule=each_rule: self.handle_remove_adj_rule_btn(lframe, lrule))
                remove_adj_btn.grid(row=i+1, column=3, padx=5, pady=5)

            else:
                self.input.adjacencies.remove(each_rule)

    def recall_non_adj_constraints_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        non_adj_cons_label = tk.Label(frame, text="Non adjacencies")
        non_adj_cons_label.grid(row=0, padx=5, pady=5)

        self.non_adj_cons_frame_list = []

        for i, each_rule in enumerate(self.input.non_adjacencies):
            each_frame = tk.Frame(frame)
            each_frame.grid(row=i+1)

            if each_rule[0] in self.input.rooms.keys() and each_rule[1] in self.input.rooms.keys():
                left_label = tk.Label(
                    each_frame, text=self.input.rooms[each_rule[0]])
                left_label.grid(row=i+1, column=0, padx=5, pady=5)

                door_sign = tk.Label(each_frame, text="<=>")
                door_sign.grid(row=i+1, column=1, padx=5, pady=5)

                right_label = tk.Label(
                    each_frame, text=self.input.rooms[each_rule[1]])
                right_label.grid(row=i+1, column=2, padx=5, pady=5)

                remove_non_adj_btn = tk.Button(each_frame, text="Remove Rule", command=lambda lframe=frame,
                                               lrule=each_rule: self.handle_remove_non_adj_rule_btn(lframe, lrule))
                remove_non_adj_btn.grid(row=i+1, column=3, padx=5, pady=5)

            else:
                self.input.non_adjacencies.remove(each_rule)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
