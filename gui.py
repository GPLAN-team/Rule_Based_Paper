from os import add_dll_directory
import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
from input import Input
import json

helv36 = ("Helvetica", 15, "bold")


#
# class Room:
#     def __init__(self) -> None:
#


class App:
    def __init__(self) -> None:
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
        self.input = Input()

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
        logo_canvas.create_text(50, 50, text="GPLAN", font=helv36)

    def custom_rfp_section(self):
        self.custom_rfp_choice_frame = tk.Frame(self.root)
        self.custom_rfp_choice_frame.grid(row=0, column=1, padx=10, pady=10)
        self.oneBHK_Button = tk.Button(self.custom_rfp_choice_frame, text="1 BHK", font=helv36,
                                       command=self.oneBHK_Button_click)
        self.oneBHK_Button.grid(row=0, column=0, padx=10, pady=10)
        self.twoBHK_Button = tk.Button(self.custom_rfp_choice_frame, text="2 BHK", font=helv36,
                                       command=self.twoBHK_Button_click)
        self.twoBHK_Button.grid(row=0, column=1, padx=10, pady=10)
        self.threeBHK_Button = tk.Button(self.custom_rfp_choice_frame, text="3 BHK", font=helv36,
                                         command=self.threeBHK_Button_click)
        self.threeBHK_Button.grid(row=0, column=2, padx=10, pady=10)
        self.reset_Button = tk.Button(self.custom_rfp_choice_frame, text="Reset", font=helv36,
                                          command=self.reset_Button_click)
        self.reset_Button.grid(row=0, column=3, padx=10, pady=10)

    def properties_section(self):
        pass

    def modification_section(self):
        self.modify_frame = tk.Frame(self.root)
        self.modify_frame.grid(row=1, column=0, padx=10, pady=10)

        self.modify_rooms_button = tk.Button(self.modify_frame, text="Modify Rooms", font=helv36,
                                             command=self.modify_rooms_Button_click)
        self.modify_rooms_button.grid(row=2, column=0, padx=10, pady=10)

        self.modify_rules_button = tk.Button(self.modify_frame, text="Modify Rules", font=helv36,
                                             command=self.modify_rules_Button_click)
        self.modify_rules_button.grid(row=3, column=0, padx=10, pady=10)

    def rfp_draw_section(self):
        self.rfp_draw_frame = tk.Frame(self.root)
        self.rfp_draw_frame.grid(row=1, column=1, padx=10, pady=10, rowspan=10, columnspan=10)

        self.rfp_canvas = tk.Canvas(self.rfp_draw_frame, background="#FFFFFF", width=1000, height=800)
        self.rfp_canvas.grid(row=0, column=0, rowspan=10, columnspan=10)

    def oneBHK_Button_click(self):
        print("[LOG] One BHK Button Clicked")

        
        self.input.reset()
        with open('./one_bhk.json') as one_file:
            one_bhk_data = json.load(one_file)

        new_rooms = one_bhk_data['rooms']
        new_adj_list = one_bhk_data['adjacency_constraints']


        self.input.add_rooms_from(room_list = new_rooms)
        self.input.add_rules_from(adjcancy_list = new_adj_list)

        print(self.input.rooms)
        print(self.input.adjacencies)




    def twoBHK_Button_click(self):
        print("[LOG] two BHK Button Clicked")

        self.input.reset()
        with open('./two_bhk.json') as one_file:
            one_bhk_data = json.load(one_file)

        new_rooms = one_bhk_data['rooms']
        new_adj_list = one_bhk_data['adjacency_constraints']


        self.input.add_rooms_from(room_list = new_rooms)
        self.input.add_rules_from(adjcancy_list = new_adj_list)

        print(self.input.rooms)
        print(self.input.adjacencies)

    def threeBHK_Button_click(self):
        print("[LOG] three BHK Button Clicked")

        self.input.reset()
        with open('./three_bhk.json') as one_file:
            one_bhk_data = json.load(one_file)

        new_rooms = one_bhk_data['rooms']
        new_adj_list = one_bhk_data['adjacency_constraints']


        self.input.add_rooms_from(room_list = new_rooms)
        self.input.add_rules_from(adjcancy_list = new_adj_list)

        print(self.input.rooms)
        print(self.input.adjacencies)

    def reset_Button_click(self):
        print("[LOG] Reset Button Clicked")
        self.input.reset()


    def recall_room_list_frame(self, frame):
        
        head = tk.Label(frame, text="Room List")
        head.grid(row=0,column=0, padx=5, pady=5)

        self.room_label_list = []
        self.remove_room_btn_list = []

        for i, each_room in self.input.rooms.items():
            print(each_room)
            each_room_label = tk.Label(frame, text=each_room)
            each_room_label.grid(row=i+1, column=0, padx=5, pady=5)
            self.room_label_list.append(each_room_label)


            each_remove_room_btn = tk.Button(frame, text="Remove",command= lambda i=i: self.handle_remove_room_btn(i))
            each_remove_room_btn.grid(row=i+1, column=1, padx=5, pady=5)

            self.remove_room_btn_list.append(each_remove_room_btn)


    def modify_rooms_Button_click(self):
        print("[LOG] Modify Rooms Button Clicked")

        room_win = tk.Toplevel(self.root)


        room_win.title("Room Modifier")
        room_win.geometry(str(1000) + 'x' + str(400))

        

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
        print(f"current room list = {self.input.rooms}")

    def modify_rules_Button_click(self):
        print("[LOG] Modify Rules Button Clicked")
        
        rules_win = tk.Toplevel(self.root)
        
        rules_win.title("Rules Modifier")
        rules_win.geometry(str(1000) + 'x' + str(400))


        adj_frame = tk.Frame(rules_win)
        adj_frame.grid(row=0)

        self.recall_adj_constraints_frame(adj_frame)

        add_new_adj_frame = tk.Frame(rules_win)
        add_new_adj_frame.grid(row=1)





        new_adj_text = tk.Text(add_new_adj_frame, height=1, width=8)
        new_adj_text.grid(row=0, column=0, padx=5, pady=5)

        add_new_adj_btn = tk.Button(add_new_adj_frame, text="Add adj", command = lambda i = new_adj_text: self.handle_add_new_adj_btn(i,prev_adj_list_frame))
        add_new_adj_btn.grid(row=0, column=1)




        rules_win.wait_variable()



    def recall_adj_constraints_frame(self, frame):
        adj_cons_label = tk.Label(frame, text=" Door Connections")
        adj_cons_label.grid(row=0, padx=5, pady=5)

        self.adj_cons_frame_list = []

        for i, each_rule in enumerate(self.input.adjacencies):
            each_frame = tk.Frame(frame)
            each_frame.grid(row=i+1)

            if each_rule[0] in self.input.rooms.keys() and each_rule[1] in self.input.rooms.keys():
                left_label = tk.Label(each_frame,text=self.input.rooms[each_rule[0]])
                left_label.grid(row = 0, column=0, padx=5, pady=5)

                door_sign = tk.Label(each_frame, text="<=>")
                door_sign.grid(row = 0,column=1, padx=5, pady=5)

                right_label = tk.Label(each_frame, text=self.input.rooms[each_rule[1]])
                right_label.grid(row = 0,column=2, padx=5, pady=5)

            else:
                self.input.adjacencies.remove(each_rule)

             









    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
