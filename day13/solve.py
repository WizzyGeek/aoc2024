from itertools import starmap
from operator import mul
from typing import Sequence
import wafle as wf
import re

pat = re.compile(r"^\D*(\d+)\D*(\d+)$")

content = wf.M(open("in.txt", "r").read().split("\n\n")) | str.splitlines | (lambda k: (
    wf.M(k)
    | pat.match
    | (lambda k: list(map(int, k.groups())))
) >= list) >= list

# Given a vector
# and new basis
# find the new vector
# B x X = N
# Basis Matrix times Vector in new Basis = Vector in old basis
# X = B ^ -1 * N

# Forgot matrices make a Group, so derived left inverse of the multiplication
# Rediscovered the adjoint method of finding inverse :D
def left_inverse_matrix(col1: list[int], col2: list[int]) -> list[list[float]]:
    a, b = col1[0], col2[0]
    c, d = col1[1], col2[1]

    det = a * d - b * c
    x = d / det
    y = -1 * b / det
    z = -1 * c / det
    w = a / det

    return [[x, y],
            [z, w]]

# left times right matrix multiplication while transposing right
def left_matmul(mat: Sequence[Sequence[float]], vec: Sequence[float | int]) -> Sequence[float]:
    return list(map(lambda row: sum(starmap(mul, zip(row, vec))),  mat))

def process(problem: list[list[int]], part2=True):
    inv = left_inverse_matrix(problem[0], problem[1])
    tar = problem[2]
    if part2:
        tar = [problem[2][0] + 10000000000000, problem[2][1] + 10000000000000]
        presses = left_matmul(inv, tar)
        # print(presses, left_matmul([[problem[0][0], problem[1][0]], [problem[0][1], problem[1][1]]], list(map(round, presses))),  tar)
    else:
        presses = left_matmul(inv, tar)
        # print(presses, left_matmul([[problem[0][0], problem[1][0]], [problem[0][1], problem[1][1]]], list(map(round, presses))), tar)

    if left_matmul([[problem[0][0], problem[1][0]], [problem[0][1], problem[1][1]]], list(map(round, presses))) == tar:
        return round(presses[0]) * 3 + round(presses[1])
    else:
        return 0
k = 0
for p in content:
    s = process(p)
    print(s)
    k += s

print(int(k), k.is_integer())
# print(left_inverse_matrix([1, 0], [0, 1]))