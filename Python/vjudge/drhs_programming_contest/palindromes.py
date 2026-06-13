C_str = input()
size = len(C_str)

ans = 0

for i in range(1, size):
    ans = (ans + (9 * (10 ** ((i - 1) // 2)))) % (1000000007)

# print("ans", ans)

def recursion(string, insize, first, bigger):
    # print(string)
    global ans
    if insize == 0:
        ans += (not bigger)
        ans %= 1000000007
        return
    if insize == 1:
        ans += int(string) + (not (first or bigger))
        ans %= 1000000007
        return

    digit1 = int(string[0])
    if digit1 != 0:
        ans = (ans + ((digit1 - (first)) * (10 ** ((insize - 1) // 2)))) % (1000000007)
    
    # print("string", string)
    # print("ans", ans)
    # print("bigger", bigger)
    
    recursion(string[1:-1], insize - 2, False, (int(string[-1]) < digit1) or ((int(string[-1]) == digit1) and bigger))

recursion(C_str, size, True, False)
print(ans)

# brute_force = 0
# for i in range(1, int(C_str) + 1):
#     if str(i) == str(i)[::-1]:
#         brute_force += 1
#         # print(str(i))
# print(brute_force)