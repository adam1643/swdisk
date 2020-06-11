import unittest
from solver_random import SolverRandom
import numpy as np
from nonogram import Nonogram


class TestSolverRandom(unittest.TestCase):
    def test_parser(self):
        game = Nonogram()
        solver = SolverRandom(game)

        hints = [1, 3]
        b, w = sum(hints), 6
        row = solver.get_correct_row(hints, w, b)
        print(row)
