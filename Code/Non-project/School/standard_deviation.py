from math import sqrt

regular_oreos = [3.1, 3.2, 3.6, 3.6, 3.33, 4.03, 3.44, 4.26, 3.4, 3.2, 3.3, 3.0, 2.8, 3.0, 3.3, 3.1]
# double_stuff = [6.0, 4.9, 5.9, 4.9, 5.5, 5.5, 5.7, 5.2]
# mega_stuff = [9.93, 9.50, 10.86, 10.48, 8.89, 9.60, 9.49, 9.43]


summed = 0
list_avg =  3.4
n = len(regular_oreos)
# print(sum(mega_stuff)/n)

for i in list(regular_oreos):
    summed += (i - list_avg)**2

standard_deviation = sqrt(summed/(n - 1))
print(standard_deviation)

standard_error = standard_deviation/sqrt(n)
print(standard_error)