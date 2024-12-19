from collections import defaultdict
from email.policy import default
import functools
from itertools import pairwise
from pprint import pprint
import wafle as wf
import re

p, cont = open("day19/in.txt", "r").read().split("\n\n")

p = wf.M(p.strip().split()) | (lambda k: k.strip(",")) >= set
cont = cont.splitlines()

# trie = dict()

# for k in p:
#     t = trie
#     for c in (k + "$"):
#         t[c] = t.get(c, dict() if c != "$" else None)
#         t = t[c]

bt = defaultdict(set)
for k in p:
    bt[k[0]].add(k)

# def num_match(idx, line, tre) -> int:
#     if idx == len(line) and "$" in tre:
#         return 1
#     if idx == len(line):
#         return 0

#     c = line[idx]
#     s = 0

#     if c in tre:
#         # print(" " * idx + c, end="\n")
#         s += num_match(idx + 1, line, tre[c])

#     if "$" in tre:
#         # print(" " * idx + "$", end="\n")
#         return num_match(idx + 1, line, trie[c]) + s

#     return s

@functools.cache
def num_match(line: str) -> int:
    if line == "":
        return 1

    s = 0
    for k in bt[line[0]]:
        if line.startswith(k):
            s += num_match(line.removeprefix(k))
    return s

s = 0
for idx, line in enumerate(cont):
    s += num_match(line)
    # print(str(idx), flush=True)
print(s)