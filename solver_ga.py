from random import randint, random, shuffle
import numpy as np


class SolverGA:
    def __init__(self, game):
        self.game = game    # object of Nonogram class
        self.finished = False
        self.solved = False

        self.fit_unchanged_count = 0
        self.mass_mutations_count = 0
        self.reset_count = 0
        self.generation = 0

        self.pool_size = 50

        self.solutions = []

        self.last_fitness = -1

        self.all_fitnesses = []
        self.all_counts = []

    def solve(self):
        """Method for solving Nonograms. If time consuming, should be run in another thread"""
        self.init_solver()
        while True:
            if not self.finished:
                if self.fit_unchanged_count >= 300:
                    self.mass_mutate()
                    self.mass_mutations_count += 1
                    self.fit_unchanged_count = 0
                    print("mass mutated!")

            if self.mass_mutations_count >= 8:
                self.reset()
                self.reset_count += 1
                print("reset")
                self.mass_mutations_count = 0

            if self.reset_count >= 3:
                self.finished = True
                self.solved = False
                print("CANNOT SOLVE!")
                return

            self.evolve()
            best_solution = self.get_best_solution()

            if best_solution.fitness == self.last_fitness:
                self.fit_unchanged_count += 1
            else:
                self.fit_unchanged_count = 0
                self.last_fitness = best_solution.fitness
                self.game.board = self.get_best_solution().board

            # print(best_solution.fitness)

            if best_solution.fitness == 0:
                self.finished = True
                self.solved = True
                print("best fitness", best_solution.fitness)
                print("best solution", best_solution.board)
                return

            if self.is_converged():
                self.finished = True
                self.solved = False
                return

    def init_solver(self):
        self.rows = self.game.height
        self.columns = self.game.width
        self.solutions = []

        for i in range(self.pool_size):
            solution = Solution(self.rows, self.columns)
            self.solutions.append(solution)

        self.calculate_fitness()

    def mass_mutate(self):
        for solution in self.solutions:
            if self.get_best_solution() != solution:
                # print("before", solution.board)
                # print('shuffled')
                solution.shuffle()
                # print("after", solution.board)
            else:
                print("best not mutate!")

    def reset(self):
        self.solutions = []
        for i in range(self.pool_size):
            solution = Solution(self.rows, self.columns)
            self.solutions.append(solution)
        self.calculate_fitness()

    def is_converged(self):
        fitness = self.solutions[0].fitness

        for solution in self.solutions:
            if solution.fitness != fitness:
                return False

        return True

    def evolve(self):
        new_solutions = []
        new_solutions.append(self.get_best_solution())
        for _ in range(len(self.solutions) - 1):
            parent_a = self.tour_select()
            parent_b = self.tour_select()
            child = self.crossover(parent_a, parent_b)
            child.mutate()
            new_solutions.append(child)
            # print(child.board)

        shuffle(new_solutions)
        self.solutions = new_solutions

        self.calculate_fitness()
        self.generation += 1

    def tour_select(self):
        # tournament = shuffle(self.solutions)[:5]
        sorted = self.solutions.copy()
        # shuffle(sorted)
        # sorted = sorted[:10]
        sorted.sort(key=lambda x: x.fitness)
        # print("sorted", sorted[0].board)
        # print("tour", sorted[0].board)
        # print("fitt", sorted[0].fitness)
        return sorted[randint(0, 2)]

    def crossover(self, parent_a, parent_b):
        board_a = parent_a.board.flatten()
        board_b = parent_b.board.flatten()

        board = []
        for i in range(len(board_a)):
            if random() < 0.5:
                board.append(board_a[i])
            else:
                board.append(board_b[i])

        child = Solution(self.rows, self.columns)
        child.set_flatten_board(board)
        return child

    def calculate_fitness(self):
        for solution in self.solutions:
            solution.calculate_fitness(self.game.rows, self.game.cols)
            if solution.fitness not in self.all_fitnesses:
                self.all_fitnesses.append(solution.fitness)
                self.all_counts.append(1)
            else:
                self.all_counts[self.all_fitnesses.index(solution.fitness)] += 1

    def get_best_solution(self):
        sorted_solutions = self.solutions.copy()
        sorted_solutions.sort(key=lambda x: x.fitness)
        # print("best fitness", sorted_solutions[0].fitness)
        return sorted_solutions[0]


class Solution:
    def __init__(self, rows, cols):
        self.fitness = 0

        self.rows = rows
        self.cols = cols
        self.board = np.zeros((self.rows, self.cols), dtype=int)

        for i in range(self.rows):
            for j in range(self.cols):
                if random() < 0.6:
                    self.board[i][j] = 1

    def set_flatten_board(self, board):
        self.board = np.zeros((self.rows, self.cols), dtype=int)
        # print("board", board, self.rows, self.cols)
        idx = 0
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = board[idx]
                idx += 1

    def mutate(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if random() < 0.1:
                    if self.board[i][j] == 1:
                        self.board[i][j] = 0
                    else:
                        self.board[i][j] = 1

    def prepare_line(self, line):
        data = []
        index = 0
        while index < len(line):
            tmp = 0
            while index < len(line) and line[index] == 1:
                tmp += 1
                index += 1
            if tmp > 0:
                data.append(tmp)
            index += 1
        return np.array(data, dtype=int)

    def calculate_fitness(self, row_hints, col_hints):
        fitness = 0
        # print(self.board)
        for i in range(self.rows):
            fitness += self.calculate_difference(row_hints[i], self.prepare_line(self.board[i]))

        for i in range(self.cols):
            fitness += self.calculate_difference(col_hints[i], self.prepare_line(self.board[:, i]))

        self.fitness = fitness

    def calculate_difference(self, arr1, arr2):
        arr1 = list(arr1)
        arr2 = list(arr2)
        while len(arr1) > len(arr2):
            arr2.append(0)

        while len(arr2) > len(arr1):
            arr1.append(0)

        score = 0
        for a, b in zip(arr1, arr2):
            score += abs(a-b)
        return score

    def shuffle(self):
        flat = self.board.flatten()
        shuffle(flat)
        self.set_flatten_board(flat)


