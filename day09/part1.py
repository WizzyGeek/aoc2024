import enum
import wafle as wf
from itertools import dropwhile, repeat, takewhile, chain
from collections import defaultdict

p = wf.M(open("in.txt", "r").read()) | str.strip >= list

c = [None] * (len(p) * 10)

# print(c)
k = True
l = 0
f = 0
free = []
ff = 0
for i in p:
    if k:
        c[l:(l+int(i))] = repeat(f, int(i))
        f += 1
    else:
        ff += int(i)
        free.append(range(l,l+int(i)))

    l += int(i)
    k = not k

l = l - 1

fpos = chain.from_iterable(free)

for _ in range(ff):
    f = c[l]
    if f != None:
        pos = next(fpos)
        if pos < l:
            c[pos] = f
            c[l] = None
            l = l - 1
        else:
            # print("WTF", c, pos, f)
            break
    else:
        l = l - 1

s = 0
for i, j in enumerate(c):
    if j == None: break
    s += i * j

print(s)