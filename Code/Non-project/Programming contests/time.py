# sample input:
# 5
# 14:30 +5.00 1 0
# 23:00 -3.50 0 1
# 17:31 +6.00 1 1
# 03:13 +0.00 0 0
# 12:45 -9.00 1 1

# sample output:
# 18:30
# 20:30
# 23:31
# 03:13
# 03:45

def convert_float_to_date_time(time_diff):
    hours = int(time_diff)
    minutes = int(60 * (time_diff % 1))
    return hours, minutes

for _ in range(int(input())):
    start_time, time_diff, my_DSI, their_DSI = input().split()
    sign = time_diff[0]
    time_diff = time_diff[1:]
    time_diff = float(time_diff)
    hours_diff, minutes_diff = convert_float_to_date_time(time_diff)
    my_hours, my_minutes = map(int, start_time.split(":"))
    if sign == "+":
        my_hours += hours_diff
        my_minutes += minutes_diff
    else:
        my_hours -= hours_diff
        my_minutes -= minutes_diff
    
    if my_minutes >= 60:
        my_hours += 1
        my_minutes %= 60
    elif my_minutes < 0:
        my_hours -= 1
        my_minutes %= 60
    
    my_hours += int(their_DSI) - int(my_DSI)
    my_hours %= 24
    print(f"{my_hours:02}:{my_minutes:02}")