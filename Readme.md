# Nonograms

# Getting started
After downloading or cloning repository, please install all packages from requirements.txt file with command:
```sh
$ pip install -r requirements.txt
```
# Files
- main.py - main app script - use to start GUI
- maintenance.py - script for downloading puzzles/parsing puzzles/creating database - you do not need to use it if you use database file puzzles.db
- gui.py - file containing GUI class
- nonogram.py - file containing Nonogram class
- database.py - file containing DatabaseHandler class
- puzzle_downloader.py - file containing PuzzleDownloader class + methods for downloading puzzles in batches
- parser.py - file containing parser for XML files with puzzles
- puzzles.db - file with SQLite database containing over 9000 puzzles

# DB structure of puzzles.db:
TABLE 'puzzle':
| id              | rows       | cols | row_hints | col_hints | is_unique | difficulty | colors
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| INT (PRIMARY KEY) | INT        | INT  | TEXT | TEXT | INT | INT | INT
