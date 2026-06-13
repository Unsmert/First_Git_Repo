from sys import stdin
S = stdin.readline().strip()

cnt = {"C": 0, "O": 0, "W": 0}
res = []

str1 = ""
str2 = ""

for c in S:
    cnt[c] += 1
    if cnt[c] % 2 == 1:
        res.append("1")
        str1 += c
    else:
        res.append("2")
        str2 += c

print(res)
print(str1)
print(str2)