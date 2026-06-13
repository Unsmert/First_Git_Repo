N, Q = map(int, input().split())
given_arr = list(map(int, input().split()))

indicies = [0] * (N + 1)

for i in range(N):
    indicies[given_arr[i]] = i + 1

ans = []

for _ in range(Q):
    L, R = map(int, input().strip("()").split(", "))
    l_idx, r_idx = indicies[L], indicies[R]
    l_idx, r_idx = min(l_idx, r_idx), max(l_idx, r_idx)

    ans.append("NO" if any([l_idx <= indicies[i] <= r_idx for i in (L - 1, L + 1, R - 1, R + 1) if i <= N]) else "YES")

print("\n".join(ans))