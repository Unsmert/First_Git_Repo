import sys

def solve() -> None:
    it = iter(sys.stdin.read().strip().split())
    n = int(next(it))
    a = [int(next(it)) for _ in range(n)]
    max_a = max(a)

    # frequency of each pile size
    freq = [0] * (max_a + 2)
    for x in a:
        freq[x] += 1

    # prefix sums of frequencies
    pref = [0] * (max_a + 2)
    for i in range(1, max_a + 1):
        pref[i] = pref[i-1] + freq[i]

    ans = 0

    # try every possible first move size s
    for s in range(1, max_a + 1):
        qmax = max_a // s
        odd_q = []      # list of quotients with odd count (q >= 1)
        odd_cnt = []    # corresponding counts
        for q in range(1, qmax + 1):
            L = q * s
            R = (q + 1) * s - 1
            if R > max_a:
                R = max_a
            cnt = pref[R] - pref[L-1]   # number of piles with floor(a_i/s) = q
            if cnt & 1:
                odd_q.append(q)
                odd_cnt.append(cnt)
                if len(odd_q) > 2:
                    break
        if len(odd_q) > 2:
            continue
        if len(odd_q) == 1 and odd_q[0] == 1:
            ans += odd_cnt[0]
        elif len(odd_q) == 2 and odd_q[1] == odd_q[0] + 1:
            ans += odd_cnt[1]   # the larger quotient

    print(ans)


if __name__ == "__main__":
    solve()