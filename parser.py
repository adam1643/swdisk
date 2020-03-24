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


def check_all_notes(filepath):
    try:
        f = open(filepath)
    except FileNotFoundError:
        return
    tree = ET.parse(filepath)
    root = tree.getroot()
    data = root[1][6].text.split(',')
    for d in data:
        if d not in note_list:
            note_list.append(d)


note_list = []
array = [f'puzzles/puzzle{i}.xml' for i in range(1, 33763+1)]
for a in array:
    check_all_notes(a)

print(note_list)
