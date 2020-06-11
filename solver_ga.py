from random import randint, random, shuffle
from utils import timer, DEFAULT_TIMEOUT
import numpy as np
import threading

POOL_SIZE = 50
MAX_CROSSOVERS_WITHOUT_MASS_MUTATE = 1000
MAX_MASS_MUTATIONS = 20
MAX_RESETS = 3


class SolverGA:
    def __init__(self, game, supporting=False):
        self.game = game    # object of Nonogram class
        self.finished = False
        self.solved = False

        self.rows = 0
        self.columns = 0

        self.fit_unchanged_count = 0
        self.mass_mutations_count = 0
        self.reset_count = 0
        self.generation = 0

        self.pool_size = POOL_SIZE

        self.solutions = []

        self.last_fitness = -1

        self.all_fitnesses = []
        self.all_counts = []

        self.supporting = supporting

        self.original_board = self.game.board

    def solve(self, stop=None, game_id=None, queue=None, algorithm=None):
        """Method for solving Nonograms. If time consuming, should be run in another thread"""
        event = threading.Event()
        threading.Thread(target=timer, args=(event, stop if stop is not None else DEFAULT_TIMEOUT), daemon=True).start()
        if self.supporting is False:
            self.preprocess()

        self.init_solver()
        while not event.is_set():
            if not self.finished:
                if self.fit_unchanged_count >= MAX_CROSSOVERS_WITHOUT_MASS_MUTATE:
                    self.mass_mutate()
                    self.mass_mutations_count += 1
                    self.fit_unchanged_count = 0

            if self.mass_mutations_count >= 20:
                self.reset()
                self.reset_count += 1
                self.mass_mutations_count = MAX_MASS_MUTATIONS

            if self.reset_count >= MAX_RESETS:
                self.finished = True
                self.solved = False
                break

            self.evolve()
            best_solution = self.get_best_solution()

            if best_solution.fitness == self.last_fitness:
                self.fit_unchanged_count += 1
            else:
                self.fit_unchanged_count = 0
                self.last_fitness = best_solution.fitness
                self.game.board = self.get_best_solution().board

            if best_solution.fitness == 0:
                self.finished = True
                self.solved = True
                break

            if self.is_converged():
                self.finished = True
                self.solved = False
                break
        if queue is not None:
            queue.append(['result', [game_id, self.solved], algorithm])

    def init_solver(self):
        self.rows = self.game.height
        self.columns = self.game.width
        self.solutions = []

        for i in range(self.pool_size):
            solution = Solution(self.rows, self.columns, self.original_board if self.supporting else None)
            self.solutions.append(solution)

        self.solutions[0] = Solution(self.rows, self.columns, self.original_board if self.supporting else None)
        self.solutions[0].set_flatten_board(self.game.board.flatten())

        self.solutions[1] = Solution(self.rows, self.columns, self.original_board if self.supporting else None)
        self.solutions[1].set_flatten_board(self.game.board.flatten())

        self.solutions[2] = Solution(self.rows, self.columns, self.original_board if self.supporting else None)
        self.solutions[2].set_flatten_board(self.game.board.flatten())

        self.calculate_fitness()

    def mass_mutate(self):
        for solution in self.solutions:
            if self.get_best_solution() != solution:
                solution.shuffle()

    def reset(self):
        self.solutions = []
        for i in range(self.pool_size):
            solution = Solution(self.rows, self.columns, self.game.original_board if self.supporting else None)
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

        shuffle(new_solutions)
        self.solutions = new_solutions

        self.calculate_fitness()
        self.generation += 1

    def tour_select(self):
        sorted = self.solutions.copy()
        sorted.sort(key=lambda x: x.fitness)
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

        child = Solution(self.rows, self.columns, self.original_board if self.supporting else None)
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
        return sorted_solutions[0]

    def preprocess(self):
        for idx, row in enumerate(self.game.rows):
            if len(row) == 0:
                for i in range(self.game.width):
                    self.game.set_board_tile(i, idx, -1)
                continue

            hint_sum = 0
            for r in row:
                hint_sum += r + 1
            hint_sum -= 1

            if hint_sum == self.game.width:
                curr_idx = 0
                for r in row:
                    for _ in range(r):
                        self.game.set_board_tile(curr_idx, idx, 1)
                        curr_idx += 1
                    if curr_idx < self.game.width - 1:
                        self.game.set_board_tile(curr_idx, idx, -1)
                        curr_idx += 1
                continue

            hint_start, hint_end = [], []
            start, end = 0, 0
            for r_idx, r in enumerate(row):
                start += r
                hint_start.append(start-1)
                start += 1
            for r_idx, r in reversed(list(enumerate(row))):
                end += r
                hint_end.append(self.game.width - end)
                end += 1
            hint_end = reversed(list(hint_end))
            for s, e in zip(hint_start, hint_end):
                if s >= e:
                    for i in range(e, s+1):
                        self.game.set_board_tile(i, idx, 1)

        for idx, col in enumerate(self.game.cols):
            if len(col) == 0:
                for i in range(self.game.height):
                    self.game.set_board_tile(idx, i, -1)
                continue

            hint_sum = 0
            for c in col:
                hint_sum += c + 1
            hint_sum -= 1

            if hint_sum == self.game.height:
                curr_idx = 0
                for c in col:
                    for _ in range(c):
                        self.game.set_board_tile(idx, curr_idx, 1)
                        curr_idx += 1
                    if curr_idx < self.game.height - 1:
                        self.game.set_board_tile(idx, curr_idx, -1)
                        curr_idx += 1
                continue

            hint_start, hint_end = [], []
            start, end = 0, 0
            for c_idx, c in enumerate(col):
                start += c
                hint_start.append(start-1)
                start += 1
            for c_idx, c in reversed(list(enumerate(col))):
                end += c
                hint_end.append(self.game.height - end)
                end += 1
            hint_end = reversed(list(hint_end))
            for s, e in zip(hint_start, hint_end):
                if s >= e:
                    for i in range(e, s+1):
                        self.game.set_board_tile(idx, i, 1)


class Solution:
    def __init__(self, rows, cols, original_board=None):
        self.fitness = 0

        self.rows = rows
        self.cols = cols
        self.original = original_board
        if self.original is None:
            self.original = np.zeros((self.rows, self.cols), dtype=int)
        self.board = np.zeros((self.rows, self.cols), dtype=int)

        for i in range(self.rows):
            for j in range(self.cols):
                if self.original[i][j] == 0 and random() < 0.6:
                    self.board[i][j] = 1
                else:
                    self.board[i][j] = self.original[i][j]

    def set_flatten_board(self, board):
        self.board = np.zeros((self.rows, self.cols), dtype=int)
        idx = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.original[i][j] == 0:
                    self.board[i][j] = board[idx]
                else:
                    self.board[i][j] = self.original[i][j]
                idx += 1

    def mutate(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if random() < 0.05:
                    if self.original[i][j] != 0:
                        continue
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

        if len(arr1) == 0 and len(arr2) != 0:
            return 10*sum(arr2)

        score = 0
        for a, b in zip(arr1, arr2):
            score += abs(a-b)
        return score

    def shuffle(self):
        flat = self.board.flatten()
        shuffle(flat)
        self.set_flatten_board(flat)
