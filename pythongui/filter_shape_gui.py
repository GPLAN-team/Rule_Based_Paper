import tkinter as tk
from tkinter import font
from tkinter import messagebox


class ST_GUI:
    def __init__(self, choices) -> None:
        self.output = 'N'
        self.choices = choices
        self.choices.append('N')

    def handle_st_gui(self):
        
        root = tk.Toplevel()
        self.root = root

        root.title('Filters')
        root.geometry(str(1200) + 'x' + str(700))

        head = tk.Label(root, text='Choose a room shape')
        head.grid()

        option_lists = {"L": "L-shaped", "T": "T-shaped", "C": "C-shaped", "F": "F-shaped", "S": "Stair shaped", "N": "No Preference"}

        self.shape_chosen = tk.IntVar()
        idx = 0
        for choice in self.choices:
            btn = tk.Radiobutton(root, text=option_lists[choice], variable=self.shape_chosen, value=idx)
            btn.grid()
            idx += 1

        submit_btn = tk.Button(root, text="Submit", command=self.handle_submit_btn)
        submit_btn.grid()

        root.wait_window(root)
        return self.output


    def handle_submit_btn(self):
        self.output = self.choices[self.shape_chosen.get()]
        self.root.destroy()







def filter_shape(choices):
    
    gui_class = ST_GUI(choices)
    return gui_class.handle_st_gui()



if __name__ == "__main__":
    ch = ['L', 'C', 'T']
    print(filter_shape(ch))