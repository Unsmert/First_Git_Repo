distance, m = map(int, input().split())

mirrors = [int(i) for i in input().split(' ')]
dur = [int(i) for i in input().split(' ')]

total = distance
for i in range(m):
    total += 2 * mirrors[i] * dur[i]
total %= 1000000007
print(total)