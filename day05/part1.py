import wafle as wf
from itertools import dropwhile, takewhile
from collections import defaultdict

parsed = wf.M(open("in.txt", "r").readlines()) | str.strip >= list
coms = wf.M(takewhile(lambda k: k != "", parsed)) | (lambda k: k.split("|")) | (lambda p: tuple(map(int, p))) >= list
rest = wf.M(list(dropwhile(lambda k: k!= "", parsed))[1:]) | (lambda k: k.split(",")) | (lambda p: list(map(int, p))) >= list

before, after = defaultdict(set), defaultdict(set)

for i, j in coms:
    before[j].add(i)
    after[i].add(j)

def is_correct(i):
    seen = set()
    for j in i:
        if after[j].intersection(seen):
            return False
        seen.add(j)
    return True

s = 0
for i in rest:
    if is_correct(i):
        s += i[len(i) // 2]

print(s)