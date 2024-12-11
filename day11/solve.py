# Firstly, the input array is irrelavant it can be processed in parallel
# This process forms a Directed Graph
# 0 -> 1
# even number of digits -> left part and right part (leading zeroes gone)
# num -> 2024 * num
# The problematic part is splitting of the numbers
# we could have 2^25 (33554432) different numbers worst case
# To process that we would get 4 ns if we want to solve in one second
# say it takes 400ns to process one number, it would take 1 minute 40 seconds
# 1.75^25 say average case, would offer a 28x speedup, 3.57 seconds
# we have 9 numbers, it would take half a minute to process the input

# by some logarithmic estimation 49% of numbers that are multiplied by 2024 will split next iteration,
# but if they dont split next interation have a very high (around 98ish i think) to split the very next,
# so 2024 can be said to have a sqrt(2) branching factor half the time and cbrt(2) the other half,
# we can safely assume 1.3x thanks to zero only reducing it which cancels the unlikely case of case of twice splitting with cbrt(4)
# 0 has a sqrt(2) branching factor
# even split has a 2x branching factor
# we would be looking at 200k numbers in an average case
# The worse random numbers would see 2.5M-33.5M with a bf over 1.8

# Experiment 1, Recurison takes 4000 ns, not 400ns
# But, many numbers occur more than once
# we can bank on this being true to process numbers at even 4ns

import time
import wafle as wf
from collections import defaultdict

freq = defaultdict(lambda: 0)


def blink(n, table, wtable):
    if n == 0:
        wtable[1] += table[0]
        return
    s = str(n)
    k = len(s)
    if k % 2 == 0:
        w = 10 ** (k // 2)
        wtable[n // w] += table[n]
        wtable[n % w] += table[n]
        return
    wtable[n * 2024] += table[n]
    return

p = wf.M(open("in.txt", "r").read().strip().split(" ")) | int >= list

for i in p:
    freq[i] += 1

wtab = defaultdict(lambda: 0)
s = sum(freq.values())

for i in range(75):
    for k in freq:
        blink(k, freq, wtab)
    freq, wtab = wtab, freq
    os = s
    s = sum(freq.values())
    print(str(i+1).ljust(2, " "), "| unique nums: ", str(len(freq)).ljust(10, " "), " | Branching factor: ", f"{s / os:.13f}", " | stones: ", s)
    wtab.clear()
    # input()

print(sum(freq.values()))
# print((time.perf_counter_ns() - now) / len(p))