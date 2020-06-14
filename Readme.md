# Nonograms

# Getting started
**This project is for `python3` only and requires `tkinter` library installed!**


After downloading or cloning repository, please install all packages from requirements.txt file with command:
```sh
$ python3 -m pip install -r requirements.txt
```

Alternatively, i.e. PyCharm will automatically suggest you to install modules from `requirements.txt` file when you open this repository as project.

To run the application run `main.py` file while in main project directory:
```sh
$ python3 main.py
```

**Application works on all systems, however saving results to file is available only for Unix based systems (Ubuntu, Debian, macOS, etc.)**

# DB structure of puzzles.db:
TABLE `puzzle`:

| id              | rows       | cols | row_hints | col_hints | is_unique | difficulty | colors
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| INT (PRIMARY KEY) | INT        | INT  | TEXT | TEXT | INT | INT | INT

### Sample row from DB
| id              | rows       | cols | row_hints | col_hints | is_unique | difficulty | colors
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
1|10|5|[[2], [2, 1], [1, 1], [3], [1, 1], [1, 1], [2], [1, 1], [1, 2], [2]]|[[2, 1], [2, 1, 3], [7], [1, 3], [2, 1]]|1|0|2
