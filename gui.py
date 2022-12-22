import tkinter as tk
from FastPLAN import FastPLAN
from input import Input
import json
from FastPLAN.FastPLAN import runner
from FastPLAN.FastPLAN import my_plot
import matplotlib.pyplot as plt
from api import multigraph_to_rfp, dimensioning_part

import Temp_Code.gengraphs as gengraphs

helv15 = ("Helvetica", 15, "bold")
helv8 = ("Helvetica", 8, "bold")

INPUTGRAPH_JSON_PATH = ("./FastPLAN/inputgraph.json")

rgb_colors = [ 	
    (123,104,238), #medium slate blue	
    (64,224,208), #turqouise
    (255,127,80), #coral
    (255,105,180), #hot pink	
    (230,230,250), #lavender
    (250,128,114), #salmon
    (152,251,152), #pale green
    (186,85,211), #medium orchid
    (176,196,222), #light steel blue
    (255,165,0), #orange
    (255,218,185), #peach puff
    (100,149,237), #corn flower blue
    ]*10

hex_colors = [
    "#7B68EE", #medium slate blue	
    "#40E0D0", #turqouise
    "#FF7F50", #coral
    "#FF69B4", #hot pink	
    "#E6E6FA", #lavender
    "#FA8072", #salmon
    "#98FB98", #pale green
    "#BA55D3", #medium orchid
    "#B0C4DE", #light steel blue
    "#FFA500", #orange
    "#FFDAB9", #peach puff
    "#6495ED", #corn flower blue
]*10

class App:
    def __init__(self) -> None:
        self.input = Input()
        self.initialise_root()
        self.add_logo()
        self.custom_rfp_section()
        self.properties_section()
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

    def initialise_root(self):
        self.root = tk.Tk()
        self.root.title("Rule Based GPLAN")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(str(str(self.screen_width) + 'x' + str(self.screen_height)))

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
        
        self.dimCheckVar = tk.IntVar()
        
        self.dim_Button = tk.Checkbutton(self.custom_rfp_choice_frame, text="Dimensioned", font=helv15,
                                          command=self.dimensioned_checkbox_click, variable=self.dimCheckVar, onvalue=1, offvalue=0)

        self.dim_Button.grid(row=0, column=4, padx=10, pady=10)

    def properties_section(self):
        self.properties_frame = tk.Frame(self.root)
        self.properties_frame.grid(row=1, column=11, padx=10, pady=10)

        self.colors_table_frame = tk.Frame(self.properties_frame)
        self.colors_table_frame.grid()
        self.colors_table_canvas = tk.Canvas(self.colors_table_frame, width = 300, height = 500)
        self.colors_table_canvas.grid()

        self.update_colors_table()

    def modification_section(self):
        self.modify_frame = tk.Frame(self.root)
        self.modify_frame.grid(row=1, column=0, padx=10, pady=10)

        self.modify_rooms_button = tk.Button(self.modify_frame, text="Modify Rooms", font=helv15,
                                             command=self.modify_rooms_Button_click)
        self.modify_rooms_button.grid(row=2, column=0, padx=10, pady=10)

        self.modify_doors_button = tk.Button(self.modify_frame, text="Modify Doors", font=helv15,
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
        
        self.prev_btn = tk.Button(self.modify_frame, text= "Previous", font=helv15, command= self.handle_prev_btn)
        self.prev_btn.grid(row=7, column=0, padx=10, pady=10)
        
        self.next_btn = tk.Button(self.modify_frame, text= "Next", font=helv15, command= self.handle_next_btn)
        self.next_btn.grid(row=8, column=0, padx=10, pady=10)
        
        self.exit_btn = tk.Button(self.modify_frame, text= "Exit", font=helv15, command= self.handle_exit_btn)
        self.exit_btn.grid(row=9, column=0, padx=11, pady=10)

    def rfp_draw_section(self):
        self.rfp_draw_frame = tk.Frame(self.root)
        self.rfp_draw_frame.grid(row=1, column=1, padx=10, pady=10, rowspan=10, columnspan=10)

        self.rfp_canvas = tk.Canvas(self.rfp_draw_frame, background="#FFFFFF", width=800, height=800)
        self.rfp_canvas.grid(row=0, column=0, rowspan=10, columnspan=10)

    def handle_prev_btn(self):
        self.curr_rfp -= 1
        if self.curr_rfp == 0:
            tk.messagebox.showwarning("The Start", "Please try new options")
            return

        self.draw_one_rfp(self.output_rfps[self.curr_rfp])

    def handle_next_btn(self):
        if self.curr_rfp == len(self.output_rfps) - 1:
            tk.messagebox.showwarning("The End", "You have exhausted all the options")
            return

        self.curr_rfp += 1

        self.draw_one_rfp(self.output_rfps[self.curr_rfp])
        
    def handle_exit_btn(self):
        self.root.destroy()

    def update_colors_table(self):

        self.colors_table_canvas.delete("all")
        for i, each_room in enumerate(self.input.rooms.values()):
            self.colors_table_canvas.create_rectangle(100, 100 + i*30, 120, 120 + i*30 , fill=self.colors_map[each_room])
            self.colors_table_canvas.create_text(200, 105 + i*30, text=each_room)
            
    def draw_one_rfp(self, rfp, origin = (200, 200), scale = 1):
        x, y = origin
        self.rfp_canvas.delete("all")

        
        for each_room in rfp:
            print(f"each room {each_room}")
            self.colors_map[self.input.rooms[each_room['label']]] = hex_colors[each_room['label']]
            self.rfp_canvas.create_rectangle(x + scale* each_room['left'], y + scale * each_room['top'], x +  scale * (each_room['left'] + each_room['width']) , y + scale * (each_room['top'] + each_room['height']), fill=hex_colors[each_room['label']])
            # self.rfp_canvas.create_text( x + scale*(each_room['left'] + each_room['width']/2), y + scale * (each_room['top'] + each_room['height']/2), text=self.input.rooms[each_room['label']], font= helv8)

        self.update_colors_table()
        

    def run_Rect_Button_click(self):
        print("[LOG] Rectangular Floorplans Button Clicked")

        print(f"Room List is {list(self.input.rooms.values())}")
        print(f"Doors List is {self.input.adjacencies}")
        print(f"Non-Adjacencies List is {self.input.non_adjacencies}")
        self.create_inputgraph_json()
        # graphs = runner(False)
        self.interior_rooms.sort()
        print("Exterior rooms: ", self.exterior_rooms, "  Interior rooms: ", self.interior_rooms)
        graphs, coord_list, room_mapping = gengraphs.generate_graphs(self.exterior_rooms, self.interior_rooms, rect_floorplans=True, adjacencies=self.input.adjacencies, non_adjacencies=self.input.non_adjacencies)
        
        self.input.add_rooms_from(room_mapping)
        
        if self.dimCheckVar.get() == 1:
            print("[LOG] Dimensioned selected")
            
            # print(graphs)
            my_plot(graphs)
            plt.show()
            
            print("[LOG] Now will wait for dimensions input")
            
            dim_floorplans =  dimensioning_part(graphs, coord_list)
            print("[LOG] Dimensioned floorplan object\n")
            print(dim_floorplans)

            print(f"{len(graphs)} output_graphs = {str(graphs)}")
            
            # self.draw_one_rfp(dim_floorplans)

            # output_rfps = multigraph_to_rfp(graphs, rectangular=True)
            # print(f"number of rfps = {len(output_rfps)}")
            # self.output_rfps = output_rfps

            # self.output_found = True
            # self.curr_rfp = -1

            # print(f"{len(output_rfps)} output rfps = {str(output_rfps)}")

            # print(f"one rfp = {output_rfps[0]}")

            # self.handle_next_btn()
            
        else:    
            # print(graphs)
            my_plot(graphs)
            plt.show()

            print(f"{len(graphs)} output_graphs = {str(graphs)}")

            output_rfps = multigraph_to_rfp(graphs, rectangular=True)
            print(f"number of rfps = {len(output_rfps)}")
            self.output_rfps = output_rfps

            self.output_found = True
            self.curr_rfp = -1

            print(f"{len(output_rfps)} output rfps = {str(output_rfps)}")

            print(f"one rfp = {output_rfps[0]}")

            self.handle_next_btn()
            
    def run_Irreg_Button_click(self):
        print("[LOG] Irregular Floorplans Button Clicked")

        print(f"Room List is {list(self.input.rooms.values())}")
        print(f"Doors List is {self.input.adjacencies}")
        self.create_inputgraph_json()
        # graphs = runner(False)
        self.interior_rooms.sort()
        print("Exterior rooms: ", self.exterior_rooms, "  Interior rooms: ", self.interior_rooms)
        graphs, coord_list, room_mapping = gengraphs.generate_graphs(self.exterior_rooms, self.interior_rooms, rect_floorplans=False, adjacencies=self.input.adjacencies, non_adjacencies=self.input.non_adjacencies)
        
        self.input.add_rooms_from(room_mapping)
        
        if self.dimCheckVar.get() == 1:
            print("[LOG] Dimensioned selected")
            
            # print(graphs)
            my_plot(graphs)
            plt.show()
            
            print("[LOG] Now will wait for dimensions input")
            
            dim_floorplans =  dimensioning_part(graphs, coord_list)
            print("[LOG] Dimensioned floorplan object\n")
            print(dim_floorplans)

            print(f"{len(graphs)} output_graphs = {str(graphs)}")
            
            # self.draw_one_rfp(dim_floorplans)

            # output_rfps = multigraph_to_rfp(graphs, rectangular=False)
            # print(f"number of rfps = {len(output_rfps)}")
            # self.output_rfps = output_rfps

            # self.output_found = True
            # self.curr_rfp = -1

            # print(f"{len(output_rfps)} output rfps = {str(output_rfps)}")

            # print(f"one rfp = {output_rfps[0]}")

            # self.handle_next_btn()
            
        else:    
            # print(graphs)
            my_plot(graphs)
            plt.show()

            print(f"{len(graphs)} output_graphs = {str(graphs)}")

            output_rfps = multigraph_to_rfp(graphs, rectangular=False)
            print(f"number of irfps = {len(output_rfps)}")
            self.output_rfps = output_rfps

            self.output_found = True
            self.curr_rfp = -1

            print(f"{len(output_rfps)} output irfps = {str(output_rfps)}")

            print(f"one irfp = {output_rfps[0]}")

            self.handle_next_btn()

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


        self.input.add_rooms_from(room_list = new_rooms)
        self.input.add_doors_from(adjcancy_list = new_adj_list)

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
        

        self.input.add_rooms_from(room_list = new_rooms)
        self.input.add_doors_from(adjcancy_list = new_adj_list)
        self.input.add_non_adjacencies_from(non_adjacency_list= new_non_adj_list)

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

        self.input.add_rooms_from(room_list = new_rooms)
        self.input.add_doors_from(adjcancy_list = new_adj_list)
        
        print(self.input.rooms)
        print(self.input.adjacencies)

    def reset_Button_click(self):
        print("[LOG] Reset Button Clicked")
        self.input.reset()
        
    def dimensioned_checkbox_click(self):
        check = "Checked" if self.dimCheckVar.get() == 1 else "Unchecked"
        print("[LOG] Dimensioned checkbox ", check)

    def recall_room_list_frame(self, frame):
        
        head = tk.Label(frame, text="Room List")
        head.grid(row=0,column=0, padx=5, pady=5)

        self.room_label_list = []
        self.remove_room_btn_list = []
        self.interior_rooms = []
        self.exterior_rooms = []
        self.interior_rooms_btn_list = []
        for i, each_room in self.input.rooms.items():
            print(each_room)
            self.exterior_rooms.append(i)
            print(self.exterior_rooms)
            print("\n")
            each_room_label = tk.Label(frame, text=each_room)
            each_room_label.grid(row=i+1, column=0, padx=5, pady=5)
            self.room_label_list.append(each_room_label)


            each_remove_room_btn = tk.Button(frame, text="Remove",command= lambda i=i: self.handle_remove_room_btn(i))
            each_remove_room_btn.grid(row=i+1, column=1, padx=5, pady=5)
            
            each_intext_room_btn = tk.Button(
                frame, text="Interior", command=lambda i=i: self.handle_intext_room_btn(i))
            each_intext_room_btn.grid(row=i+1, column=2, padx=5, pady=5)

            self.interior_rooms_btn_list.append(each_intext_room_btn)
            
            self.remove_room_btn_list.append(each_remove_room_btn)

    def modify_rooms_Button_click(self):
        print("[LOG] Modify Rooms Button Clicked")

        room_win = tk.Toplevel(self.root)


        room_win.title("Room Modifier")
        # room_win.geometry(str(1000) + 'x' + str(400))
        prev_room_list_frame = tk.Frame(room_win)

        prev_room_list_frame.grid()

        self.recall_room_list_frame(prev_room_list_frame)

        new_room_frame = tk.Frame(room_win)
        new_room_frame.grid(row=1, column=0)

        new_room_text = tk.Text(new_room_frame, height=1, width=8)
        new_room_text.grid(row=0, column=0, padx=5, pady=5)

        add_new_room_btn = tk.Button(new_room_frame, text="Add Room", command = lambda i = new_room_text: self.handle_add_new_room_btn(i,prev_room_list_frame))
        add_new_room_btn.grid(row=0, column=1)

        room_win.wait_window()

    def handle_add_new_room_btn(self, new_room, prev_room_list_frame):
        idx = len(self.input.rooms)
        self.input.rooms[idx] = new_room.get("1.0","end")

        self.recall_room_list_frame(prev_room_list_frame)

    def handle_remove_room_btn(self,room_id):
        print(f"room to remove is {room_id}")
        self.input.rooms.pop(room_id)
        self.room_label_list[room_id].destroy()
        self.remove_room_btn_list[room_id].destroy()
        self.interior_rooms_btn_list[room_id].destroy()
        print(f"current room list = {self.input.rooms}")
        
    def handle_intext_room_btn(self, room_id):
        # print(f"room is {room_id}")
        self.exterior_rooms.remove(room_id)
        self.interior_rooms.append(room_id)
        self.interior_rooms_btn_list[room_id].configure(
            highlightbackground='blue')
        print(self.exterior_rooms)
        # print(f"current room list = {self.input.rooms}")

    def modify_doors_Button_click(self):
        print("[LOG] Modify Doors Button Clicked")
        
        doors_win = tk.Toplevel(self.root)
        
        doors_win.title("Doors Modifier")
        # doors_win.geometry(str(1000) + 'x' + str(400))


        adj_frame = tk.Frame(doors_win)
        adj_frame.grid(row=0)

        self.recall_adj_constraints_frame(adj_frame)

        add_new_adj_frame = tk.Frame(doors_win)
        add_new_adj_frame.grid(row=1)

        cur_new_adj_frame_row = 0

        add_new_adj_label = tk.Label(add_new_adj_frame, text="Add New Door") 
        add_new_adj_label.grid(row=cur_new_adj_frame_row, columnspan=5)

        self.new_adj_text_left = tk.StringVar()
        self.new_adj_text_right = tk.StringVar()

        cur_new_adj_frame_row += 1

        new_adj_option_left = tk.OptionMenu(add_new_adj_frame, self.new_adj_text_left, *list(self.input.rooms.values()))
        new_adj_option_left.grid(row=cur_new_adj_frame_row,column=0, padx=5, pady=5)

        new_adj_door_sign = tk.Label(add_new_adj_frame, text="<=>")
        new_adj_door_sign.grid(row=cur_new_adj_frame_row,column=1, padx=5, pady=5)
        
        new_adj_option_right = tk.OptionMenu(add_new_adj_frame, self.new_adj_text_right, *list(self.input.rooms.values()))
        new_adj_option_right.grid(row=cur_new_adj_frame_row,column=2, padx=5, pady=5)

        add_new_adj_btn = tk.Button(add_new_adj_frame, text="Add Rule", command = lambda : self.handle_add_new_adj_btn(adj_frame))
        add_new_adj_btn.grid(row=cur_new_adj_frame_row, column=3, padx=5, pady=5)

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

        add_new_non_adj_label = tk.Label(add_new_non_adj_frame, text="Add New Non-Adjacencies") 
        add_new_non_adj_label.grid(row=cur_new_non_adj_frame_row, columnspan=5)

        self.new_non_adj_text_left = tk.StringVar()
        self.new_non_adj_text_right = tk.StringVar()

        cur_new_non_adj_frame_row += 1

        new_non_adj_option_left = tk.OptionMenu(add_new_non_adj_frame, self.new_non_adj_text_left, *list(self.input.rooms.values()))
        new_non_adj_option_left.grid(row=cur_new_non_adj_frame_row,column=0, padx=5, pady=5)

        new_non_adj_door_sign = tk.Label(add_new_non_adj_frame, text="<=>")
        new_non_adj_door_sign.grid(row=cur_new_non_adj_frame_row,column=1, padx=5, pady=5)
        
        new_non_adj_option_right = tk.OptionMenu(add_new_non_adj_frame, self.new_non_adj_text_right, *list(self.input.rooms.values()))
        new_non_adj_option_right.grid(row=cur_new_non_adj_frame_row,column=2, padx=5, pady=5)

        add_new_non_adj_btn = tk.Button(add_new_non_adj_frame, text="Add Rule", command = lambda : self.handle_add_new_non_adj_btn(non_adj_frame))
        add_new_non_adj_btn.grid(row=cur_new_non_adj_frame_row, column=3, padx=5, pady=5)

        doors_win.wait_variable()


    def handle_add_new_adj_btn(self,frame):
        right = self.new_adj_text_right.get()
        left = self.new_adj_text_left.get()
        rule_dict = self.input.rooms
        rev_dict = dict(zip(rule_dict.values(), rule_dict.keys()))
        self.input.adjacencies.append([rev_dict[left], rev_dict[right]])
        self.recall_adj_constraints_frame(frame)
        
    def handle_add_new_non_adj_btn(self,frame):
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
        adj_cons_label = tk.Label(frame, text="Door Connections")
        adj_cons_label.grid(row=0, padx=5, pady=5)

        self.adj_cons_frame_list = []

        for i, each_rule in enumerate(self.input.adjacencies):
            each_frame = tk.Frame(frame)
            each_frame.grid(row=i+1)

            if each_rule[0] in self.input.rooms.keys() and each_rule[1] in self.input.rooms.keys():
                left_label = tk.Label(each_frame,text=self.input.rooms[each_rule[0]])
                left_label.grid(row = i+1, column=0, padx=5, pady=5)

                door_sign = tk.Label(each_frame, text="<=>")
                door_sign.grid(row = i+1,column=1, padx=5, pady=5)

                right_label = tk.Label(each_frame, text=self.input.rooms[each_rule[1]])
                right_label.grid(row = i+1,column=2, padx=5, pady=5)

                remove_adj_btn = tk.Button(each_frame, text="Remove Rule", command= lambda lframe = frame, lrule = each_rule: self.handle_remove_adj_rule_btn(lframe, lrule))
                remove_adj_btn.grid(row = i+1,column=3, padx=5, pady=5)

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
                left_label = tk.Label(each_frame,text=self.input.rooms[each_rule[0]])
                left_label.grid(row = i+1, column=0, padx=5, pady=5)

                door_sign = tk.Label(each_frame, text="<=>")
                door_sign.grid(row = i+1,column=1, padx=5, pady=5)

                right_label = tk.Label(each_frame, text=self.input.rooms[each_rule[1]])
                right_label.grid(row = i+1,column=2, padx=5, pady=5)

                remove_non_adj_btn = tk.Button(each_frame, text="Remove Rule", command= lambda lframe = frame, lrule = each_rule: self.handle_remove_non_adj_rule_btn(lframe, lrule))
                remove_non_adj_btn.grid(row = i+1,column=3, padx=5, pady=5)

            else:
                self.input.non_adjacencies.remove(each_rule)
             
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
