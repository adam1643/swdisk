import PySimpleGUI as sg


class GUI:
    def __init__(self, game_width, game_height):
        self.game_width = game_width
        self.game_height = game_height
        self.WINDOW_SIZE_X = 300
        self.WINDOW_SIZE_Y = 300
        self.BOX_WIDTH = self.WINDOW_SIZE_X // self.game_width
        self.BOX_HEIGHT = self.WINDOW_SIZE_Y // self.game_height

        self.TIP_SIZE = 100

        self.board_ids = [[None for _ in range(self.game_width)] for _ in range(self.game_height)]
        self.row_hint_ids = []
        self.col_hint_ids = []

        # init display variables
        self.layout = None
        self.window = None
        self.puzzle = None
        self.row_hints = None
        self.col_hints = None

    def reload(self, game_width, game_height):
        self.game_width = game_width
        self.game_height = game_height
        self.BOX_WIDTH = self.WINDOW_SIZE_X // self.game_width
        self.BOX_HEIGHT = self.WINDOW_SIZE_Y // self.game_height

    def set_layout(self):
        self.layout = [
            [sg.Text('Nonogram Puzzle'), sg.Text('', key='-OUTPUT-')],
            [sg.Graph((self.TIP_SIZE + self.WINDOW_SIZE_X, self.TIP_SIZE),
                      (0, self.TIP_SIZE), (self.TIP_SIZE + self.WINDOW_SIZE_X, 0),
                      key='-COLUMNS-', change_submits=True, drag_submits=False)],
            [sg.Graph((self.TIP_SIZE, self.WINDOW_SIZE_Y),
                      (0, self.WINDOW_SIZE_Y), (self.TIP_SIZE, 0),
                      key='-ROWS-', change_submits=True, drag_submits=False),
             sg.Graph((self.WINDOW_SIZE_X, self.WINDOW_SIZE_Y),
                      (0, self.WINDOW_SIZE_Y + 10), (self.WINDOW_SIZE_X + 10, 0),
                      key='-GRAPH-', change_submits=True, drag_submits=False)],
            [sg.Button('Check'), sg.Button('Exit'), sg.FileBrowse('Load file', target='-FILEBROWSE-')],
            [sg.Input(key='-FILEBROWSE-', enable_events=True, visible=False)]
        ]

        self.window = sg.Window('Window Title', self.layout, finalize=True)
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
        for row in range(self.game_width):
            for col in range(self.game_height):
                self.puzzle.delete_figure(self.board_ids[row][col])
        self.board_ids = [[None for _ in range(self.game_width)] for _ in range(self.game_height)]

    def redraw_hints(self, rows, cols):
        # first remove all existing hints
        self.clear_hints()

        # populate all row hints
        for row_index, row in enumerate(rows):
            for index, num in enumerate(row):
                rh = self.row_hints.draw_text('{}'.format(num if num > 0 else ""),
                                              (self.BOX_WIDTH // 2 + self.TIP_SIZE * (index / len(row)),
                                               self.BOX_HEIGHT // 2 + row_index * self.BOX_HEIGHT),
                                              text_location=sg.TEXT_LOCATION_CENTER)
                self.row_hint_ids.append(rh)

        # populate all column hints
        for col_index, col in enumerate(cols):
            for index, num in enumerate(col):
                ch = self.col_hints.draw_text('{}'.format(num if num > 0 else ""),
                                              (self.TIP_SIZE + self.BOX_WIDTH // 2 + col_index * self.BOX_WIDTH,
                                               10 + self.TIP_SIZE * (index / len(col))),
                                              text_location=sg.TEXT_LOCATION_CENTER)
                self.col_hint_ids.append(ch)
