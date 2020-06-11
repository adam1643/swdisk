import time
from random import randint
import numpy as np
from random import randint, random, shuffle
from utils import timer, DEFAULT_TIMEOUT
import threading
from solver_ga import SolverGA


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

    def subprocedure_1(self, line, hints):
        left_most, right_most = self.prepare_edge_cases(line, hints)
        if left_most is None:
            return

        hint_sum = 0
        for hint in hints:
            hint_sum += hint + 1
        hint_sum -= 1

        for l, r in zip(left_most, right_most):
            l_range = list(range(l[0], l[1]+1))
            r_range = list(range(r[0], r[1]+1))
            cross_section = list(set(l_range) & set(r_range))
            for pos in cross_section:
                line[pos] = 1

    def subprocedure_2(self, line, hints):
        line_len = len(line)
        left_most, right_most = self.prepare_edge_cases(line, hints)
        if left_most is None:
            return

        hint_sum = 0
        for hint in hints:
            hint_sum += hint + 1
        hint_sum -= 1

        if len(left_most) != len(right_most):
            return

        for i in range(len(hints)):
            if i == 0:
                for idx in range(left_most[i][0]):
                    line[idx] = -1

            if i == len(hints) - 1:
                for idx in range(right_most[i][1] + 1, line_len):
                    line[idx] = -1
                continue

            if right_most[i][1] < left_most[i+1][0] - 1:
                for j in range(right_most[i][1]+1, left_most[i+1][0]):
                    line[j] = -1

    def subprocedure_3(self, line, hints):
        idx = 0
        while line[idx] == -1:
            idx += 1
        for i in range:
            pass

    def prepare_edge_cases(self, line, hints):
        line = line.copy()
        left_most = self.prepare_left_most(line, hints)

        size = len(line)
        right_most = self.prepare_left_most(list(reversed(line)), list(reversed(hints)))
        if right_most is None:
            return None, None
        right_most = list(reversed([(size - b - 1, size - a - 1) for a, b in right_most]))

        if left_most is None or right_most is None:
            return None, None
        return left_most, right_most

    def prepare_left_most(self, line, hints):
        line_len = len(line)
        left_most = []

        hint_sum = 0
        for hint in hints:
            hint_sum += hint + 1
        hint_sum -= 1

        pos = 0
        offset = [0 for _ in range(len(hints))]
        max_offset_idx = len(offset) - 1
        curr_offset_idx = max_offset_idx
        perf_index = 0
        calc_index = 0
        while calc_index < 5000:
            calc_index += 1
            perf_index += 1
            left_line = line.copy()
            left_most = []
            pos = 0

            for idx, hint in enumerate(hints):
                pos += offset[idx]
                while pos + hint <= line_len:
                    if self.insert_line(left_line, pos, hint):
                        left_most.append((pos, pos + hint - 1))
                        pos += hint
                        break
                    pos += 1

                if pos > line_len:
                    if self.check_line(line, hints):
                        print(perf_index)
                        return left_most
                    else:
                        pass
                        # raise ValueError("Position too far! ", pos)

            # print(left_line)
            if not self.is_line_possible(left_line, hints, always_true=False):
                if hint_sum + sum(offset) < line_len:
                    offset[curr_offset_idx] += 1
                else:
                    while hint_sum + sum(offset) >= line_len:
                        offset[curr_offset_idx] = 0
                        offset[curr_offset_idx-1] += 1
                        curr_offset_idx -= 1
                        if hint_sum + sum(offset) == line_len:
                            break
                    curr_offset_idx = max_offset_idx
            else:
                return left_most
        return None

    def check_line(self, line, hints):
        fixed_solution = self.game.prepare_line(line)
        return np.array_equal(fixed_solution, np.array(hints, dtype=int))

    def is_line_possible(self, line, hints, always_true=True):
        if always_true:
            return True
        fixed_solution = self.game.prepare_line(line)
        if len(fixed_solution) > len(hints):
            return False
        hint_idx = 0
        for idx, sol in enumerate(fixed_solution):
            if hint_idx >= len(hints):
                return False
            if sol > hints[hint_idx]:
                hint_idx += 1

        return True

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

    def solve_step(self, proc):
        """Method for solving Nonograms. If time consuming, should be run in another thread"""
        if self.state == 0:
            self.preprocess()
            self.state = 1
            return

        status_changed = False

        for i in range(self.game.height):
            line, hints = list(self.game.get_board_row(i)), self.game.get_hints_row(i)
            if proc == 1:
                self.subprocedure_1(line, hints)
            elif proc == 2:
                self.subprocedure_2(line, hints)

            if not (list(self.game.get_board_row(i)) == line):
                index = 0
                for board, line in zip(list(self.game.get_board_row(i)), line):
                    if board != line:
                        self.game.set_board_tile(index, i, line)
                    index += 1
                print("Difference!")
                status_changed = True

        for i in range(self.game.width):
            line, hints = list(self.game.get_board_column(i)), self.game.get_hints_column(i)
            if proc == 1:
                self.subprocedure_1(line, hints)
            elif proc == 2:
                self.subprocedure_2(line, hints)

            if not (list(self.game.get_board_column(i)) == line):
                index = 0
                for board, val in zip(list(self.game.get_board_column(i)), line):
                    if board != val:
                        self.game.set_board_tile(i, index, val)
                    index += 1
                print("Difference!")
                status_changed = True

        return status_changed

    def solve(self, stop, game_id, queue, algorithm=None):
        self.solve_step(0)
        event = threading.Event()
        threading.Thread(target=timer, args=(event, stop if stop is not None else DEFAULT_TIMEOUT), daemon=True).start()

        status = True
        try:
            while status and not event.is_set():
                s1 = self.solve_step(1)
                s2 = self.solve_step(2)

                if not s1 and not s2:
                    status = False
        except:
            pass

        if not event.is_set():
            solved = self.game.check_solution()
            if not solved:
                ga = SolverGA(self.game, supporting=True)
                ga.init_solver()
                ga.solve(stop=5)

        solved = self.game.check_solution()
        if queue is not None:
            queue.append(['result', [game_id, solved], algorithm])
