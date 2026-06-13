def riffle_shuffle(list_of_nums):
    half_length = len(list_of_nums)//2
    ans = []
    for i in range(half_length):
        ans.append(list_of_nums[i + half_length])
        ans.append(list_of_nums[i])
    return ans

n, k = map(int, input().split())
odd = False
if n % 2 == 1:
    odd = True
    n -= 1

ans = [i + 1 for i in range(n)]
initial_ans = ans.copy()

cycle_length = 0
flag = False

for i in range(k):
    ans = riffle_shuffle(ans)
    if ans == initial_ans:
        cycle_length = i + 1
        flag = True
        break

if flag:
    for i in range(k % cycle_length):
        ans = riffle_shuffle(ans)

if odd:
    ans.append(n + 1)

print(" ".join(list(map(str, ans))))