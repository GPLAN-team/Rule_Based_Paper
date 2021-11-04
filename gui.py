import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image

helv36 = ("Helvetica", 15, "bold")


#
# class Room:
#     def __init__(self) -> None:
#


class App:
    New_win = 0

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
        self.customBHK_Button = tk.Button(self.custom_rfp_choice_frame, text="Custom", font=helv36,
                                          command=self.customBHK_Button_click)
        self.customBHK_Button.grid(row=0, column=3, padx=10, pady=10)

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

    def twoBHK_Button_click(self):
        print("[LOG] two BHK Button Clicked")

    def threeBHK_Button_click(self):
        print("[LOG] three BHK Button Clicked")

    def customBHK_Button_click(self):
        print("[LOG] custom BHK Button Clicked")

    def modify_rooms_Button_click(self):
        print("[LOG] Modify Rooms Button Clicked")
        if self.New_win == 0:
            self.openNewWindow()
            self.New_win = 1

    def modify_rules_Button_click(self):
        print("[LOG] Modify Rules Button Clicked")

    def run(self):
        self.root.mainloop()

    def openNewWindow(self):
        self.newWindow = tk.Toplevel(self.root)
        self.newWindow.title("Choose Rooms:")
        self.newWindow.geometry(str(400) + 'x' + str(400))
        Room_names = ['Living room', 'Master room', 'Kitchen ', 'Bathroom', 'Dining room', 'Child room', 'Study room',
                      'Second room', 'Guest room', 'Balcony', 'Entrance', 'Storage']
        # mp = {}
        for i in range(0, 12):
            self.room_checkobj.append(tk.IntVar())
            self.room_freq.append(tk.IntVar())
            # mp[self.room_checkobj[i]] = i
        checkList = []

        for i in range(0, 12):
            label = tk.Label(self.newWindow, text=Room_names[i])
            label.grid(row=i, column=0)
            self.freqbox.append(tk.Entry(self.newWindow, textvariable=self.room_freq[i]))
            self.freqbox[i].grid(row=i, column=2)
            checkList.append(tk.Checkbutton(self.newWindow, variable=self.room_checkobj[i], onvalue=1, offvalue=0))
            checkList[i].grid(row=i, column=1)

        button = tk.Button(self.newWindow, text='Submit', padx=5, command=lambda: self.Submit_clicked())  # Submit_clicked to be implemented
        button.grid()
        self.newWindow.wait_window(self.newWindow)

        # self.newWindow.protocol("WM_DELETE_WINDOW", self.Val1)

    def Val1(self):
        self.New_win = 0
        self.newWindow.destroy()

if __name__ == "__main__":
    app = App()
    app.run()
