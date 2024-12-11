import enum
import wafle as wf
from itertools import dropwhile, takewhile
from collections import defaultdict

p = wf.M(open("in.txt", "r").readlines()) | str.strip | (lambda k: k.split(":")) | (lambda k: (int(k[0]), list(map(int, k[1].strip().split(" "))))) >= list

def can_e(tgt, lis: list, part2=True):
    if lis[0] > tgt: return False

    if len(lis) >= 2:
        top = lis.pop(0)
        second = lis[0]
        intr = top + second
        try:
            lis[0] = intr
            if can_e(tgt, lis):
                return True
            intr = top * second
            lis[0] = intr
            if can_e(tgt, lis):
                return True
            if part2:
                lis[0] = int(str(top) + str(second))
                if can_e(tgt, lis):
                    return True
        finally:
            lis[0] = second
            lis.insert(0, top)
    elif lis and lis[0] == tgt:
        return True

    return False

print(sum(map(lambda k: k[0], filter(wf.star(wf.partial(can_e, part2=False)), p))))
print(sum(map(lambda k: k[0], filter(wf.star(can_e), p))))