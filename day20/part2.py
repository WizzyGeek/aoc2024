from collections import defaultdict, namedtuple
from queue import PriorityQueue
from functools import cache
from typing import Any
import wafle as wf
from itertools import chain, product

board = wf.M(open("day20/ex2.txt", "r").readlines()) | str.strip | list >= list

mx = len(board[0])
my = len(board)

def isvalid(c: complex):
    return c.real < mx and c.imag < my and c.real >= 0 and c.imag >= 0

def getch(c: complex):
    if not isvalid(c): return "#"
    return board[int(c.imag)][int(c.real)]

def setch(c: complex, v: Any):
    board[int(c.imag)][int(c.real)] = v


# print(board, mx, my)
# print("\n".join("".join(ch for ch in row) for row in board))
end = 0
start = 0

for y, row in enumerate(board):
    for x, ch in enumerate(row):
        if ch == "E": end = complex(x, y)
        if ch == "S": start = complex(x, y)

Node = namedtuple("Node", ["priority", "cost", "p"])
Node.__lt__ = lambda self, value: self[0] < value[0]

def estimate_cost(p):
    return abs(p - end) / 2 + abs(p.real - end.real) + abs(p.imag - end.imag)

def make_rotations(node):
    if getch(node.p + 1j) != "#":
        yield 1j
    if getch(node.p - 1j) != "#":
        yield -1j
    if getch(node.p + 1) != "#":
        yield 1
    if getch(node.p - 1) != "#":
        yield -1

rotations = (1j, -1j) # a c

visited = {}
inf = 10000000000

# strict_visited = {}

md = inf
mn = ()

q = PriorityQueue()
q.put_nowait(Node(estimate_cost(start), 0, start))

while not q.empty():
    state = q.get_nowait()
    visited[state.p] = min(visited.get(state.p, inf), state.cost)

    # k = getch(state.p)
    # setch(state.p, "O")
    # print("\n".join("".join(ch for ch in row) for row in board))
    # setch(state.p, k)
    # input()
    # strict_visited[(state.p, state.v)] = min(strict_visited.get((state.p, state.v), inf), state.cost)

    for r in make_rotations(state):
        newp = state.p + r
        ncost = state.cost + 1
        if (visited.get(newp, inf) > ncost):
            q.put_nowait(Node(ncost + estimate_cost(newp), ncost, newp))

    if (state.p == end) and md > state.cost:
        md = min(md, state.cost)
        mn = state
        print(md, mn, q.qsize())

delta = set()
for m in range(1, 21):
    delta |= set(map(lambda i: complex(i, m - i), range(m + 1)))
    delta |= set(map(lambda i: complex(i, i - m), range(m + 1)))
    delta |= set(map(lambda i: complex(-1 * i, m - i), range(m + 1)))
    delta |= set(map(lambda i: complex(-1 * i, i - m), range(m + 1)))

# delta = set(filter(lambda k: abs(k.real) + abs(k.imag) <= 20, delta))

print(len(delta))

st = defaultdict(lambda: 0)

sm = 0
for k, cost in visited.items():
    for d in delta:
        k2 = k + d
        savings = -1 * inf
        if getch(k2) != "#":
            savings = (visited[k2] - cost) - int(abs(d.real) + abs(d.imag))

        if savings >= 30:
            sm += 1
            st[savings] += 1
            # print(k, k2)

print(st)
print(sm)