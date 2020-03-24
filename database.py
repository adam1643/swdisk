import sqlite3
import ast


class DatabaseHandler:
    def __init__(self):
        self.conn = sqlite3.connect('puzzles.db')
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
                            (rows, cols, f'{row_hints}', f'{col_hints}', is_unique, difficulty, colors))
        self.conn.commit()

    def select_data_by_id(self, id):
        self.cursor.execute('''SELECT * FROM puzzle WHERE id=?''', str(id))
        return self.cursor.fetchall()

    def select_unique_data_by_size(self, row, col):
        self.cursor.execute('''SELECT * FROM puzzle WHERE is_unique=0 and rows=? and cols=?''', (row, col))
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


dh = DatabaseHandler()
# create_table(c)
# conn.commit()
# dh.insert_data(6, 6, [[1,2],[3,4],[5,6]], [[7,8],[9,10],[11,12]], 0, 3, 2)
# conn.commit()
b = dh.select_data_by_id(6)
print(dh.parse_data_from_database(b[0]))
dh.close_connection()

