"""Main GUI of the project (implemented using Tkinter).


"""

import ast
import json
import os
import pickle
import random
import sys
import tkinter as tk
import tkinter.ttk as ttk
import turtle
import warnings
from tkinter import ALL, EventType, Label, Menu, filedialog, messagebox
import matplotlib.pyplot as plt
import networkx as nx
from PIL import Image, ImageTk
import tablenoscroll
import final
done = True
# col = ["#3b429f","#8043B1","#f5d7e3","#f4a5ae","#a8577e"]
# col = ["#3b429f","#button","#tk","#cavas","#a8577e"]
# col = ["#788585","#9A8C98","#F2E9E4","#C9ADA7","#e1eaec"]
col = ["white","#9A8C98","light grey","white"]
font={'font' : ("lato bold",10,"")}
# reloader = Reloader()
warnings.filterwarnings("ignore") 
class ScrollFrame(tk.Frame):
            def __init__(self, parent):
                super().__init__(parent) # create a frame (self)

                self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")          #place canvas on self
                self.viewPort = tk.Frame(self.canvas, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets 
                self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
                self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

                # self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
                # self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
                self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                        tags="self.viewPort")

                self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
                self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the viewPort frame changes.

                self.onFrameConfigure(None)                                                 #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

            def onFrameConfigure(self, event):                                              
                '''Reset the scroll region to encompass the inner frame'''
                self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

            def onCanvasConfigure(self, event):
                '''Reset the canvas window to encompass inner frame when required'''
                canvas_width = event.width
                self.canvas.itemconfig(self.canvas_window, width = canvas_width)            #whenever the size of the canvas changes alter the window region respectively.

class gui_class:
    def __init__(self):
        border_details = {'bg': col[2], 'highlightbackground': 'black', 'highlightcolor': 'black', 'highlightthickness': 1}        
        
        self.open = False
        self.command = "Null"
        self.value = []
        self.root =tk.Tk()
        self.open_ret = []
        # self.root.filename = 
        self.root.config(bg=col[2])
        self.textbox = tk.Text
        # self.pen = turtle.Screen()
        # self.pen = turtle.RawTurtle
        # self.pen.screen.bgcolor(col[2])
        self.end= tk.IntVar(self.root)
        self.frame2 = tk.Frame(self.root,bg=col[2])
        self.frame2.grid(row=0,column=1,rowspan=6,sticky='news')
        self.frame5 = tk.Frame(self.root,bg=col[2])
        self.frame5.grid(row=0,column=2,rowspan=3,sticky='news',padx=10)
        self.tablehead = tk.Label(self.frame5,text='Room Info',bg =col[2])
        self.tablehead.pack()

        self.app = self.PlotApp(self.frame2,self)
        self.root.state('normal')
        self.root.title('Input Graph')
        self.checkvar1 = tk.IntVar()

        self.tabledata = []
        self.frame1 = tk.Frame(self.root,bg=col[2])
        self.frame1.grid(row=0,column=0)
        label1 = tk.LabelFrame(self.frame1,text="tools")
        label1.grid(row=0,column=0,pady=10)
        self.frame3 = tk.Frame(self.root,bg=col[2])
        self.frame3.grid(row=1,column=0)
        self.Buttons(self.frame1,self)
        self.menu(self)
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.tbox = self.output_text(self.frame3)
        self.ocan = self.output_canvas(self.frame2)
        self.pen = self.ocan.getpen()
        self.root_window = self.ocan.getroot()   
        self.root.wait_variable(self.end)
        self.graph_ret()
        while((self.value[0] == 0) and done):
            # print(done)
            self.root.wait_variable(self.end)
            self.value=self.app.return_everything()
            tk.messagebox.showinfo("error","The graph is empty , please draw a graph")

    class Nodes():
        def __init__(self,id,x,y):
            self.circle_id=id
            self.pos_x=x
            self.pos_y=y
            self.radius=15
            self.adj_list=[]
        
        def clear(self):
            self.circle_id=-1
            self.pos_x=0
            self.pos_y=0
            self.radius=0
            self.adj_list=[]
    
    class PlotApp(object):

        def __init__(self, root,master):
            self.l1 = tk.Label(root,text='Draw a test graph here',bg=col[2])
            self.l1.grid(row=0,column=0)
            self._root = root
            self.radius_circle=15
            self.rnames = []
            self.master = master
            self.command = "Null"
            self.table = tablenoscroll.Table(self.master.frame5,["Index", "Room Name"], column_minwidths=[None, None])
            self.table.pack(padx=10,pady=10)
            self.table.config(bg="#F4A5AE")
            self.createCanvas()

            
        colors = ['#edf1fe','#c6e3f7','#e1eaec','#e5e8f2','#def7fe','#f1ebda','#f3e2c6','#fff2de','#ecdfd6','#f5e6d3','#e3e7c4','#efdbcd','#ebf5f0','#cae1d9','#c3ddd6','#cef0cc','#9ab8c2','#ddffdd','#fdfff5','#eae9e0','#e0dddd','#f5ece7','#f6e6c5','#f4dbdc','#f4daf1','#f7cee0','#f8d0e7','#efa6aa','#fad6e5','#f9e8e2','#c4adc9','#f6e5f6','#feedca','#f2efe1','#fff5be','#ffffdd']
        nodes_data=[]
        id_circle=[]
        name_circle= []
        edge_count=0
        hex_list = []
        multiple_rfp = 0
        cir=0
        edges=[]
        random_list = []
        connection=[]
        oval = [] 
        rcanframe = []
        abc = 0
        xyz = 0
        elines = []

        def return_everything(self):
            return [len(self.nodes_data),self.edge_count,self.edges,self.command,self.master.checkvar1.get(),list(filter(None, [row[1].get() for row in self.table._data_vars])),self.hex_list]

        def createCanvas(self):
            self.id_circle.clear()
            self.name_circle.clear()
            for i in range(0,100):
                self.id_circle.append(i)
            for i in range(0,100):
                self.name_circle.append("Room "+ str(i))
            self.nodes_data.clear()
            self.edges.clear()
            self.table._pop_all()
            self.edge_count = 0
            self.oval.clear()
            self.rcanframe.clear()
            self.abc  =0
            self.hex_list.clear()
            self.xyz = 0
            self.elines.clear()
            # border_details = {'highlightbackground': 'black', 'highlightcolor': 'black', 'highlightthickness': 1}
            self.canvas = tk.Canvas(self._root,bg=col[3], width=1000, height=370)
            self.canvas.grid(column=0,row =1, sticky='nwes')
            self.canvas.bind("<Button-3>",self.addH)
            self.connection=[]
            self.canvas.bind("<Button-1>",self.button_1_clicked) 
            self.canvas.bind("<Button-2>",self.remove_node)
            self.ButtonReset = tk.Button(self._root, text="Reset",fg='white',width=10,height=2 ,**font,relief = 'flat',bg=col[1] ,command=self.reset)
            self.ButtonReset.grid(column=0 ,row=1,sticky='n',pady=20,padx=40)
            
            self.instru = tk.Button(self._root, text="Instructions",fg='white',height=2 , **font ,relief = 'flat', bg=col[1] ,command=self.instructions)
            self.instru.grid(column=0 ,row=1,sticky='wn',pady=22,padx=40)

            self.lay = tk.Button(self._root, text="Switch to Layout",fg='white',height=2 ,**font,relief = 'flat',bg=col[1] ,command=self.switch)
            self.lay.grid(column=0 ,row=1,sticky='ne',pady=20,padx=40)

        def switch(self):
            self.master.root.destroy()
            final.run()
        def instructions(self):
            tk.messagebox.showinfo("Instructions",
            "--------User Instructrions--------\n 1. Draw the input graph. \n 2. Use right mouse click to create a new room. \n 3. left click on one node then left click on another to create an edge between them. \n 4. You can give your own room names by clicking on the room name in the graph or the table on the right. \n 5. After creating a graph you can choose one of the option to create it's corresponding RFP or multiple RFPs with or without dimension. You can also get the corridor connecting all the rooms by selecting 'circultion' or click on 'RFPchecker' to check if RFP exists for the given graph. \n 6. You can also select multiple options .You can also add rooms after creating RFP and click on RFP to re-create a new RFP. \n 7.Reset button is used to clear the input graph. \n 8. Press 'Exit' if you want to close the application or Press 'Restart' if you want to restart the application")

        def addH(self, event):
            random_number = random.randint(0,35)
            while(random_number in self.random_list):
                random_number = random.randint(0,35)
            self.random_list.append(random_number)
            hex_number = self.colors[random_number]
            # print(random_number)
            # print(hex_number)
            self.hex_list.append(hex_number)
            if(len(self.random_list) == 36):
                self.random_list = []
            x, y = event.x, event.y
            id_node=self.id_circle[0]
            self.id_circle.pop(0)
            node=self.master.Nodes(id_node,x,y)
            self.nodes_data.append(node)
            self.rframe = tk.Frame(self._root,width=20,height=20)
            self.rname= tk.StringVar(self._root)
            self.rnames.append(self.rname)
            self.rname.set(self.name_circle[0])
            self.table.insert_row(list((id_node,self.rname.get())),self.table._number_of_rows)
            self.name_circle.pop(0)
            # self.rframe.grid(row=0,column=1)
            self.oval.append(self.canvas.create_oval(x-self.radius_circle,y-self.radius_circle,x+self.radius_circle,y+self.radius_circle,width=3, fill=hex_number,tag=str(id_node)))
            # self.canvas.create_text(x,y-self.radius_circle-9,text=str(id_node),font=("Purisa",14))
            # self.buttonBG = self.canvas.create_rectangle(x-15,y-self.radius_circle-20, x+15,y-self.radius_circle, fill="light grey")
            # self.buttonTXT = self.canvas.create_text(x,y-self.radius_circle-9, text="click")
            self.rcanframe.append(self.canvas.create_window(x,y-self.radius_circle-12, window=self.rframe))
            # self.canvas.tag_bind(self.buttonBG, "<Button-1>", self.room_name) ## when the square is clicked runs function "clicked".
            # self.canvas.tag_bind(self.buttonTXT, "<Button-1>", self.room_name) ## same, but for the text.
            # def _on_configure(self, event):
            #     self.entry.configure(width=event.width)
            self.entry = tk.Entry(self.rframe,textvariable=self.table._data_vars[self.id_circle[0]-1][1],relief='flat',justify='c',width=15,bg=col[2])
            # self.entry.bind("<Configure>", _on_configure)
            
            # but =tk.Button(self.rframe)
            # but.grid()
            self.entry.grid()
            # print(self.rname.get())
        def button_1_clicked(self,event):
            if len(self.connection)==2:
                self.canvas.itemconfig(self.oval[self.xyz],outline='black')
                self.canvas.itemconfig(self.oval[self.abc],outline='black')
                self.connection=[]
            if len(self.nodes_data)<=1:
                tk.messagebox.showinfo("Connect Nodes","Please make 2 or more nodes")
                return
            x, y = event.x, event.y
            value=self.get_id(x,y)
            self.abc= self.xyz
            self.xyz= self.nodes_data[value].circle_id
            self.hover_bright(event)
            if value == -1:
                return
            else:
                if value in self.connection:
                    tk.messagebox.showinfo("Connect Nodes","You have clicked on same node. Please try again")
                    return
                self.connection.append(value)

            if len(self.connection)>1:
                node1=self.connection[0]
                node2=self.connection[1]

                if node2 not in self.nodes_data[node1].adj_list:
                    self.nodes_data[node1].adj_list.append(node2)
                if node1 not in self.nodes_data[node2].adj_list:
                    self.nodes_data[node2].adj_list.append(node1)
                    self.edge_count+=1
                self.edges.append(self.connection)
                self.connect_circles(self.connection)

            # for i in self.nodes_data:
            # 	print("id: ",i.circle_id)
            # 	print("x,y: ",i.pos_x,i.pos_y)
            # 	print("adj list: ",i.adj_list)
            
        def connect_circles(self,connections):
            node1_id=connections[0]
            node2_id=connections[1]
            node1_x=self.nodes_data[node1_id].pos_x
            node1_y=self.nodes_data[node1_id].pos_y
            node2_x=self.nodes_data[node2_id].pos_x
            node2_y=self.nodes_data[node2_id].pos_y
            self.elines.append([self.canvas.create_line(node1_x,node1_y,node2_x,node2_y,width=3),connections])

        def get_id(self,x,y):
            for j,i in enumerate(self.nodes_data):
                distance=((i.pos_x-x)**2 + (i.pos_y-y)**2)**(1/2)
                if distance<=self.radius_circle:
                    return j
            tk.messagebox.showinfo("Connect Nodes","You have clicked outside all the circles. Please try again")
            return -1
        
        def remove_node(self,event):
            id = self.get_id(event.x,event.y)
            # id = self.nodes_data[id].circle_id
            self.canvas.delete(self.oval[id])
            self.canvas.delete(self.rcanframe[id])
            for i in self.elines:
                if i[1][0]==id or i[1][1]==id:
                    self.canvas.delete(i[0])
                    self.edges.remove(i[1])
                    self.edge_count-=1
            self.nodes_data[id].clear()
            self.nodes_data.pop(id)
            self.hex_list.pop(id)
            for j in range(self.table.number_of_columns):
                self.table._data_vars[id][j].set("")
            self.table._data_vars.pop(id)
            # self.edges.pop(id)
            # self.table.delete_row(id)
            i = id
            # while i < self.table._number_of_rows-1:
            #     row_of_vars_1 = self.table._data_vars[i]
            #     row_of_vars_2 = self.table._data_vars[i+1]

            #     j = 0
            #     while j <self.table._number_of_columns:
            #         row_of_vars_1[j].set(row_of_vars_2[j].get())
            #         j+=1
            #     i += 1

            # self.table._pop_n_rows(1)
            # self.table._number_of_rows-=1
            # self.table._data_vars.pop(id)
            for j in range(self.table.number_of_columns):
                self.table.grid_slaves(row=i+1, column=j)[0].destroy()
            self.table._number_of_rows -=1

            # if self.table._on_change_data is not None: self.table._on_change_data()
        
        def hover_bright(self,event):
            self.canvas.itemconfig(self.oval[self.xyz],outline='red')
        
        def reset(self):
            self.canvas.destroy()
            self.createCanvas()

    class Buttons:
        def __init__(self,root,master):
            
            button_details={'wraplength':'150','bg':col[1],'fg':'white','font':('lato','14') , 'padx':5 ,'pady':5,'activebackground' : col[2] }
            b1 = tk.Button(master.frame1,width=15,text='A Floor Plan',relief='flat',**button_details,command=master.single_floorplan)
            b1.grid(row=1,column=0,padx=5,pady=5)
            
            b2 = tk.Button(master.frame1,width=15, text='Multiple Floor Plans',relief='flat',**button_details,command=master.multiple_floorplan)
            b2.grid(row=2,column=0,padx=5,pady=5)
            
            c1 = tk.Checkbutton(master.frame1, text = "Dimensioned",relief='flat',**button_details,selectcolor='#4A4E69',width=13 ,variable = master.checkvar1,onvalue = 1, offvalue = 0)
            c1.grid(row=3,column=0,padx=5,pady=5)
           
            # b3 = tk.Button(master.frame1,width=15, text='Circulation',relief='flat',**button_details,command=master.circulation)
            # b3.grid(row=4,column=0,padx=5,pady=5)
            
            b4 = tk.Button(master.frame1,width=15, text='RFPchecker' ,relief='flat',**button_details,command=master.checker)
            b4.grid(row=5,column=0,padx=5,pady=5)
            
            # b6 = tk.Button(master.frame1,width=15, text='Restart',relief='flat', **button_details,command=master.restart)
            # b6.grid(row=6,column=0,padx=5,pady=5)
           
            # b5 = tk.Button(master.frame1,width=15, text='EXIT',relief='flat', **button_details,command=master.exit)
            # b5.grid(row=7,column=0,padx=5,pady=5)

    class menu:
        def __init__(self,master):
            root  = master.root
            menubar = tk.Menu(root,bg=col[3])
            menubar.config(background=col[3])
            filemenu = tk.Menu(menubar,bg=col[3], tearoff=2)
            filemenu.add_command(label="New",command=master.restart)
            filemenu.add_command(label="Open",command=master.open_file)
            filemenu.add_command(label="Save",command=master.save_file)
            filemenu.add_command(label="Save as...",command=master.save_file)
            filemenu.add_command(label="Close",command=master.exit)

            filemenu.add_separator()

            filemenu.add_command(label="Exit", command=master.exit)
            menubar.add_cascade(label="File", menu=filemenu)
            editmenu = tk.Menu(menubar,bg=col[3], tearoff=0)
            editmenu.add_command(label="Undo")

            editmenu.add_separator()

            editmenu.add_command(label="Cut")
            editmenu.add_command(label="Copy")
            editmenu.add_command(label="Paste")
            editmenu.add_command(label="Delete")
            editmenu.add_command(label="Select All")

            menubar.add_cascade(label="Edit", menu=editmenu)
            helpmenu = tk.Menu(menubar,bg=col[3], tearoff=0)
            helpmenu.add_command(label="About...")
            menubar.add_cascade(label="Help", menu=helpmenu)
            
            root.config(menu=menubar)
    
    class output_canvas:
        def __init__(self,root):
            self.root=root
            self.root_window = tk.PanedWindow(root)
            self.l1 = tk.Label(self.root_window, text= 'Rectangular Dual')
            self.root_window.grid(row=2,column=0,pady=5)
            self.tabs = []
            self.tabno = -1
            self.tabControl = ttk.Notebook(self.root_window)
            # self.tabs = ttk.Frame(self.tabControl)
            
            # self.tabControl.add(self.tabs, text='Tab 1')
            self.tabControl.pack(expand=1, fill="both")
            # tk.Label(tabs, text="Welcome to GeeksForGeeks").grid(column=0, row=0, padx=30, pady=30)
            # tk.Label(self.tab2, text="Lets dive into the world of computers").grid(column=0, row=0, padx=30, pady=30)
            self.add_tab()
            
        def add_tab(self):
            self.tabno+=1
            self.tabs.append( ttk.Frame(self.tabControl) )
            self.tabControl.add(self.tabs[self.tabno], text='Tab '+str(self.tabno+1))
            self.tabControl.select(self.tabno)
            self.canvas = turtle.ScrolledCanvas(self.tabs[self.tabno],width=970,height=350)
            self.canvas.bind("<Double-Button-1>",self.zoom)
            self.canvas.grid(column=0, row=1, padx=2, pady=2)
            self.tscreen = turtle.TurtleScreen(self.canvas)
            self.tscreen.screensize(50000,1000)
            self.tscreen.bgcolor(col[3])
            self.pen = turtle.RawTurtle(self.tscreen)
            self.pen.speed(10000000)

            self.canvas.bind("<MouseWheel>",  self.do_zoom)
            self.canvas.bind('<Button-1>', lambda event: self.canvas.scan_mark(event.x, event.y))
            self.canvas.bind("<B1-Motion>", lambda event: self.canvas.scan_dragto(event.x, event.y, gain=1))
            imname = "./close1.png"
            im1 = Image.open(imname).convert("1")
            size = (im1.width // 4, im1.height // 4)
            # im1.resize(size)
            # # im1.show()
            # im1 = ImageTk.BitmapImage(im1.resize(size)) 
            im2 = ImageTk.PhotoImage(Image.open(imname).resize(size))
            
            butimg = ImageTk.PhotoImage(file="./close1.png")
            # flat, groove, raised, ridge, solid, or sunke
            # self.canvas.create_image(20,20,anchor='ne',image=butimg)
            self.closeb = tk.Button(self.tabs[self.tabno],relief='solid',bg=col[3],activebackground=col[2],image=im2,command=self.close)
            self.closeb.image=im2
            self.closeb.grid(row=1,column=0,sticky='ne',pady=20,padx=70)
        def do_zoom(self,event):
            factor = 1.001 ** event.delta
            self.canvas.scale(ALL, event.x, event.y, factor, factor)

        def getpen(self):
            return self.pen

        def getroot(self):
            return self.root_window
        
        def zoom(self,event):
            self.canvas.config(width=self.root.winfo_screenwidth(),height=self.root.winfo_screenheight())

        def close(self):
            self.tabno-=1
            self.tabs.pop()
            self.tabControl.forget(self.tabControl.select())
    
    class output_text:
        def __init__(self,root):
            self.textbox = tk.Text(root,bg=col[3],fg='black',relief='flat',height=32,width=30,padx=5,pady=5,**font)
            self.textbox.grid(row=0,column=0 ,padx=10,pady=10)

            self.textbox.insert('insert',"\t         Output\n")

        def gettext(self):
            return self.textbox
    
    def graph_ret(self):
        if not self.open:
            self.value = self.app.return_everything()
            self.textbox = self.tbox.gettext()
        else:
            self.value = self.open_ret.copy()
            self.textbox = self.tbox.gettext()

    def single_floorplan(self):
        self.app.command="single"
        self.command = "single"
        self.end.set(self.end.get()+1)
        self.root.state('normal')
        # root.destroy()

    def multiple_floorplan(self):
        self.app.command="multiple"
        self.command = "multiple"
        self.end.set(self.end.get()+1)
        # root.destroy()
    
    def circulation(self):
        self.app.command="circulation"
        self.command = "circulation"
        self.end.set(self.end.get()+1)
    
    def checker(self):
        self.app.command="checker"
        self.command = "checker"
        self.end.set(self.end.get()+1)

    def restart(self):
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    
    def exit(self):
        global done

        self.app.command="end"
        self.command = "end"
        self.end.set(self.end.get()+1)
        done = False

        # self.saver = tk.Toplevel()
        # saverlabel = tk.Label(self.saver,text="hwakeoa")
        # saverlabel.pack()

        # b1 = tk.Button(self.saver,text="No",command=sys.exit(0))
        # b1.pack()
        # self.saver.wait_window(self.saver)

        self.root.destroy()

        
        
        
        # return self.value , self.root , self.textbox , self.pen ,self.end

    def open_file(self):
        self.file = filedialog.askopenfile(mode='r',defaultextension=".txt",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
        f = self.file.read()
        print(f)
        # print("hjio")
        fname = self.file.name
        print(fname)
        fname = fname[:-3]
        fname+="png"
        print(fname)
        self.open_ret = ast.literal_eval(f)
        print(self.open_ret)
        self.graph = nx.Graph()
        self.graph.add_edges_from(self.open_ret[2])
        nx.draw_planar(self.graph)
        # plt.show()

        plt.savefig(fname)
        img = Image.open(fname)
        img = img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)

        render = ImageTk.PhotoImage(img)
        load = tk.Label(self.frame2, image=render)
        load.image = render
        load.grid(row=1,column=0,sticky='news')
        self.root.state('normal')
        img.save("img2.png", "PNG")
        self.open = True

        # with open('config.dictionary', 'rb') as config_dictionary_file:
        #     cself = pickle.load(config_dictionary_file)
        # # After config_dictionary is read from file
        # print(cself.value)

    def save_file(self):
        # self.root.filename = self.value
        f = filedialog.asksaveasfile( defaultextension=".txt",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")),initialfile="Rectangular Dual Graph.txt")
        if f is None:
            return


        f.write(str(self.value))
        f.close()

        # with open('config.dictionary', 'wb') as config_dictionary_file:
        #     pickle.dump(self.app, config_dictionary_file)
    # def copy_to_file(self):


            
if __name__ == '__main__':
    value=gui_class()
