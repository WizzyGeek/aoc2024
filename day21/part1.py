from math import inf, nan
import wafle as wf
from functools import cache

nump = [
    "789",
    "456",
    "123",
    " 0A"
]

numpv = {ch: complex(x, idx) for idx, row in enumerate(nump) for x, ch in enumerate(row)}

def numpad(f: str, t: str):
    s = numpv[f]
    d = numpv[t]
    return d - s

unsafe_nump = numpv[" "]

def hsafe_nump(s: complex, m: complex):
    return (s + m.real) != unsafe_nump

def vsafe_nump(s: complex, m: complex):
    return (s + 1j * m.imag) != unsafe_nump

keyp = [
    " ^A",
    "<v>",
]

keypv = {ch: complex(x, idx) for idx, row in enumerate(keyp) for x, ch in enumerate(row)}

dir2pos = {
    1: keypv[">"],
    -1: keypv["<"],
    -1j: keypv["^"],
    1j: keypv["v"]
}

d2pos = lambda c: dir2pos[c / abs(c)]

unsafe_keyp = keypv[" "]


def hsafe_keyp(s: complex, m: complex):
    return (s + m.real) != unsafe_keyp

def vsafe_keyp(s: complex, m: complex):
    return (s + m.imag) != unsafe_keyp

def keypad(f: str, t: str):
    s = keypv[f]
    d = keypv[t]
    return d - s

def code2vec(code: str):
    i = numpv["A"]
    for c in code:
        d = numpv[c]
        m = d - i
        yield m, hsafe_nump(i, m), vsafe_nump(i, m)
        i = d

# <A^A^^>AvvvA
# eg this is the input to first bot
# For the second bot
# it must navigate to "<" from "A" and itself press A
# then it must maviagte back to "A" and itself press A

# so
# <A, ^A, ^^>A, vvvA
# these can all be parallelised
# all same starting position "A"

# <A becomes
# v<<A>>^A for second robot

# Sometimes
# we have 1+1j , >vA or v>A
# vA<A or (v<A>A or <vA>A) these are the 3 possible solutions
# simlarly one level deeper the answer is given by splitting each solution and finding them parallely
# Divide and conquer

# let our recursive function be f(v, hsafe, vsafe, depth)
# if v is a staright vector ie <<A or ^A and depth is 0, then return vector magnitude plus one
# if depth is zero and v is diagonal with hsafe or vsafe true, ie <vA or v<A return manhattan + 1
# if depth is non-zero and v is straight
#  return f(A to keypad direction to go in, ..., depth - 1) + (magnitude v) - 1
# if depth is non-zero and v is diagonal with both hsafe and vsafe set
# returm minimum of f(the y direction of v on keypad, ..., depth - 1 ) + y distance - 1 + f(x direction button - y button selected, computed hsafe, vsafe, depth - 1) + x distance - 1,
#   f(the x direction of v on keypad, ..., depth - 1 ) + x distance - 1 + f(y direction button - x button selected, computed hsafe, vsafe, depth - 1) + y distance - 1,
# if hsafe is false dont compute the path that goes horizontal first
# if vsafe is false dont compute the path that goes vertical first
# if both are false default return NaN or inf

def safety(fro: complex, to: complex):
    return hsafe_keyp(fro, to - fro), vsafe_keyp(fro, to - fro)

def f(v: complex, safe, depth):
    hsafe, vsafe = safe
    if depth == 0:
        # This is the last remote, must termintate in this branch
        if hsafe or vsafe:
            return abs(v.real) + abs(v.imag) + 1
        else: return nan
    else:
        # print(v, safe, depth)
        if v.real != 0 and v.imag != 0: # <<vA
            # >^A or ^>A
            x = d2pos((v + v.conjugate()) / 2) # horizontal vector
            y = d2pos((v - v.conjugate()) / 2) # vertical vector

            mcost = inf
            if hsafe:
                sf = safety(keypv["A"], x)
                sf2 = safety(x, y)
                mcost = min(mcost, f(x - keypv["A"], sf, depth - 1) + abs(v.real) - 1
                            + f(y - x, sf2, depth - 1) + abs(v.imag) - 1 + f(keypv["A"] - y, safety(y, keypv["A"]), depth - 1))
            if vsafe:
                sf = safety(keypv["A"], y)
                sf2 = safety(y, x)
                mcost = min(mcost, f(y - keypv["A"], sf, depth - 1) + abs(v.imag) - 1
                            + f(x - y, sf2, depth - 1) + abs(v.real) - 1 + f(keypv["A"] - x, safety(x, keypv["A"]), depth - 1))
            # print(v, safe, depth, mcost, x - keypv["A"])
            return mcost
        elif v.real != v.imag: # Straigth vector # >>A
            if (v.real and hsafe) or (v.imag and vsafe):
                n = d2pos(v / abs(v))
                sf = safety(keypv["A"], n)
                # print(v, depth, n - keypv["A"], f(n - keypv["A"], sf, depth - 1), abs(v) - 1,  f(keypv["A"] - n, safety(n, keypv["A"]), depth - 1))
                return f(n - keypv["A"], sf, depth - 1) + abs(v) - 1 + f(keypv["A"] - n, safety(n, keypv["A"]), depth - 1)
            else:
                return nan
        else: # just A
            return 1

def code2complexity(code: str):
    vecs = code2vec(code)
    s = 0
    for vec in vecs:
        t = f(vec[0], (vec[1], vec[2]), 2)
        s += t

    print(s, code)
    return s * int(code[:-1])

ans = wf.M(open("day21/in.txt").read().splitlines()) | code2complexity >= sum
print(ans)

# code2complexity("0")
# print(f(1-2j, (True, True), 1))
# v<<A>>^A
