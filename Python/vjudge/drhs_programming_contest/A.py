line1 = [char for char in input()]
line2 = [char for char in input()]
line3 = [char for char in input()]

defdict = {
    'X': 1,
    'O': -1,
    '#': 0
}

Board = [
    [defdict[char] for char in line1],
    [defdict[char] for char in line2],
    [defdict[char] for char in line3],
]

X_row = any([sum(row) == 2 for row in Board])
X_col = any([Board[0][i] + Board[1][i] + Board[2][i] == 2 for i in range(3)])
X_diag_1 = sum([Board[i][i] for i in range(3)]) == 2
X_diag_2 = sum([Board[2 - i][i] for i in range(3)]) == 2

X_wins = any([X_row, X_col, X_diag_1, X_diag_2])

O_row = any([sum(row) == -2 for row in Board])
O_col = any([Board[0][i] + Board[1][i] + Board[2][i] == -2 for i in range(3)])
O_diag_1 = sum([Board[i][i] for i in range(3)]) == -2
O_diag_2 = sum([Board[2 - i][i] for i in range(3)]) == -2

O_wins = any([O_row, O_col, O_diag_1, O_diag_2])

if X_wins and O_wins:
    print("BOTH")
elif X_wins:
    print("XWINS")
elif O_wins:
    print("OWINS")
else:
    print("IDK")