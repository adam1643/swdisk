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
text = None
# sg.popup('Results', 'The value returned from PopupGetText', text)

while g.event_handler():
    pass
    # event, values = g.window.read()
    # if event in (None, 'Exit'):
    #     break
    # if stored_size != g.window.Size:
    #     stored_size = g.change_size(g.window.Size[0], g.window.Size[1])
    #     continue
    #
    # if event in ('Check'):
    #     game.check_solution()
    #     text = sg.popup_get_text('Title', 'Please input something')
    # if event in ('-FILEBROWSE-'):
    #     filename = values['-FILEBROWSE-']
    #     game.load_from_file(filename)
    #     g.reload()
    #     g.redraw_hints(game.rows, game.cols)
    #     g.redraw()
    #
    # if event == '-GRAPH-':
    #     mouse = values['-GRAPH-']
    #     if mouse == (None, None):
    #         continue
    #     box_x = mouse[1] // g.BOX_HEIGHT
    #     box_y = mouse[0] // g.BOX_WIDTH
    #     # check/uncheck box
    #     if game.board[box_x][box_y] == 0:
    #         game.board[box_x][box_y] = 1
    #         g.update_box(box_x, box_y)
    #     else:
    #         game.board[box_x][box_y] = 0
    #         g.update_box(box_x, box_y)

g.window.close()
