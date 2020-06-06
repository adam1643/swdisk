import PySimpleGUI as sg
import ast
from nonogram import Nonogram
from gui_v2.gui_game import GUIGame
from gui_v2.gui_database import GUIDatabase
import threading


class GUIMain:
    def __init__(self):
        self.layout = None
        self.window = None

        self.game_gui_opened = False
        self.game_gui = None

        self.database_gui_opened = False
        self.database_gui = None

        self.queue = []
        self.games_queue = []
        self.algorithm = 0
        self.games_results = [[0, 0] for _ in range(4)]
        self.mean_times = [[] for _ in range(4)]

        self.games = []
        self.calc_timeout = 30

    def set_layout(self):
        sg.theme('default')
        menu_definition = [
                            ['Game', ['Open from...', ['...database', '...file']]],
                            ['Database', ['Browse database']],
                            ['Help', ['About...']],
                          ]

        menu_layout = [[sg.Button('Load game from file', key='-FILE_LOAD-'), sg.Button('Load game from database', key='-DB_LOAD-')]]

        algorithms_layout = [[sg.Button('Random', key='-SOLVER1-'), sg.Button('DFS', key='-SOLVER2-'), sg.Button('Genetic Algorithms', key='-SOLVER3-'), sg.Button('Heuristics with GA', key='-SOLVER4-')]]

        loaded_layout = [[sg.Multiline('', key='-LOADED_DATA-')],
                         [sg.Button('Init games with loaded data', key='-INIT_GAMES-'), sg.Button('Reset', key='-RESET-')],
                         [sg.Frame('Solve with algorithm', algorithms_layout)],
                         [sg.Text('Timeout solver after [s]:'), sg.Input('30', key='-TIMEOUT_INPUT-', size=(10, 10)), sg.Button('Set', key='-TIMEOUT-')]
                         ]

        loading_data_layout = [
            [sg.Menu(menu_definition)],
            [sg.Frame('Single game', menu_layout)],
            [sg.Frame('Loaded puzzles', loaded_layout)]
        ]

        s1_layout = [[sg.Text('Solved/unsolved:', text_color='black'), sg.Text('0/0', key='-S1_RATIO-', font='Arial 15 bold', size=(5, 1)), sg.Text('  % solved:'), sg.Text('0 %', key='-S1_PER-', font='Arial 14 bold', size=(4, 1)), sg.Text('  Mean solving time [s]: '), sg.Text('0', key='-S1_TIME-', font='Arial 15 bold', size=(7, 1))]]
        s2_layout = [[sg.Text('Solved/unsolved:', text_color='black'), sg.Text('0/0', key='-S2_RATIO-', font='Arial 15 bold', size=(5, 1)), sg.Text('  % solved:'), sg.Text('0 %', key='-S2_PER-', font='Arial 14 bold', size=(4, 1)), sg.Text('  Mean solving time [s]: '), sg.Text('0', key='-S2_TIME-', font='Arial 15 bold', size=(7, 1))]]
        s3_layout = [[sg.Text('Solved/unsolved:', text_color='black'), sg.Text('0/0', key='-S3_RATIO-', font='Arial 15 bold', size=(5, 1)), sg.Text('  % solved:'), sg.Text('0 %', key='-S3_PER-', font='Arial 14 bold', size=(4, 1)), sg.Text('  Mean solving time [s]: '), sg.Text('0', key='-S3_TIME-', font='Arial 15 bold', size=(7, 1))]]
        s4_layout = [[sg.Text('Solved/unsolved:', text_color='black'), sg.Text('0/0', key='-S4_RATIO-', font='Arial 15 bold', size=(5, 1)), sg.Text('  % solved:'), sg.Text('0 %', key='-S4_PER-', font='Arial 14 bold', size=(4, 1)), sg.Text('  Mean solving time [s]: '), sg.Text('0', key='-S4_TIME-', font='Arial 15 bold', size=(7, 1))]]

        results_layout = [
            [sg.Text('Games loaded: ', font='Arial 20 bold', text_color='black'), sg.Text('0', key='-NO_OF_GAMES-', font='Arial 20 bold', text_color='black', size=(5, 1))],
            [sg.Frame('Random', s1_layout, font='bold')],
            [sg.Frame('DFS', s2_layout, font='bold')],
            [sg.Frame('Genetic algorithm', s3_layout, font='bold')],
            [sg.Frame('Heuristics with GA', s4_layout, font='bold')],
        ]

        self.layout = [
            [sg.Frame('Game data', loading_data_layout), sg.Frame('Results', results_layout)]
        ]

        self.window = sg.Window('Nonogram solver', self.layout, finalize=True, resizable=True)

    def reset_games(self):
        self.games = []
        self.algorithm = 0
        self.games_results = [[0, 0] for _ in range(4)]
        self.mean_times = [[] for _ in range(4)]

        self.window['-S1_RATIO-'].update(f'{0}/{0}')
        self.window['-S2_RATIO-'].update(f'{0}/{0}')
        self.window['-S3_RATIO-'].update(f'{0}/{0}')
        self.window['-S4_RATIO-'].update(f'{0}/{0}')

        self.window['-S1_PER-'].update(f'0 %')
        self.window['-S2_PER-'].update(f'0 %')
        self.window['-S3_PER-'].update(f'0 %')
        self.window['-S4_PER-'].update(f'0 %')

        self.window['-S1_TIME-'].update(f'0')
        self.window['-S2_TIME-'].update(f'0')
        self.window['-S3_TIME-'].update(f'0')
        self.window['-S4_TIME-'].update(f'0')

        self.window['-NO_OF_GAMES-'].update('0')

    def read_queue(self, item):
        if item[0] == 'ids':
            self.window['-LOADED_DATA-'].update(item[1])

    def read_games_queue(self, item):
        if item[0] == 'result':
            result = item[1]
            if result[1] is True:
                print("Before", self.games_results, self.algorithm, self.games_results[self.algorithm-1][0])
                self.games_results[self.algorithm - 1][0] += 1
                print("After", self.games_results, self.algorithm, self.games_results[self.algorithm-1][0])
            else:
                self.games_results[self.algorithm - 1][1] += 1
            print(f'result of {result[0]} = {result[1]}')
            ratio = self.games_results[self.algorithm - 1][0] / (self.games_results[self.algorithm - 1][0] + self.games_results[self.algorithm - 1][1])

            self.window[f'-S{self.algorithm}_RATIO-'].update(f'{self.games_results[self.algorithm - 1][0]}/{self.games_results[self.algorithm - 1][1]}')
            self.window[f'-S{self.algorithm}_PER-'].update(f'{round(100*ratio)}%')

            if self.games_results[self.algorithm - 1][0] + self.games_results[self.algorithm - 1][1] == len(self.games):
                sg.popup_ok('Calculations finished! Results updated!')

        if item[0] == 'time':
            print("time", item)
            self.mean_times[self.algorithm - 1].append(item[1])
            mean_time = sum(self.mean_times[self.algorithm - 1]) / len(self.mean_times[self.algorithm - 1])
            self.window[f'-S{self.algorithm}_TIME-'].update(str(round(mean_time, 3)))

    def event_handler(self):
        event, values = self.window.read(timeout=100)

        # handle queue from other GUI windows
        while len(self.queue) > 0:
            self.read_queue(self.queue.pop(-1))

        while len(self.games_queue) > 0:
            self.read_games_queue(self.games_queue.pop(-1))

        if event in (None,):
            return False

        if event in '-INIT_GAMES-':
            self.reset_games()
            try:
                loaded_data = ast.literal_eval(self.window['-LOADED_DATA-'].get())
                if not isinstance(loaded_data, list):
                    raise ValueError()
                self.games = []
                for id in loaded_data:
                    if not isinstance(id, int):
                        raise ValueError()
                    nonogram = Nonogram(self.games_queue)
                    nonogram.load_from_db(id)
                    self.games.append(nonogram)
            except (ValueError, SyntaxError):
                sg.popup_error('Entered data incorrect')
            self.window['-NO_OF_GAMES-'].update(str(len(self.games)))

        if event in'-SOLVER1-':
            self.algorithm = 1
            for idx, game in enumerate(self.games):
                game.choose_solver('random')
                threading.Thread(target=game.solve, args=(self.calc_timeout, idx), daemon=True).start()

        if event in'-SOLVER2-':
            self.algorithm = 2
            for idx, game in enumerate(self.games):
                game.choose_solver('dfs')
                threading.Thread(target=game.solve, args=(self.calc_timeout, idx), daemon=True).start()

        if event in'-SOLVER3-':
            self.algorithm = 3
            for idx, game in enumerate(self.games):
                game.choose_solver('ga')
                threading.Thread(target=game.solve, args=(self.calc_timeout, idx), daemon=True).start()

        if event in'-SOLVER4-':
            self.algorithm = 4
            for idx, game in enumerate(self.games):
                game.choose_solver('heuristics')
                threading.Thread(target=game.solve, args=(self.calc_timeout, idx), daemon=True).start()

        if event in '-RESET-':
            self.reset_games()

        if event in '-TIMEOUT-':
            self.calc_timeout = int(self.window['-TIMEOUT_INPUT-'].get())
            sg.popup_auto_close(f'Set timeout to {self.calc_timeout} s', auto_close_duration=1, button_type=sg.POPUP_BUTTONS_NO_BUTTONS)

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

