time = list(map(int, input().split(':')))

def CheckUnique(timing):
    return len(set("".join([str(timing[i]) if timing[i] > 9 else "0" + str(timing[i]) for i in range(3)])))

def iterate_timing(timing):
    if timing[2] == 59:
        timing[2] = 0
        if timing[1] == 59:
            timing[1] = 0
            if timing[0] == 23:
                timing[0] = 0
            else:
                timing[0] += 1
        else:
            timing[1] += 1
    else:
        timing[2] += 1
                
def print_time(timing):
    print(":".join([str(timing[i]) if timing[i] > 9 else "0" + str(timing[i]) for i in range(3)]))

while CheckUnique(time) > 3:
    iterate_timing(time)
print_time(time)