import re
import wafle as wf

c = open("in.txt", "r").read()

s = 0
f = True
for i, j, d in re.findall(r"mul\((\d+),(\d+)\)|(do\(\)|don't\(\))", c):
    if d == "don't()":
        f = False
        continue
    elif d == "do()":
        f = True
    elif f:
        s += int(i) * int(j)

print(s)