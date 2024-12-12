from collections import defaultdict
from functools import cache
import wafle as wf
from itertools import chain, filterfalse, pairwise

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

def perim_cell(c, ch, pset):
    for i in [1, -1, 1j, -1j]:
        if (not isvalid(i + c)) or getch(i + c) != ch:
            pset.add(c + i / 2)

def vertical(c):
    return c.imag * 2 % 2 == 1

def diff_vperi(vedge, peri):
    return (vedge + 0.5j + 0.5 in peri) or (vedge + 0.5j - 0.5 in peri)

def diff_hperi(hedge, peri):
    return (hedge + 0.5 + 0.5j in peri) or (hedge + 0.5 - 0.5j in peri)

c = 0
for rep, region in children.items():
    ch = getch(rep)
    area = len(region)
    peri = set()
    wf.void(map(wf.rpartial(perim_cell, ch, peri), region))
    hset = filterfalse(vertical, peri)
    vset = filter(vertical, peri)

    ysame = defaultdict(list)
    for edge in vset:
        ysame[edge.imag].append(edge.real)

    xsame = defaultdict(list)
    for edge in hset:
        xsame[edge.real].append(edge.imag)

    sides = 0
    for col, edges in xsame.items():
        edges.sort()
        sides += sum(map(lambda k: k[1] - k[0] != 1 or (diff_vperi(complex(col, k[0]), peri)), pairwise(edges))) + 1

    for level, edges in ysame.items():
        edges.sort()
        sides += sum(map(lambda k: k[1] - k[0] != 1 or (diff_hperi(complex(k[0], level), peri)), pairwise(edges))) + 1


    c += area * sides


print(c)