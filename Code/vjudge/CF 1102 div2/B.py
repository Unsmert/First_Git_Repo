ans = []

small_palindromes = []
for i in range(100001):
    if str(i) == str(i)[::-1]:
        small_palindromes.append(i)

for _ in range(int(input())):
    N = input()
    # Always guaranteed to find an answer
    if len(N) >= 6:
        m3 = 0
        for char in N:
            m3 += int(char)
        m3 %= 3

        num = int(N[-2:])
        rem = num % 4
        rem = rem if rem != 0 else 4

        mid = ((m3 + rem) % 3)
        a = rem * 10001 + mid * 100

        # print(rem, mid, last6, a, (int(N) - a) % 12)

        b = int(N) - a
        ans.append(f"{a} {b}")
    else:
        N = int(N)
        flag = True
        for palin in small_palindromes:
            if palin <= N and (N - palin) % 12 == 0:
                ans.append(f"{palin} {N - palin}")
                flag = False
                break
        
        if flag:
            ans.append('-1')

print("\n".join(ans))