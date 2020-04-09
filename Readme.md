# Nonograms

# Getting started
**This project is for `python3` only and requires `tkinter` library installed!**


After downloading or cloning repository, please install all packages from requirements.txt file with command:
```sh
$ pip3 install -r requirements.txt
```

Alternatively, i.e. PyCharm will automatically suggest you to install modules from `requirements.txt` file when you open this repository as project.
# Files
- main.py - main app script - use to start GUI
- maintenance.py - script for downloading puzzles/parsing puzzles/creating database - you do not need to use it if you use database file puzzles.db
- gui.py - file containing GUI class
- nonogram.py - file containing Nonogram class
- database.py - file containing DatabaseHandler class
- puzzle_downloader.py - file containing PuzzleDownloader class + methods for downloading puzzles in batches
- parser.py - file containing parser for XML files with puzzles
- puzzles.db - file with SQLite database containing over 9000 puzzles


# Nonogram structure

Nonogram board consists of 2D array which is indexed from left-top corner:

| (0, 0) | (1, 0) | (2, 0) | ... | (width, 0)
| ------ | ------ | ------ | ------ | ------
| (0, 1) | (1, 1) | (2, 1) | ... | (width, 1)
| (0, 2) | (1, 2) | (2, 2) | ... | (width, 2)
| ... | ... | ... | ... | ...
| (0, height) | (1, height) | ... | ... | (width, height)


#### Allowed value for board tiles are:
- `0` - color of the tile unknown; this is initial value for each tile
- `1` - tile is definetely black
- `-1` - tile is definetely white

Values `0` and `-1` are only for distguishing between tiles that have unknown color and tiles not colored (white). While checking for a solution only black tiles (with value `1`) count.

#### Retriving puzzle data for solving
You can retrieve puzzle data, such as hints and board rows/columns using these methods:
- `get_board_row(index)`
- `get_board_column(index)`
- `get_board_tile(x, y)`
- `get_hints_row(index)`
- `get_hints_column(index)`

Please use only method `set_board_tile(x, y, value)` for modifying puzzle data!

You can always use method `check_solution()` for checking if puzzle is solved correctly. It will return `True` is solution is correct and `False` otherwise.

# DB structure of puzzles.db:
TABLE `puzzle`:

| id              | rows       | cols | row_hints | col_hints | is_unique | difficulty | colors
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| INT (PRIMARY KEY) | INT        | INT  | TEXT | TEXT | INT | INT | INT

### Sample row from DB
| id              | rows       | cols | row_hints | col_hints | is_unique | difficulty | colors
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
1|10|5|[[2], [2, 1], [1, 1], [3], [1, 1], [1, 1], [2], [1, 1], [1, 2], [2]]|[[2, 1], [2, 1, 3], [7], [1, 3], [2, 1]]|1|0|2
