from collections import defaultdict
from functools import reduce
from operator import mul
import re
import time
import wafle as wf
from math import lcm


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

qc = [0] * 5
qs = defaultdict(lambda: 0)

# hypotheses: Cycle length of all point is max mx * my
# since px + s * vx modulo mx == px
# and py + s * vy modulo my == py
# verified, it is exactly mx * my

# lemma:
# To find a desired state in a cycle we need to explore only n / 2 + 1 states
# where n in loop length

# hypotheses 2: every robot goes to every location, verified

# hypothese 3: A picture of a christmas tree will have least mutual distance, VERIFIED!!!!

def compute_score(se):
    s = 0
    for p in se:
        for p2 in se:
            s += abs(p - p2)
        # if s > lm:
        if s > 7812246.078861076: # I forgot to print the time lol
            return 10000000000
    return s

bo = [list("." * mx) for _ in range(my)]

lm = 100000000000
mm = set()
ms = 0

for s in range(8080, 8091): # forgot to print solutiom :(
    m = {p,}
    for p, v in zip(ps, vs):
        m.add(position(p, v, s))
    # if len(m) < lm:
    # score = len(m)
    score = compute_score(m)
    if score < lm:
        mm = lm
        lm = score
        ms = s
    if s % 10 == 0:
        print(s, lm)

print(lm)

bo = [list("." * mx) for _ in range(my)]
for p, v in zip(ps, vs):
    t = position(p, v, ms)
    bo[int(t.imag)][int(t.real)] = "1"

print("\n".join("".join(ch for ch in row) for row in bo))
print(ms)

# Visual try, I stopped right before the colution lol
# now = time.time()
# try:
#     for s in range(1, mx * my + 1):
#         # flag = False
#         # for p, v in zip(ps, vs):
#         #     t = position(p, v, s)
#         #     if abs(t.real - qx) <= 1:
#         #         flag = True
#         # if flag:
#         bo = [list("." * mx) for _ in range(my)]
#         for p, v in zip(ps, vs):
#             t = position(p, v, s)
#             bo[int(t.imag)][int(t.real)] = "1"
#         print("\n".join("".join(ch for ch in row) for row in bo))
#         print("==")
#         input()
# except KeyboardInterrupt:
#     print("Seconds per second: ", s / (time.time() - now), "| steps: ", s, " | Time to 10403: ", 10403 / (s / (time.time() - now)))

# len 33
# vertical lines, 16, 46, 29 spaces in between
# ................1..............1..1.1.........1......................................................

# len 31
# Y lines, 30, 62, 31 spaces in betwween

# ....................................................................................................1
# ......................1..............................................................................
# ..........................................1..........................................................
# .......1.........1............................1......................................................
# .1...................................................................................................
# ........................................................................1............................
# ...........1.........................................................................................
# .................1...............................................................1...................
# .........................................................................................1...........
# .....................................................................................................
# 1.......1....................................................................1.......................
# 11....1..............................................................................................
# ..................1.....................1............................................................
# .............1...................................................1...................................
# ............................................................1.................1......................
# ........................................................................................1............
# ...........1....1............................1.......................................................
# ...................................................................................1.................
# ...1.................................................1........................................1......
# ....................1..1..........................1..................................................
# .....................................................................................................
# ................1....................................................................................
# .................................................................................1....1...1..........
# ..................................1......1................................1..........................
# ............................1.............................................1..........................
# ....................................................1................................................
# ....................................................................................................1
# ..............................................................................1.....1................
# ....1.........................1.........................1.................................1..........
# .....................................................................................................
# 1..1......11.11........1...1.11......1.........1..1...1...1......1..11...1.1.1.11.1..........1.1.....
# .....................1.......................................................................1.......
# .................................1..........1..............1..........1..............................
# .................................1...........1.......................1...............................
# ...............................................................1...................................1.
# ......1..................................................1...................1.......................
# .........1.1............1.......................................1...............1.......1............
# .....................................1.....................1....1.......1......1.............1.......
# .......1.....................1............1...................................1.........1....1...1..1
# ...111..1.....................................1..1.......1......11............1..........1...........
# ...........1.......1.............11........1....1.......1...1............1...........................
# .......1..........1.....1..1........1.................1...........................11.........1.......
# .......1.........1...........1...............1...1.....11..1........................1.1.1............
# 11......1........................1..1..1....1...1.......1...1....1.....................1...1..1......
# ......1........111....1..............1.........1.1..........1..1...1...1......1........1.1....1.....1
# ..1......1....11.........................11..........1............1....1............1....1.......11..
# ...........1..........1........1......1.1..........1..1...1...........1....................1..11.....
# .1.......1...................1....1..........1.1..1......1......1....11......1..........1...1.....1..
# 1..1.1..1...1......1..1.........1.....1.............11...1................11.1.......1.............1.
# 1......11....1.11.1....1...1....1.................1.......1.......1.....1.........1.....11..1.....11.
# .......................11....1.1..1....1........111......1..1..1..............1......1........1..1..1
# .......1.1......11.....111..1..1...1.1....1....................1.......1........11.1...........1.....
# ..1.1....1...1..1.................1..............1....1..1.............1.1....1.1.1..1.1....1.1...1.1
# ......1.........1.1...11.1.1..................1....1.1.1..1..............1..1...1....1.....11.1..1...
# .........1....1.1..11.1.1...1.....1..1............1..1....1....1.......1...1..........1.............1
# .....1.....1.............1..................................................1.....1...............1..
# ................................1..111........................1.....................1................
# .1...............1.........1................................................1....11..................
# ....1...........1............................................................1.......................
# ...1..................1......1.......................................................................
# .................................................................1.................11................
# ...............1...........1..............................................1..........................
# ........1....111.1....1......1.....11..1......1.1...1....11......11....11...11..1....11.....1..1....1
# .....................................................................................................
# ....................................1...................................1............................
# .............................................................1.......................................
# ....................1................1...............................................................
# .......................................................1...........1.................................
# .............................................1.............1.........................................
# 11...................................................................................................
# .....................................................................................................
# .......1...........1..........................................1...........1..........................
# .........1..........................................................................1................
# .............................................................................1.1.....................
# ...............................................1....1.............1........................1.........
# ........................................................................................1............
# ............1.............................................................................1..........
# ........................1............................................................................
# .....................................................................................................
# .....................................................................................................
# .........................1....................................1......................................
# .....................1...............................................................1...............
# .........................1...........................................................................
# ..................1........................................1.........................................
# ...............1..................................1..........................................1.......
# ..................................................................1..................................
# ......................................................................1.........1....................
# ....................1...........................................................................1....
# .......................................................1.............................................
# .............................................................................................11......
# .....................................................................................................
# .....................................................................................................
# ......................................................................1..............................
# ....................................................................................................1
# ..............................................................................................1......
# .............................1...................................................1...................
# ..................................................1..................................................
# .1....................1..............................................................................
# ........................1..........................................1............1.............1......
# .............................................1.......................................................
# ..............................................................................1......................
# ................................................................1............1.......................
# ...........1..1....................................................1.................................