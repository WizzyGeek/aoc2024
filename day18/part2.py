from collections import defaultdict, namedtuple
from queue import PriorityQueue
from functools import cache
from typing import Any
import wafle as wf
from itertools import chain

mx = 71
my = mx

cords = wf.M(open("day18/in.txt", "r").readlines()) | (lambda k: complex(*map(int, k.split(",")))) >= list

board = [["."] * mx for _ in range(my)]

def isvalid(c: complex):
    return c.real < mx and c.imag < my and c.real >= 0 and c.imag >= 0

def getch(c: complex):
    if not isvalid(c): return "#"
    return board[int(c.imag)][int(c.real)]

def setch(c: complex, v: Any):
    board[int(c.imag)][int(c.real)] = v


for i in cords[:1024]:
    setch(i, "#")

# print(board, mx, my)
print("\n".join("".join(ch for ch in row) for row in board))
end = 0
start = 0


end = complex(mx-1, my-1)
start = 0

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

inf = 10000000000

def visitable():
    visited = {}

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

        if (state.p == end):
            return True
    return False

# linear executed in time it took to code
# def make_board()

# def bin_search():
#     lo = 1024
#     hi = len(cords) - 1

for idx, i in enumerate(cords[1024:], 1024):
    setch(i, "#")
    if not visitable():
        print(idx, i.real + "," + "i.imag")
        break

# forgot to print solution
# xxxx = int("redacted")
# print(cords[xxxx])