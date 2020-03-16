import PySimpleGUI as sg
import numpy as np
from nonogram import Nonogram
from gui import GUI

game = Nonogram()
game.load_from_file('test.txt')


g = GUI(game=game)
g.set_layout()
g.reload(game.width, game.height)

g.redraw_hints(game.rows, game.cols)
g.redraw()

while True:
    event, values = g.window.read()
    if event in (None, 'Exit'):
        break
    if event in ('Check'):
        game.check_solution()
    if event in ('_FILEBROWSE_'):
        filename = values['_FILEBROWSE_']
        g.reload(game.width, game.height)
        g.redraw_hints(game.rows, game.cols)
        g.redraw()

    mouse = values['-GRAPH-']
    if event == '-GRAPH-':
        if mouse == (None, None):
            continue
        box_x = mouse[1]//g.BOX_WIDTH
        box_y = mouse[0]//g.BOX_HEIGHT
        if game.board[box_x][box_y] == 0:
            game.board[box_x][box_y] = 1
            g.change_box(box_x, box_y)
        else:
            game.board[box_x][box_y] = 0
            g.change_box(box_x, box_y)

g.window.close()
