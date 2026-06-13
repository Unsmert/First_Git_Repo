from math import comb
n = int(input())
print(comb(n, n//2) % ((int)(1e9 + 7)))