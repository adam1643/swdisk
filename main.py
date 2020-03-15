import os
import PySimpleGUI as sg
import random
import string
import numpy as np
import ast  # for evaluating data loaded from file

from nonogram import Nonogram


game = Nonogram()
r = [[1], [1,1,1], [1], [1], [2,1]]
c = [[1, 1], [2], [1], [1,1,1], [1]]
game.init_game(5, 5, r, c)


# sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
WINDOW_SIZE_X = 300
WINDOW_SIZE_Y = 300
BOX_SIZE = WINDOW_SIZE_X//game.width
BOX_WIDTH = WINDOW_SIZE_X//game.width
BOX_HEIGHT = WINDOW_SIZE_Y//game.height

TIP_SIZE = 100


layout = [
    [sg.Text('Nonogram'), sg.Text('', key='-OUTPUT-')],
    [sg.Graph((TIP_SIZE + WINDOW_SIZE_X, TIP_SIZE), (0, TIP_SIZE), (TIP_SIZE + WINDOW_SIZE_X, 0), key='-COLUMNS-', change_submits=True, drag_submits=False)],
    [sg.Graph((TIP_SIZE, WINDOW_SIZE_Y), (0, WINDOW_SIZE_Y), (TIP_SIZE, 0), key='-ROWS-', change_submits=True, drag_submits=False),
     sg.Graph((WINDOW_SIZE_X, WINDOW_SIZE_Y), (0, WINDOW_SIZE_Y+10), (WINDOW_SIZE_X+10, 0), key='-GRAPH-',
              change_submits=True, drag_submits=False)],
    [sg.Button('Show'), sg.Button('Exit')]
]

window = sg.Window('Window Title', layout, finalize=True)
g = window['-GRAPH-']
ROWS = window['-ROWS-']
COLUMNS = window['-COLUMNS-']

board = [[None for _ in range(game.width)] for _ in range(game.height)]


def redraw_hints():
    for row_index, row in enumerate(game.rows):
        for index, num in enumerate(row):
            ROWS.draw_text('{}'.format(num if num > 0 else ""),
                           (BOX_WIDTH//2 + TIP_SIZE*(index/len(row)), BOX_HEIGHT//2 + row_index*BOX_HEIGHT),
                           text_location=sg.TEXT_LOCATION_CENTER)

    for col_index, col in enumerate(game.cols):
        for index, num in enumerate(col):
            COLUMNS.draw_text('{}'.format(num if num > 0 else ""),
                              (TIP_SIZE + BOX_WIDTH//2 + col_index*BOX_WIDTH, 10 + TIP_SIZE*(index/len(col))),
                              text_location=sg.TEXT_LOCATION_CENTER)


def redraw():

    for row in range(game.width):
        for col in range(game.height):
            if board[row][col] is not None:
                continue
            if game.board[row][col] == 0:
                board[row][col] = g.draw_rectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black')
            else:
                board[row][col] = g.draw_rectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color='black')

            # draw tile number in the tile
            # g.draw_text('{}'.format(row * game.height + col + 1),
            #             (col * BOX_SIZE + 10, row * BOX_SIZE + 8))


redraw()
redraw_hints()

while True:             # Event Loop
    event, values = window.read()
    # print(event, values)
    if event in (None, 'Exit'):
        break
    if event in ('Show'):
        game.check_solution()

    mouse = values['-GRAPH-']

    if event == '-GRAPH-':
        if mouse == (None, None):
            continue
        box_x = mouse[0]//BOX_SIZE
        box_y = mouse[1]//BOX_SIZE
        letter_location = (box_x * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
        # print(box_x, box_y)
        if game.board[box_y][box_x] == 0:
            game.board[box_y][box_x] = 1
            g.delete_figure(board[box_y][box_x])
            board[box_y][box_x] = None
            print(board[box_y][box_x])
        else:
            game.board[box_y][box_x] = 0
            print(board[box_y][box_x])
            g.delete_figure(board[box_y][box_x])
            board[box_y][box_x] = None

        redraw()

window.close()
