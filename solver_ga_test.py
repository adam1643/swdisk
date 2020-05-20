import unittest
from solver_ga import SolverGA, Solution
import numpy as np
from nonogram import Nonogram


class TestSolverGA(unittest.TestCase):
    def test_parser(self):
        game = Nonogram()
        # game.load_from_file('test.txt')
        game.load_from_db(4050)
        print(game.board, game.rows, game.cols)
        solver = SolverGA(game)
        solver.init_solver()

        solver.solve()
        if solver.finished:
            # print(solver.__dict__)
            print(solver.get_best_solution().board)
            print("generation", solver.generation)
            return


        print("best solution", solver.get_best_solution().board, "fitness", solver.get_best_solution().fitness)
        print("generation", solver.generation)
        print("all ftinesses", solver.all_fitnesses)
        print("all counts   ", solver.all_counts, sum(solver.all_counts))

    def test_solutions(self):
        sol = Solution(5, 5)
        game = Nonogram()
        game.load_from_file('test.txt')
        sol.calculate_fitness(game.rows, game.cols)
        print(sol.fitness)
        print("diff", sol.calculate_difference([1,1,1], [5]))
