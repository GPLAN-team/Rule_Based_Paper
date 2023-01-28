"""Drawing Module

"""
import networkx as nx
import numpy as np
import turtle
# import ptpg
import source.floorplangen.dual as dual
import math

scale = 300
origin = {'x': 300, 'y': -150}

# Draw rectangular dual of graph


def draw_rdg(graph_data, count, pen, mode, color_list, room_names, origin):
    pen.width(1.5)
    pen.color('black')
    pen.hideturtle()
    pen.penup()
    width = np.amax(graph_data['room_width'])
    height = np.amax(graph_data['room_height'])
    if (width == 0):
        width = 1
    if (height == 0):
        height = 1
    if (width < height):
        width = height
    scale = 200*(math.exp(-0.30*width+math.log(0.8)) + 0.1)
    # origin = {'x': graph_data[origin, 'y': -550}
    dim = [0, 0]
    origin = {'x': origin - 400, 'y': -100}
    for i in range(graph_data['room_x'].shape[0]):
        if graph_data['room_width'][i] == 0 or i in graph_data['extranodes']:
            continue
        if i in graph_data['mergednodes']:
            pen.fillcolor(
                color_list[graph_data['irreg_nodes'][graph_data['mergednodes'].index(i)]])
        else:
            pen.fillcolor(color_list[i])
        pen.begin_fill()
        pen.setposition(graph_data['room_x'][i] * scale + origin['x'],
                        graph_data['room_y'][i] * scale + origin['y'])

        pen.pendown()

        pen.setposition((graph_data['room_x_bottom_left'][i]) * scale + origin['x'],
                        graph_data['room_y'][i] * scale + origin['y'])

        pen.penup()

        pen.setposition((graph_data['room_x_bottom_right'][i]) * scale + origin['x'],
                        graph_data['room_y'][i] * scale + origin['y'])

        pen.pendown()

        pen.setposition((graph_data['room_x'][i] + graph_data['room_width'][i]) * scale + origin['x'],
                        (graph_data['room_y'][i]) * scale + origin['y'])
        pen.setposition((graph_data['room_x'][i] + graph_data['room_width'][i]) * scale + origin['x'],
                        (graph_data['room_y_right_bottom'][i]) * scale + origin['y'])

        pen.penup()

        pen.setposition((graph_data['room_x'][i] + graph_data['room_width'][i]) * scale + origin['x'],
                        (graph_data['room_y_right_top'][i]) * scale + origin['y'])

        pen.pendown()

        pen.setposition((graph_data['room_x'][i] + graph_data['room_width'][i]) * scale + origin['x'],
                        (graph_data['room_y'][i] + graph_data['room_height'][i]) * scale + origin['y'])
        pen.setposition((graph_data['room_x_top_right'][i]) * scale + origin['x'],
                        (graph_data['room_y'][i] + graph_data['room_height'][i]) * scale + origin['y'])

        pen.penup()

        pen.setposition((graph_data['room_x_top_left'][i]) * scale + origin['x'],
                        (graph_data['room_y'][i] + graph_data['room_height'][i]) * scale + origin['y'])

        pen.pendown()

        pen.setposition((graph_data['room_x'][i]) * scale + origin['x'],
                        (graph_data['room_y'][i] + graph_data['room_height'][i]) * scale + origin['y'])
        pen.setposition((graph_data['room_x'][i]) * scale + origin['x'],
                        (graph_data['room_y_left_top'][i]) * scale + origin['y'])

        pen.penup()

        pen.setposition((graph_data['room_x'][i]) * scale + origin['x'],
                        (graph_data['room_y_left_bottom'][i]) * scale + origin['y'])

        pen.pendown()

        pen.setposition(graph_data['room_x'][i] * scale + origin['x'],
                        graph_data['room_y'][i] * scale + origin['y'])
        pen.penup()
        pen.end_fill()

        x_index = int(
            np.where(graph_data['room_x'] == np.min(graph_data['room_x']))[0][0])
        y_index = int(
            np.where(graph_data['room_y'] == np.max(graph_data['room_y']))[0][0])
        pen.setposition((graph_data['room_x'][x_index]) * scale + origin['x'], (graph_data['room_y']
                        [y_index] + graph_data['room_height'][y_index]) * scale + origin['y'] + 200)

        pen.write(count, font=("Arial", 20, "normal"))
        pen.penup()
        if (graph_data['room_x'][i] + graph_data['room_width'][i] > dim[0]):
            dim[0] = graph_data['room_x'][i] + graph_data['room_width'][i]
        if (graph_data['room_y'][i] + graph_data['room_height'][i] > dim[1]):
            dim[1] = graph_data['room_y'][i] + graph_data['room_height'][i]

    # pen.setposition(0* scale + origin['x'], 0 * scale + origin['y'])
    # pen.pendown()
    # pen.setposition(dim[0]* scale + origin['x'], 0 * scale + origin['y'])
    # pen.setposition(dim[0]* scale + origin['x'], dim[1]* scale + origin['y'])
    # pen.setposition(0* scale + origin['x'], dim[1]* scale + origin['y'])
    # pen.setposition(0* scale + origin['x'], 0 * scale + origin['y'])
    # pen.penup()
    # if mode == 2:
    #     for i in graph_data['mergednodes']:
    #         pen.color('red')
    #         pen.setposition(graph_data[room_x[i] * scale + origin['x'], graph_data[room_y[i] * scale + origin['y'])

    #         pen.pendown()
    #         pen.setposition((graph_data[room_x[i] + graph_data[room_width[i]) * scale + origin['x'],
    #                             (graph_data[room_y[i]) * scale + origin['y'])
    #         pen.setposition((graph_data[room_x[i] + graph_data[room_width[i]) * scale + origin['x'],
    #                             (graph_data[room_y[i]+ graph_data[room_height[i]) * scale + origin['y'])
    #         pen.setposition((graph_data[room_x[i]) * scale + origin['x'],
    #                             (graph_data[room_y[i]+ graph_data[room_height[i]) * scale + origin['y'])
    #         pen.setposition((graph_data[room_x[i]) * scale + origin['x'],
    #                             (graph_data[room_y_left_top][i]) * scale + origin['y'])
    #         pen.setposition(graph_data[room_x][i] * scale + origin['x'], graph_data[room_y][i] * scale + origin['y'])
    #         pen.penup()
    for i in range(graph_data['room_x'].shape[0]):
        if i in graph_data['extranodes']:
            continue
        pen.color('black')
        if (i not in graph_data['mergednodes']):
            pen.setposition(((2 * graph_data['room_x'][i]) * scale / 2) + origin['x'] + 5,
                            ((2 * graph_data['room_y'][i] + graph_data['room_height'][i]) * scale / 2) + origin['y'])
            pen.write(room_names[i])
            pen.penup()
        if (i in graph_data['mergednodes'] and mode == 2):
            pen.setposition(((2 * graph_data['room_x'][i]) * scale / 2) + origin['x'] + 5,
                            ((2 * graph_data['room_y'][i] + graph_data['room_height'][i]) * scale / 2) + origin['y'])
            pen.write(room_names[i])
            pen.penup()

    value = 1
    if (len(graph_data['area']) != 0):

        pen.setposition(dim[0] * scale + origin['x']+50,
                        dim[1] * scale + origin['y']-30)
        pen.write('Area of Each Room', font=("Arial", 20, "normal"))
        for i in range(0, len(graph_data['area'])):
            if i in graph_data['extranodes']:
                continue
            pen.setposition(dim[0] * scale + origin['x']+50,
                            dim[1] * scale + origin['y']-30-value*30)
            pen.write('Room ' + str(i) + ': ' +
                      str(graph_data['area'][i]), font=("Arial", 15, "normal"))
            pen.penup()
            value += 1


def draw_rfp(graph, pen, count):
    pen.width(4)
    pen.color('black')
    pen.hideturtle()
    pen.penup()
    # scale = 75
    scale = 20
    origin = {'x': graph.origin, 'y': -400}
    for i in range(graph.room_x.shape[0]):
        if graph.room_width[i] == 0:
            continue
        pen.setposition(
            graph.room_x[i] * scale + origin['x'], graph.room_y[i] * scale + origin['y'])
        pen.pendown()
        pen.setposition((graph.room_x[i] + graph.room_width[i]) * scale + origin['x'],
                        graph.room_y[i] * scale + origin['y'])
        pen.setposition((graph.room_x[i] + graph.room_width[i]) * scale + origin['x'],
                        (graph.room_y[i] + graph.room_height[i]) * scale + origin['y'])
        pen.setposition(graph.room_x[i] * scale + origin['x'],
                        (graph.room_y[i] + graph.room_height[i]) * scale + origin['y'])
        pen.setposition(
            graph.room_x[i] * scale + origin['x'], graph.room_y[i] * scale + origin['y'])
        pen.penup()
        pen.setposition(((2 * graph.room_x[i]) * scale / 2) + origin['x'] + 5,
                        ((2 * graph.room_y[i] + graph.room_height[i]) * scale / 2) + origin['y'])
        pen.write(graph.room_names[i].get())
        pen.setposition(((2 * graph.room_x[i] + graph.room_width[i]) * scale / 2 - scale/2) + origin['x'],
                        ((2 * graph.room_y[i] + graph.room_height[i]) * scale / 2 - scale/2) + origin['y'])
        pen.write('( ' + str(round(graph.room_height[i], 2)) + ' x ' + str(
            round(graph.room_width[i], 2)) + ' )', font=('Times', 7))
        pen.penup()
        x_index = int(np.where(graph.room_x == np.min(graph.room_x))[0][0])
        y_index = int(np.where(graph.room_y == np.max(graph.room_y))[0][0])
        pen.setposition((graph.room_x[x_index]) * scale + origin['x'],
                        (graph.room_y[y_index] + graph.room_height[y_index]) * scale + origin['y'] + 200)
        pen.write(count, font=("Arial", 20, "normal"))
        pen.penup()


def draw_rdg_circulation(graph, count, pen, to_be_merged_vertices, orig):
    pen.width(1.5)
    # pen.color('white')
    pen.hideturtle()
    pen.penup()
    width = np.amax(graph.room_width)
    height = np.amax(graph.room_height)
    if (width == 0):
        width = 1
    if (height == 0):
        height = 1
    if (width < height):
        width = height
    scale = 70*(math.exp(-0.30*width+math.log(0.8)) + 0.1)
    # origin = {'x': graph.origin, 'y': -550}
    dim = [0, 0]
    origin = {'x': graph.origin - 400, 'y': -100}
    for i in range(graph.room_x.shape[0]):
        if (i not in to_be_merged_vertices):
            pen.color('white')
        else:
            pen.color(graph.node_color[i])
        if graph.room_width[i] == 0 or i in graph.biconnected_vertices:
            continue
        pen.fillcolor(graph.node_color[i])
        pen.begin_fill()
        pen.setposition(
            graph.room_x[i] * scale + origin['x'], graph.room_y[i] * scale + origin['y'])

        pen.pendown()

        pen.setposition((graph.room_x_bottom_left[i]) * scale + origin['x'],
                        graph.room_y[i] * scale + origin['y'])

        pen.penup()

        pen.setposition((graph.room_x_bottom_right[i]) * scale + origin['x'],
                        graph.room_y[i] * scale + origin['y'])

        pen.pendown()

        pen.setposition((graph.room_x[i] + graph.room_width[i]) * scale + origin['x'],
                        (graph.room_y[i]) * scale + origin['y'])
        pen.setposition((graph.room_x[i] + graph.room_width[i]) * scale + origin['x'],
                        (graph.room_y_right_bottom[i]) * scale + origin['y'])

        pen.penup()

        pen.setposition((graph.room_x[i] + graph.room_width[i]) * scale + origin['x'],
                        (graph.room_y_right_top[i]) * scale + origin['y'])

        pen.pendown()

        pen.setposition((graph.room_x[i] + graph.room_width[i]) * scale + origin['x'],
                        (graph.room_y[i] + graph.room_height[i]) * scale + origin['y'])
        pen.setposition((graph.room_x_top_right[i]) * scale + origin['x'],
                        (graph.room_y[i] + graph.room_height[i]) * scale + origin['y'])

        pen.penup()

        pen.setposition((graph.room_x_top_left[i]) * scale + origin['x'],
                        (graph.room_y[i] + graph.room_height[i]) * scale + origin['y'])

        pen.pendown()

        pen.setposition((graph.room_x[i]) * scale + origin['x'],
                        (graph.room_y[i] + graph.room_height[i]) * scale + origin['y'])
        pen.setposition((graph.room_x[i]) * scale + origin['x'],
                        (graph.room_y_left_top[i]) * scale + origin['y'])

        pen.penup()

        pen.setposition((graph.room_x[i]) * scale + origin['x'],
                        (graph.room_y_left_bottom[i]) * scale + origin['y'])

        pen.pendown()

        pen.setposition(
            graph.room_x[i] * scale + origin['x'], graph.room_y[i] * scale + origin['y'])
        pen.penup()
        pen.end_fill()
        if (i not in to_be_merged_vertices):
            pen.setposition(((2 * graph.room_x[i]) * scale / 2) + origin['x'] + 5,
                            ((2 * graph.room_y[i] + graph.room_height[i]) * scale / 2) + origin['y'])
            pen.write(graph.room_names[i])
            pen.penup()
        x_index = int(np.where(graph.room_x == np.min(graph.room_x))[0][0])
        y_index = int(np.where(graph.room_y == np.max(graph.room_y))[0][0])
        pen.setposition((graph.room_x[x_index]) * scale + origin['x'],
                        (graph.room_y[y_index] + graph.room_height[y_index]) * scale + origin['y'] + 200)

        pen.color('black')
        pen.write(count, font=("Arial", 20, "normal"))
        pen.penup()
        if (graph.room_x[i] + graph.room_width[i] > dim[0]):
            dim[0] = graph.room_x[i] + graph.room_width[i]
        if (graph.room_y[i] + graph.room_height[i] > dim[1]):
            dim[1] = graph.room_y[i] + graph.room_height[i]
        graph.origin += np.amax(graph.room_width)

    pen.setposition(0 * scale + origin['x'], 0 * scale + origin['y'])
    pen.pendown()
    pen.setposition(dim[0] * scale + origin['x'], 0 * scale + origin['y'])
    pen.setposition(dim[0] * scale + origin['x'], dim[1] * scale + origin['y'])
    pen.setposition(0 * scale + origin['x'], dim[1] * scale + origin['y'])
    pen.setposition(0 * scale + origin['x'], 0 * scale + origin['y'])
    pen.penup()

    value = 1
    if (len(graph.area) != 0):
        pen.setposition(origin['x'], origin['y']-100)
        pen.write('      Area', font=("Arial", 24, "normal"))
        for i in range(0, len(graph.area)):

            pen.setposition(origin['x'], origin['y']-100-value*30)
            pen.write('Room ' + str(i) + ': ' +
                      str(graph.area[i]), font=("Arial", 24, "normal"))
            pen.penup()
            value += 1
