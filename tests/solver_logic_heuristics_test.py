import unittest
from solver_logic_heuristics import SolverLogicHeuristics
import numpy as np
from nonogram import Nonogram


class TestSolverLogicHeuristics(unittest.TestCase):
    def test_parser(self):
        game = Nonogram
        solver = SolverLogicHeuristics(game)

        # hints = [2, 3, 3]
        # line = [0 for _ in range(12)]
        # # print(solver.insert_line(line, 0, 4))
        # # print(solver.insert_line(line, 3, 4))
        # solver.subprocedure_1(line, hints)
        # print(line)


        # hints = [2, 3, 3]
        # line = [1,1,0,0,1,0,0,0,1,1]
        # print(solver.is_line_possible(line, hints))
        #
        #
        # hints = [3, 2]
        # line = [0 for _ in range(10)]
        # line[2] = -1
        # solver.subprocedure_2(line, hints)
        # print(line)

        # solver.subprocedure_1(line, hints)
        # print("Line", line)

        # hints = [3, 2]
        # line = [0 for _ in range(10)]
        # line[7] = 1
        # a, b = solver.prepare_edge_cases(line, hints)
        # print("edge cases", a, b)
        #
        # hints = [7, 4]
        # line = [0 for _ in range(30)]
        # line[2] = 1
        # line[3] = 1
        # line[7] = 1
        # solver.subprocedure_1(line, hints)
        # print(line)








        # hints = [4]
        # size = 20
        # line = [0 for _ in range(size)]
        # # line[3] = 1
        # # line[5] = 1
        # # line[15] = 1
        # left_most = solver.prepare_left_most(line, hints)
        # print("From left:", left_most)
        # #
        # right_most = solver.prepare_left_most(list(reversed(line)), list(reversed(hints)))
        # right_most = list(reversed([(size - b - 1, size - a - 1) for a, b in right_most]))
        # print("From right:", right_most)
        # print("Answer", solver.prepare_edge_cases(line, hints))
        #
        # print("Before: ", line)
        # solver.subprocedure_2(line, hints)
        # print("After:  ", line)
        #
        # hints = [4,4]
        # line = [0 for _ in range(size)]
        # line[0] = 1
        # line[18] = -1
        # line[17] = 1
        # print("Before: ", line)
        # solver.subprocedure_1(line, hints)
        # solver.subprocedure_2(line, hints)
        # print("After:  ", line)
        #
        #
        # # line = [0 for _ in range(size)]
        # line = [1, 1, 1, 1, 1, 0, 1, -1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0]
        # hints = [5, 1, 3, 5]
        # solver.subprocedure_2(line, hints)
        # print("Sub1", line)
        #
        # line = [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # hints = [6]
        # solver.subprocedure_2(line, hints)
        # print("sub2", line)
        #
        # # line = [0, 0, 1, 1, 1, 1, 1, 1, -1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0]
        # # hints = [8, 1, 7]
        # print("--------------")
        # print("--------------")
        # hints = [7, 1, 8]
        # line = [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, -1, 1, 1, 1, 1, 1, 1, 0, 0]
        # solver.subprocedure_1(line, hints)
        # print("edge", solver.prepare_edge_cases(line, hints))
        # print("sub1", line)

        print("--------------")
        print("--------------")
        print("--------------")
        print("--------------")
        hints = [1, 2, 1, 2]
        line = [0, 0, 0, 0, 0, -1, 0, 0, 0, 1, 1, -1, 1, 0, -1, 0, 0, 0, 0, 0]
        print('edges', solver.prepare_edge_cases(line, hints))