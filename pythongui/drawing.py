"""Drawing Module

"""
import networkx as nx
import numpy as np
import turtle
# import ptpg
import source.floorplangen.dual as dual
import math
# import source.polygonal.poly as poly
# from source.polygonal.draw import DrawOuterBoundary

scale = 300
origin = {'x': 300, 'y': -150}


def find_points(x1, y1, x2, y2,
                x3, y3, x4, y4):
    x7 = max(x1, x3)
    y8 = max(y1, y3)
    x8 = min(x2, x4)
    y7 = min(y2, y4)
    first_rect = ""
    second_rect = ""
    if (x7 == x8):
        if (x7 == x2):
            first_rect = "right"
            second_rect = "left"
        elif (x7 == x1):
            first_rect = "left"
            second_rect = "right"
    if (y7 == y8):
        if (y7 == y2):
            first_rect = "top"
            second_rect = "bottom"
        elif (y7 == y1):
            first_rect = "bottom"
            second_rect = "top"

    return [(x7, y7), (x8, y8)], first_rect, second_rect


# Draw rectangular dual of graph

def draw_grid(pen, scale, coord):
    pen.setpos(-100, -100)
    pen.speed(0)
    pen.left(90)
    pen.width(2)
    pen.color("aliceblue")
    # {-200,-300}, passing through this point
    limit = 40
    grid_size = scale
    left_grid = 15
    for i in range(-left_grid, limit+1):
        pen.up()
        pen.setpos(coord[0]+grid_size*(i), coord[1]-grid_size*(left_grid))
        pen.down()

        # line
        pen.forward((limit+left_grid)*grid_size)

    pen.right(90)
    for i in range(-left_grid, limit):
        pen.up()
        pen.setpos(coord[0]-grid_size*(left_grid), coord[1]+grid_size*(i))
        pen.down()

        # line
        pen.forward((limit+left_grid)*grid_size)


def draw_rdg(graph_data, count, pen, mode, color_list, room_names, origin):
    coordinates = {}
    for i in range(graph_data['room_x'].shape[0]):
        data = []
        data.append([(graph_data['room_x'][i], graph_data['room_y'][i]),
                     (graph_data['room_x'][i] + graph_data['room_width'][i], graph_data['room_y'][i])])
        data.append([(graph_data['room_x'][i] + graph_data['room_width'][i], graph_data['room_y'][i]),
                     (graph_data['room_x'][i] + graph_data['room_width'][i], graph_data['room_y'][i] + graph_data['room_height'][i])])
        data.append([(graph_data['room_x'][i] + graph_data['room_width'][i], graph_data['room_y'][i] + graph_data['room_height'][i]),
                     (graph_data['room_x'][i], graph_data['room_y'][i] + graph_data['room_height'][i])])
        data.append([(graph_data['room_x'][i], graph_data['room_y'][i] + graph_data['room_height'][i]),
                     (graph_data['room_x'][i], graph_data['room_y'][i])])
        coordinates[i] = data

    for i in range(len(graph_data['mergednodes'])):
        node_1 = graph_data['mergednodes'][i]
        node_2 = graph_data['irreg_nodes'][i]
        common_points, first_room_dir, second_room_dir = find_points(graph_data['room_x'][node_1],
                                                                     graph_data['room_y'][node_1],
                                                                     graph_data['room_x'][node_1] +
                                                                     graph_data['room_width'][node_1],
                                                                     graph_data['room_y'][node_1] +
                                                                     graph_data['room_height'][node_1],
                                                                     graph_data['room_x'][node_2],
                                                                     graph_data['room_y'][node_2],
                                                                     graph_data['room_x'][node_2] +
                                                                     graph_data['room_width'][node_2],
                                                                     graph_data['room_y'][node_2] + graph_data['room_height'][node_2])
        if (first_room_dir == 'bottom'):
            coordinates[node_1][0].append(common_points[0])
            coordinates[node_1][0].append(common_points[1])
        elif (first_room_dir == 'right'):
            coordinates[node_1][1].append(common_points[0])
            coordinates[node_1][1].append(common_points[1])
        elif (first_room_dir == 'top'):
            coordinates[node_1][2].append(common_points[0])
            coordinates[node_1][2].append(common_points[1])
        elif (first_room_dir == 'left'):
            coordinates[node_1][3].append(common_points[0])
            coordinates[node_1][3].append(common_points[1])

        if (second_room_dir == 'bottom'):
            coordinates[node_2][0].append(common_points[0])
            coordinates[node_2][0].append(common_points[1])
        elif (second_room_dir == 'right'):
            coordinates[node_2][1].append(common_points[0])
            coordinates[node_2][1].append(common_points[1])
        elif (second_room_dir == 'top'):
            coordinates[node_2][2].append(common_points[0])
            coordinates[node_2][2].append(common_points[1])
        elif (second_room_dir == 'left'):
            coordinates[node_2][3].append(common_points[0])
            coordinates[node_2][3].append(common_points[1])

    for i in coordinates:
        coordinates[i][0] = sorted(coordinates[i][0], key=lambda x: x[0])
        coordinates[i][1] = sorted(coordinates[i][1], key=lambda x: x[1])
        coordinates[i][2] = sorted(
            coordinates[i][2], key=lambda x: x[0], reverse=True)
        coordinates[i][3] = sorted(
            coordinates[i][3], key=lambda x: x[1], reverse=True)

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
    # top_y = (float)(max(list(graph_data['room_y'])))
    # bottom_y = (float)(min(list(graph_data['room_y'])) - height)
    # print(f"TOP Y : {top_y} , BOTTOM Y : {bottom_y}\n")
    # scale = 450/(top_y - bottom_y)

    # area_sum = (sum(list((graph_data['area']))))
    area_list = []
    # print("Length of graph data room x: ", len(graph_data['room_x']))
    # print("Graph data room x: ", graph_data['room_x'])
    # print("Length of graph data area: ", len(graph_data['area']))
    # print("Graph data area: ", graph_data['area'])
    for i in range(len(graph_data['area'])):
        try:
            dat = graph_data['area'][i].split(':')
            area_list.append(float(dat[-1]))
        except:
            area_list.append(graph_data['area'][i])

    area_sum = sum(area_list)
    scale = pow((300*400)/area_sum, 1/2)
    # print(f"\nGraph area: {graph_data['area']}")
    # scale = 150*(math.exp(-0.30*height+math.log(0.8)) + 0.1)
    # print("Scale: ", scale)
    # origin = {'x': graph_data[origin, 'y': -550}
    dim = [0, 0]
    origin = {'x': origin - 400, 'y': -300}
    for i in range(graph_data['room_x'].shape[0]):
        if graph_data['room_width'][i] == 0 or i in graph_data['extranodes']:
            continue
        if i in graph_data['mergednodes']:
            pen.fillcolor(
                color_list[graph_data['irreg_nodes'][graph_data['mergednodes'].index(i)]])
        else:
            pen.fillcolor(color_list[i])
        pen.begin_fill()
        for dir in range(4):
            for idx in range(len(coordinates[i][dir])):
                if (idx % 2 == 0):
                    pen.setposition(coordinates[i][dir][idx][0] * scale + origin['x'],
                                    coordinates[i][dir][idx][1] * scale + origin['y'])
                    pen.pendown()
                else:
                    pen.setposition(coordinates[i][dir][idx][0] * scale + origin['x'],
                                    coordinates[i][dir][idx][1] * scale + origin['y'])
                    pen.penup()

        pen.end_fill()
        if (graph_data['room_x'][i] + graph_data['room_width'][i] > dim[0]):
            dim[0] = graph_data['room_x'][i] + graph_data['room_width'][i]
        if (graph_data['room_y'][i] + graph_data['room_height'][i] > dim[1]):
            dim[1] = graph_data['room_y'][i] + graph_data['room_height'][i]
    x_index = int(np.where(graph_data['room_x']
                  == np.min(graph_data['room_x']))[0][0])
    y_index = int(np.where(graph_data['room_y']
                  == np.max(graph_data['room_y']))[0][0])
    pen.setposition((graph_data['room_x'][x_index]) * scale + origin['x'], (graph_data['room_y']
                    [y_index] + graph_data['room_height'][y_index]) * scale + origin['y'] + 200)
    # pen.write(count, font=("Arial", 20, "normal"))
    pen.penup()

    # Grid

    # pen.setpos(-100, -100)
    # pen.speed(500)
    # pen.left(90)
    # pen.width(2)
    # pen.color("springgreen")
    # # {-200,-300}, passing through this point
    # limit = 40
    # grid_size = scale
    # left_grid = 5
    # for i in range(-left_grid, limit+1):
    #     pen.up()
    #     pen.setpos(-200+grid_size*(i), -300-grid_size*(left_grid))
    #     pen.down()

    #     # line
    #     pen.forward((limit+left_grid)*grid_size)

    # pen.right(90)
    # for i in range(-left_grid, limit):
    #     pen.up()
    #     pen.setpos(-200-grid_size*(left_grid), -300+grid_size*(i))
    #     pen.down()

    #     # line
    #     pen.forward((limit+left_grid)*grid_size)

    # print("AREA: ", graph_data['area'])
    for i in range(len(graph_data['area'])):
        try:
            dat = graph_data['area'][i].split(':')
            area = dat[-1]
        except:
            area = graph_data['area'][i]
        if i in graph_data['extranodes']:
            continue
        pen.color('black')
        if (i not in graph_data['mergednodes']):
            pen.penup()
            pen.setposition(((2 * graph_data['room_x'][i]) * scale / 2) + origin['x'] + 5,
                            ((2 * graph_data['room_y'][i] + graph_data['room_height'][i]) * scale / 2) + origin['y'])
            pen.write(room_names[i], font=("Arial", 14, "normal"))
            pen.color('darkred')
            pen.setposition(((2 * graph_data['room_x'][i]) * scale / 2) + origin['x'] + 5,
                            ((2 * graph_data['room_y'][i] + graph_data['room_height'][i]) * scale / 2) + origin['y']-20)

            pen.write(f"({str(area)})", font=("Arial", 14, "normal"))

        if (i in graph_data['mergednodes'] and mode == 2):
            pen.penup()

            pen.setposition(((2 * graph_data['room_x'][i]) * scale / 2) + origin['x'] + 5,
                            ((2 * graph_data['room_y'][i] + graph_data['room_height'][i]) * scale / 2) + origin['y'])
            pen.write(room_names[i], font=("Arial", 14, "normal"))
            pen.setposition(((2 * graph_data['room_x'][i]) * scale / 2) + origin['x'] + 5,
                            ((2 * graph_data['room_y'][i] + graph_data['room_height'][i]) * scale / 2) + origin['y']-20)
            pen.color('darkred')
            pen.write(str(area), font=("Arial", 14, "normal"))
    # value = 1
    # if (len(graph_data['area']) != 0):
    #     pen.setposition(dim[0] * scale + origin['x']-650,
    #                     dim[1] * scale + origin['y']-30)
    #     pen.write('Area of Each Room', font=("Arial", 20, "normal"))
    #     for i in range(0, len(graph_data['area'])):
    #         if i in graph_data['extranodes']:
    #             continue
    #         pen.setposition(dim[0] * scale + origin['x']-650,
    #                         dim[1] * scale + origin['y']-30-value*30)
    #         pen.write('Room ' + str(i) + ': ' +
    #                   str(graph_data['area'][i]), font=("Arial", 15, "normal"))
    #         pen.penup()
    #         value += 1
    return scale, [coordinates[0][0][0][0] * scale + origin['x'], coordinates[0][0][0][1] * scale + origin['y']]


def draw_poly(graph_data, count, pen, mode, color_list, room_names, origin, outer_boundary, shape):
    innerBoundary = []
    if (outer_boundary != []):  # To take active front as input first in the drawing
        temp = outer_boundary[0]
        for i in range(0, len(outer_boundary)):
            corner = []
            if i == 0:
                corner.append(outer_boundary[i][2])
                corner.append(outer_boundary[i][3])
            else:
                corner.append(outer_boundary[i][2])
                corner.append(2*outer_boundary[0][3] - outer_boundary[i][3])
            innerBoundary.append(corner)
        corner1 = []
        corner1.append(outer_boundary[0][0])
        corner1.append(outer_boundary[0][1])
        innerBoundary.append(corner1)

    db = poly.dissected(graph_data, pen, color_list, shape, innerBoundary)
    # obj = DrawOuterBoundary(graph_data,pen,color_list)
