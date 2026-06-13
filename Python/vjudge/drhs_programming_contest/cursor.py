string = []
size = 1
cursor = 0

for _ in range(int(input())):
    command = input()
    if command == "LEFT":
        cursor = (cursor - 1) % size
    elif command == "RIGHT":
        cursor = (cursor + 1) % size
    elif command == "BACKSPACE":
        if cursor != 0:
            string.pop(cursor - 1)
            size -= 1
            cursor -= 1
    elif command == "DELETE":
        if cursor != size - 1:
            size -= 1
            string.pop(cursor)
    else:
        string.insert(cursor, command.split()[-1])
        size += 1
        cursor += 1
    # print(string)
    # print(size)
    # print(cursor)

print("".join(string))