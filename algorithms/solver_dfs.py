from typing import List
import copy
import time
import numpy as np
from utils.utils import timer, DEFAULT_TIMEOUT
import threading


class Constraints:
    def __init__(self, game):
        self.width = game.width
        self.height = game.height
        self.rows = game.rows
        self.columns = game.cols


class PuzzleState:
    EMPTY = False
    BLOCK = True

    def __init__(self, constraints):
        self.constraints = constraints
        self._state = [
            [None for _ in range(constraints.width)] for _ in range(constraints.height)
        ]

    def _check_limits(self, row, column):
        return (0 <= row < self.constraints.height) and \
               (0 <= column < self.constraints.width)

    def set(self, row, column, value):
        assert self._check_limits(row, column)
        self._state[row][column] = value

    def set_row(self, row, values):
        assert len(values) == self.constraints.width
        self._state[row] = values

    def get(self, row, column):
        assert self._check_limits(row, column)
        return self._state[row][column]

    def get_board(self):
        board = [
            [0 for _ in range(self.constraints.width)] for _ in range(self.constraints.height)
        ]
        for i in range(0, self.constraints.height):
            for j in range (0, self.constraints.width):
                if self._state[i][j] is True:
                    board[i][j] = 1
        return board

    def validate(self, completed_rows):
        if completed_rows <= 0:
            return True

        completed_rows += 1

        for i in range(self.constraints.width):
            column_constraints = self.constraints.columns[i]

            # if there are no blocks in the current column
            if len(column_constraints) == 0:
                # return false if there is any block
                for j in range(completed_rows):
                    if self.get(j, i):
                        return False

                # column is valid
                continue

            in_block = False  # flag if the current position is in a block
            block_index = 0  # the index of the next block
            num_cells = None  # the number of remaing cells in the current block

            for j in range(completed_rows):
                if self.get(j, i):  # the current cell is occupied
                    if in_block:
                        num_cells -= 1  # consume one cell of the remaining ones
                        if num_cells < 0:
                            # there are more cells in the block than in the constraint
                            return False
                    else:
                        if block_index >= len(column_constraints):
                            return False  # a new block starts but there are no more in the constraints

                        num_cells = column_constraints[block_index] - 1
                        block_index += 1
                        in_block = True
                elif in_block:
                    if num_cells != 0:
                        return False  # if not all cells were consumed the state is not valid
                    in_block = False

            if completed_rows == self.constraints.height and block_index != len(column_constraints):
                return False  # there were too few blocks in the current state

            # check if the column can't be completed with the remaining blocks
            remaining_cells = self.constraints.height - completed_rows
            remaining_constraints = column_constraints[block_index:]
            if sum(remaining_constraints) + len(remaining_constraints) - 1 > remaining_cells:
                return False

        return True  # no errors were found so the state is valid


class Permutation:
    def __init__(self, constraints):
        self.constraints = constraints
        self.cache = dict()

    def get_permutations(self, row):
        if row in self.cache:
            return self.cache[row]

        blocks = self.constraints.rows[row]
        if not blocks:
            return [[PuzzleState.EMPTY for _ in range(self.constraints.width)]]

        positions = [0]
        for block in range(1, len(blocks)):
            positions.append(positions[-1] + blocks[block - 1] + 1)
        self.cache[row] = []
        self._next_permutation(row, positions, len(positions) - 1)
        return self.cache[row]

    def _positions_to_row(self, row, positions):
        blocks = [PuzzleState.EMPTY for _ in range(self.constraints.width)]
        for index, pos in enumerate(positions):
            length = self.constraints.rows[row][index]
            blocks[pos:pos + length] = [PuzzleState.BLOCK for _ in range(length)]

        return blocks

    def _can_shift(self, row, positions, block_index):
        if block_index + 1 == len(positions):
            return positions[block_index] + self.constraints.rows[row][block_index] < self.constraints.width

        return positions[block_index] + self.constraints.rows[row][block_index] + 1 < positions[block_index + 1]

    def _next_permutation(self, row, positions, block_index):
        self.cache[row].append(self._positions_to_row(row, positions))
        if block_index < 0:
            return

        while self._can_shift(row, positions, block_index):
            positions[block_index] += 1
            self._next_permutation(row, [p for p in positions], block_index - 1)


class PuzzleSolver:
    def __init__(self, constraints):
        self.constraints = constraints
        self.permutation = Permutation(constraints)

    def _depth_first_search(self, row, event=None):
        if event.is_set():
            return

        self.nodes += 1
        if row > self.max_row:
            self.max_row = row

        if not self.state.validate(row):
            return

        if row + 1 == self.constraints.height:
            self.solutions.append(copy.deepcopy(self.state))
            return

        for perm in self.permutation.get_permutations(row + 1):
            self.state.set_row(row + 1, perm)
            self._depth_first_search(row + 1, event)

        self.state.set_row(row + 1, [None for _ in range(self.constraints.width)])

    def solve(self, event=None):
        self.state: PuzzleState = PuzzleState(self.constraints)
        self.solutions: List[PuzzleState] = []

        self.nodes = -1
        self.max_row = 0
        self.start_time = time.perf_counter()
        self._depth_first_search(-1, event)

        return self.solutions


class SolverDFS:
    def __init__(self, game):
        self.game = game

    def solve(self, stop=None, game_id=None, queue=None, algorithm=None):
        event = threading.Event()
        threading.Thread(target=timer, args=(event, stop if stop is not None else DEFAULT_TIMEOUT), daemon=True).start()

        instance = Constraints(self.game)

        solver = PuzzleSolver(instance)
        solutions = []
        try:
            solutions = solver.solve(event)
        except:
            pass

        board = None

        if len(solutions) == 0:
            pass
        else:
            board = solutions[0].get_board()

        if board is not None:
            self.game.board = np.array(board)

        solved = self.game.check_solution()

        if not solved and not event.is_set():
            print(f"DFS: Puzzle with id {game_id} not solvable!")

        if queue is not None:
            queue.append(['result', [game_id, solved], algorithm])
