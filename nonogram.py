import numpy as np
import ast  # for evaluating data loaded from file
from database import DatabaseHandler


class Nonogram:
    def __init__(self):
        self.width = 0      # number of columns
        self.height = 0     # number of rows
        self.rows = []      # 2d array storing hints for rows
        self.cols = []      # 2d array storing hints for columns
        self.board = []     # 2D numpy array storing board tiles state

        self.db_handler = DatabaseHandler()     # pointer to database handler used for loading puzzles from database
        self.solution = []  # 2d array storing solution of the puzzle (1st row, 2nd row, etc.)

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
        print(game_data)
        self.width = game_data[2]
        self.height = game_data[1]
        self.rows = np.array(ast.literal_eval(game_data[3]))
        self.cols = np.array(ast.literal_eval(game_data[4]))

        self.board = np.zeros((self.height, self.width), dtype=int)

    def init_game(self, width, height, rows, cols):
        self.width = width
        self.height = height
        self.rows = np.array(rows)
        self.cols = np.array(cols)
        self.board = np.zeros((self.height, self.width), dtype=int)

    def solve(self):
        pass

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

    def check_solution(self):
        # check if every row is correct
        for index, row in enumerate(self.rows):
            a = self.prepare_line(self.board[index])
            if not np.array_equal(row, a):
                print("WRONG ROW", row, a, index)
                return False
        # check if every column is correct
        for index, col in enumerate(self.cols):
            a = self.prepare_line(self.board[:, index])
            if not np.array_equal(col, a):
                print("WRONG COL", col, a, index)
                return False
        print("CORRECT")
        return True

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
