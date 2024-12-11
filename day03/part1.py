import re
import wafle as wf

c = open("in.txt", "r").read()

print(wf.M(re.findall(r"mul\((\d+),(\d+)\)", c)) | (lambda k: int(k[0]) * int(k[1])) >= sum)