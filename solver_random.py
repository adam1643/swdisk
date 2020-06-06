from utils import timer, DEFAULT_TIMEOUT
from random import randint
import numpy as np
import threading


class SolverRandom:
    def __init__(self, game):
        self.game = game    # object of Nonogram class=

    def solve(self, stop=None, game_id=None, queue=None):
        """Method for solving Nonograms. If time consuming, should be run in another thread"""
        event = threading.Event()
        threading.Thread(target=timer, args=(event, stop if stop is not None else DEFAULT_TIMEOUT), daemon=True).start()

        while not event.is_set() and not self.game.check_solution():
            for index in range(self.game.height):
                row = self.game.get_board_row(index)
                hints = self.game.get_hints_row(index)
                if np.array_equal(self.game.prepare_line(row), np.array(hints, dtype=int)):
                    continue

                row = self.get_correct_row(hints, self.game.width - sum(hints), sum(hints))
                for idx in range(len(row)):
                    self.game.set_board_tile(idx, index, row[idx])

            for index in range(self.game.width):
                col = self.game.get_board_column(index)
                hints = self.game.get_hints_column(index)
                if np.array_equal(self.game.prepare_line(col), np.array(hints, dtype=int)):
                    continue

                col = self.get_correct_row(hints, self.game.height - sum(hints), sum(hints))
                for idx in range(len(col)):
                    self.game.set_board_tile(index, idx, col[idx])

        if game_id is not None:
            queue.append(['result', [game_id, self.game.check_solution()]])

    def random_permutation(self, white, black):
        row = [0 for _ in range(white)] + [1 for _ in range(black)]
        return np.random.permutation(row)

    def get_correct_row(self, hints, white, black):
        while True:
            row = self.random_permutation(white, black)
            if np.array_equal(self.game.prepare_line(row), np.array(hints, dtype=int)):
                return row
