import enum
import wafle as wf
from itertools import dropwhile, takewhile
from collections import defaultdict

p = wf.M(open("in.txt", "r").read()) | str.strip >= list

c = [None] * (len(p) * 10)

print(c)
k = True
l = 0
f = 0
free = 0
for _, i in enumerate(p):
    if k:
        for j in range(int(i)):
            c[l] = f
            l += 1
        f += 1
    else:
        l += int(i)
        free += int(i)
    k = not k

l = l - 1

for _ in range(free):
    f = c[l]
    pos = c.index(None)
    if pos < l:
        c[pos] = f
        c[l] = None
        l = l - 1
    else:
        print("WTF", c, pos, f)
        break

s = 0
for i, j in enumerate(c):
    if j == None: break
    s += i * j

print(s)