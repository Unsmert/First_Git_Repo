# from pprint import pprint
# arr = list(map(int, input().split()))
# arr.append(0)

# new_arrays = [arr[i:] + arr[:i] for i in range(len(arr) - 1, -1, -1)]
# new_arrays.sort()
# res = ""
# for array in new_arrays:
#     res += f"{array[-1]} "
#     print(array[-1], end = " ")
# print()

# ending_nums = list(map(int, res.split()))
# starting_nums = sorted(ending_nums)

size, M = map(int, input().split())
ending_nums = list(map(int, input().split()))
starting_nums = sorted(ending_nums)

def add_occurance(iterable):
    count = {i: 0 for i in range(M + 1)}
    return_mem = []
    for x in iterable:
        count[x] += 1
        return_mem.append((x, count[x]))
    
    return return_mem

ending_nums = add_occurance(ending_nums)
starting_nums = add_occurance(starting_nums)


speed = {starting_nums[i]: i for i in range(size + 1)}
index = 0
ans = []

for i in range(len(ending_nums) - 1):
    new = ending_nums[index]
    ans.append(new[0])
    index = speed[new]

print(" ".join(map(str, ans[::-1])))