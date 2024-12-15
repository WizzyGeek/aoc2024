from collections import defaultdict
from functools import reduce
from operator import mul
import re
import wafle as wf


ls = wf.M(open("day14/in.txt", "r").readlines()) | str.strip
pat = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")

ps, vs = [], []
for l in ls:
    px, py, vx, vy = wf.M(pat.match(l).groups()) | int >= tuple
    p = complex(px, py)
    v = complex(vx, vy)
    ps.append(p)
    vs.append(v)

# print(ps, vs)

# mx, my = 11, 7
mx, my = 101, 103

qx, qy = mx // 2, my // 2

def position(p, v, s):
    n = p + v * s
    return complex(n.real % mx, n.imag % my)

# 1 2
# 3 4

def quad(c):
    if c.real != qx and c.imag != qy:
        return (c.real > qx) + (c.imag > qy) * 2 + 1
    return 0

qc = [0] * 5
qs = defaultdict(lambda: 0)

for p, v in zip(ps, vs):
    qc[quad(position(p, v, 100))] += 1
    # qs[position(p, v, 100)] += 1
    # print(position(p, v, 100), p, v, quad(position(p, v, 100)))

print(reduce(mul, qc[1:], 1), qc)