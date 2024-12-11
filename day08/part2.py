import enum
import pprint
import wafle as wf
from itertools import combinations, dropwhile, pairwise, product, takewhile
from collections import defaultdict

board = wf.M(open("in.txt", "r").readlines()) | str.strip | list >= list

mx = len(board[0])
my = len(board)

def isvalid(c: complex):
    return c.real < mx and c.imag < my and c.real >= 0 and c.imag >= 0

def getch(c: complex):
    return board[int(c.imag)][int(c.real)]

positions = defaultdict(list)

for y, i in enumerate(board):
    for x, j in enumerate(i):
        positions[j].append(complex(x, y))

def make_pair_pos(a, b):
    ta = a - a
    ab = b - a

    pro = b + ab
    while isvalid(pro):
        yield pro
        pro += ab

    pro = a - ab
    while isvalid(pro):
        yield pro
        pro -= ab

    yield a
    yield b

del positions["."]

an = set()

for c, poss in positions.items():
    for a, b in combinations(poss, 2):
        for n in make_pair_pos(a, b):
            board[int(n.imag)][int(n.real)] = "#"
            an.add(n)

print(len(an))
# print("\n".join("".join(b) for b in board))