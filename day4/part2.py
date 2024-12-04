
import wafle as wf

board = wf.M(open("in.txt", "r").readlines()) | str.strip >= list
# print(board)

my = len(board)
mx = len(board[0])

def is_valid(c: complex):
    return c.real >= 0 and c.imag >= 0 and c.real < mx and c.imag < my

deltas = (
    -1-1j, 1-1j,
)

def getch(c):
    if not is_valid(c): return ""
    return board[int(c.imag)][int(c.real)]


def check(pos):
    if getch(pos) != "A":
        return False

    s = 0
    for i in deltas:
        if (getch(pos + i) + getch(pos - i)) in ("MS", "SM"):
            s += 1

    if s == 2:
        return 1
    return 0

s = 0
for i in range(my):
    for j in range(mx):
        s += check(complex(i, j))

print(s)