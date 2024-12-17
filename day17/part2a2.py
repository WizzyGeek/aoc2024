import z3
import wafle as wf

b, m = open("day17/in.txt", "r").read().split("\n\n")

m = wf.M(m.split()[-1].split(",")) | int >= list
b = wf.M(b.splitlines()) | str.split | (lambda k: int(k[-1])) >= list

solver = z3.Solver()

A = z3.BitVec("A", 50)
b = [A, 0, 0]

registers = [0, 1, 2, 3] + b + [float("NaN"), 0]

print(registers)

def do_op(opc, op, reg):
    # print(opc, op)
    match opc:
        case 0:
            reg[4] = reg[4] >> reg[op]
        case 1:
            reg[5] = reg[5] ^ op
        case 2:
            reg[5] = reg[op] & 7
        case 3:
            # we gonna ignore this shid lol
            # if reg[4] != 0:
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

def csat(p, reg):
    eidx = 0
    lp = len(p)
    while eidx != lp:
        x = do_op(p[reg[8]], p[reg[8] + 1], reg)
        if x != None:
            solver.add(x == p[eidx])
            eidx += 1
        reg[8] += 2

    solver.add(reg[4] == 0)

csat(m, registers)
print(solver)

if solver.check():
    print(solver.model())
