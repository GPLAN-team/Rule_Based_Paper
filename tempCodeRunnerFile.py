G.create_single_dual(1,gclass.pen,gclass.textbox)
						draw.draw_rdg(G,1,gclass.pen,G.to_be_merged_vertices,G.rdg_vertices,1,gclass.value[6],[])


						W = ptpg.PTPG(gclass.value)
						if not trng.Check_Chordality(W.graph, 0) and W.triangulation_type == "wall":
							# gclass.graph_ret()
							gclass.ocan.add_tab()

							# gclass.ocan.tscreen.resetscreen()
							gclass.pen = gclass.ocan.getpen()
							gclass.pen.speed(100000)

							W.create_single_dual(1,gclass.pen,gclass.textbox, "wall")
							draw.draw_rdg(W,1,gclass.pen,W.to_be_merged_vertices,W.rdg_vertices,1,gclass.value[6],[])
							
