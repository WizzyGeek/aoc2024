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

visited = set()

while isvalid(pos):
    visited.add(pos)
    new = pos + vel
    # print("====")
    while isobs(new):
        # print(new)
        vel = turn(vel)
        new = pos + vel
    # print(pos, new)
    pos = new

print(len(visited), pos, vel)