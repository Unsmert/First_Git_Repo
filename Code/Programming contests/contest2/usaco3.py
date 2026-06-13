import sys
# 1. Faster input handling
N = int(input())
A = list(map(int, input().split()))

distinct_elements = set(A)
K = len(distinct_elements)

if K == 1:
    print(' '.join(['0'] * N))
    sys.exit(0)

# Use 3N to handle cyclic wrap-around without modulo headaches
AA = A + A + A
ans = [float('inf')] * (3 * N)

# 2. Sliding Window to find all minimal intervals
l = 0
count = {}
have = 0

# We only need to find windows that could impact the middle N elements
for r in range(3 * N):
    val = AA[r]
    count[val] = count.get(val, 0) + 1
    if count[val] == 1:
        have += 1
    
    while have == K:
        # Current minimal window covering all elements is [l, r]
        length = r - l
        # The cost at the endpoints is just the length
        if length < ans[l]: ans[l] = length
        if length < ans[r]: ans[r] = length
        
        # Shrink from left
        left_val = AA[l]
        count[left_val] -= 1
        if count[left_val] == 0:
            have -= 1
        l += 1

# 3. Linear Propagation (The "Breadth-First" approach to costs)
# Forward pass: cost increases as we move away from a left endpoint
for i in range(1, 3 * N):
    if ans[i-1] + 1 < ans[i]:
        ans[i] = ans[i-1] + 1
        
# Backward pass: cost increases as we move away from a right endpoint
for i in range(3 * N - 2, -1, -1):
    if ans[i+1] + 1 < ans[i]:
        ans[i] = ans[i+1] + 1

# Output the middle N results
print(*(ans[N : 2 * N]))