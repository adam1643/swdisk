import PySimpleGUI as sg
import numpy as np
from nonogram import Nonogram
from gui import GUI

game = Nonogram()
game.load_from_file('test.txt')


g = GUI(game=game)
g.set_layout()
g.reload()

g.redraw_hints(game.rows, game.cols)
g.redraw()

stored_size = (0, 0)

while True:
    event, values = g.window.read()
    if stored_size != g.window.Size:
        print(stored_size)
        # stored_size = g.window.Size
        stored_size = g.change_size(g.window.Size[0], g.window.Size[1])
        continue
    print(values)
    if event in (None, 'Exit'):
        break
    if event in ('Check'):
        game.check_solution()
    if event in ('-FILEBROWSE-'):
        filename = values['-FILEBROWSE-']
        game.load_from_file(filename)
        g.reload()
        g.redraw_hints(game.rows, game.cols)
        g.redraw()

    mouse = values['-GRAPH-']
    if event == '-GRAPH-':
        # x = g.window['-GRAPH-'].get_size()
        # # print("graph size", x)
        # x = g.window.Size
        # # g.window['-GRAPH-'].set_size((300, 300))
        # g.change_size(300, 300)
        # print("window size", x)
        if mouse == (None, None):
            continue
        box_x = mouse[1]//g.BOX_HEIGHT
        box_y = mouse[0]//g.BOX_WIDTH
        print(box_x, box_y)
        if game.board[box_x][box_y] == 0:
            game.board[box_x][box_y] = 1
            g.change_box(box_x, box_y)
        else:
            game.board[box_x][box_y] = 0
            g.change_box(box_x, box_y)

g.window.close()
