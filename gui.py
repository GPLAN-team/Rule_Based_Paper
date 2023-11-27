import math
import tkinter as tk
from FastPLAN import FastPLAN
from input import Input
import json
import os.path
import pickle
from FastPLAN.FastPLAN import runner
from FastPLAN.FastPLAN import my_plot
import matplotlib.pyplot as plt
from api import multigraph_to_rfp, dimensioning_part
import networkx as nx
from tkinter import ttk
import sys
import turtle
import numpy as np
import pythongui.drawing as draw
import Temp_Code.gengraphs as gengraphs
import source.inputgraph as inputgraph
from source.graphoperations.operations import get_encoded_matrix
from pythongui import dimensiongui as dimgui
import circulation as cir
from os.path import exists
import source.lettershape.lshape.Lshaped as Lshaped

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from pythongui.catalogue_maker import generate_catalogue_dimensioned


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
        self.input = Input()  # setting rooms, adjacencies and non-adjacencies list values

        print("intialise_root() called.")
        self.initialise_root()  # sets title
        print("add_logo() called.")
        self.add_logo()  # sets name
        print("custom_rfp_section() called.")
        self.custom_rfp_section()  # sets the horizontal toolbox
        # self.properties_section()
        print("modification_section() called.")
        self.modification_section()  # sets the vertical toolbox
        print("rfp_draw_section() called.")
        self.rfp_draw_section()  # creates canvas where floorplans are displayed
        self.room_check = []
        self.room_checkobj = []
        self.curr_map = {}
        self.room_freq = []
        self.curr_adjacencies =[]
        self.value = []
        # self.exterior_rooms = []
        # self.interior_rooms = []
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
        self.arr_altered = False
        self.dimensional_constraints = []
        self.room_list = []
        self.bhk = ""
        

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
        self.custom_rfp_choice_frame.grid(row=0, column=1, padx=10, pady=10)
        # master = self.custom_rfp_choice_frame

        self.oneBHK_Button = tk.Button(
            self.custom_rfp_choice_frame, text="1 BHK", font=helv15, command=self.oneBHK_Button_click)
        self.oneBHK_Button.grid(row=0, column=0, padx=10, pady=10)

        self.twoBHK_Button = tk.Button(
            self.custom_rfp_choice_frame, text="2 BHK", font=helv15, command=self.twoBHK_Button_click)
        self.twoBHK_Button.grid(row=0, column=1, padx=10, pady=10)

        self.threeBHK_Button = tk.Button(
            self.custom_rfp_choice_frame, text="3 BHK", font=helv15, command=self.threeBHK_Button_click)
        self.threeBHK_Button.grid(row=0, column=2, padx=10, pady=10)

        self.reset_Button = tk.Button(
            self.custom_rfp_choice_frame, text="Reset", font=helv15, command=self.reset_Button_click)
        self.reset_Button.grid(row=0, column=3, padx=10, pady=10)

        self.dimCheckVar = tk.IntVar(value=1)
        self.gridCheckVar = tk.IntVar()
        self.circCheckVar = tk.IntVar()

        # self.dimCheckVar = 1
        # self.dim_Button = tk.Checkbutton(self.custom_rfp_choice_frame, text="Dimensioned", font=helv15, command=self.dimensioned_checkbox_click, variable=self.dimCheckVar, onvalue=1, offvalue=0)
        # self.dim_Button.grid(row=0, column=4, padx=10, pady=10)

        self.grid_Button = tk.Checkbutton(self.custom_rfp_choice_frame, text="Grid", font=helv15,
                                          command=self.grid_checkbox_click, variable=self.gridCheckVar, onvalue=1, offvalue=0)
        self.grid_Button.grid(row=0, column=4, padx=10, pady=10)

        self.circ_Button = tk.Checkbutton(self.custom_rfp_choice_frame, text="Circulation", font=helv15,
                                          command=self.circ_checkbox_click, variable=self.circCheckVar, onvalue=1, offvalue=0)
        self.circ_Button.grid(row=0, column=5, padx=10, pady=10)

        self.showGraph_Button = tk.Button(
            self.custom_rfp_choice_frame, text="Graph", font=helv15, command=self.showGraph_Button_click)
        self.showGraph_Button.grid(row=0, column=6, padx=10, pady=10)

        self.changeDimButton = tk.Button(
            self.custom_rfp_choice_frame, text="Dimensions", font=helv15, command=self.changeDimButtonClick)
        self.changeDimButton.grid(row=0, column=7, padx=10, pady=10)

        self.changeDimButton = tk.Button(
            self.custom_rfp_choice_frame, text="Show Adjacencies", font=helv15, command=self.change_adjacencies)
        self.changeDimButton.grid(row=0, column=8, padx=10, pady=10)

        # self.changeDimButton = tk.Button(
        #     self.custom_rfp_choice_frame, text="Default Dimensions", font=helv15, command=self.changeDefaultDimButtonClick)
        # self.changeDimButton.grid(row=0, column=8, padx=10, pady=10)

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

        self.modify_rooms_button = tk.Button(
            self.modify_frame, text="Modify Rooms", font=helv15, command=self.modify_rooms_Button_click)
        self.modify_rooms_button.grid(row=2, column=0, padx=10, pady=10)

        self.modify_adjacencies_Button = tk.Button(
            self.modify_frame, text="Adjacencies", font=helv15, command=self.modify_adjacencies_Button_click)
        self.modify_adjacencies_Button.grid(row=3, column=0, padx=10, pady=10)

        self.modify_non_adj_Button = tk.Button(
            self.modify_frame, text="Non-Adjacencies", font=helv15, command=self.modify_non_adj_Button_click)
        self.modify_non_adj_Button.grid(row=4, column=0, padx=10, pady=10)

        self.run_button = tk.Button(
            self.modify_frame, text="Rectangular floorplan", font=helv15, command=self.run_Rect_Button_click)
        self.run_button.grid(row=5, column=0, padx=10, pady=10)

        self.run_button = tk.Button(
            self.modify_frame, text="Irregular floorplan", font=helv15, command=self.run_Irreg_Button_click)
        self.run_button.grid(row=6, column=0, padx=10, pady=10)

        # self.run_button = tk.Button(
        #     self.modify_frame, text="L-Shaped floorplan", font=helv15, command=self.run_Lshaped_Button_click)
        self.run_button.grid(row=7, column=0, padx=10, pady=10)

        self.prev_btn = tk.Button(
            self.modify_frame, text="Previous", font=helv15, command=self.handle_prev_btn)
        self.prev_btn.grid(row=8, column=0, padx=10, pady=10)

        self.next_btn = tk.Button(
            self.modify_frame, text="Next", font=helv15, command=self.handle_next_btn)
        self.next_btn.grid(row=9, column=0, padx=10, pady=10)

        # self.exit_btn = tk.Button(
        #     self.modify_frame, text="Exit", font=helv15, command=self.handle_exit_btn)
        # self.exit_btn.grid(row=10, column=0, padx=10, pady=10)

        self.downnload_Button = tk.Button(
            self.modify_frame, text="Download Catalogue", font=helv15, command=self.download_catalogue)
        self.downnload_Button.grid(row=10, column=0, padx=10, pady=10)

        self.downnload_Button = tk.Button(
            self.modify_frame, text="L-Shaped Floorplan", font=helv15, command=self.run_Lshaped_Button_click)
        self.downnload_Button.grid(row=11, column=0, padx=10, pady=10)

        # self.circ_button = tk.Button(self.modify_frame, text="Circulation floorplan", font=helv15,
        #                              command=self.run_Circ_Button_click)
        # self.circ_button.grid(row=10, column=0, padx=10, pady=10)
    
    def rfp_draw_section(self):
        self.dragging = False
        self.zoom_level = 1.0
        self.rfp_draw_frame = tk.Frame(self.root)
        self.rfp_draw_frame.grid(
            row=1, column=1, padx=10, pady=10, rowspan=10, columnspan=10)
        #scroll bar
        self.scrollbar = tk.Scrollbar(self.rfp_draw_frame, orient="vertical")
        self.scrollbar.grid(row=0, column=10, rowspan=10, sticky="ns")
        # Create a turtle canvas in the tkinter frame
        self.rfp_canvas = turtle.ScrolledCanvas(
            self.rfp_draw_frame, width=900, height=550)
        self.rfp_canvas.grid(row=0, column=0, rowspan=10, columnspan=10)
        self.rfp_canvas.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.rfp_canvas.yview)
        self.pen = turtle.RawTurtle(self.rfp_canvas)
        #dragging
        self.rfp_canvas.bind("<Button-1>", self.on_canvas_click)
        self.rfp_canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.rfp_canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        self.pen = turtle.RawTurtle(self.rfp_canvas)
        self.pen.speed(0)  # Set the turtle's speed as needed
        #zoom binding
        self.rfp_canvas.bind("<MouseWheel>", self.on_mouse_wheel)
    
    def on_canvas_click(self, event):
        self.dragging = True
        self.prev_x = event.x
        self.prev_y = event.y

    def on_canvas_drag(self, event):
        if self.dragging:
            x, y = event.x, event.y
            self.rfp_canvas.xview_scroll(self.prev_x - x, "units")
            self.rfp_canvas.yview_scroll(self.prev_y - y, "units")
            self.prev_x, self.prev_y = x, y

    def on_canvas_release(self, event):
        self.dragging = False
    

    def on_mouse_wheel(self, event):
        zoom_factor = 1.1 if event.delta > 0 else 1/1.1  # Zoom in or out
        self.zoom_canvas(zoom_factor)
        self.zoom_turtle(zoom_factor)

    def zoom_canvas(self, zoom_factor):
        # Scale the canvas to achieve zoom
        self.rfp_canvas._canvas.scale("all", 0, 0, zoom_factor, zoom_factor)

    def zoom_turtle(self, zoom_factor):
        # Scale the turtle graphics to match the canvas
        self.pen.turtlesize(self.pen.turtlesize()[0] * zoom_factor, self.pen.turtlesize()[1] * zoom_factor)
        self.pen.resizemode("auto")  # Automatically adjust turtle siz
   



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
        print(graph_data)
        self.draw_one_rfp(graph_data)

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
            self.colors_map[self.input.rooms[i]] = hex_colors[i]
            # if self.irreg_check == 1:
            #     self.rfp_canvas.create_rectangle(x + scale * each_room['left'], y + scale * each_room['top'], x + scale * (
            #         each_room['left'] + each_room['width']), y + scale * (each_room['top'] + each_room['height']), fill=hex_colors[each_room['label']])
            #     # self.rfp_canvas.create_text( x + scale*(each_room['left'] + each_room['width']/2), y + scale * (each_room['top'] + each_room['height']/2), text=self.input.rooms[each_room['label']], font= helv8)

        # self.update_colors_table()
        # if self.irreg_check != 1:
        self.grid_scale, self.grid_coord = draw.draw_rdg(
            graph_data, 1, self.pen, 1, list(self.colors_map.values()), self.input.rooms, 200)
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
        room_list = []
        for i, room in self.input.rooms.items():
            room_list.append(room)
            # if (room == "Living"):
            #     min_width.append(6)
            #     min_height.append(8)
            #     max_width.append(14)
            #     max_height.append(18)
            #     min_aspect.append(0.35)
            #     max_aspect.append(2)
            # elif (room == "Kitchen"):
            #     min_width.append(4)
            #     min_height.append(6)
            #     max_width.append(10)
            #     max_height.append(13)
            #     min_aspect.append(0.5)
            #     max_aspect.append(2.2)
            # elif (room == "Bed 2"):
            #     min_width.append(5)
            #     min_height.append(5)
            #     max_width.append(12)
            #     max_height.append(11)
            #     min_aspect.append(0.5)
            #     max_aspect.append(2.2)
            # elif (room == "Bed 3"):
            #     min_width.append(5)
            #     min_height.append(5)
            #     max_width.append(12)
            #     max_height.append(11)
            #     min_aspect.append(0.5)
            #     max_aspect.append(2.2)
            # elif (room == "Bed 1"):
            #     min_width.append(6)
            #     min_height.append(6)
            #     max_width.append(13)
            #     max_height.append(14)
            #     min_aspect.append(.5)
            #     max_aspect.append(2.2)
            # elif (room == "WC 1"):
            #     min_width.append(1.5)
            #     min_height.append(6)
            #     max_width.append(7)
            #     max_height.append(8)
            #     min_aspect.append(0.5)
            #     max_aspect.append(2.2)
            # elif (room == "WC 2"):
            #     min_width.append(2)
            #     min_height.append(1.5)
            #     max_width.append(7)
            #     max_height.append(7)
            #     min_aspect.append(0.5)
            #     max_aspect.append(2.2)
            # elif (room == "WC 3"):
            #     min_width.append(2)
            #     min_height.append(1.5)
            #     max_width.append(7)
            #     max_height.append(7)
            #     min_aspect.append(0.5)
            #     max_aspect.append(2.2)
            # elif (room == "Store"):
            #     min_width.append(2)
            #     min_height.append(2)
            #     max_width.append(8)
            #     max_height.append(8)
            #     min_aspect.append(0.5)
            #     max_aspect.append(2.2)
            # elif (room == "Dining"):
            #     min_width.append(3)
            #     min_height.append(2)
            #     max_width.append(9)
            #     max_height.append(8)
            #     min_aspect.append(0.5)
            #     max_aspect.append(2.2)
            # elif (room == "Office"):
            #     min_width.append(3)
            #     min_height.append(2)
            #     max_width.append(9)
            #     max_height.append(8)
            #     min_aspect.append(0.5)
            #     max_aspect.append(2.2)
            # else:
            min_width.append(0)
            min_height.append(0)
            max_width.append(9999)
            max_height.append(9999)
            min_aspect.append(0.1)
            max_aspect.append(100)

        self.dim_constraints = [min_width, max_width,
                                min_height, max_height, min_aspect, max_aspect]
        self.dimensional_constraints = [min_width, max_width, min_height,
                                        max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height]
        self.room_list = room_list
        
        return min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height
    
 

    def GraphStore(self, isRect=True):
        val = ""
        for i, each_room in enumerate(self.input.rooms.values()):
            if (i in self.interior_rooms):
                val = val + each_room[0]+"int"
            else:
                val = val + each_room[0]
        if (isRect):
            self.filename = f"graphs/{self.bhk}{val}.pkl"
        else:
            self.filename = f"graphs/{self.bhk}{val}Irreg.pkl"

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
        canvas.mpl_connect('button_press_event', lambda event: self.on_edge_click(
            event, ax, graph_window))

        # add a button to close the window
        button = tk.Button(master=graph_window, text="Close",
                           command=graph_window.destroy)
        button.pack(side=tk.BOTTOM)
    
    def changeDefaultDimButtonClick(self):
        if self.grid_scale != 0:
            tk.messagebox.showwarning(
                "The End", "Cannot change default dimensions after floorplan is generated")
            return
        else:
            print("[LOG] Change Default Dimensions Button Clicked")

        


    def changeDimButtonClick(self):
        if self.grid_scale == 0:
            tk.messagebox.showwarning(
                "The End", "You need to draw the floor plan first")
            return
        else:
            print("[LOG] Change Dimensions Button Clicked")
            min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = self.default_dim()
            min_width.clear()
            min_height.clear()
            for i in range(len(self.graph_objs[self.curr_rfp]["room_width"])):
                min_width.append(math.floor(
                    self.graph_objs[self.curr_rfp]["room_width"][i]))
                min_height.append(math.floor(
                    self.graph_objs[self.curr_rfp]["room_height"][i]))
                # min_width=self.graph_objs[self.curr_rfp]["room_width"]
                # min_height=self.graph_objs[self.curr_rfp]["room_height"]
            old_dims = [
                min_width, max_width,
                min_height, max_height,
                symm_string,
                min_aspect, max_aspect,
                plot_width, plot_height
            ]

            print("\n\ndimgui.fui_fnc() starts: ")
            min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = dimgui.gui_fnc(
                old_dims, self.graphs_param[0][0], self.room_mapping)
            # should I write (above) :
            # self.graphs_param[0][0] or
            # self.graph_objs[self.curr_rfp]["nodecnt"]
            # for #nodes
            print("dimgui.gui_fnc() ends.\n\n")
            self.dim_params = [min_width, max_width, min_height, max_height,
                               symm_string, min_aspect, max_aspect, plot_width, plot_height]

            # representing node count, edge count, edge set, node coordinates as the 4-tuple
            dgraph = inputgraph.InputGraph(self.graph_objs[self.curr_rfp]["nodecnt"], self.graph_objs[self.curr_rfp]["edgecnt"],
                                           self.graph_objs[self.curr_rfp]["edgeset"], self.graph_objs[self.curr_rfp]["coord"])
            # above creates a graph with provided data
            # below generates dual for the computed graph and corresponding encoded matrix and rel matrix
            dgraph.irreg_multiple_dual()
            dgraph.single_floorplan(self.dim_params[0], self.dim_params[2], self.dim_params[1], self.dim_params[3],
                                    self.dim_params[4], self.dim_params[5], self.dim_params[6], self.dim_params[7], self.dim_params[8])
            # generate floorplan using the computed encoded matrix / rel matrix implementing optimisation techniques on vertical and horizonal st flows
            print("Floorplan exists? ", dgraph.floorplan_exist)
            if (dgraph.floorplan_exist):
                dgraph_data = {
                    'room_x': dgraph.room_x,
                    'room_y': dgraph.room_y,
                    'room_width': dgraph.room_width,
                    'room_height': dgraph.room_height,
                    'area': dgraph.area,
                    'extranodes': dgraph.extranodes,
                    'mergednodes': dgraph.mergednodes,
                    'irreg_nodes': dgraph.irreg_nodes1,
                    'nodecnt': self.graph_objs[self.curr_rfp]["nodecnt"],
                    'edgecnt': self.graph_objs[self.curr_rfp]["edgecnt"],
                    'edgeset': self.graph_objs[self.curr_rfp]["edgeset"],
                    'coord': self.graph_objs[self.curr_rfp]["coord"]
                }
                # self.graph_objs.append(graph_data)
                # self.floorplan_graphs.append(self.graphs[i])
                # will work only once i.e. the change dimensions will take values of the initial one.
            else:
                tk.messagebox.showwarning(
                    "The End", "Floorplan doesn't exists with changed dimensions")
                print("Floorplan doesn't exists with changed dimensions")
                return

            self.draw_one_rfp(dgraph_data)

    # def draw_graph(self, ax):
    #     gnx = nx.Graph(self.floorplan_graphs[self.curr_rfp])
    #     nx.draw_kamada_kawai(gnx, node_size=100, with_labels=True, node_color='orange', font_size=10, ax=ax)
    #     ax.set_title("Floor Plan Graph")

    def change_adjacencies(self):

        self.adjacency_window = tk.Toplevel(self.root)
        self.adjacency_window.title("Adjacencies")

        gnx = nx.Graph(self.floorplan_graphs[self.curr_rfp])
        labels = {node: room for node, room in zip(
            gnx.nodes, self.input.rooms.values())}

        # Create a list of adjacent node name tuples
        adjacent_nodes = []
        for edge in gnx.edges():
            adjacent_nodes.append((edge[0], edge[1]))

        # Create labels and buttons for each adjacency
        for i, adjacency in enumerate(adjacent_nodes):
            room1 = labels[adjacency[0]]
            room2 = labels[adjacency[1]]
            label = tk.Label(self.adjacency_window, text=f"Adjacency {i + 1}: {room1} - {room2}")
            label.pack()

            remove_button = tk.Button(self.adjacency_window, text="Remove", command=lambda adj=adjacency: self.remove_adjacency(adj, adjacent_nodes))
            remove_button.pack()
        
        submit_button = tk.Button(self.adjacency_window, text="Submit", command=self.submit_action)
        submit_button.pack()
    

    def submit_action(self):
        # Perform the action you want when the Submit button is clicked
        # This function will be called when the "Submit" button is clicked.
        # You can add your desired functionality here.
        print("Submit button clicked")
        self.adjacency_window.destroy()
        # new_adj_list  = []
        # for adj in self.input.adjacencies:
        #     tup = [self.input.rooms[adj[0]],self.input.rooms[adj[1]]]
        #     new_adj_list.append(tup)
        # self.input.adjacencies = new_adj_list

        new_nonadj_list  = []
        for adj in self.input.non_adjacencies:
            tup = [self.input.rooms[adj[0]],self.input.rooms[adj[1]]]
            new_nonadj_list.append(tup)
        self.input.non_adjacencies = new_nonadj_list
        
        self.run_Rect_Button_click()
    
    



    
    

    def remove_adjacency(self, adjacency, adj_nodes):
        # Perform the removal of the adjacency in your graph data structure here
        # You may need to update your graph data structure
        adj_nodes = [t for t in adj_nodes if t!=adjacency]
        adj_nodes = list(adj_nodes)

        new_adj_list  = []
        for adj in adj_nodes:
            tup = [self.input.rooms[adj[0]],self.input.rooms[adj[1]]]
            new_adj_list.append(tup)
        self.input.adjacencies = new_adj_list

        adjacency_list = list(adjacency)
        print("Data type of adjacency:", type(adjacency_list))

        # Assuming self.input.non_adjacencies is a list
        print("Data type of self.input.non_adjacencies:", type(self.input.non_adjacencies))
        print(self.input.non_adjacencies)
        self.input.non_adjacencies.append(adjacency_list)
        # self.run_Rect_Button_click()

        


    def draw_graph(self, ax):
        gnx = nx.Graph(self.floorplan_graphs[self.curr_rfp])

        # create a dictionary of node labels where the keys are the node labels and the values are the room names
        labels = {node: room for node, room in zip(
            gnx.nodes, self.input.rooms.values())}

        # draw the graph with the node labels
        nx.draw_kamada_kawai(gnx, node_size=100, with_labels=True,
                             node_color='orange', font_size=10, labels=labels, ax=ax)

        adjacent_nodes = []
        for edge in gnx.edges():
            adjacent_nodes.append((labels[edge[0]], labels[edge[1]]))
        
        print(adjacent_nodes)
        self.curr_adjacencies = adjacent_nodes


        ax.set_title("Floor Plan Graph")

    # def on_edge_click(self, event, ax, graph_window):
    #     # get the mouse coordinates and the graph layout
    #     x, y = event.xdata, event.ydata
    #     pos = nx.kamada_kawai_layout(self.floorplan_graphs[self.curr_rfp])

    #     # compute the maximum spanning tree of the graph and get its edges in order of increasing weight
    #     mst_edges = list(nx.algorithms.tree.mst.maximum_spanning_edges(self.floorplan_graphs[self.curr_rfp], algorithm='kruskal', data=False))

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
    #     self.floorplan_graphs[self.curr_rfp].remove_edge(*closest_edge)
    #     is_triangulate = traingulated(nx.Graph(self.floorplan_graphs[self.curr_rfp]))
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
        pos = nx.kamada_kawai_layout(self.floorplan_graphs[self.curr_rfp])

        # find the clicked edge, if any
        clicked_edge = None
        min_dist = float('inf')
        for u, v in self.floorplan_graphs[self.curr_rfp].edges():
            # iterate over each edge segment
            for i in range(len(pos[u])-1):
                p1 = np.array([pos[u][i], pos[u][i+1]])
                p2 = np.array([pos[v][i], pos[v][i+1]])

                # calculate the distance from the mouse click to the edge segment
                dist = np.linalg.norm(
                    np.cross(p2-p1, p1-np.array([x, y])))/np.linalg.norm(p2-p1)

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
            # print(get_encoded_matrix(self.graph_objs[self.curr_rfp]["nodecnt"], self.graph_objs[self.curr_rfp]["room_x"],
            #       self.graph_objs[self.curr_rfp]["room_y"], self.graph_objs[self.curr_rfp]["room_width"], self.graph_objs[self.curr_rfp]["room_height"]))
            # print(self.graph_objs[self.curr_rfp]["extranodes"])
            # print(self.graph_objs[self.curr_rfp]["mergednodes"])
            # print(self.dim_params[0])
            # print(self.graph_objs[self.curr_rfp][])
            self.floorplan_graphs[self.curr_rfp].remove_edge(*clicked_edge)
            is_triangulate = traingulated(
                nx.Graph(self.floorplan_graphs[self.curr_rfp]))

            if is_triangulate:

                ax.clear()
                self.draw_graph(ax)
                ax.set_title("Floor Plan Graph (click an edge to remove it)")
                ax.figure.canvas.draw()
                # self.update_floorplan()

                graph_param = []
                graph_param.append([len(self.input.rooms), nx.number_of_edges(
                    self.floorplan_graphs[self.curr_rfp]), self.floorplan_graphs[self.curr_rfp].edges])
                graph = inputgraph.InputGraph(
                    graph_param[0][0], graph_param[0][1], graph_param[0][2], self.coord_list)
                # print(get_encoded_matrix(len(self.input.rooms), graph.room_x,
                #                          graph.room_y, graph.room_width, graph.room_height))
                # print(graph.extranodes)
                # print(graph.mergednodes)
                # print(self.dim_params[0])
                # generates dual for the computed graph and corresponding encoded matrix and rel matrix
                graph.irreg_multiple_dual()
                graph.single_floorplan(self.dim_params[0], self.dim_params[2], self.dim_params[1], self.dim_params[3],
                                       self.dim_params[4], self.dim_params[5], self.dim_params[6], self.dim_params[7], self.dim_params[8])
                # generate floorplan using the computed encoded matrix / rel matrix implementing optimisation techniques on vertical and horizonal st flows
                print("Floorplan exists? ", graph.floorplan_exist)
                if (graph.floorplan_exist):
                    # considering only those graphs for which floorplan exists
                    graph_data = {
                        'room_x': graph.room_x,
                        'room_y': graph.room_y,
                        'room_width': graph.room_width,
                        'room_height': graph.room_height,
                        'area': graph.area,
                        'extranodes': graph.extranodes,
                        'mergednodes': graph.mergednodes,
                        'irreg_nodes': graph.irreg_nodes1,
                        'nodecnt': graph_param[0][0],
                        'edgecnt': graph_param[0][1],
                        'edgeset': graph_param[0][2],
                        'coord': self.coord_list
                    }
                    floorplan_window = tk.Toplevel()
                    floorplan_window.title("New Floorplan")
                    floorplan_window.config(width=300, height=200)
                    self.draw_one_rfp(graph_data)

            else:
                # show an error message if the graph is not triangulated
                ax.set_title(
                    "Floor Plan Graph - Cannot remove edge because graph is not triangulated")
                print("Error: Graph is not triangulated.")
        else:
            # do nothing if the click is on white space
            pass

        ax.figure.canvas.draw()
        # graph_data = self.graph_objs[self.curr_rfp]
        # self.draw_one_rfp(graph_data)

    # def update_floorplan(self):
    #     # create a new empty dictionary to store the updated floorplan information
    #     new_floorplan = {}

    #     # iterate over each room in the original floorplan and create a new graph for it based on the modified graph
    #     for room, graph in self.graph_data.items():
    #         new_graph = nx.Graph()
    #         for u, v in graph.edges():
    #             if self.floorplan_graphs[self.curr_rfp].has_edge(u, v):
    #                 new_graph.add_edge(u, v)
    #         new_floorplan[room] = new_graph

    #     # update the graph_data dictionary with the new floorplan information
    #     self.graph_objs[self.curr_rfp] = new_floorplan

    # def on_edge_click(self, event, ax, graph_window):
    #     # get the mouse coordinates and the graph layout
    #     x, y = event.xdata, event.ydata
    #     pos = nx.kamada_kawai_layout(self.floorplan_graphs[self.curr_rfp])

    #     # find the clicked edge, if any
    #     clicked_edge = None
    #     min_dist = float('inf')
    #     for u, v in self.floorplan_graphs[self.curr_rfp].edges():
    #         # iterate over each edge segment
    #         for i in range(len(pos[u])-1):
    #             p1 = np.array([pos[u][i], pos[u][i+1]])
    #             p2 = np.array([pos[v][i], pos[v][i+1]])

    #             # calculate the distance from the mouse click to the edge segment
    #             dist = np.linalg.norm(
    #                 np.cross(p2-p1, p1-np.array([x, y])))/np.linalg.norm(p2-p1)

    #             if dist < min_dist and dist < 0.05:  # check if the distance is small enough to be considered a click on the edge
    #                 min_dist = dist
    #                 clicked_edge = (u, v)

    #     def traingulated(G):
    #         for cycle in nx.cycle_basis(G):
    #             if len(cycle) >= 4 and not nx.chordal.is_chordal(nx.Graph(G.subgraph(cycle))):
    #                 return False
    #         return True

    #     if clicked_edge is not None:
    #         # remove the clicked edge and redraw the graph
    #         modified_graph = nx.Graph(self.floorplan_graphs[self.curr_rfp])
    #         modified_graph.remove_edge(*clicked_edge)

    #         is_triangulate = traingulated(modified_graph)
    #         if is_triangulate:
    #             # create a new floorplan based on the modified graph
    #             new_floorplan = []
    #             for i, (x, y) in enumerate(pos.values()):
    #                 new_floorplan.append({'id': i, 'x': x, 'y': y})

    #             new_graph_data = {
    #                 'vertices': self.graph_data[self.curr_rfp]['vertices'],
    #                 'edges': [(u, v) for u, v in modified_graph.edges()]
    #             }

    #             self.floorplan_graphs[self.curr_rfp] = modified_graph
    #             self.graph_data[self.curr_rfp] = new_graph_data

    #             # redraw the graph and update the title
    #             ax.clear()
    #             self.draw_graph(ax)
    #             ax.set_title("Floor Plan Graph (click an edge to remove it)")
    #         else:
    #             # show an error message if the graph is not triangulated
    #             ax.set_title(
    #                 "Floor Plan Graph - Cannot remove edge because graph is not triangulated")
    #             print("Error: Graph is not triangulated.")
    #     else:
    #         # do nothing if the click is on white space
    #         pass

    #     ax.figure.canvas.draw()
    #     graph_data = self.graph_objs[self.curr_rfp]
    #     self.draw_one_rfp(graph_data)

    def run_Rect_Button_click(self):
        print("[LOG] Rectangular Floorplans Button Clicked")
        if os.path.exists("CONSTRAINTS_DUMP.pk1"):
            with open("CONSTRAINTS_DUMP.pk1", 'rb') as file:
                # Load the dictionary from the pickle file
                self.curr_map = pickle.load(file)
                
        
        hashvalue = ""
        for room in self.input.rooms.values():
            hashvalue += room
        hashvalue+="exterior"
        for room in self.exterior_rooms:
            hashvalue+=str(room)
        hashvalue+="interior"
        for room in self.interior_rooms:
            hashvalue+=str(room)
        for k in self.input.adjacencies:
            for room in k:
                print(room)
                hashvalue+=str(room)
        
        for k in self.input.non_adjacencies:
            for room in k:
                hashvalue+=str(room)
        print(hashvalue)
        

        
        
        
        self.graph_objs = []
        print(f"Room List is {list(self.input.rooms.values())}")
        print(f"Doors List is {self.input.adjacencies}")
        print(f"Non-Adjacencies List is {self.input.non_adjacencies}")
        print(self.exterior_rooms)
        
        self.create_inputgraph_json()
        
        
        print(self.input.rooms)
        self.interior_rooms.sort()
        print("Exterior rooms: ", self.exterior_rooms,
              "\nInterior rooms: ", self.interior_rooms)

        self.GraphStore(True)

        # coord_list =[]
        if (not (self.arr_altered) and exists(self.filename)):
            print("File exists")

        # check_file = os.path.exists(self.filename)
        # print(check_file)
        # if (check_file):
            with open(self.filename, 'rb') as f:
                list_of_dicts = pickle.load(f)

            graphs = [nx.Graph(graph) for graph in list_of_dicts]

            self.graphs = graphs
            self.coord_list, self.room_mapping, adjacencies_modified, non_adjacencies_modified = gengraphs.generate_graphs(
                self.exterior_rooms, self.interior_rooms, list(self.input.rooms.values()), fileExists=True, rect_floorplans=True, adjacencies=self.input.adjacencies, non_adjacencies=self.input.non_adjacencies)
            self.graphs_param = []
            for G in graphs:
                self.graphs_param.append(
                    [len(self.exterior_rooms)+len(self.interior_rooms), nx.number_of_edges(G), G.edges])

        elif (not (self.arr_altered) and not (exists(self.filename))):
            self.graphs, self.coord_list, self.room_mapping, adjacencies_modified, non_adjacencies_modified, self.graphs_param = gengraphs.generate_graphs(
                self.exterior_rooms, self.interior_rooms, list(self.input.rooms.values()), fileExists=False, rect_floorplans=True, adjacencies=self.input.adjacencies, non_adjacencies=self.input.non_adjacencies)
            graphs = self.graphs
            list_of_dicts = [nx.to_dict_of_dicts(graph) for graph in graphs]

            with open(self.filename, 'wb') as f:
                pickle.dump(list_of_dicts, f)
        else:
            self.graphs, self.coord_list, self.room_mapping, adjacencies_modified, non_adjacencies_modified, self.graphs_param = gengraphs.generate_graphs(
                self.exterior_rooms, self.interior_rooms, list(self.input.rooms.values()), fileExists=False, rect_floorplans=True, adjacencies=self.input.adjacencies, non_adjacencies=self.input.non_adjacencies)
            graphs = self.graphs

        # self.graphs, self.coord_list, self.room_mapping, adjacencies_modified, non_adjacencies_modified, self.graphs_param = gengraphs.generate_graphs(
        #     self.exterior_rooms, self.interior_rooms, list(self.input.rooms.values()), fileExists=False, rect_floorplans=True, adjacencies=self.input.adjacencies, non_adjacencies=self.input.non_adjacencies, )
        # graphs = self.graphs

        self.input.add_rooms_from(self.room_mapping)
        self.input.add_doors_from(adjacencies_modified)
        self.input.add_non_adjacencies_from(non_adjacencies_modified)

        min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = self.default_dim()
        self.dim_params = [min_width, max_width, min_height, max_height,
                           symm_string, min_aspect, max_aspect, plot_width, plot_height]

        if hashvalue in self.curr_map:
            self.graph_objs = self.curr_map[hashvalue][0]
            self.floorplan_graphs = self.curr_map[hashvalue][1]
            my_plot(graphs)
            plt.show()
            self.handle_next_btn()
            return 
        for i in range(len(self.graphs)):
            # representing node count, edge count, edge set, node coordinates as the 4-tuple
            graph = inputgraph.InputGraph(
                self.graphs_param[i][0], self.graphs_param[i][1], self.graphs_param[i][2], self.coord_list)
            # above creates a graph with provided data
            # generates dual for the computed graph and corresponding encoded matrix and rel matrix
            try:
                graph.irreg_multiple_dual()
                graph.single_floorplan(self.dim_params[0], self.dim_params[2], self.dim_params[1], self.dim_params[3],
                                       self.dim_params[4], self.dim_params[5], self.dim_params[6], self.dim_params[7], self.dim_params[8])
                # generate floorplan using the computed encoded matrix / rel matrix implementing optimisation techniques on vertical and horizonal st flows
                print("Floorplan exists? ", graph.floorplan_exist)
                if (graph.floorplan_exist):
                    # considering only those graphs for which floorplan exists
                    graph_data = {
                        'room_x': graph.room_x,
                        'room_y': graph.room_y,
                        'room_width': graph.room_width,
                        'room_height': graph.room_height,
                        'area': graph.area,
                        'extranodes': graph.extranodes,
                        'mergednodes': graph.mergednodes,
                        'irreg_nodes': graph.irreg_nodes1,
                        'nodecnt': self.graphs_param[i][0],
                        'edgecnt': self.graphs_param[i][1],
                        'edgeset': self.graphs_param[i][2],
                        'coord': self.coord_list
                    }
                    
                    self.graph_objs.append(graph_data)
                    self.floorplan_graphs.append(self.graphs[i])
                    break
            except:  # Problem : more than 5 cip is not implemented in multiple bdys
                continue
            #     # nx.draw_kamada_kawai(
            #     #     self.graphs[i], node_size=100, with_labels=True, node_color='orange', font_size=10)
            #     my_plot([self.graphs[i]])
            #     plt.show()
        self.curr_map[hashvalue] = [self.graph_objs,self.floorplan_graphs]
        with open("CONSTRAINTS_DUMP.pk1", 'wb') as file:
            # Pickle the curr_map dictionary and write it to the file
            pickle.dump(self.curr_map, file)
        print("[LOG] Dimensioned selected")

        # print(graphs)
        my_plot(graphs)
        plt.show()
        # nodecnt = len(graphs[0].nodes)
        print("[LOG] Waiting for dimensions input")

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
        print(f"#Floor Plans : {len(self.graph_objs)}")
        self.handle_next_btn()  # to draw curr_rfp+1 th floorplan

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

    def run_Irreg_Button_click(self):
        print("[LOG] Irregular Floorplans Button Clicked")

        self.graph_objs = []
        print(f"Room List is {list(self.input.rooms.values())}")
        print(f"Doors List is {self.input.adjacencies}")
        print(f"Non-Adjacencies List is {self.input.non_adjacencies}")
        self.create_inputgraph_json()
        # graphs = runner(False)
        self.irreg_check = 1
        self.interior_rooms.sort()
        print("Exterior rooms: ", self.exterior_rooms,
              "  Interior rooms: ", self.interior_rooms)

        self.GraphStore(False)

        # coord_list =[]
        if (not (self.arr_altered) and exists(self.filename)):
            print("File exists")

        # check_file = os.path.exists(self.filename)
        # print(check_file)
        # if (check_file):
            with open(self.filename, 'rb') as f:
                list_of_dicts = pickle.load(f)

            graphs = [nx.Graph(graph) for graph in list_of_dicts]

            self.graphs = graphs
            self.coord_list, self.room_mapping, adjacencies_modified, non_adjacencies_modified = gengraphs.generate_graphs(
                self.exterior_rooms, self.interior_rooms, list(self.input.rooms.values()), fileExists=True, rect_floorplans=False, adjacencies=self.input.adjacencies, non_adjacencies=self.input.non_adjacencies)
            self.graphs_param = []
            for G in graphs:
                self.graphs_param.append(
                    [len(self.exterior_rooms)+len(self.interior_rooms), nx.number_of_edges(G), G.edges])

        elif (not (self.arr_altered) and not (exists(self.filename))):
            self.graphs, self.coord_list, self.room_mapping, adjacencies_modified, non_adjacencies_modified, self.graphs_param = gengraphs.generate_graphs(
                self.exterior_rooms, self.interior_rooms, list(self.input.rooms.values()), fileExists=False, rect_floorplans=False, adjacencies=self.input.adjacencies, non_adjacencies=self.input.non_adjacencies)
            graphs = self.graphs
            list_of_dicts = [nx.to_dict_of_dicts(graph) for graph in graphs]

            with open(self.filename, 'wb') as f:
                pickle.dump(list_of_dicts, f)
        else:
            self.graphs, self.coord_list, self.room_mapping, adjacencies_modified, non_adjacencies_modified, self.graphs_param = gengraphs.generate_graphs(
                self.exterior_rooms, self.interior_rooms, list(self.input.rooms.values()), fileExists=False, rect_floorplans=False, adjacencies=self.input.adjacencies, non_adjacencies=self.input.non_adjacencies)
            graphs = self.graphs

        # self.graphs, self.coord_list, self.room_mapping, adjacencies_modified, non_adjacencies_modified, self.graphs_param = gengraphs.generate_graphs(
        #     self.exterior_rooms, self.interior_rooms, list(
        #         self.input.rooms.values()),
        #     fileExists=False, rect_floorplans=False, adjacencies=self.input.adjacencies, non_adjacencies=self.input.non_adjacencies, )
        # graphs = self.graphs

        self.input.add_rooms_from(self.room_mapping)
        self.input.add_doors_from(adjacencies_modified)
        self.input.add_non_adjacencies_from(non_adjacencies_modified)

        min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = self.default_dim()
        self.dim_params = [min_width, max_width, min_height, max_height,
                           symm_string, min_aspect, max_aspect, plot_width, plot_height]

        for i in range(len(self.graphs)):
            # representing node count, edge count, edge set, node coordinates as the 4-tuple
            graph = inputgraph.InputGraph(
                self.graphs_param[i][0], self.graphs_param[i][1], self.graphs_param[i][2], self.coord_list)
            # above creates a graph with provided data
            # below generates dual for the computed graph and corresponding encoded matrix and rel matrix
            # also populates the mergednodes and extranodes information if any is their self attributes.
            graph.irreg_multiple_dual()
            graph.single_floorplan(self.dim_params[0], self.dim_params[2], self.dim_params[1], self.dim_params[3],
                                   self.dim_params[4], self.dim_params[5], self.dim_params[6], self.dim_params[7], self.dim_params[8])
            # generate floorplan using the computed encoded matrix / rel matrix implementing optimisation techniques on vertical and horizonal st flows
            print("\nFloorplan exists" if graph.floorplan_exist ==
                  True else "Floorplan doesn't exists")
            if (graph.floorplan_exist):
                graph_data = {
                    'room_x': graph.room_x,
                    'room_y': graph.room_y,
                    'room_width': graph.room_width,
                    'room_height': graph.room_height,
                    'area': graph.area,
                    'extranodes': graph.extranodes,
                    'mergednodes': graph.mergednodes,
                    'irreg_nodes': graph.irreg_nodes1,
                    'nodecnt': self.graphs_param[i][0],
                    'edgecnt': self.graphs_param[i][1],
                    'edgeset': self.graphs_param[i][2],
                    'coord': self.coord_list
                }
                print(
                    f"Irregular nodes1: {graph.irreg_nodes1}\nMerged Nodes : {graph.mergednodes}\nIrregular nodes2: {graph.irreg_nodes2}")
                self.graph_objs.append(graph_data)
                self.floorplan_graphs.append(self.graphs[i])
                print(f"Possible Floorplan added to list, scanning next graph data.\n")

        # if self.dimCheckVar.get() == 1:
        # print("[LOG] Dimensioned selected")

        # print(graphs)
        my_plot(graphs)
        plt.show()

        # nodecnt = len(graphs[0].nodes)
        # print("[LOG] Now will wait for dimensions input")

        # old_dims = [[0] * nodecnt, [0] * nodecnt, [0] * nodecnt,
        #             [0] * nodecnt, "", [0] * nodecnt, [0] * nodecnt]
        # min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = dimgui.gui_fnc(
        #     old_dims, nodecnt)

        # dim_graphdata = dimensioning_part(graphs, coord_list)
        # print("[LOG] Dimensioned floorplan object\n")
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
        self.graphs, self.coord_list, self.room_mapping, adjacencies_modified, non_adjacencies_modified, self.graphs_param = gengraphs.generate_graphs(
            self.exterior_rooms, self.interior_rooms, list(self.input.rooms.values()), fileExists=False, rect_floorplans=True, adjacencies=self.input.adjacencies, non_adjacencies=self.input.non_adjacencies, )
        graphs = self.graphs
        self.input.add_rooms_from(self.room_mapping)
        self.input.add_doors_from(adjacencies_modified)
        self.input.add_non_adjacencies_from(non_adjacencies_modified)

        min_width, max_width, min_height, max_height, symm_string, min_aspect, max_aspect, plot_width, plot_height = self.default_dim()
        self.dim_params = [min_width, max_width, min_height, max_height,
                           symm_string, min_aspect, max_aspect, plot_width, plot_height]

        for i in range(len(self.graphs)):
            graph = inputgraph.InputGraph(
                self.graphs_param[i][0], self.graphs_param[i][1], self.graphs_param[i][2], self.coord_list)

            Lshaped.LShapedFloorplan(graph, self.coord_list)
            # All rels are in it. Currently we have only 1.
            graph.rel_matrix_list.append(graph.matrix)


            # Since multiple rfp are generated before calling single_floorplan, all the parameters need to be
            # converted list of lists
            # temp_lst = np.array([])
            # np.append(temp_lst,graph.extranodes)
            graph.extranodes = np.array(graph.extranodes, ndmin=2)
            # temp_lst =np.array([])
            # np.append(temp_lst,graph.mergednodes)
            graph.mergednodes = np.array(graph.mergednodes, ndmin=2)
            # temp_lst =np.array([])
            # np.append(temp_lst,graph.irreg_nodes1)
            graph.irreg_nodes1 = np.array(graph.irreg_nodes1, ndmin=2)
            # temp_lst =np.array([])
            # np.append(temp_lst,graph.room_x)
            graph.room_x = np.array(graph.room_x, ndmin=2)
            # temp_lst =np.array([])
            # np.append(temp_lst,graph.room_y)
            graph.room_y = np.array(graph.room_y, ndmin=2)
            # temp_lst =np.array([])
            # np.append(temp_lst,graph.room_width)
            graph.room_width = np.array(graph.room_width, ndmin=2)
            # temp_lst =np.array([])
            # np.append(temp_lst,graph.room_height)
            graph.room_height = np.array(graph.room_height, ndmin=2)

            graph.nodecnt -= 4  # Because Lshaped was counting NESW as well

            graph.single_floorplan(self.dim_params[0], self.dim_params[2], self.dim_params[1], self.dim_params[3],
                                   self.dim_params[4], self.dim_params[5], self.dim_params[6], self.dim_params[7], self.dim_params[8])
            print(graph.floorplan_exist)
            # graph.floorplan_exist = True
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
        #     my_plothra(graphs)
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

    def download_catalogue(self):
        generate_catalogue_dimensioned(len(
            self.graph_objs), self.graph_objs, self.dimensional_constraints, room_name=self.room_list, is_rb=True)

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

        self.input.reset()  # setting rooms, adjacencies and non-adjacencies list to empty
        with open('./one_bhk.json') as one_file:
            # getting default rooms, adjacencies and non-adjacencies
            one_bhk_data = json.load(one_file)

        new_rooms = one_bhk_data['rooms']
        new_adj_list = one_bhk_data['adjacency_constraints']

        self.input.add_rooms_from(room_list=new_rooms)
        self.input.add_doors_from(adjcancy_list=new_adj_list)

        print(self.input.rooms)
        print(self.input.adjacencies)

    def twoBHK_Button_click(self):
        print("[LOG] two BHK Button Clicked")

        self.input.reset()  # setting rooms, adjacencies and non-adjacencies list to empty
        with open('./two_bhk.json') as one_file:
            # getting default rooms, adjacencies and non-adjacencies
            two_bhk_data = json.load(one_file)

        # setting default rooms, adjacencies and non-adjacencies
        new_rooms = two_bhk_data['rooms']
        new_adj_list = two_bhk_data['adjacency_constraints']
        new_non_adj_list = two_bhk_data['non_adjacency_constraints']

        self.input.add_rooms_from(room_list=new_rooms)
        self.input.add_doors_from(adjcancy_list=new_adj_list)
        self.input.add_non_adjacencies_from(
            non_adjacency_list=new_non_adj_list)

        print("self.input.adjacencies : ", self.input.non_adjacencies)

        print("Input rooms: ", self.input.rooms)
        print("Adjacencies: ", self.input.adjacencies)
        print("Non-Adjacencies: ", self.input.non_adjacencies)
        self.bhk = "2bhk"

    def threeBHK_Button_click(self):
        print("[LOG] three BHK Button Clicked")

        self.input.reset()  # setting rooms, adjacencies and non-adjacencies list to empty
        with open('./three_bhk.json') as one_file:
            # getting default rooms, adjacencies and non-adjacencies
            two_bhk_data = json.load(one_file)

        # setting default rooms, adjacencies and non-adjacencies
        new_rooms = two_bhk_data['rooms']
        new_adj_list = two_bhk_data['adjacency_constraints']
        new_non_adj_list = two_bhk_data['non_adjacency_constraints']

        self.input.add_rooms_from(room_list=new_rooms)
        self.input.add_doors_from(adjcancy_list=new_adj_list)
        self.input.add_non_adjacencies_from(
            non_adjacency_list=new_non_adj_list)

        print("Input rooms: ", self.input.rooms)
        print("Adjacencies: ", self.input.adjacencies)
        print("Non-Adjacencies: ", self.input.non_adjacencies)
        self.bhk = "3bhk"

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
        rem_room_list = ["Dining", "Store", "WC 2", "WC 3"]
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
            if (each_room in rem_room_list):
                each_remove_room_btn = tk.Button(
                    frame, text="Remove", command=lambda i=i: self.handle_remove_room_btn(i, self.mod_room_win))
                each_remove_room_btn.grid(row=i+1, column=1, padx=5, pady=5)
                if (each_room != "WC 2" and each_room != "WC 3"):
                    each_intext_room_btn = tk.Button(
                        frame, text="Interior", command=lambda i=i: self.handle_intext_room_btn(i))
                    each_intext_room_btn.grid(
                        row=i+1, column=2, padx=5, pady=5)

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
        self.arr_altered = True
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
        # for each_rule in self.input.adjacencies:
        #     if (self.input.rooms[room_id] in each_rule):
        #         self.input.adjacencies.remove(each_rule)
        # for each_rule in self.input.non_adjacencies:
        #     if (self.input.rooms[room_id] in each_rule):
        #         self.input.non_adjacencies.remove(each_rule)
        i = 0
        while i < len(self.input.adjacencies):
            if (self.input.rooms[room_id] in self.input.adjacencies[i]):
                self.input.adjacencies.remove(self.input.adjacencies[i])
                continue
            i = i+1
        i = 0
        while i < len(self.input.non_adjacencies):
            if (self.input.rooms[room_id] in self.input.non_adjacencies[i]):
                self.input.non_adjacencies.remove(
                    self.input.non_adjacencies[i])
                continue
            i = i+1

        print(f"current adjs is {self.input.adjacencies}")
        print(f"current non-adjs is {self.input.non_adjacencies}")

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
    
    #ROOM MANAGEMENT GUI START
    
    #ROOM MANAGEMENT GUI END 

    def modify_adjacencies_Button_click(self):
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
        self.arr_altered = True
        right = self.new_adj_text_right.get()
        left = self.new_adj_text_left.get()
        # rule_dict = self.input.rooms
        # rev_dict = dict(zip(rule_dict.values(), rule_dict.keys()))
        # self.input.adjacencies.append([rev_dict[left], rev_dict[right]])
        self.input.adjacencies.append([left, right])
        self.recall_adj_constraints_frame(frame)

    def handle_add_new_non_adj_btn(self, frame):
        self.arr_altered = True
        right = self.new_non_adj_text_right.get()
        left = self.new_non_adj_text_left.get()
        # rule_dict = self.input.rooms
        # rev_dict = dict(zip(rule_dict.values(), rule_dict.keys()))
        # self.input.non_adjacencies.append([rev_dict[left], rev_dict[right]])
        self.input.non_adjacencies.append([left, right])
        self.recall_non_adj_constraints_frame(frame)

    def handle_remove_adj_rule_btn(self, frame: tk.Frame, rule):
        self.arr_altered = True
        print(f"rule to remove {rule}")
        self.input.adjacencies.remove(rule)
        print(f"current adjs is {self.input.adjacencies}")
        self.recall_adj_constraints_frame(frame)

    def handle_remove_non_adj_rule_btn(self, frame: tk.Frame, rule):
        self.arr_altered = True
        print(f"rule to remove {rule}")
        self.input.non_adjacencies.remove(rule)
        print(f"current non-adjs is {self.input.non_adjacencies}")
        self.recall_non_adj_constraints_frame(frame)

    def recall_adj_constraints_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        adj_cons_label = tk.Label(frame, text="Adjacencies")
        adj_cons_label.grid(row=0, padx=5, pady=5)

        self.adj_cons_frame_list = []
        print("self.input.adjacencies : ", self.input.adjacencies)

        for i, each_rule in enumerate(self.input.adjacencies):
            each_frame = tk.Frame(frame)
            each_frame.grid(row=i+1)

            if each_rule[0] in self.input.rooms.values() and each_rule[1] in self.input.rooms.values():
                left_label = tk.Label(
                    each_frame, text=each_rule[0])
                left_label.grid(row=i+1, column=0, padx=5, pady=5)

                door_sign = tk.Label(each_frame, text="<=>")
                door_sign.grid(row=i+1, column=1, padx=5, pady=5)

                right_label = tk.Label(
                    each_frame, text=each_rule[1])
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

            if each_rule[0] in self.input.rooms.values() and each_rule[1] in self.input.rooms.values():
                left_label = tk.Label(
                    each_frame, text=each_rule[0])
                left_label.grid(row=i+1, column=0, padx=5, pady=5)

                door_sign = tk.Label(each_frame, text="<=>")
                door_sign.grid(row=i+1, column=1, padx=5, pady=5)

                right_label = tk.Label(
                    each_frame, text=each_rule[1])
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
