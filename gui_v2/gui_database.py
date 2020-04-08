import PySimpleGUI as sg
from database import DatabaseHandler


class GUIDatabase:
    def __init__(self, queue):
        self.queue = queue

        self.layout = None
        self.window = None

        self.db_handler = DatabaseHandler('puzzles.db')
        self.selected_data = []

    def set_layout(self):
        diff_layout = [[sg.Checkbox('Very easy', size=(15, 1))], [sg.Checkbox('Easy', default=True)],
                        [sg.Checkbox('Medium', size=(15, 1))], [sg.Checkbox('Hard', default=True)],
                        [sg.Checkbox('Very hard', size=(15, 1))]]
        results_layout = [[sg.Text('ID\tRows\tCols\tDiff', size=(30, 1))],
                          [sg.Listbox(key='-SEL_PUZZLES-', values=[], select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED, size=(30, 15))],
                          [sg.Button(button_text='Load all puzzles'), sg.Button(button_text='Load selected puzzles')]]

        self.layout = [[sg.Text('Search in database'), sg.Text('', key='-OUTPUT-')],
                       [sg.Frame('Difficulty', diff_layout)],
                       [sg.Text('No. of rows', size=(10, 1)), sg.InputCombo(('<', '<=', '=', '>=', '>'), default_value='=', size=(3, 1)), sg.InputCombo([str(5*i) for i in range(1, 21)], default_value=5, size=(8, 1))],
                       [sg.Text('No. of cols', size=(10, 1)), sg.InputCombo(('<', '<=', '=', '>=', '>'), default_value='=', size=(3, 1)), sg.InputCombo([str(5 * i) for i in range(1, 21)], default_value=5, size=(8, 1))],
                       [sg.Submit(button_text='Search', tooltip='Click to submit this form')],
                       [sg.Frame('Results', results_layout)]
        ]

        self.window = sg.Window('Database browser', self.layout, finalize=True, resizable=True)

    def prepare_select(self, values):
        difficulties = [i for i in range(0, 5) if values[i] is True]
        difficulties = str(tuple(difficulties))
        rows = values[6]
        cols = values[8]

        sql = f'SELECT id, rows, cols, difficulty from puzzle where difficulty in {difficulties} and rows{values[5]}{rows} and cols{values[7]}{cols} order by id;'
        data = self.db_handler.query_sql(sql)

        # parse data for displaying
        parsed_data = [f'{d[0]}\t\t{d[1]}\t\t{d[2]}\t{d[3]}' for d in data]
        self.window['-SEL_PUZZLES-'].update(values=parsed_data)

        # save IDs of selected puzzles
        self.selected_data = [d[0] for d in data]

    def event_handler(self):
        event, values = self.window.read(timeout=0)

        if event in (None,):
            return False

        if event in 'Load all puzzles':
            if len(self.selected_data) > 0:
                self.queue.append(['ids', self.selected_data])
                self.window.close()
                return False

        if event in 'Load selected puzzles':
            selected = self.window['-SEL_PUZZLES-'].get_indexes()
            self.queue.append(['ids', [self.selected_data[i] for i in selected]])
            self.window.close()
            return False

        if event in 'Search':
            self.prepare_select(values)
        return True
