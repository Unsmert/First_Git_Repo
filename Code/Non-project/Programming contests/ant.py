size = int(input()[0])
height_map = []
for i in range(size):
    height_map.append(list(map(int, input().split())))

bunker_map = []

for i in range(size):
    bunker_map.append(list(map(int, input().split())))

time = 0
while True:
    for i in range(size):
        for j in range(size):
            if bunker_map[i][j] == 0 and height_map[i][j] == time:
                bunker_map[i][j] = -2
            elif bunker_map[i][j] == -2:
                if i > 0 and bunker_map[i - 1][j] != -1:
                    bunker_map[i - 1][j] = -2
                if i < size - 1 and bunker_map[i + 1][j] != -1:
                    bunker_map[i + 1][j] = -2
                if j > 0 and bunker_map[i][j - 1] != -1:
                    bunker_map[i][j - 1] = -2
                if j < size - 1 and bunker_map[i][j + 1] != -1:
                    bunker_map[i][j + 1] = -2
    for i in range(size):
        for j in range(size):
            if bunker_map[i][j] == 1:
                time += 1
                continue
    
    break
print(time)