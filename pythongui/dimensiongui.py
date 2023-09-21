import tkinter as tk
from tkinter import font
from tkinter import messagebox


# def gui_fnc(old_dims, nodes, room_mapping):
#     min_width = []
#     max_width = []
#     min_height = []
#     max_height = []
#     min_aspect = []
#     max_aspect = []
#     symmetric_text = []

#     root = tk.Toplevel()

#     root.title('Dimensional Input')
#     root.geometry(str(1200) + 'x' + str(700))
#     Upper_right = tk.Label(root, text="Enter dimensional constraints for each room", font=("Times New Roman", 12))

#     Upper_right.place(relx=0.60, rely=0.1, anchor='ne')

#     text_head_width = []
#     text_head_width1 = []
#     text_head_area = []
#     text_head_area1 = []
#     text_room = []
#     text_min_aspect_ratio = []
#     text_max_aspect_ratio = []
#     value_width = []
#     value_width1 = []
#     value_area = []
#     value_area1 = []
#     value_min_aspect_ratio = []
#     value_max_aspect_ratio = []
#     w = []
#     w1 = []
#     minA = []
#     maxA = []
#     min_ar = []
#     max_ar = []

#     sym_var = (tk.StringVar(value=old_dims[4]))
#     plot_height = tk.IntVar(root, 0)
#     plot_height.set(-1)
#     plot_width = tk.IntVar(root, 0)
#     plot_width.set(-1)

#     for i in range(0, nodes):
#         i_value_x = 0
#         i_value_y = i
#         min_width.append(tk.IntVar(value=old_dims[0][i]))
#         max_width.append(tk.IntVar(value=old_dims[1][i]))
#         min_height.append(tk.IntVar(value=old_dims[2][i]))
#         max_height.append(tk.IntVar(value=old_dims[3][i]))
#         min_aspect.append(tk.DoubleVar(value=old_dims[5][i]))
#         max_aspect.append(tk.DoubleVar(value=old_dims[6][i]))

#         if (i_value_y == 0):
#             text_head_width.append("text_head_width_" + str(i_value_x + 1))
#             text_head_width[i_value_x] = tk.Label(root, text="Min Width")
#             text_head_width[i_value_x].place(relx=0.30 + 0.20 * i_value_x, rely=0.2, anchor='ne')
            
#             text_head_width1.append("text_head_width1_" + str(i_value_x + 1))
#             text_head_width1[i_value_x] = tk.Label(root, text="Max Width")
#             text_head_width1[i_value_x].place(relx=0.40 + 0.20 * i_value_x, rely=0.2, anchor='ne')
            
#             text_head_area.append("text_head_area_" + str(i_value_x + 1))
#             text_head_area[i_value_x] = tk.Label(root, text="Min Height")
#             text_head_area[i_value_x].place(relx=0.50 + 0.20 * i_value_x, rely=0.2, anchor='ne')
            
#             text_head_area1.append("text_head_area1_" + str(i_value_x + 1))
#             text_head_area1[i_value_x] = tk.Label(root, text="Max Height")
#             text_head_area1[i_value_x].place(relx=0.60 + 0.20 * i_value_x, rely=0.2, anchor='ne')
            
#             text_min_aspect_ratio.append("text_head_minaspect_" + str(i_value_x + 1))
#             text_min_aspect_ratio[i_value_x] = tk.Label(root, text="Min Aspect Ratio")
#             text_min_aspect_ratio[i_value_x].place(relx=0.70 + 0.20 * i_value_x, rely=0.2, anchor='ne')
#             text_max_aspect_ratio.append("text_head_maxaspect_" + str(i_value_x + 1))
#             text_max_aspect_ratio[i_value_x] = tk.Label(root, text="Max Aspect Ratio")
#             text_max_aspect_ratio[i_value_x].place(relx=0.80 + 0.20 * i_value_x, rely=0.2, anchor='ne')
        
#         text_room.append("text_room_" + str(i))
#         text_room[i] = tk.Label(root, text=str(room_mapping[i]), font=("Times New Roman", 8))
#         text_room[i].place(relx=0.20 + 0.20 * i_value_x, rely=0.3 + (0.030 * i_value_y), anchor='ne')
        
#         min_width_slider = tk.Scale(root, from_=0, to=100, orient='horizontal', variable=min_width[i])
#         min_width_slider.place(relx=0.30 + 0.20 * i_value_x, rely=0.3 + (0.030) * i_value_y, anchor='ne')
        
#         max_width_slider = tk.Scale(root, from_=0, to=100, orient='horizontal', variable=max_width[i])
#         max_width_slider.place(relx=0.40 + 0.20 * i_value_x, rely=0.3 + (0.030) * i_value_y, anchor='ne')
        
#         min_height_slider = tk.Scale(root, from_=0, to=100, orient='horizontal', variable=min_height[i])
#         min_height_slider.place(relx=0.50 + 0.20 * i_value_x, rely=0.3 + (0.030) * i_value_y, anchor='ne')
        
#         max_height_slider = tk.Scale(root, from_=0, to=100, orient='horizontal', variable=max_height[i])
#         max_height_slider.place(relx=0.60 + 0.20 * i_value_x, rely=0.3 + (0.030) * i_value_y, anchor='ne')
        
#         min_aspect_slider = tk.Scale(root, from_=0, to=10, orient='horizontal', resolution=0.1, variable=min_aspect[i])
#         min_aspect_slider.place(relx=0.70 + 0.20 * i_value_x, rely=0.3 + (0.030) * i_value_y, anchor='ne')

#         max_aspect_slider = tk.Scale(root, from_=0, to=10, orient='horizontal', resolution=0.1, variable=max_aspect[i])
#         max_aspect_slider.place(relx=0.80 + 0.20 * i_value_x, rely=0.3 + (0.030) * i_value_y, anchor='ne')

#     def button_clicked():
#         for i in range(0, nodes):
#             min_width_val = min_width[i].get()
#             max_width_val = max_width[i].get()
#             min_height_val = min_height[i].get()
#             max_height_val = max_height[i].get()
#             min_aspect_val = min_aspect[i].get()
#             max_aspect_val = max_aspect[i].get()
#             min_width.append(min_width_val)
#             max_width.append(max_width_val)
#             min_height.append(min_height_val)
#             max_height.append(max_height_val)
#             min_aspect.append(min_aspect_val)
#             max_aspect.append(max_aspect_val)
#         print("dimguisubmit")
#         print(sym_var.get())
#         symmetric_text.append(sym_var.get())
#         root.destroy()

#     def free_dim_func():
#         for i in range(0, nodes):
#             min_width[i].set(0)
#             max_width[i].set(100)
#             min_height[i].set(0)
#             max_height[i].set(100)
#             min_aspect[i].set(0)
#             max_aspect[i].set(10)
#         sym_var.set("()")

#     button = tk.Button(root, text='Submit', padx=5, command=button_clicked)
#     button.place(relx=0.45, rely=0.6, anchor='ne')

#     free_dim_btn = tk.Button(root, text="Free Constraints", padx=5, command=free_dim_func)
#     free_dim_btn.place(relx=0.55, rely=0.6, anchor='ne')

#     root.wait_window(root)
#     print("dimgui")
#     print(min_width, max_width, min_height, max_height, symmetric_text[0], min_aspect, max_aspect)
#     return min_width, max_width, min_height, max_height, symmetric_text[0], min_aspect, max_aspect, plot_width.get(), plot_height.get()

# def gui_fnc(old_dims, nodes, room_mapping):
#     min_width = []
#     max_width = []
#     min_height = []
#     max_height = []
#     min_aspect = []
#     max_aspect = []
#     symmetric_text = []

#     root = tk.Toplevel()

#     root.title('Dimensional Input')
#     root.geometry(str(1200) + 'x' + str(700))
#     Upper_right = tk.Label(root, text="Enter dimensional constraints for each room", font=("Times New Roman", 12))

#     Upper_right.place(relx=0.60, rely=0.1, anchor='ne')

#     text_head_width = []
#     text_head_width1 = []
#     text_head_area = []
#     text_head_area1 = []
#     text_room = []
#     text_min_aspect_ratio = []
#     text_max_aspect_ratio = []
#     value_width = []
#     value_width1 = []
#     value_area = []
#     value_area1 = []
#     value_min_aspect_ratio = []
#     value_max_aspect_ratio = []
#     w = []
#     w1 = []
#     minA = []
#     maxA = []
#     min_ar = []
#     max_ar = []

#     sym_var = (tk.StringVar(value=old_dims[4]))
#     plot_height = tk.IntVar(root, 0)
#     plot_height.set(-1)
#     plot_width = tk.IntVar(root, 0)
#     plot_width.set(-1)
#     #!!! does this setting work everytime???

#     for i in range(0, nodes):
#         i_value_x = 0
#         i_value_y = i
#         w.append(tk.IntVar(value=old_dims[0][i]))
#         w1.append(tk.IntVar(value=old_dims[1][i]))
#         minA.append(tk.IntVar(value=old_dims[2][i]))
#         maxA.append(tk.IntVar(value=old_dims[3][i]))
#         min_ar.append(tk.DoubleVar(value=old_dims[5][i]))
#         max_ar.append(tk.DoubleVar(value=old_dims[6][i]))

#         if (i_value_y == 0):
#             text_head_width.append("text_head_width_" + str(i_value_x + 1))
#             text_head_width[i_value_x] = tk.Label(root, text="Actual Width")
#             text_head_width[i_value_x].place(relx=0.30 + 0.20 * i_value_x, rely=0.2, anchor='ne')
            
#             text_head_width1.append("text_head_width1_" + str(i_value_x + 1))
#             text_head_width1[i_value_x] = tk.Label(root, text="Max Width")
#             text_head_width1[i_value_x].place(relx=0.40 + 0.20 * i_value_x, rely=0.2, anchor='ne')
            
#             text_head_area.append("text_head_area_" + str(i_value_x + 1))
#             text_head_area[i_value_x] = tk.Label(root, text="Actual Height")
#             text_head_area[i_value_x].place(relx=0.50 + 0.20 * i_value_x, rely=0.2, anchor='ne')
            
#             text_head_area1.append("text_head_area1_" + str(i_value_x + 1))
#             text_head_area1[i_value_x] = tk.Label(root, text="Max Height")
#             text_head_area1[i_value_x].place(relx=0.60 + 0.20 * i_value_x, rely=0.2, anchor='ne')
            
#             text_min_aspect_ratio.append("text_head_minaspect_" + str(i_value_x + 1))
#             text_min_aspect_ratio[i_value_x] = tk.Label(root, text="Min Aspect Ratio")
#             text_min_aspect_ratio[i_value_x].place(relx=0.70 + 0.20 * i_value_x, rely=0.2, anchor='ne')
#             text_max_aspect_ratio.append("text_head_maxaspect_" + str(i_value_x + 1))
#             text_max_aspect_ratio[i_value_x] = tk.Label(root, text="Max Aspect Ratio")
#             text_max_aspect_ratio[i_value_x].place(relx=0.80 + 0.20 * i_value_x, rely=0.2, anchor='ne')
        
#         text_room.append("text_room_" + str(i))
#         # text_room[i] = tk.Label(root, text="Room" + str(i), font=("Times New Roman", 8))
#         text_room[i] = tk.Label(root, text=str(room_mapping[i]), font=("Times New Roman", 8))
#         text_room[i].place(relx=0.20 + 0.20 * i_value_x, rely=0.3 + (0.030 * i_value_y), anchor='ne')
        
#         value_width.append("value_width" + str(i))
#         value_width[i] = tk.Entry(root, width=5, textvariable=w[i])
#         value_width[i].place(relx=0.30 + 0.20 * i_value_x, rely=0.3 + (0.030) * i_value_y, anchor='ne')
        
#         value_width1.append("value_width1" + str(i))
#         value_width1[i] = tk.Entry(root, width=5, textvariable=w1[i])
#         value_width1[i].place(relx=0.40 + 0.20 * i_value_x, rely=0.3 + (0.030) * i_value_y, anchor='ne')
        
#         value_area.append("value_area" + str(i))
#         value_area[i] = tk.Entry(root, width=5, textvariable=minA[i])
#         value_area[i].place(relx=0.50 + 0.20 * i_value_x, rely=0.3 + (0.030) * i_value_y, anchor='ne')
        
#         value_area1.append("value_area1" + str(i))
#         value_area1[i] = tk.Entry(root, width=5, textvariable=maxA[i])
#         value_area1[i].place(relx=0.60 + 0.20 * i_value_x, rely=0.3 + (0.030) * i_value_y, anchor='ne')
        
#         value_min_aspect_ratio.append("value_aspect_min" + str(i))
#         value_min_aspect_ratio[i] = tk.Entry(root, width=5, textvariable=min_ar[i])
#         value_min_aspect_ratio[i].place(relx=0.70 + 0.20 * i_value_x, rely=0.3 + (0.030) * i_value_y, anchor='ne')

#         value_max_aspect_ratio.append("value_aspect_max" + str(i))
#         value_max_aspect_ratio[i] = tk.Entry(root, width=5, textvariable=max_ar[i])
#         value_max_aspect_ratio[i].place(relx=0.80 + 0.20 * i_value_x, rely=0.3 + (0.030) * i_value_y, anchor='ne')

#     def button_clicked():
#         for i in range(0, nodes):
#             min_width.append(int(value_width[i].get()))
#             max_width.append(int(value_width1[i].get()))
#             min_height.append(int(value_area[i].get()))
#             max_height.append(int(value_area1[i].get()))
#             min_aspect.append(float(value_min_aspect_ratio[i].get()))
#             max_aspect.append(float(value_max_aspect_ratio[i].get()))
#         print("dimguisubmit")
#         print(sym_var.get())
#         symmetric_text.append(sym_var.get())
#         root.destroy()

#     def free_dim_func():
#         for i in range(0, nodes):
#             w[i].set(0)
#             w1[i].set(99999)
#             minA[i].set(0)
#             maxA[i].set(99999)
#             min_ar[i].set(0)
#             max_ar[i].set(99999)
#         sym_var.set("()")

#     button = tk.Button(root, text='Submit', padx=5, command=button_clicked)
#     button.place(relx=0.45, rely=0.6, anchor='ne')

#     free_dim_btn = tk.Button(root, text="Free Dimensions", padx=5, command=free_dim_func)
#     free_dim_btn.place(relx=0.55, rely=0.6, anchor='ne')

#     root.wait_window(root)
#     print("dimgui")
#     print(min_width, max_width, min_height, max_height, symmetric_text[0], min_aspect, max_aspect)
#     return min_width, max_width, min_height, max_height, symmetric_text[0], min_aspect, max_aspect, plot_width.get(), plot_height.get()

import tkinter as tk

def gui_fnc(old_dims, nodes, room_mapping=None):
    min_width = [tk.DoubleVar(value=value) for value in old_dims[0]]
    max_width = [tk.DoubleVar(value=value) for value in old_dims[1]]
    min_height = [tk.DoubleVar(value=value) for value in old_dims[2]]
    max_height = [tk.DoubleVar(value=value) for value in old_dims[3]]
    min_aspect = [tk.DoubleVar(value=value) for value in old_dims[5]]
    max_aspect = [tk.DoubleVar(value=value) for value in old_dims[6]]
    symmetric_text = [tk.StringVar(value=old_dims[4])]
    root = tk.Toplevel()
    root.title('Dimensional Input')
    plot_height = tk.IntVar(root, 0)
    plot_height.set(-1)
    plot_width = tk.IntVar(root, 0)
    plot_width.set(-1)

    sliders = []  # Create a list to store the sliders

    for i in range(nodes):
        i_value_x = 0
        i_value_y = i

        if room_mapping:
            text_room = tk.Label(root, text=str(room_mapping[i]), font=("Times New Roman", 8))
            text_room.grid(row=i, column=0, padx=10, pady=5)

        slider_labels = ["Actual Width", "Max Width", "Actual Height", "Max Height", "Min Aspect Ratio", "Max Aspect Ratio"]
        slider_vars = [min_width[i], max_width[i], min_height[i], max_height[i], min_aspect[i], max_aspect[i]]

        for j, label in enumerate(slider_labels):
            slider_label = tk.Label(root, text=label)
            slider_label.grid(row=i, column=j * 2 + 1, padx=5, pady=5)
            slider = tk.Scale(root, from_=0, to=20, orient="horizontal", resolution=0.01, variable=slider_vars[j])
            slider.grid(row=i, column=j * 2 + 2, padx=5, pady=5)
            sliders.append(slider)  # Append the slider to the list

    def button_clicked():
        print("dimguisubmit")
        symmetric_text[0].set(sym_var.get())
        root.destroy()

    def free_dim_func():
        for i in range(nodes):
            min_width[i].set(0)
            max_width[i].set(0)
            min_height[i].set(0)
            max_height[i].set(0)
            min_aspect[i].set(0)
            max_aspect[i].set(0)
        sym_var.set("()")

    sym_var = tk.StringVar(value=old_dims[4])

    button = tk.Button(root, text='Submit', padx=5, command=button_clicked)
    button.grid(row=nodes, column=0, pady=10)

    free_dim_btn = tk.Button(root, text="Free Dimensions", padx=5, command=free_dim_func)
    free_dim_btn.grid(row=nodes, column=1, pady=10)

    root.wait_window(root)
    print("dimgui")
    print([min_width[i].get() for i in range(nodes)], [max_width[i].get() for i in range(nodes)],
          [min_height[i].get() for i in range(nodes)], [max_height[i].get() for i in range(nodes)],
          symmetric_text[0].get(), [min_aspect[i].get() for i in range(nodes)], [max_aspect[i].get() for i in range(nodes)])

    return (
        [min_width[i].get() for i in range(nodes)], [max_width[i].get() for i in range(nodes)],
        [min_height[i].get() for i in range(nodes)], [max_height[i].get() for i in range(nodes)],
        symmetric_text[0].get(), [min_aspect[i].get() for i in range(nodes)], [max_aspect[i].get() for i in range(nodes)],
        plot_width.get(), plot_height.get()
    )

if __name__ == "__main__":
    gui_fnc([], 3)
