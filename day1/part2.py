import wafle as wf
from collections import Counter

parsed = wf.M(filter(bool, open("inp.txt", "r").readlines())) | str.strip | str.split | (lambda k: (int(k[0]), int(k[1])))

a, b = (zip(*parsed) >= wf.mapper) | Counter

ss = 0
for k, v in a.items():
    if k in b:
        ss += v * k * b[k]

print(ss)