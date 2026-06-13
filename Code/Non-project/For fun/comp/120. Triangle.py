num = [[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]
nums_list = num[0]
for i in range(1, len(num)):
    answer_list = []
    new_list = num[i]
    answer_list.append(new_list[0] + nums_list[0])
    for index in range(len(nums_list) - 1):
        answer_list.append(min(nums_list[index], nums_list[index + 1]) + new_list[index + 1])
    answer_list.append(nums_list[-1] + new_list[-1])
    nums_list = answer_list
print(min(nums_list))