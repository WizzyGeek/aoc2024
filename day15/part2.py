from collections import defaultdict
import enum
from itertools import filterfalse
import wafle as wf

b, m = open("in.txt", "r").read().split("\n\n")

b = b.replace("#", "##").replace(".", "..").replace("O", "[]").replace("@", "@.")
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


def move(c: complex, d: complex, constrained = False):
    new = c + d
    if not isvalid(new):
        return False
    ch = getch(c)
    if ch == ".":
        return True
    if ch == "#":
        return False

    t = getch(new)
    if t == "#":
        return False
    if t == ".":
        board[int(new.imag)][int(new.real)] = getch(c)
        board[int(c.imag)][int(c.real)] = "."
        return True
    if d.real != 0:
        if t == "[" or t == "]":
            if move(new, d):
                t = getch(new)
                board[int(new.imag)][int(new.real)] = getch(c)
                board[int(c.imag)][int(c.real)] = t
                return True
            else:
                return False
    else:
        new2 = 0
        if t == "[":
            new2 = new + 1
        elif t == "]":
            new2 = new - 1

        if move(new, d) and move(new2, d, True):
            t = getch(new)
            board[int(new.imag)][int(new.real)] = getch(c)
            board[int(c.imag)][int(c.real)] = t
            t2 = getch(new2)
            # c2 = new2 - d
            # board[int(new2.imag)][int(new2.real)] = getch(c2)
            # board[int(c2.imag)][int(c2.real)] = t2
            return True
    return False

m2d = {
    "^": -1j,
    "v": 1j,
    "<": -1,
    ">": 1,
}
debug2d = {
    "D": -1,
    "C": 1,
    "B": 1j,
    "A": -1j
}

backup = list(map(list.copy, board))

# print("\n".join("".join(ch for ch in row) for row in board))

for mo in m:
    # d = debug2d[input()[-1]]
    d = m2d[mo]
    backup = list(map(list.copy, board))
    if move(pos, d):
        pos += d
    else:
        board = backup

    # print(mo)
    # print("\n".join("".join(ch for ch in row) for row in board))
    # print("\n".join("".join(ch for ch in row) for row in backup))


# print("\n".join("".join(ch for ch in row) for row in board))s

s = 0
for y, row in enumerate(board):
    for x, ch in enumerate(row):
        if ch == "[":
            s += x + 100 * y

print(s)