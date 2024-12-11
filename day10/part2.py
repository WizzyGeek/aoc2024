from functools import cache
from operator import getitem
import wafle as wf
from itertools import chain

board = wf.M(open("ex2.txt", "r").readlines()) | str.strip | (lambda k: wf.M(k) | int >= list) >= list

mx = len(board[0])
my = len(board)

e = lambda: (wf.M(board) | enumerate > enumerate)
ec = lambda: (
    e()
    | wf.star(
        lambda idx, l:
            wf.M(l) |
            (lambda k: (complex(k[0], idx), k[1]))
    )
)

ecxf = lambda x: (
    ec()
    | wf.partial(filter, lambda k: k[1] == x)
    | list
    | (lambda l: list(map(wf.rpartial(getitem, 0), l)))
    > chain.from_iterable
)

ecnf = ecxf(9)

c2bs = dict(ecnf
             .apply(enumerate)
             .map(lambda k: (k[1], 1 << k[0]))
             )

def isvalid(c: complex):
    return c.real < mx and c.imag < my and c.real >= 0 and c.imag >= 0

def getch(c: complex):
    return board[int(c.imag)][int(c.real)]

deltas = wf.M([1, -1, 1j, -1j])

@cache
def nclosure(c: complex) -> int:
    curr = getch(c)
    if curr == 9:
        return 1
    return (deltas
     .map(lambda k: k + c)
     .apply(wf.partial(filter, lambda k: isvalid(k) and (getch(k) - curr == 1)))
     .map(nclosure)
     .consume(sum)
    )

eczf = ecxf(0)
print(eczf | nclosure >= sum)