N, Q = map(int, input().split())
arr = list(map(int, input().split()))

idx = [0] * (N + 2)
prefix_li = [0] * (N + 2)
prefix_ld = [0] * (N + 2)
prefix_ri = [0] * (N + 2)
prefix_rd = [0] * (N + 2)

for i in range(N):
    idx[arr[i]] = i
    prefix_li[arr[i]] = prefix_li[arr[i] - 1] + 1
    prefix_ld[arr[i]] = prefix_ld[arr[i] + 1] + 1

    prefix_ri[arr[N - i - 1]] = prefix_ri[arr[N - i - 1] - 1] + 1
    prefix_rd[arr[N - i - 1]] = prefix_rd[arr[N - i - 1] + 1] + 1

def solve():
    global prefix_ld, prefix_li, prefix_rd, prefix_ri
    query = list(map(int, input().strip("()").split(", ")))
    if (query[0] == query[1]):
        return "YES"

    L, R = query[idx[query[0]] > idx[query[1]]], query[idx[query[0]] <= idx[query[1]]]

    if all(idx[v] < idx[v + 1] for v in range(min(L, R), max(L, R))) or all(idx[v] > idx[v + 1] for v in range(min(L, R), max(L, R))):
        return "NO"

    if (N - prefix_rd[L + 1] * (idx[L + 1] > idx[L]) - prefix_ri[L - 1] * (idx[L - 1] > idx[L])) <= idx[R]:
        return "NO"

    if (prefix_li[R - 1] * (idx[R - 1] < idx[R]) + prefix_ld[R + 1] * (idx[R + 1] < idx[R])) > idx[L]:
        return "NO"

    return "YES"

ans = []

for _ in range(Q):
    ans.append(solve())

print("\n".join(ans))