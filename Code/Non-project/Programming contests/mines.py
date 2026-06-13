def factorial(num):
    if num == 0:
        return 1
    result = 1
    for i in range(1, num + 1):
        result *= i
    return result

def comb(n, k):
    if k > n or n < 0 or k < 0:
        return 0
    numerator = factorial(n)
    denominator = factorial(k) * factorial(n - k)
    return numerator // denominator
xi, yi, xf, yf, mx1, my1, mx2, my2 = map(int, input().split())

s1 = xf - xi
s2 = yf - yi
mx1 = mx1 - xi
my1 = my1 - yi
mx2 = mx2 - xi
my2 = my2 - yi

def some_func_idek_lmaooo(x, y):
    return comb(x + y, (x + y)//2 - (abs(x - y))//1)

total_cases = some_func_idek_lmaooo(s1, s2)
print(total_cases)
mine1_cases = some_func_idek_lmaooo(mx1, my1) * some_func_idek_lmaooo(s1 - mx1, s2 - my1)
print(mine1_cases)
mine2_cases = some_func_idek_lmaooo(mx2, my2) * some_func_idek_lmaooo(s1 - mx2, s2 - my2)
print(mine2_cases)
extra_cases = 0
if mx1 <= mx2 and my1 <= my2:
    extra_cases = some_func_idek_lmaooo(mx1, my1) * some_func_idek_lmaooo(mx2 - mx1, my2 - my1) * some_func_idek_lmaooo(s1 - mx2, s2 - my2)
elif mx2 <= mx1 and my2 <= my1:
    extra_cases = some_func_idek_lmaooo(mx2, my2) * some_func_idek_lmaooo(mx1 - mx2, my1 - my2) * some_func_idek_lmaooo(s1 - mx1, s2 - my1)
print(extra_cases)

print(total_cases - mine1_cases - mine2_cases + extra_cases)