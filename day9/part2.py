import wafle as wf
from collections import defaultdict

p = wf.M(open("in.txt", "r").read()) | str.strip >= list

files = []
frees = defaultdict(list)
k = True
l = 0
f = 0
free = 0
for _, i in enumerate(p):
    if k:
        files.append((int(i), l, f))
        l += int(i)
        f += 1
    else:
        frees[int(i)].append((int(i), l))
        l += int(i)
        free += int(i)
    k = not k

l = l - 1

for k in frees:
    frees[k].sort(key=lambda k: k[1])

def getfree(k, w):
    m = None, 100000000000000000
    l = -1
    for f in frees:
        if k <= f and frees[f] and m[1] > frees[f][0][1] and frees[f][0][1] < w:
            m = frees[f][0]
            l = f
    if l > -1:
        return frees[l].pop(0)
    return m

newalloc = []

while files:
    much, where, what = files.pop()
    muchf, wheref = getfree(much, where)
    if muchf != None:
        newfile = (much, wheref, what)
        newfree = (muchf - much, wheref + much)
    else:
        newfile = (much, where, what)
        newfree = (muchf, wheref)

    if newfree[0] and newfree[0] > 0:
        frees[newfree[0]].append(newfree)
        frees[newfree[0]].sort(key=lambda k: k[1])

    newalloc.append(newfile)

# print(newalloc)

s = 0
for much, where, what in newalloc:
    s += what * sum(range(where, where + much))

print(s)
