arr = list(map(int, input().split()))
arr.append(0)

new_arrays = [arr[i:] + arr[:i] for i in range(len(arr) - 1, -1, -1)]
new_arrays.sort()
res = []
for array in new_arrays:
    res.append(array[-1])

ending_nums = res
starting_nums = sorted(ending_nums)

print(ending_nums)
print(starting_nums)

# Step 3: tag occurrences
def tag(col):
    count = {}
    tagged = []
    for x in col:
        count[x] = count.get(x, 0) + 1
        tagged.append((x, count[x]))
    return tagged

L_tag = tag(ending_nums)
F_tag = tag(starting_nums)

print(L_tag)
print(F_tag)

# Step 4: LF-mapping
lf = {F_tag[i]: i for i in range(len(F_tag))}
print(lf)

# Step 5: reconstruct
idx = L_tag.index((0, 1))   # start from end marker
res = []

for _ in range(len(ending_nums) - 1):
    idx = lf[L_tag[idx]]
    res.append(ending_nums[idx])

print(" ".join(map(str, res[::-1])))