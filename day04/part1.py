import wafle as wf

board = wf.M(open("in.txt", "r").readlines()) | str.strip >= list
print(board)

my = len(board)
mx = len(board[0])

def is_valid(c: complex):
    return c.real >= 0 and c.imag >= 0 and c.real < mx and c.imag < my

deltas = (
    -1-1j, 0-1j, 1-1j,
    -1+0j,       1+0j,
    -1+1j, 0+1j, 1+1j,
)

word = "XMAS"

def getch(c):
    if not is_valid(c): return ""
    return board[int(c.imag)][int(c.real)]

def check(pos):
    if getch(pos) != word[0]:
        return False

    s = 0
    for i in deltas:
        if getch(pos + i) == word[1] and getch(pos + i * 2) == word[2] and getch(pos + i * 3) == word[3]:
            s += 1

    return s

s = 0
for i in range(my):
    for j in range(mx):
        s += check(complex(i, j))

print(s)