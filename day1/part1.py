import wafle as wf

parsed = wf.M(filter(bool, open("inp.txt", "r").readlines())) | str.strip | str.split | (lambda k: (int(k[0]), int(k[1])))

a, b = (zip(*parsed) >= wf.mapper) | list
a.sort()
b.sort()

_ = wf.M(zip(a, b))
_ |= lambda k: k[0] - k[1]
_ |= abs

print(_ >= sum)