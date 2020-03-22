import numpy as np
import ast  # for evaluating data loaded from file


class Nonogram:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.rows = []
        self.cols = []
        self.board = []

    def load_from_file(self, filename):
        f = open(filename, 'r')

        # read dimensions of the puzzle
        buffer = f.readline()
        self.width, self.height = [int(s) for s in buffer.split(' ')]

        # read hints for rows
        buffer = f.readline()
        self.rows = np.array(ast.literal_eval(buffer))

        # read hints for columns
        buffer = f.readline()
        self.cols = np.array(ast.literal_eval(buffer))

        f.close()
        self.board = np.zeros((self.width, self.height), dtype=int)

    def init_game(self, width, height, rows, cols):
        self.width = width
        self.height = height
        self.rows = np.array(rows)
        self.cols = np.array(cols)
        self.board = np.zeros((self.width, self.height), dtype=int)

    def solve(self):
        pass

    @staticmethod
    # converts line of drawing to list containing lengths of continuous colored fields
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
