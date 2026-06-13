# 1 <= N <= 10**5 | 1 <= Q <= 10**4
N, Q = map(int, input().split())

# 1 <= cost <= 10**9 | cost_i < cost_i+1
costs = list(map(int, input().split()))

# preprocess
for i in range(1, N):
    costs[i] = min(costs[i], 2 * costs[i - 1])

# name is self-explanitory
# bit manipulation is cool
def map_bits_to_costs(x, costs):
    result = 0
    bit_index = 0

    while x:
        if x & 1:
            if bit_index >= N:
                result += costs[-1] * (2 ** (bit_index - N + 1))
            else:
                result += costs[bit_index]
        x >>= 1
        bit_index += 1

    return result

ans_list = []
for _ in range(Q):
    ans_list.append(str(map_bits_to_costs(int(input()), costs)))

print('\n'.join(ans_list))