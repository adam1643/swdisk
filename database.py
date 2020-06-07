import sqlite3
import ast
import numpy as np


class DatabaseHandler:
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.cursor = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    def create_table(self):
        try:
            self.cursor.execute('''DROP TABLE puzzle''')
        except:
            print("Error")
            pass

        new_table = '''CREATE TABLE puzzle
        (id INTEGER PRIMARY KEY, rows INTEGER, cols INTEGER, row_hints TEXT, col_hints TEXT, is_unique INTEGER, difficulty INTEGER, colors INTEGER)'''
        self.cursor.execute(new_table)
        self.conn.commit()

    def insert_data(self, rows, cols, row_hints, col_hints, is_unique, difficulty, colors):
        self.cursor.execute('''INSERT INTO puzzle (rows, cols, row_hints, col_hints, is_unique, difficulty, colors) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (rows, cols, str(row_hints), str(col_hints), is_unique, difficulty, colors))
        self.conn.commit()

    def select_data_by_id(self, game_id):
        game_id = str(game_id)
        self.cursor.execute('''SELECT * FROM puzzle WHERE id=?''', (game_id,))
        return self.cursor.fetchall()

    def select_unique_data_by_size(self, row, col):
        self.cursor.execute('''SELECT * FROM puzzle WHERE is_unique=0 and rows=? and cols=?''', (row, col))
        return self.cursor.fetchall()

    def select_square_data_by_id(self, game_id):
        game_id = str(game_id)
        self.cursor.execute('''SELECT * FROM puzzle WHERE rows=cols AND id=?''', (game_id,))
        return self.cursor.fetchall()

    def select_unique_square_data_by_id(self, game_id):
        game_id = str(game_id)
        self.cursor.execute('''SELECT * FROM puzzle WHERE is_unique=1 AND rows=cols AND id=?''', (game_id,))
        return self.cursor.fetchall()

    '''Select all unioque square nonograms from database'''
    def select_unique_square_data(self):
        self.cursor.execute('''SELECT * FROM puzzle WHERE is_unique=1 AND rows=cols''')
        return self.cursor.fetchall()

    '''Select unique squares nonograms at easy level - easy level are nonograms with size from 5x5 to 20x20'''
    def select_easy_unique_square_data(self):
        self.cursor.execute('''SELECT * FROM puzzle WHERE is_unique=1 AND rows=cols AND (rows > 4 AND rows < 21)''')
        return self.cursor.fetchall()

    '''Select unique squares nonograms at medium level - easy level are nonograms with size from 21x21 to 40x40'''
    def select_medium_unique_square_data(self):
        self.cursor.execute('''SELECT * FROM puzzle WHERE is_unique=1 AND rows=cols AND (rows > 20 AND rows < 41)''')
        return self.cursor.fetchall()

    '''Select unique squares nonograms at hard level - easy level are nonograms with size from 41x41 to 99x99'''
    def select_hard_unique_square_data(self):
        self.cursor.execute('''SELECT * FROM puzzle WHERE is_unique=1 AND rows=cols AND (rows > 40 AND rows < 100)''')
        return self.cursor.fetchall()

    '''Method returns random 100 unique square nonograms at specific level'''
    def select_random_100_unique_square_data_by_level(self, level):
        if level == "easy":
            data = self.select_easy_unique_square_data()
        elif level == "medium":
            data = self.select_medium_unique_square_data()
        elif level == "hard":
            data = self.select_hard_unique_square_data()
        else:
            data = self.select_unique_square_data()

        np.random.shuffle(data)
        return data[:100]

    def query_sql(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def parse_data_from_database(self, data):
        id = data[0]
        rows = data[1]
        cols = data[2]
        row_hints = ast.literal_eval(data[3])
        col_hints = ast.literal_eval(data[4])
        is_unique = True if data[5] == 1 else False
        difficulty = data[6]
        colors = data[7]

        return id, rows, cols, row_hints, col_hints, is_unique, difficulty, colors


