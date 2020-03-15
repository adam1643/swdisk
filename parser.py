import xml.etree.ElementTree as ET
import ast
import numpy as np
tree = ET.parse('/Users/adamstanislawski/nonograms/3.xml')
root = tree.getroot()

# for type_tag in root.findall('puzzleset/puzzle/clues'):
#     value = type_tag.get('line')
#     print(value)

cols = root[1][9]
rows = root[1][10]

row_hints = []
col_hints = []

for row in rows:
    # value = type_tag.get('line')
    row_hints.append([])
    for num in row:
        row_hints[-1].append(int(num.text))

for col in cols:
    # value = type_tag.get('line')
    col_hints.append([])
    for num in col:
        col_hints[-1].append(int(num.text))

f = open('test1.txt', 'w')
f.write('{} '.format(len(row_hints)))
f.write('{}\n'.format(len(col_hints)))
f.write('{}\n'.format(row_hints))
f.write('{}\n'.format(col_hints))
f.close()

# def load_from_file(file):
#     f = open(file, 'r')
#     buffer = f.readline()
#     a, b = [int(s) for s in buffer.split(' ')]
#     buffer = f.readline()
#     r = ast.literal_eval(buffer)
#     buffer = f.readline()
#     c = ast.literal_eval(buffer)
#     print(a, b)
#     f.close()
#
# load_from_file('test.txt')