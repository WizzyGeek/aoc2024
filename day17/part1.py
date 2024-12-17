from collections import defaultdict
import enum
from itertools import filterfalse, groupby
import wafle as wf

b, m = open("day17/in.txt", "r").read().split("\n\n")

m = wf.M(m.split()[-1].split(",")) | int >= list
b = wf.M(b.splitlines()) | str.split | (lambda k: int(k[-1])) >= list
print(b, m)

# 4 literals, 3 registers, NaN, follewed by IP
registers = [0, 1, 2, 3] + b + [float("NaN"), 0]
print(registers)

out = ""

def do_op(opc, op, reg):
    global out
    match opc:
        case 0:
            reg[4] = reg[4] // (1 << reg[op])
        case 1:
            reg[5] = reg[5] ^ op
        case 2:
            reg[5] = reg[op] % 8
        case 3:
            if reg[4] != 0:
                reg[8] = op - 2
        case 4:
            reg[5] = reg[5] ^ reg[6]
        case 5:
            out += str(reg[op] % 8) + ","
        case 6:
            reg[5] = reg[4] // (1 << reg[op])
        case 7:
            reg[6] = reg[4] // (1 << reg[op])
        case x:
            print("WTF", x)

def execute_program(p, reg):
    lp = len(p)
    while reg[8] < lp:
        do_op(p[reg[8]], p[reg[8] + 1], reg)
        reg[8] += 2

execute_program(m, registers)

print("out: ", out)