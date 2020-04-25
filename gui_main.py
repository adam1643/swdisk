import PySimpleGUI as sg
import ast
from nonogram import Nonogram
from gui_v2.gui_game import GUIGame
from gui_v2.gui_database import GUIDatabase


class GUIMain:
    def __init__(self):
        self.layout = None
        self.window = None

        self.game_gui_opened = False
        self.game_gui = None

        self.database_gui_opened = False
        self.database_gui = None

        self.queue = []

        self.games = []

    def set_layout(self):
        menu_definition = [
                            ['Game', ['Open from...', ['...database', '...file']]],
                            ['Database', ['Browse database']],
                            ['Help', ['About...']],
                          ]

        menu_layout = [[sg.Button('Load game from file', key='-FILE_LOAD-'), sg.Button('Load game from database', key='-DB_LOAD-')]]

        loaded_layout = [[sg.Multiline('', key='-LOADED_DATA-')],
                         [sg.Button('Init games with loaded data', key='-INIT_GAMES-')],
                         [sg.Button('Solver1', key='-SOLVER1-'), sg.Button('Solver2', key='-SOLVER2-'), sg.Button('Solver3', key='-SOLVER2-')],
                         ]

        loading_data_layout = [
            [sg.Menu(menu_definition)],
            [sg.Frame('Single game', menu_layout)],
            [sg.Frame('Loaded puzzles', loaded_layout)]
        ]

        self.layout = [
            [sg.Frame('Game data', loading_data_layout), sg.Graph(canvas_size=(400, 400), graph_bottom_left=(0, 400), graph_top_right=(400, 0), background_color='black', key='graph', tooltip='Perforamnce graph')]
        ]

        self.window = sg.Window('Nonogram solver', self.layout, finalize=True, resizable=True)
        self.window['graph'].draw_text('Placeholder for results graph/table', (200, 200), text_location=sg.TEXT_LOCATION_CENTER, font='Courier 15', color='white')

    def read_queue(self, item):
        if item[0] == 'ids':
            self.window['-LOADED_DATA-'].update(item[1])

    def event_handler(self):
        event, values = self.window.read(timeout=100)

        # handle queue from other GUI windows
        while len(self.queue) > 0:
            self.read_queue(self.queue[-1])
            self.queue.pop(-1)

        if event in (None,):
            return False

        if event in '-INIT_GAMES-':
            try:
                loaded_data = ast.literal_eval(self.window['-LOADED_DATA-'].get())
                if not isinstance(loaded_data, list):
                    raise ValueError()
                self.games = []
                for id in loaded_data:
                    if not isinstance(id, int):
                        raise ValueError()
                    nonogram = Nonogram()
                    nonogram.load_from_db(id)
                    self.games.append(nonogram)
            except (ValueError, SyntaxError):
                sg.popup_error('Entered data incorrect')

        if not self.game_gui_opened and event in ('...file', '-FILE_LOAD-'):
            self.game_gui = GUIGame(self.queue, 'test.txt')
            self.game_gui.set_layout()
            self.game_gui_opened = True

        if not self.game_gui_opened and event in ('...database', '-DB_LOAD-'):
            popup_text = sg.popup_get_text('Choose puzzle ID (1-9800)', 'Load puzzle from database')
            if popup_text:
                puzzle_id = int(popup_text)
                if 0 < puzzle_id < 9801:
                    self.game_gui = GUIGame(self.queue, db_id=puzzle_id)
                    self.game_gui.set_layout()
                    self.game_gui_opened = True

                    self.game_gui.reload()
                    self.game_gui.redraw_hints(self.game_gui.game.rows, self.game_gui.game.cols)
                    self.game_gui.redraw()

        if not self.database_gui_opened and event == 'Browse database':
            self.database_gui = GUIDatabase(self.queue)
            self.database_gui.set_layout()
            self.database_gui_opened = True

        if self.game_gui_opened and not self.game_gui.event_handler():
            self.game_gui = None
            self.game_gui_opened = False

        if self.database_gui_opened and not self.database_gui.event_handler():
            self.database_gui = None
            self.database_gui_opened = False

        return True

