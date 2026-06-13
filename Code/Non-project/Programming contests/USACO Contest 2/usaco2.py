from math import comb

N, x = map(int, input().split())

def count(M_count, O_count):
    # min_count = min(O_count, M_count)
    # return (string, 0 if O_count < 2 else M_count * comb(O_count, 2), min_count, comb(20, min_count))
    return (0 if O_count < 2 else M_count * comb(O_count, 2), comb(N, min(O_count, M_count)))

# maximum = max([count("M" * (20 - i) + "O" * i) for i in range(21)], key = lambda x: x[1])

precompute = [count(20 - i, i) for i in range(N + 1)]

# for element in precompute:
#     print(element)

ans = 0
maximum = float('-inf')
for element in precompute:
    ans += element[1] * (element[0] >= x)
    if element[0] > maximum:
        maximum = element[0]

if ans != 0:
    print(x, ans)
else:
    ans += sum([element[1] for element in precompute if element[0] == maximum])
    print(maximum, ans)
# print(sum(map(lambda x: x[-1], precompute)))
# print(2**20)

# print(maximum)