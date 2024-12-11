import wafle as wf
from itertools import pairwise

parsed = wf.M(filter(bool, open("inp.txt", "r").readlines())) | str.strip | str.split | wf.M
parsed |= lambda k: (k | int) >= list # type: ignore

def is_safe(l):
    if l[0] == max(l) and sorted(l, reverse=True) == l and all(wf.M(pairwise(l)) | (lambda k: 3 >= abs(k[0] - k[1]) >= 1)):
        return True
    elif sorted(l) == l and all(wf.M(pairwise(l)) | (lambda k: 3 >= abs(k[0] - k[1]) >= 1)):
        return True
    return False

parsed |= is_safe

print(parsed >= sum)