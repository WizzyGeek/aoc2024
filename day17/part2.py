from collections import defaultdict
import enum
from itertools import filterfalse, groupby
import wafle as wf

b, m = open("day17/ex2.txt", "r").read().split("\n\n")

m = wf.M(m.split()[-1].split(",")) | int >= list
b = wf.M(b.splitlines()) | str.split | (lambda k: int(k[-1])) >= list
print(b, m)

# 4 literals, 3 registers, NaN, follewed by IP
registers = [0, 1, 2, 3] + b + [float("NaN"), 0]
print(registers)

def do_op(opc, op, reg):
    match opc:
        case 0:
            reg[4] = reg[4] >> reg[op]
        case 1:
            reg[5] = reg[5] ^ op
        case 2:
            reg[5] = reg[op] & 7
        case 3:
            # we gonna ignore this shid lol
            if reg[4] != 0:
                reg[8] = op - 2
        case 4:
            reg[5] = reg[5] ^ reg[6]
        case 5:
            return reg[op] & 7
        case 6:
            reg[5] = reg[4]  >> reg[op]
        case 7:
            reg[6] = reg[4] >> reg[op]
        case x:
            print("WTF", x)
    return None


def execute_program(p, reg):
    eidx = 0
    lp = len(p)
    while reg[8] < lp:
        x = do_op(p[reg[8]], p[reg[8] + 1], reg)
        if x != None:
            if eidx < lp and p[eidx] != x:
                return False
            elif eidx >= lp:
                return False
            else:
                eidx += 1
        reg[8] += 2

    return eidx == lp


# regc = registers.copy()
# regc[4] = 117440
# print(execute_program(m, regc))

regc = registers.copy()
i = 0
while True:
    regc[4] = i
    regc[5:] = registers[5:]
    if execute_program(m, regc):
        print(i)
        break

    if i % 1000000 == 0: print("#", end="", flush=True)
    i += 1