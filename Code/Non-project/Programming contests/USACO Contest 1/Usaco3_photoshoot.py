from sys import stdin
N, K = stdin.readline().split()
N, K = int(N), int(K)

picture_arr_size = N - K + 1
Cow_beauty = [0 for _ in range(N**2)]
Picture_beauty = [0 for _ in range(picture_arr_size**2)]

ans_list = []
max_beauty = 0

for _ in range(int(input())):
    x, y, b = stdin.readline().split()
    x, y, b = int(x) - 1, int(y) - 1, int(b)

    index = x * N + y
    Cow_beauty[index], beauty_diff = b, b - Cow_beauty[index]

    start_row = max(0, x - K + 1)
    end_row = min(picture_arr_size - 1, x)
    start_col = max(0, y - K + 1)
    end_col = min(picture_arr_size - 1, y)
    potential_beauty = [max_beauty]

    for row in range(start_row, end_row + 1):
        for col in range(start_col, end_col + 1):
            actual_element = row * picture_arr_size + col
            Picture_beauty[actual_element] += beauty_diff
            potential_beauty.append(Picture_beauty[actual_element])
    max_beauty = max(potential_beauty)
    
    ans_list.append(max_beauty)

print("\n".join(map(str, ans_list)))