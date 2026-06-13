N, Q = map(int, input().split())

costs = list(map(int, input().split()))

# Preprocess
for i in range(1, N):
    costs[i] = min(costs[i], costs[i - 1] * 2)

# self explanatory
# Been looking for a reason to use bitmasking
def map_bits_to_cost(x, costs):
    running_total = 0
    bit_index = 0

    low_bits = x % (1 << N - 1)
    high_bits = x >> N - 1

    while low_bits:
        if low_bits & 1:
            running_total += costs[bit_index]
            if running_total > costs[bit_index + 1]:
                running_total = costs[bit_index + 1]
        bit_index += 1
        low_bits >>= 1
    
    return running_total + high_bits * costs[-1]
ans_list = []
for _ in range(Q):
    ans_list.append(str(map_bits_to_cost(int(input()), costs)))

print("\n".join(ans_list))