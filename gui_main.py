import PySimpleGUI as sg
import ast
from nonogram import Nonogram
from gui_v2.gui_game import GUIGame
from gui_v2.gui_database import GUIDatabase
import threading

SOLVERS = [0, 'random', 'dfs', 'ga', 'heuristics']


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

        self.all_to_solve = 0
        self.solves_finished = 0

        self.results = []

    def set_layout(self):
        sg.theme('default')
        sg.change_look_and_feel('DefaultNoMoreNagging')
        menu_definition = [
                            ['Game', ['Open from...', ['...database', '...file']]],
                            ['Database', ['Browse database']],
                            ['Help', ['About...']],
                          ]

        menu_layout = [[sg.Button('Load game from file', key='-FILE_LOAD-'), sg.Button('Load game from database', key='-DB_LOAD-')]]

        algorithms_layout = [
                             [sg.Checkbox('Random', key='-CH_SOLVER1-')],
                             [sg.Checkbox('DFS', key='-CH_SOLVER2-')],
                             [sg.Checkbox('Genetic Algorithm', key='-CH_SOLVER3-')],
                             [sg.Checkbox('Heuristic with GA', key='-CH_SOLVER4-')],
                             [sg.Button('Solve (slow, accurate)', key='-SOLVE_CHECKED-'), sg.Button('Solve (faster, less accurate)', key='-SOLVE_SIM-')]
                             ]

        loaded_layout = [[sg.Multiline('', key='-LOADED_DATA-')],
                         [sg.Frame('Solve with algorithm', algorithms_layout)],
                         [sg.Text('Timeout solver after [s]:'), sg.Input('30', key='-TIMEOUT_INPUT-', size=(10, 10)), sg.Button('Set', key='-TIMEOUT-')]
                         ]

        loading_data_layout = [
            [sg.Menu(menu_definition)],
            [sg.Button('Open database browser', key='-BROWSE-DB-')],
            [sg.Frame('Single game', menu_layout)],
            [sg.Frame('Loaded puzzles', loaded_layout)]
        ]

        s1_layout = [[sg.Text('Solved/unsolved:', text_color='black'), sg.Text('0/0', key='-S1_RATIO-', font='Arial 15 bold', size=(5, 1)), sg.Text('  % solved:'), sg.Text('0 %', key='-S1_PER-', font='Arial 14 bold', size=(4, 1)), sg.Text('  Mean solving time [s]: '), sg.Text('0', key='-S1_TIME-', font='Arial 15 bold', size=(7, 1))]]
        s2_layout = [[sg.Text('Solved/unsolved:', text_color='black'), sg.Text('0/0', key='-S2_RATIO-', font='Arial 15 bold', size=(5, 1)), sg.Text('  % solved:'), sg.Text('0 %', key='-S2_PER-', font='Arial 14 bold', size=(4, 1)), sg.Text('  Mean solving time [s]: '), sg.Text('0', key='-S2_TIME-', font='Arial 15 bold', size=(7, 1))]]
        s3_layout = [[sg.Text('Solved/unsolved:', text_color='black'), sg.Text('0/0', key='-S3_RATIO-', font='Arial 15 bold', size=(5, 1)), sg.Text('  % solved:'), sg.Text('0 %', key='-S3_PER-', font='Arial 14 bold', size=(4, 1)), sg.Text('  Mean solving time [s]: '), sg.Text('0', key='-S3_TIME-', font='Arial 15 bold', size=(7, 1))]]
        s4_layout = [[sg.Text('Solved/unsolved:', text_color='black'), sg.Text('0/0', key='-S4_RATIO-', font='Arial 15 bold', size=(5, 1)), sg.Text('  % solved:'), sg.Text('0 %', key='-S4_PER-', font='Arial 14 bold', size=(4, 1)), sg.Text('  Mean solving time [s]: '), sg.Text('0', key='-S4_TIME-', font='Arial 15 bold', size=(7, 1))]]

        results_layout = [
            [sg.Text('Games loaded: ', font='Arial 20 bold', text_color='black'), sg.Text('100', key='-NO_OF_GAMES-', font='Arial 20 bold', text_color='black', size=(5, 1))],
            [sg.Frame('Random', s1_layout, font='bold')],
            [sg.Frame('DFS', s2_layout, font='bold')],
            [sg.Frame('Genetic algorithm', s3_layout, font='bold')],
            [sg.Frame('Heuristics with GA', s4_layout, font='bold')]
        ]
        self.layout = [
            [sg.Frame('Game data', loading_data_layout), sg.Frame('Results', results_layout)],
            [sg.ProgressBar(100, key='-PROGRESS-', size=(40, 10))]
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

        self.solves_finished = 0
        self.results = []

    def read_queue(self, item):
        if item[0] == 'ids':
            self.window['-LOADED_DATA-'].update(item[1])

    def read_games_queue(self, item):
        if item[0] == 'result':
            result = item[1]
            algorithm = item[2]
            if result[1] is True:
                self.games_results[algorithm - 1][0] += 1
            else:
                self.games_results[algorithm - 1][1] += 1
            ratio = self.games_results[algorithm - 1][0] / (self.games_results[algorithm - 1][0] + self.games_results[algorithm - 1][1])

            self.window[f'-S{algorithm}_RATIO-'].update(f'{self.games_results[algorithm - 1][0]}/{self.games_results[algorithm - 1][1]}')
            self.window[f'-S{algorithm}_PER-'].update(f'{round(100*ratio)}%')

            self.solves_finished += 1
            self.window['-PROGRESS-'].update_bar(self.solves_finished)

            if self.all_to_solve == self.solves_finished:
                decision = sg.popup_yes_no('Calculations finished! Do you want to save results to file?', title='')
                if decision in 'Yes':
                    folder = sg.popup_get_folder('Select folder where file should be saved', keep_on_top=True)
                    file_name = sg.popup_get_text('Select filename:', default_text='results.txt', keep_on_top=True)
                    self.save_results_to_file(folder + '/' + file_name)

        if item[0] == 'time':
            _, time, algorithm, game_id, result = item
            time = round(time, 3)
            self.results.append(item)
            if result is True:
                self.mean_times[algorithm - 1].append(time)
                mean_time = sum(self.mean_times[algorithm - 1]) / len(self.mean_times[algorithm - 1])
                self.window[f'-S{algorithm}_TIME-'].update(str(round(mean_time, 3)))

    def init_games(self):
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

    def solve_separately(self, checked_solvers):
        for sol in checked_solvers:
            self.algorithm = sol
            for idx, game in enumerate(self.games):
                game.choose_solver(SOLVERS[self.algorithm])
                a = threading.Thread(target=game.solve, args=(self.calc_timeout, idx, self.algorithm))
                a.start()
                a.join()

    def save_results_to_file(self, filename):
        f = open(filename, 'w')

        f.write(f'Loaded games|{len(self.games)}\n\n')
        mean_times = []
        for i in range(4):
            if len(self.mean_times[i]) == 0:
                mean_times.append(0)
            else:
                mean_times.append(round(sum(self.mean_times[i])/len(self.mean_times[i]), 3))
        f.write('Mean times\n')
        f.write('Random|DFS|GA|Heuristics + GA|\n')
        f.write(f'{mean_times[0]}|{mean_times[1]}|{mean_times[2]}|{mean_times[3]}|\n\n')

        ratio_results = []
        for i in range(4):
            if self.games_results[i][0] + self.games_results[i][1] == 0:
                ratio = 0
            else:
                ratio = self.games_results[i][0] / (self.games_results[i][0] + self.games_results[i][1])
            ratio_results.append(ratio)
        f.write('Results (%)\n')
        f.write('Random|DFS|GA|Heuristics + GA|\n')
        f.write(f'{100*ratio_results[0]}|{100*ratio_results[1]}|{100*ratio_results[2]}|{100*ratio_results[3]}|\n\n')

        f.write('|Random||DFS||GA||Heuristics + GA\n')
        f.write('ID|Result|Time|Result|Time|Result|Time|Result|Time\n')
        game_ids = []
        for entry in self.results:
            _, time, algorithm, game_id, result = entry
            if game_id in [row[0] for row in game_ids]:
                index = [row[0] for row in game_ids].index(game_id)
                game_ids[index][algorithm*2-1] = result
                game_ids[index][algorithm*2] = round(time, 3)
            else:
                game_ids.append([game_id, 0, 0, 0, 0, 0, 0, 0, 0])
                game_ids[-1][algorithm*2-1] = result
                game_ids[-1][algorithm*2] = round(time, 3)

        for game in game_ids:
            line = ''
            for res in game:
                line += str(res) + '|'
            f.write(line + '\n')

        f.close()

    def event_handler(self):
        event, values = self.window.read(timeout=100)

        # handle queue from other GUI windows
        while len(self.queue) > 0:
            self.read_queue(self.queue.pop(-1))

        # handle queue for solvers
        while len(self.games_queue) > 0:
            self.read_games_queue(self.games_queue.pop(-1))

        if event in (None,):
            return False

        if event in '-SOLVE_SIM-':
            self.reset_games()
            self.init_games()

            checked_solvers = []
            if self.window['-CH_SOLVER1-'].get():
                checked_solvers.append(1)
            if self.window['-CH_SOLVER2-'].get():
                checked_solvers.append(2)
            if self.window['-CH_SOLVER3-'].get():
                checked_solvers.append(3)
            if self.window['-CH_SOLVER4-'].get():
                checked_solvers.append(4)

            self.all_to_solve = len(checked_solvers)*len(self.games)
            self.window['-PROGRESS-'].update_bar(0, self.all_to_solve)

            for sol in checked_solvers:
                self.algorithm = sol
                for idx, game in enumerate(self.games):
                    game.choose_solver(SOLVERS[self.algorithm])
                    threading.Thread(target=game.solve, args=(self.calc_timeout, idx, self.algorithm), daemon=True).start()

        if event in '-SOLVE_CHECKED-':
            self.reset_games()
            self.init_games()

            checked_solvers = []
            if self.window['-CH_SOLVER1-'].get():
                checked_solvers.append(1)
            if self.window['-CH_SOLVER2-'].get():
                checked_solvers.append(2)
            if self.window['-CH_SOLVER3-'].get():
                checked_solvers.append(3)
            if self.window['-CH_SOLVER4-'].get():
                checked_solvers.append(4)

            self.all_to_solve = len(checked_solvers)*len(self.games)
            self.window['-PROGRESS-'].update_bar(0, self.all_to_solve)

            threading.Thread(target=self.solve_separately, args=(checked_solvers,), daemon=True).start()

        if event in '-TIMEOUT-':
            self.calc_timeout = int(self.window['-TIMEOUT_INPUT-'].get())
            sg.popup_auto_close(f'Set timeout to {self.calc_timeout} s', auto_close_duration=1, button_type=sg.POPUP_BUTTONS_NO_BUTTONS, title='')

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

        if not self.database_gui_opened and (event == 'Browse database' or event == '-BROWSE-DB-'):
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
