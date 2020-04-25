import unittest
from solver_logic_heuristics import SolverLogicHeuristics
import numpy as np


class TestSolverLogicHeuristics(unittest.TestCase):
    def test_parser(self):
        solver = SolverLogicHeuristics(None)

        hints = [2, 3, 3]
        line = [0 for _ in range(12)]
        # print(solver.insert_line(line, 0, 4))
        # print(solver.insert_line(line, 3, 4))
        solver.subprocedure_1(line, hints)
        print(line)

        # solver.subprocedure_1(line, hints)
        # print("Line", line)
