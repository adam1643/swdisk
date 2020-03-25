from nonogram import Nonogram
from gui import GUI

# init game and load test puzzle
game = Nonogram()
game.load_from_file('test.txt')

# init GUI
g = GUI(game=game)
g.set_layout()
g.reload()
g.redraw_hints(game.rows, game.cols)
g.redraw()

# loop for event handling of GUI
while g.event_handler():
    pass

g.window.close()
