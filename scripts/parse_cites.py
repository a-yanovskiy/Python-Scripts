"""
Parse items from cites.txt (from e-book).
It groups cites by books, and creates own file for each book.
Writes to .md
"""

import re
import os
from itertools import groupby


def parse_cites(path):
    filename = os.path.join(path, 'cites.txt')
    pattern = r'(\d{4})-(\d{2}-\d{2})'
    reg = re.compile('[^a-zA-Zа-яА-Я1-9.,\s]|\n')

    with open(filename, 'r', encoding="utf8") as onyx:
        lines = onyx.readlines()

    grouped = groupby(lines, lambda x: x == '\n')

    listed = [list(group) for k, group in grouped if not k]

    result = {}

    for i in listed:
        for j in i:
            if re.search(pattern, j):
                key = i[i.index(j) + 2]
                val = ''.join(i[i.index(j) + 3:])
                try:
                    result[key] += '\n***\n' + val
                except KeyError:
                    result[key] = val

    for key, val in result.items():
        key = reg.sub('', key)
        book_path = os.path.join(path, key)
        with open(book_path + '.md', 'w', encoding="utf8") as f:
            f.write(val)

    f.close()


def main():
    path = ''
    parse_cites(path)


if __name__ == '__main__':
    main()
