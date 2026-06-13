N, K = map(int, input().split())
cin = [char for char in input()]

print(len(cin))

ans_list = []

for _ in range(K):
    if N == 1:
        break

    pairs = {}

    for i in range(N - 1):
        pair = (cin[i], cin[i + 1])
        pairs[pair] = pairs.get(pair, 0) + 1
    
    a = ""
    maximum = -1
    for pair in pairs:
        if pairs[pair] > maximum:
            a = pair
            maximum = pairs[pair]

        elif pairs[pair] == maximum:
            a = min(pair, a)
    
    ans_list.append(str(a[0]) + " " + str(a[1]))

    i = 1
    while i < N:
        qpair = (cin[i - 1], cin[i])
        if qpair == a:
            cin[i - 1] = a[0] + a[1]
            cin.pop(i)
            N -= 1
        
        i += 1

print("\n".join(ans_list))