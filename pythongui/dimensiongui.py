import tkinter as tk
from tkinter import font
from tkinter import messagebox


def gui_fnc(old_dims, nodes, room_mapping):
    min_width = []
    max_width = []
    min_height = []
    max_height = []
    min_aspect = []
    max_aspect = []
    symmetric_text = []

    root = tk.Toplevel()

    root.title('Dimensional Input')
    root.geometry(str(1200) + 'x' + str(700))
    Upper_right = tk.Label(root, text="Enter dimensional constraints for each room", font=("Times New Roman", 12))

    Upper_right.place(relx=0.60, rely=0.1, anchor='ne')

    text_head_width = []
    text_head_width1 = []
    text_head_area = []
    text_head_area1 = []
    text_room = []
    text_min_aspect_ratio = []
    text_max_aspect_ratio = []
    value_width = []
    value_width1 = []
    value_area = []
    value_area1 = []
    value_min_aspect_ratio = []
    value_max_aspect_ratio = []
    w = []
    w1 = []
    minA = []
    maxA = []
    min_ar = []
    max_ar = []

    sym_var = (tk.StringVar(value=old_dims[4]))
    plot_height = tk.IntVar(root, 0)
    plot_height.set(-1)
    plot_width = tk.IntVar(root, 0)
    plot_width.set(-1)
    #!!! does this setting work everytime???

    for i in range(0, nodes):
        i_value_x = 0
        i_value_y = i
        w.append(tk.IntVar(value=old_dims[0][i]))
        w1.append(tk.IntVar(value=old_dims[1][i]))
        minA.append(tk.IntVar(value=old_dims[2][i]))
        maxA.append(tk.IntVar(value=old_dims[3][i]))
        min_ar.append(tk.DoubleVar(value=old_dims[5][i]))
        max_ar.append(tk.DoubleVar(value=old_dims[6][i]))

        if (i_value_y == 0):
            text_head_width.append("text_head_width_" + str(i_value_x + 1))
            text_head_width[i_value_x] = tk.Label(root, text="Actual Width")
            text_head_width[i_value_x].place(relx=0.30 + 0.20 * i_value_x, rely=0.2, anchor='ne')
            
            text_head_width1.append("text_head_width1_" + str(i_value_x + 1))
            text_head_width1[i_value_x] = tk.Label(root, text="Max Width")
            text_head_width1[i_value_x].place(relx=0.40 + 0.20 * i_value_x, rely=0.2, anchor='ne')
            
            text_head_area.append("text_head_area_" + str(i_value_x + 1))
            text_head_area[i_value_x] = tk.Label(root, text="Actual Height")
            text_head_area[i_value_x].place(relx=0.50 + 0.20 * i_value_x, rely=0.2, anchor='ne')
            
            text_head_area1.append("text_head_area1_" + str(i_value_x + 1))
            text_head_area1[i_value_x] = tk.Label(root, text="Max Height")
            text_head_area1[i_value_x].place(relx=0.60 + 0.20 * i_value_x, rely=0.2, anchor='ne')
            
            text_min_aspect_ratio.append("text_head_minaspect_" + str(i_value_x + 1))
            text_min_aspect_ratio[i_value_x] = tk.Label(root, text="Min Aspect Ratio")
            text_min_aspect_ratio[i_value_x].place(relx=0.70 + 0.20 * i_value_x, rely=0.2, anchor='ne')
            text_max_aspect_ratio.append("text_head_maxaspect_" + str(i_value_x + 1))
            text_max_aspect_ratio[i_value_x] = tk.Label(root, text="Max Aspect Ratio")
            text_max_aspect_ratio[i_value_x].place(relx=0.80 + 0.20 * i_value_x, rely=0.2, anchor='ne')
        
        text_room.append("text_room_" + str(i))
        # text_room[i] = tk.Label(root, text="Room" + str(i), font=("Times New Roman", 8))
        text_room[i] = tk.Label(root, text=str(room_mapping[i]), font=("Times New Roman", 8))
        text_room[i].place(relx=0.20 + 0.20 * i_value_x, rely=0.3 + (0.030 * i_value_y), anchor='ne')
        
        value_width.append("value_width" + str(i))
        value_width[i] = tk.Entry(root, width=5, textvariable=w[i])
        value_width[i].place(relx=0.30 + 0.20 * i_value_x, rely=0.3 + (0.030) * i_value_y, anchor='ne')
        
        value_width1.append("value_width1" + str(i))
        value_width1[i] = tk.Entry(root, width=5, textvariable=w1[i])
        value_width1[i].place(relx=0.40 + 0.20 * i_value_x, rely=0.3 + (0.030) * i_value_y, anchor='ne')
        
        value_area.append("value_area" + str(i))
        value_area[i] = tk.Entry(root, width=5, textvariable=minA[i])
        value_area[i].place(relx=0.50 + 0.20 * i_value_x, rely=0.3 + (0.030) * i_value_y, anchor='ne')
        
        value_area1.append("value_area1" + str(i))
        value_area1[i] = tk.Entry(root, width=5, textvariable=maxA[i])
        value_area1[i].place(relx=0.60 + 0.20 * i_value_x, rely=0.3 + (0.030) * i_value_y, anchor='ne')
        
        value_min_aspect_ratio.append("value_aspect_min" + str(i))
        value_min_aspect_ratio[i] = tk.Entry(root, width=5, textvariable=min_ar[i])
        value_min_aspect_ratio[i].place(relx=0.70 + 0.20 * i_value_x, rely=0.3 + (0.030) * i_value_y, anchor='ne')

        value_max_aspect_ratio.append("value_aspect_max" + str(i))
        value_max_aspect_ratio[i] = tk.Entry(root, width=5, textvariable=max_ar[i])
        value_max_aspect_ratio[i].place(relx=0.80 + 0.20 * i_value_x, rely=0.3 + (0.030) * i_value_y, anchor='ne')

    def button_clicked():
        for i in range(0, nodes):
            min_width.append(int(value_width[i].get()))
            max_width.append(int(value_width1[i].get()))
            min_height.append(int(value_area[i].get()))
            max_height.append(int(value_area1[i].get()))
            min_aspect.append(float(value_min_aspect_ratio[i].get()))
            max_aspect.append(float(value_max_aspect_ratio[i].get()))
        print("dimguisubmit")
        print(sym_var.get())
        symmetric_text.append(sym_var.get())
        root.destroy()

    def free_dim_func():
        for i in range(0, nodes):
            w[i].set(0)
            w1[i].set(99999)
            minA[i].set(0)
            maxA[i].set(99999)
            min_ar[i].set(0)
            max_ar[i].set(99999)

        sym_var.set("()")

    button = tk.Button(root, text='Submit', padx=5, command=button_clicked)
    button.place(relx=0.45, rely=0.6, anchor='ne')

    free_dim_btn = tk.Button(root, text="Free Dimensions", padx=5, command=free_dim_func)
    free_dim_btn.place(relx=0.55, rely=0.6, anchor='ne')

    root.wait_window(root)
    print("dimgui")
    print(min_width, max_width, min_height, max_height, symmetric_text[0], min_aspect, max_aspect)
    return min_width, max_width, min_height, max_height, symmetric_text[
        0], min_aspect, max_aspect, plot_width.get(), plot_height.get()


if __name__ == "__main__":
    gui_fnc([], 3)