s = "5525"
a = 8
b = 2

s = list(map(int, s))
digits = s * 2
str_length = len(s)

def gcd(a : int, b : int) -> int:
    while b != 0:
        a, b = b, a % b
    return a

def get_best_a_shift(int_list, num_shift):
    first_num = int_list[0]
    gcd_num_shift = gcd(10, num_shift)
    
    if gcd_num_shift == 1:
        return [(int_list[i] - first_num) + (10 * (int_list[i] - first_num < 0)) for i in range(len(int_list))]
    min_first_num = min([(first_num + num_shift * i) % 10 for i in range(10//gcd_num_shift)])
    result_shift = first_num - min_first_num
    return [(int_list[i] - result_shift) + (10 * (int_list[i] - result_shift < 0)) for i in range(len(int_list))]

def combine_lists(even_list, odd_list):
    res = [0] * (2 * len(even_list))
    res[::2] = even_list
    res[1::2] = odd_list
    return res

def compare_lists(list_1, list_2):
    for i in range(len(list_1)):
        element_1 = list_1[i]
        element_2 = list_2[i]
        if element_1 < element_2:
            return list_1
        elif element_2 < element_1:
            return list_2
    return list_1

str_length = len(s)

best_case = [10] * str_length
for i in range(str_length//gcd(str_length, b)):
    new_s = digits[b * i:str_length + b*i]
    new_odd_indicies = get_best_a_shift(new_s[1::2], a)
    new_even_indicies = new_s[0::2]
    if b % 2 == 1: new_even_indicies = get_best_a_shift(new_even_indicies, a)
    new_case = combine_lists(new_even_indicies, new_odd_indicies)
    best_case = compare_lists(best_case, new_case)

print("".join(list(map(str, best_case))))