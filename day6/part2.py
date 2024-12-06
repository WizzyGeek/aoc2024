import enum
import wafle as wf
from itertools import dropwhile, takewhile
from collections import defaultdict

board = wf.M(open("in.txt", "r").readlines()) | str.strip | list >= list

mx = len(board[0])
my = len(board)

def isvalid(c: complex):
    return c.real < mx and c.imag < my and c.real >= 0 and c.imag >= 0

def getch(c: complex):
    return board[int(c.imag)][int(c.real)]

pos = 0

for idx, i in enumerate(board):
    for x, j in enumerate(i):
        if j == "^":
            pos = complex(x, idx)

vel = 0-1j

def turn(vel: complex):
    return complex(-1 * vel.imag, vel.real)

def isobs(c: complex):
    return isvalid(c) and getch(c) == "#"

def is_loop(pos, vel):
    visited = set()

    while isvalid(pos):
        if (pos, vel) in visited:
            return True
        visited.add((pos, vel))
        new = pos + vel
        # print("====")
        while isobs(new):
            # print(new)
            vel = turn(vel)
            new = pos + vel
        # print(pos, new)
        pos = new

    return False

def test_pos(x, y, pos, vel):
    if board[y][x] == "#":
        return False
    board[y][x] = "#"
    c = is_loop(pos, vel)
    board[y][x] = "."
    return c

s = 0
for idx, i in enumerate(board):
    for x, j in enumerate(i):
        if j != "^":
            s += test_pos(x, idx, pos, vel)
    print(idx)

print(s)

# print(len(visited), pos, vel)