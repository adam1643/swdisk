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

while g.event_handler():
    pass

g.window.close()
