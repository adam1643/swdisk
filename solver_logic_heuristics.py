import time
from random import randint
import numpy as np


class SolverLogicHeuristics:
    def __init__(self, game):
        self.game = game    # object of Nonogram class
        self.state = 0

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
                # if idx == 0:
                    # print(s, e)
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
                if idx == 0:
                    print(s, e)
                if s >= e:
                    for i in range(e, s+1):
                        self.game.set_board_tile(idx, i, 1)

    def subprocedure_1(self, line, hints):
        line_len = len(line)
        left_most, right_most = [], []

        hint_sum = 0
        for hint in hints:
            hint_sum += hint + 1
        hint_sum -= 1

        pos = 0
        left_line = line.copy()
        for hint in hints:
            if self.insert_line(left_line, pos, hint):
                left_most.append((pos, pos+hint-1))
                pos += hint
            pos += 1
            if pos > line_len:
                if self.check_line(line, hints):
                    print("CORRECT!")
                else:
                    raise ValueError("Position too far! ", pos)
        # print(left_line)

        pos = 0
        right_line = list(reversed(line))
        hints_reversed = list(reversed(hints))
        for hint in hints_reversed:
            if self.insert_line(right_line, pos, hint):
                right_most.append((pos, pos + hint - 1))
                pos += hint
            pos += 1
            if pos > line_len:
                pass
                # raise ValueError("Position too far! ", pos)
        right_line = list(reversed(right_line))
        right_most = list(reversed(right_most))
        right_most = [(line_len - 1 - a[1], line_len - 1 - a[0]) for a in right_most]
        # print(right_line)
        # print(line)
        # print(left_most, right_most)

        for l, r in zip(left_most, right_most):
            l_range = list(range(l[0], l[1]+1))
            r_range = list(range(r[0], r[1]+1))
            # print(l_range, r_range)
            cross_section = list(set(l_range) & set(r_range))
            for pos in cross_section:
                line[pos] = 1

    def check_line(self, line, hints):
        fixed_solution = self.game.prepare_line(line)
        return np.array_equal(fixed_solution, np.array(hints, dtype=int))

    def insert_line(self, line, pos, length):
        line_copy = line.copy()

        if pos > 0:
            if line[pos - 1] == 1:
                return False

        for i in range(length):
            if line[pos+i] != -1:
                line_copy[pos+i] = 1
            else:
                return False
        if pos + length < len(line):
            if line[pos + length] == 1:
                return False

        line.clear()
        line.extend(line_copy)
        return True

    def solve(self):
        """Method for solving Nonograms. If time consuming, should be run in another thread"""
        if self.state == 0:
            self.preprocess()
            self.state = 1
            return

        for i in range(self.game.height):
            line, hints = list(self.game.get_board_row(i)), self.game.get_hints_row(i)
            self.subprocedure_1(line, hints)

            if not (list(self.game.get_board_row(i)) == line):
                index = 0
                for board, line in zip(list(self.game.get_board_row(i)), line):
                    if board != line:
                        self.game.set_board_tile(index, i, line)
                    index += 1
                print("Difference!")

        for i in range(self.game.width):
            line, hints = list(self.game.get_board_column(i)), self.game.get_hints_column(i)
            self.subprocedure_1(line, hints)
            if not (list(self.game.get_board_column(i)) == line):
                index = 0
                for board, line in zip(list(self.game.get_board_column(i)), line):
                    if board != line:
                        self.game.set_board_tile(i, index, line)
                    index += 1
                print("Difference!")

        # while True:
        #     x, y = randint(0, 4), randint(0, 4)
        #     self.game.set_board_tile(x, y, 1)
        #     time.sleep(1)
