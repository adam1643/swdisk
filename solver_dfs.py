import time
from random import randint


class SolverDFS:
    def __init__(self, game):
        self.game = game    # object of Nonogram class

    def solve(self):
        """Method for solving Nonograms. If time consuming, should be run in another thread"""

        while True:
            x, y = randint(0, 4), randint(0, 4)
            self.game.board[x, y] = 1
            time.sleep(1)
