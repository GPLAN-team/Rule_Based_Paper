"""Main program file of the project.


"""
import warnings
import ptpg
import tkinter as tk
import gui
import check
import circulation
import checker
from tkinter import messagebox
import dimension_gui as dimgui
import boundary_gui as bdygui
import drawing as draw 
def run():
	"""Runs the GPLAN program

	Args:
		None

    Returns:
        void

    """
	def printe(string):
		"""Prints string on the console

		Args:
			string
			
	    Returns:
	        void

	    """
		gclass.textbox.insert('end',string)
		gclass.textbox.insert('end',"\n")

	warnings.filterwarnings("ignore") #Remove warnings that appear on the terminal
	gclass = gui.gui_class() 

	while (gclass.command!="end"):
		G = ptpg.PTPG(gclass.value)
		if ( gclass.command =="checker"):
			check.checker(G,gclass.textbox)
		else:
			# printe("\nEdge Set")
			# printe(G.graph.edges())
			frame = tk.Frame(gclass.root)
			frame.grid(row=2,column=1)
			if (gclass.command == "circulation"):
				m =len(G.graph)
				spanned = circulation.BFS(G.graph)
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
				C.create_single_dual(1,gclass.pen,gclass.textbox)

			elif(gclass.command == "single"):
				test_result = checker.gui_checker(G)
				if(not test_result[0]):
					messagebox.showerror("Invalid Graph", "Graph is not planar")
				# elif(not test_result[1]):
				# 	messagebox.showerror("Invalid Graph", "Graph is not triangular")
				# elif(not test_result[2]):
				# 	messagebox.showerror("Invalid Graph", "Graph is not biconnected")
				else:
					try: 
						if(G.dimensioned == 0):
							G.create_single_dual(1,gclass.pen,gclass.textbox)
							draw.draw_rdg(G,1,gclass.pen,G.to_be_merged_vertices,G.rdg_vertices,1,gclass.value[6],[])
						else:
							if(not checker.rfp_checker(G.matrix)):
								G.create_single_dual(2,gclass.pen,gclass.textbox)
								draw.draw_rdg(G,1,gclass.pen,G.to_be_merged_vertices,G.rdg_vertices,2,gclass.value[6],gclass.value[5])
								messagebox.showinfo("Orthogonal Floor Plan","The input graph has an orthogonal floorplan.Rooms with red boundary are the additional rooms which will be added but later merged.Please provide dimensions for the extra rooms as well.")
								G.width_min,G.width_max,G.height_min,G.height_max= dimgui.gui_fnc(G.original_node_count+len(G.to_be_merged_vertices))
								gclass.pen.clear()
								G.create_single_floorplan(gclass.pen,gclass.textbox,1)
								draw.draw_rdg(G,1,gclass.pen,G.to_be_merged_vertices,G.rdg_vertices,0,gclass.value[6],gclass.value[5])
							else:
								G.width_min,G.width_max,G.height_min,G.height_max = dimgui.gui_fnc(G.node_count)
								G.create_single_floorplan(gclass.pen,gclass.textbox,0)
								draw.draw_rdg(G,1,gclass.pen,G.to_be_merged_vertices,G.rdg_vertices,0,gclass.value[6],gclass.value[5])
					except:
						printe("Biconnectivity and Triangularity led to non-K4 separating triangle")
			elif(gclass.command == "multiple"):
				test_result = checker.gui_checker(G)
				if(not test_result[0]):
					messagebox.showerror("Invalid Graph", "Graph is not planar")
				# elif(not test_result[1]):
				# 	messagebox.showerror("Invalid Graph", "Graph is not triangular")
				# elif(not test_result[2]):
				# 	messagebox.showerror("Invalid Graph", "Graph is not biconnected")
				else:
			# 		print(G.original_node_count)
			# 		G.user_boundary_constraint,G.user_corner_constraint = bdygui.gui_fnc(G.node_count)
					if(G.dimensioned == 0):
						G.create_multiple_dual(1,gclass.pen,gclass.textbox)
					else:
						G.width_min,G.width_max,G.height_min,G.height_max = dimgui.gui_fnc(G.node_count)
						G.create_multiple_floorplan(gclass.pen,gclass.textbox,0)

		gclass.root.wait_variable(gclass.end)
		gclass.graph_ret()
		gclass.ocan.add_tab()

		# gclass.ocan.tscreen.resetscreen()
		gclass.pen = gclass.ocan.getpen()
		gclass.pen.speed(100000)

if __name__ == "__main__":
	run()