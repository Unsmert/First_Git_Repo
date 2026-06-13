num_dict = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'A': 10,
    'B': 11,
    'C': 12,
    'D': 13,
    'E': 14,
    'F': 15
}

num_list = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F")

def convert_hex_to_b10(base_16: str) -> int:
    return int(base_16, 16)
    # ans = 0
    # base_16 = base_16[::-1]
    # for i in range(len(base_16)):
    #     ans += num_dict[base_16[i]] * (16 ** i)
    # return ans

def hex(num: int) -> str:
    return f"{num:02X}"
    # base_16_num = ["0", "0"]
    # num_copy = num
    
    # i = 0
    # while num_copy > 0:
    #     base_16_num[i] = num_list[num_copy % 16]
    #     num_copy = num_copy // 16
    #     i += 1
    
    # return "".join(base_16_num[::-1])
        
def find_locations(string_guess: str) -> list[tuple[int, int]]:
    guess_1, distance_1 = string_guess.split(" ")
    possible_locations = []
    row, column = map(convert_hex_to_b10, (guess_1[:2], guess_1[2:]))
    d1, d2 = map(convert_hex_to_b10, (distance_1[:2], distance_1[2:]))
    
    possible_adjustments = ((1, 1), (1, -1), (-1, 1), (-1, -1))
    possible_distances = ((d1, d2), (d2, d1))
    
    for i, j in possible_adjustments:
        for x, y in possible_distances:
            if 0 <= row + (x * i) <= 255 and 0 <= column + (y * j) <= 255:
                possible_locations.append((row + (x * i), column + (y * j)))
    
    return possible_locations

def findCreature(input1: str, input2: str, input3: str) -> str:
    list_of_possible_locations = find_locations(input1)
    for i in (input2, input3):
        more_possible_locations = find_locations(i)
        list_of_possible_locations = [j for j in more_possible_locations if j in list_of_possible_locations]
    
    tuple_of_row_col = list_of_possible_locations[0]
    row, col = map(hex, tuple_of_row_col)
    
    return f"({row},{col})"

print(findCreature("1A2B 0003", "1A2E 0002", "1A2C 0004"))  # (1A,2E)