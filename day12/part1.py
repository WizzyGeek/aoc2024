from collections import defaultdict
from functools import cache
import wafle as wf
from itertools import chain

board = wf.M(open("in.txt", "r").readlines()) | str.strip | list >= list

mx = len(board[0])
my = len(board)

def isvalid(c: complex):
    return c.real < mx and c.imag < my and c.real >= 0 and c.imag >= 0

def getch(c: complex):
    return board[int(c.imag)][int(c.real)]

parent = dict()
rank = dict()
children: dict[complex, set] = dict()

for y in range(my):
    for x in range(mx):
        c = complex(x,y)
        parent[c] = c
        rank[c] = 1
        children[c] = {c,}

def find(c: complex) -> complex:
    par = parent[c]
    while parent[par] != par:
        par = parent[par]
    return par

def union(a, b):
    pa = find(a)
    pb = find(b)

    if pa == pb:
        return

    rpa = rank[pa]
    rpb = rank[pb]

    if rpa > rpb:
        parent[pa] = pb
        children[pb].update(children[pa])
        del children[pa]
    elif rpa < rpb:
        parent[pb] = pa
        children[pa].update(children[pb])
        del children[pb]
    elif rpa == rpb:
        parent[pa] = pb
        children[pb].update(children[pa])
        del children[pa]
        rank[rpb] += 1

for y in range(my):
    for x in range(mx):
        c = complex(x,y)
        ch = getch(c)

        if y != my - 1 and getch(c + 1j) == ch:
            union(c, c + 1j)
        if x != mx - 1 and getch(c + 1) == ch:
            union(c, c + 1)

# print(children, len(children), list(map(len, children.values())))

def perim_cell(c, ch):
    s = 0
    for i in [1, -1, 1j, -1j]:
        s += (not isvalid(i + c)) or getch(i + c) != ch
    return s

c = 0
for rep, region in children.items():
    ch = getch(rep)
    area = len(region)
    peri = sum(map(wf.rpartial(perim_cell, ch), region))
    c += area * peri
    # print(ch, area, peri, area * peri)

print(c)