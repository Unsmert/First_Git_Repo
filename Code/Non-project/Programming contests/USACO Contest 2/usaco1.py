output = input()
preprocessed = "".join(["M" if char == "O" else "O" for char in output])

# print(output, preprocessed)

flip = False
ans = ""
for char in range(len(output) - 1, -1, -1):
    if flip:
        element = preprocessed[char]
        if element == "O":
            flip = not flip
    else:
        element = output[char]
        if element == "O":
            flip = not flip
    ans+=element

print(ans[::-1])