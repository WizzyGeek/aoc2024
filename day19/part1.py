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

# pprint(trie)

# Half way through realised I am writing a DFA
# to match a pattern


# forward match took too much time so reversed the matching process to
# reduce number of backtracks
pat = re.compile("^(?:" + "|".join(map("".join, map(reversed, p))) + ")+$")

s = 0
for idx, line in enumerate(cont):
    if pat.match("".join(reversed(line))) != None:
        s += 1
    if idx % 10 == 0: print("#", flush=True, end="")

print(s)