import xml.etree.ElementTree as ET
import os


def parse_from_string_to_file(data, save_file):
    root = ET.fromstring(data)

    # column and row hints are saved as 9th and 10th element of puzzle XML
    cols = root[1][9]
    rows = root[1][10]

    row_hints = []
    col_hints = []

    # save row hints to dedicated array
    for row in rows:
        row_hints.append([])
        for num in row:
            row_hints[-1].append(int(num.text))

    # save column hints to dedicated array
    for col in cols:
        col_hints.append([])
        for num in col:
            col_hints[-1].append(int(num.text))

    # format data and save them to given file
    f = open(save_file, 'w')
    f.write('{} '.format(len(row_hints)))
    f.write('{}\n'.format(len(col_hints)))
    f.write('{}\n'.format(row_hints))
    f.write('{}\n'.format(col_hints))
    f.close()


def parse_puzzle_from_xml_file(filepath):
    # check if file exists, if not - return
    try:
        f = open(filepath)
    except FileNotFoundError:
        return None
    f.close()

    tree = ET.parse(filepath)
    root = tree.getroot()

    colors = len(list(root[1].getiterator('color')))
    if colors > 2:
        # TODO: handle more than 2 color puzzles
        return

    # DIFFICULTY LEVELS:
    # 1 - trivial
    # 2 - moderate lookahead
    # 3 - deep lookahead
    # 4 - some guessing
    # 5 - much guessing

    # difficulty is in 6th position
    notes = root[1][6].text
    if notes.__contains__('definitely trivial'):
        difficulty = 1
    elif notes.__contains__('definitely requires moderate lookahead'):
        difficulty = 2
    elif notes.__contains__('definitely requires deep lookahead'):
        difficulty = 3
    elif notes.__contains__('definitely requires some guessing'):
        difficulty = 4
    elif notes.__contains__('definitely requires much guessing'):
        difficulty = 5
    else:
        # difficulty unknown
        difficulty = 0

    if notes.__contains__('definitely unique'):
        is_unique = 1
    else:
        is_unique = 0

    # column and row hints are saved as 9th and 10th element of puzzle XML (ONLY FOR 2 COLOR PUZZLES!!!)
    cols = root[1][9]
    rows = root[1][10]

    row_hints = []
    col_hints = []

    # save row hints to dedicated array
    for row in rows:
        row_hints.append([])
        for num in row:
            row_hints[-1].append(int(num.text))

    # save column hints to dedicated array
    for col in cols:
        col_hints.append([])
        for num in col:
            col_hints[-1].append(int(num.text))

    # return data as tuple
    return len(row_hints), len(col_hints), row_hints, col_hints, is_unique, difficulty, colors


def remove_not_existing_puzzle(filepath):
    filepath = f'{filepath}'
    try:
        f = open(filepath)
    except FileNotFoundError:
        return
    a = f.readline()
    if a.__contains__("does not exist") or a.__contains__("not been published"):
        print(f"Puzzle {f.name} did not exist")
        os.remove(f.name)
