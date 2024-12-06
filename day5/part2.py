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

class Sortable:
    def __init__(self, val) -> None:
        self.val = val

    def __gt__(self, other) -> bool:
        return other.val in before[self.val]

    def __lt__(self, other) -> bool:
        return other.val in after[self.val]

s = 0
for i in rest:
    if not is_correct(i):
        i = sorted(map(Sortable, i))
        s += i[len(i) // 2].val

print(s)