import PySimpleGUI as sg
import queue
import threading
from solver_dfs import SolverDFS

class GUI:
    def __init__(self, game_width=5, game_height=5, game=None):
        # puzzle related variables
        self.game_width = game_width    # width of the game, used in GUI (could be different from width of current puzzle itself)
        self.game_height = game_height  # height of the game, used in GUI (could be different from ehight of current puzzle itself)
        self.game = game                # pointer to game object

        # window sizes related variables
        self.WINDOW_SIZE_X = 500    # initial width of the window
        self.WINDOW_SIZE_Y = 500    # initial height of the window
        self.BOX_WIDTH = self.WINDOW_SIZE_X // self.game_width      # width of the single puzzle tile
        self.BOX_HEIGHT = self.WINDOW_SIZE_Y // self.game_height    # height of the single puzzle tile
        self.stored_size = (0, 0)   # width and height of the last drawn window
        self.reload_size = True     # boolean for checking if the window needs to be redrawn due to window resizing

        self.TIP_SIZE = 150         # widht (for rows) or height (for columns) of box containing hints

        # variables storing object ids of hints/board
        self.board_ids = [[None for _ in range(self.game_width)] for _ in range(self.game_height)]  # array storing IDs of puzzle tiles
        self.row_hint_ids = []      # array storing IDs of drawn objects of hints for rows
        self.col_hint_ids = []      # array storing IDs of drawn objects of hints for columns

        # init display variables
        self.layout = None      # layout of current window
        self.window = None      # pointer to window object
        self.puzzle = None      # pointer to window fragment containing puzzle tiles
        self.row_hints = None   # pointer to window fragment containing hints for rows
        self.col_hints = None   # pointer to window fragment containing hints for columns

        self.queue = queue.Queue()

    def reload(self):
        self.clear_hints()
        self.clear_board()

        self.game_width = self.game.width
        self.game_height = self.game.height
        # Update box sizes according to current size of the diagram
        self.BOX_WIDTH = self.WINDOW_SIZE_X // self.game_width
        self.BOX_HEIGHT = self.WINDOW_SIZE_Y // self.game_height

        # Init array storing ids of board tiles
        self.board_ids = [[None for _ in range(self.game_width)] for _ in range(self.game_height)]

    def change_size(self, x, y):
        # calculate longest array of tips
        max_row = max([len(r) for r in self.game.rows])
        max_col = max([len(c) for c in self.game.cols])
        max_tip = max(max_row, max_col)
        self.TIP_SIZE = max_tip * 5 + 30

        self.WINDOW_SIZE_X = int(0.8*x) - self.TIP_SIZE #- 30
        self.WINDOW_SIZE_Y = int(0.8*y) - self.TIP_SIZE #- 30# - 76

        self.reload()
        self.puzzle.set_size((self.WINDOW_SIZE_X, self.WINDOW_SIZE_Y))
        self.BOX_WIDTH = self.WINDOW_SIZE_X // self.game_width
        self.BOX_HEIGHT = self.WINDOW_SIZE_Y // self.game_height

        self.row_hints.set_size((self.TIP_SIZE, self.WINDOW_SIZE_Y))
        self.col_hints.set_size((self.TIP_SIZE + self.WINDOW_SIZE_X, self.TIP_SIZE))

        self.redraw_hints(self.game.rows, self.game.cols)
        self.redraw()

        return self.window.Size

    def set_layout(self):
        menu_definition = [['File', ['Open', 'Save', 'Exit',]],
                ['Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],
                ['Help', 'About...'], ]

        self.layout = [
            [sg.Menu(menu_definition)],
            [sg.Text('Nonogram'), sg.Text('', key='-OUTPUT-')],
            [sg.Graph((self.TIP_SIZE + self.WINDOW_SIZE_X, self.TIP_SIZE),
                      (0, self.TIP_SIZE), (self.TIP_SIZE + self.WINDOW_SIZE_X, 0),
                      key='-COLUMNS-', change_submits=True, drag_submits=False)],
            [sg.Graph((self.TIP_SIZE, self.WINDOW_SIZE_Y),
                      (0, self.WINDOW_SIZE_Y), (self.TIP_SIZE, 0),
                      key='-ROWS-', change_submits=True, drag_submits=False),
             sg.Graph((self.WINDOW_SIZE_X, self.WINDOW_SIZE_Y),
                      (-1, self.WINDOW_SIZE_Y + 1), (self.WINDOW_SIZE_X + 1, -1),
                      key='-GRAPH-', change_submits=True, drag_submits=False)],
            [sg.Button('Check'), sg.Button('Exit'), sg.FileBrowse('Load file', target='-FILEBROWSE-'),
             sg.Button('Load from database'), sg.Button('Solve with DFS')],
            [sg.Input(key='-FILEBROWSE-', enable_events=True, visible=False)]
        ]

        self.window = sg.Window('Window Title', self.layout, finalize=True, resizable=True)
        self.puzzle = self.window['-GRAPH-']
        self.row_hints = self.window['-ROWS-']
        self.col_hints = self.window['-COLUMNS-']

    def clear_hints(self):
        # remove all row hints
        for ID in self.row_hint_ids:
            self.row_hints.delete_figure(ID)
        # remove all columns hints
        for ID in self.col_hint_ids:
            self.col_hints.delete_figure(ID)
        # clear variables storing ids of hints
        self.row_hint_ids = []
        self.col_hint_ids = []

    def clear_board(self):
        for row in range(self.game_height):
            for col in range(self.game_width):
                self.puzzle.delete_figure(self.board_ids[row][col])
        self.board_ids = [[None for _ in range(self.game_width)] for _ in range(self.game_height)]

    def update_box(self, x, y):
        self.puzzle.delete_figure(self.board_ids[x][y])
        self.board_ids[x][y] = None
        self.redraw()

    def redraw_hints(self, rows, cols):
        # first remove all existing hints
        self.clear_hints()

        # populate all row hints
        for row_index, row in enumerate(rows):
            for index, num in enumerate(row):
                rh = self.row_hints.draw_text('{}'.format(num if num > 0 else ""),
                                              (10 + self.TIP_SIZE * (index / len(row)),
                                               self.BOX_HEIGHT / 2 + row_index * self.BOX_HEIGHT),
                                              text_location=sg.TEXT_LOCATION_CENTER, font='Courier 20')
                self.row_hint_ids.append(rh)

        # populate all column hints
        for col_index, col in enumerate(cols):
            for index, num in enumerate(col):
                ch = self.col_hints.draw_text('{}'.format(num if num > 0 else ""),
                                              (5 + self.TIP_SIZE + self.BOX_WIDTH // 2 + col_index * self.BOX_WIDTH,
                                               10 + self.TIP_SIZE * (index / len(col))),
                                              text_location=sg.TEXT_LOCATION_CENTER, font='Courier 20')
                self.col_hint_ids.append(ch)

    def redraw(self):
        for row in range(self.game_height):
            for col in range(self.game_width):
                if self.board_ids[row][col] is not None:
                    continue
                if self.game.board[row][col] == 0:
                    self.board_ids[row][col] = self.puzzle.draw_rectangle(
                        (col * self.BOX_WIDTH, row * self.BOX_HEIGHT),
                        (col * self.BOX_WIDTH + self.BOX_WIDTH, row * self.BOX_HEIGHT + self.BOX_HEIGHT),
                        line_color='black', fill_color='white')
                elif self.game.board[row][col] == 1:
                    self.board_ids[row][col] = self.puzzle.draw_rectangle(
                        (col * self.BOX_WIDTH, row * self.BOX_HEIGHT),
                        (col * self.BOX_WIDTH + self.BOX_WIDTH, row * self.BOX_HEIGHT + self.BOX_HEIGHT),
                        line_color='black', fill_color='black')
                else:
                    self.board_ids[row][col] = self.puzzle.draw_rectangle(
                        (col * self.BOX_WIDTH, row * self.BOX_HEIGHT),
                        (col * self.BOX_WIDTH + self.BOX_WIDTH, row * self.BOX_HEIGHT+ self.BOX_HEIGHT),
                        line_color='black', fill_color='grey')

                # draw tile number in the tile
                # self.game.get_solution_from_file('solution.txt')
                # self.puzzle.draw_text('{}'.format(self.game.solution[row][col]),
                #             (col * self.BOX_WIDTH + self.BOX_WIDTH // 2, row * self.BOX_HEIGHT + self.BOX_HEIGHT // 2),
                #             text_location=sg.TEXT_LOCATION_CENTER, font='Courier 50')

    def event_handler(self):
        event, values = self.window.read(timeout=100)

        # if bad event or 'Exit' event -> close app
        if event in (None, 'Exit'):
            return False

        # handle resizing window
        if self.reload_size is True and self.stored_size != self.window.Size:
            self.reload_size = False
            self.stored_size = self.change_size(self.window.Size[0], self.window.Size[1])
        elif self.reload_size is False:
            self.reload_size = True
            self.stored_size = (self.window.Size[0], self.window.Size[1])

        # check solution
        if event in 'Check':
            if self.game.check_solution():
                sg.popup_ok('CORRECT')
            else:
                sg.popup_ok('WRONG')

        # load game from database
        if event in 'Load from database':
            popup_text = sg.popup_get_text('Choose puzzle ID (1-5584)', 'Load puzzle from database')
            if popup_text:
                puzzle_id = int(popup_text)
                if 0 < puzzle_id < 5585:
                    self.game.load_from_db(puzzle_id)
                    self.reload()
                    self.redraw_hints(self.game.rows, self.game.cols)
                    self.redraw()

        # load game from file
        if event in '-FILEBROWSE-':
            filename = values['-FILEBROWSE-']
            if filename is not '':
                self.game.load_from_file(filename)
                self.reload()
                self.redraw_hints(self.game.rows, self.game.cols)
                self.redraw()

        # solve game with DFS algorithm
        if event in 'Solve with DFS':
            thread_id = threading.Thread(target=self.game.solve, daemon=True)
            thread_id.start()

        if event in '-GRAPH-':
            mouse = values['-GRAPH-']
            if mouse == (None, None):
                return True
            box_x = mouse[1] // self.BOX_HEIGHT
            box_y = mouse[0] // self.BOX_WIDTH
            # check/uncheck box
            try:
                _ = self.game.board[box_x][box_y]
            except IndexError:
                return True
            if self.game.board[box_x][box_y] == 0:
                self.game.board[box_x][box_y] = 1
                self.update_box(box_x, box_y)
            else:
                self.game.board[box_x][box_y] = 0
                self.update_box(box_x, box_y)

        self.clear_board()
        self.redraw()
        return True
