from collections import defaultdict
import enum
from itertools import filterfalse
import wafle as wf

b, m = open("ex.txt", "r").read().split("\n\n")

board = wf.M(b.split("\n")) | list >= list
m = "".join(filterfalse(str.isspace, m))

mx = len(board[0])
my = len(board)

def isvalid(c: complex):
    return c.real < mx and c.imag < my and c.real >= 0 and c.imag >= 0

def getch(c: complex):
    return board[int(c.imag)][int(c.real)]

pos = 0
for y, row in enumerate(board):
    for x, ch in enumerate(row):
        if ch == "@":
            pos = complex(x, y)

def ismovable(c: complex, d: complex):
    new = c + d
    if not isvalid(new):
        return False
    t = getch(new)
    if t == "#":
        return False
    if t == ".":
        return True
    if t == "O":
        return ismovable(new, d)

def move(c: complex, d: complex):
    new = c + d
    if not isvalid(new):
        return False
    t = getch(new)
    if t == "#":
        return False
    if t == ".":
        board[int(new.imag)][int(new.real)] = getch(c)
        board[int(c.imag)][int(c.real)] = "."
        return True
    if t == "O" or t == "@":
        if move(new, d):
            t = getch(new)
            board[int(new.imag)][int(new.real)] = getch(c)
            board[int(c.imag)][int(c.real)] = t
            return True
    # print("WTF", t, new, getch(c), c, d)
    return False

m2d = {
    "^": -1j,
    "v": 1j,
    "<": -1,
    ">": 1,
}


for mo in m:
    d = m2d[mo]
    if move(pos, d): pos += d
    # print(mo)
    # print("\n".join("".join(ch for ch in row) for row in board))
    # input()


print("\n".join("".join(ch for ch in row) for row in board))

s = 0
for y, row in enumerate(board):
    for x, ch in enumerate(row):
        if ch == "O":
            s += x + 100 * y

print(s)