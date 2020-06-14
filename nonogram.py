import numpy as np
import ast  # for evaluating data loaded from file
from utils.database import DatabaseHandler
from algorithms.solver_dfs import SolverDFS
from algorithms.solver_logic_heuristics import SolverLogicHeuristics
from algorithms.solver_random import SolverRandom
from algorithms.solver_ga import SolverGA
from timeit import default_timer as timer


class Nonogram:
    def __init__(self, queue=None):
        self.width = 0      # number of columns
        self.height = 0     # number of rows
        self.rows = []      # 2d array storing hints for rows
        self.cols = []      # 2d array storing hints for columns
        self.board = []     # 2D numpy array storing board tiles state

        self.db_handler = DatabaseHandler('puzzles.db')  # pointer to database handler used for loading puzzles from database
        self.solution = []  # 2d array storing solution of the puzzle (1st row, 2nd row, etc.)

        self.solver = SolverGA(self)
        self.queue = queue

        self.id = 0

    def init_game(self, width, height, rows, cols):
        self.width = width
        self.height = height
        self.rows = np.array(rows)
        self.cols = np.array(cols)
        self.board = np.zeros((self.height, self.width), dtype=int)

    def reset_game(self):
        self.board = np.zeros((self.height, self.width), dtype=int)

    def choose_solver(self, solver):
        if solver == 'dfs':
            self.solver = SolverDFS(self)
        elif solver == 'heuristics':
            self.solver = SolverLogicHeuristics(self)
        elif solver == 'random':
            self.solver = SolverRandom(self)
        elif solver == 'ga':
            self.solver = SolverGA(self)
        else:
            raise TypeError(f'Solver {solver} does not exist!')

    def load_from_file(self, filename):
        f = open(filename, 'r')

        # read dimensions of the puzzle
        buffer = f.readline()
        self.height, self.width = [int(s) for s in buffer.split(' ')]

        # read hints for rows
        buffer = f.readline()
        self.rows = np.array(ast.literal_eval(buffer))

        # read hints for columns
        buffer = f.readline()
        self.cols = np.array(ast.literal_eval(buffer))

        f.close()
        self.board = np.zeros((self.height, self.width), dtype=int)

    def load_from_db(self, puzzle_id):
        sql_select = self.db_handler.select_data_by_id(puzzle_id)
        game_data = sql_select[0]
        self.width = game_data[2]
        self.height = game_data[1]
        self.rows = np.array(ast.literal_eval(game_data[3]))
        self.cols = np.array(ast.literal_eval(game_data[4]))

        self.board = np.zeros((self.height, self.width), dtype=int)
        self.solver = SolverRandom(self)

        self.id = puzzle_id

    @staticmethod
    # converts line of tiles to list containing lengths of continuous colored fields
    def prepare_line(line):
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

    def get_solution_from_file(self, filename):
        self.solution = []
        try:
            f = open(filename, 'r')
        except FileNotFoundError:
            print("File does not exist!")
            return

        for _ in range(len(self.rows)):
            buffer = f.readline()
            if buffer is not '':
                self.solution.append([int(s) for s in buffer.split(' ')])

    def check_solution(self):
        # check if every row is correct
        for index, row in enumerate(self.rows):
            a = self.prepare_line(self.board[index])
            if not np.array_equal(row, a):
                # print("WRONG ROW", row, a, index)
                return False
        # check if every column is correct
        for index, col in enumerate(self.cols):
            a = self.prepare_line(self.board[:, index])
            if not np.array_equal(col, a):
                # print("WRONG COL", col, a, index)
                return False
        return True

    def get_board_row(self, index):
        """Method for retriving given row"""
        if index < 0 or index > self.height:
            raise IndexError(f"Row index out of range! Allowed indexes are 0-{self.height-1}; given index: {index}")
        return self.board[index].copy()

    def get_board_column(self, index):
        """Method for retriving given column"""
        if index < 0 or index > self.width:
            raise IndexError(f"Column index out of range! Allowed indexes are 0-{self.width-1}; given index: {index}")
        return self.board[:, index].copy()

    def get_board_tile(self, x, y):
        """Method for getting value of given tile"""
        if x < 0 or x > self.width:
            raise IndexError(f"X coordinate out of range! Allowed indexes are 0-{self.width}; given: {x}")
        if y < 0 or y > self.height:
            raise IndexError(f"Y coordinate out of range! Allowed indexes are 0-{self.height}; given: {y}")
        return self.board[y][x]

    def get_hints_row(self, index):
        """Method for retriving all hints for given row"""
        if index < 0 or index > self.height:
            raise IndexError(f"Row index out of range! Allowed indexes are 0-{self.height-1}; given index: {index}")
        return self.rows[index]

    def get_hints_column(self, index):
        """Method for retriving all hints for given column"""
        if index < 0 or index > self.width:
            raise IndexError(f"Column index out of range! Allowed indexes are 0-{self.width-1}; given index: {index}")
        return self.cols[index]

    def set_board_tile(self, x, y, value):
        """Method for setting value of given tile"""
        if x < 0 or x > self.width:
            raise IndexError(f"X coordinate out of range! Allowed indexes are 0-{self.width}; given: {x}")
        if y < 0 or y > self.height:
            raise IndexError(f"Y coordinate out of range! Allowed indexes are 0-{self.height}; given: {y}")
        if value not in (-1, 0, 1):
            raise ValueError(f"Value incorrect. Allowed values: (-1, 0, 1); given value: {value}")
        self.board[y][x] = value

    def solve(self, timeout=None, algorithm=None):
        self.reset_game()
        start = timer()
        self.solver.solve(stop=timeout, game_id=self.id, queue=self.queue, algorithm=algorithm)
        end = timer()

        if self.queue is not None:
            self.queue.append(['time', end - start, algorithm, self.id, self.check_solution()])
