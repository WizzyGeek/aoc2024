from collections import defaultdict, namedtuple
from queue import PriorityQueue
from functools import cache
import wafle as wf
from itertools import chain

board = wf.M(open("day16/ex.txt", "r").readlines()) | str.strip | list >= list

mx = len(board[0])
my = len(board)

def isvalid(c: complex):
    return c.real < mx and c.imag < my and c.real >= 0 and c.imag >= 0

def getch(c: complex):
    return board[int(c.imag)][int(c.real)]

# print(board, mx, my)
end = 0
start = 0

for y, row in enumerate(board):
    for x, ch in enumerate(row):
        if ch == "E": end = complex(x, y)
        if ch == "S": start = complex(x, y)

Node = namedtuple("Node", ["priority", "cost", "p", "v"])
Node.__lt__ = lambda self, value: self[0] < value[0]

def estimate_cost(p):
    return 100 * (abs(p.real - end.real) + abs(p.real - end.real)) + 1500 * (end.imag != end.imag) + 1500 * (end.real != end.real) + abs(p.real) + abs(p - end)

def make_rotations(node):
    if getch(node.p + node.v * 1j) != "#":
        yield 1j
    if getch(node.p + node.v * -1j) != "#":
        yield -1j

rotations = (1j, -1j) # a c

visited = {}
inf = 10000000000

strict_visited = {}

md = inf
mn = ()

q = PriorityQueue()
q.put_nowait(Node(estimate_cost(start), 0, start, 1+0j))

while not q.empty():
    state = q.get_nowait()
    visited[state.p] = min(visited.get(state.p, inf), state.cost)
    strict_visited[(state.p, state.v)] = min(strict_visited.get((state.p, state.v), inf), state.cost)

    for r in make_rotations(state):
        newv = state.v * r
        newp = state.p
        ncost = 1000 + state.cost if r != 1 else state.cost
        if (ncost - visited.get(newp, inf) <= 1000) and strict_visited.get((newp, newv), inf) > ncost:
            q.put_nowait(Node(ncost + estimate_cost(newp), ncost, newp, newv))

    if getch(state.p + state.v) != "#":
        newp = state.p + state.v
        q.put_nowait(Node(state.cost + 1 + estimate_cost(newp), state.cost + 1, newp, state.v))

    if (getch(state.p) == "E") and md > state.cost:
        md = min(md, state.cost)
        mn = state
        print(md, mn, q.qsize())