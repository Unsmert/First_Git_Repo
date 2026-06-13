T, k = map(int, input().split())
ans_list = []
if k == 1:
    for _ in range(T):
        N = int(input())
        output = input()
        preprocessed = "".join(["M" if char == "O" else "O" for char in output])

        # print(output, preprocessed)

        flip = False
        ans = ""
        for char in range(N - 1, -1, -1):
            if flip:
                element = preprocessed[char]
                if element == "O":
                    flip = not flip
            else:
                element = output[char]
                if element == "O":
                    flip = not flip
            ans = element + ans
        ans_list.append("YES")
        ans_list.append(str(ans))
else:
    for _ in range(T):
        input()
        input()
        ans_list.append("YES")

print("\n".join(ans_list))