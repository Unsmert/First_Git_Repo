# Name: Ruohan Xu
# Block: 2
# Date: 9/29/2025

board = [["-" for j in range(3)] for i in range(3)]

def print_board(TTT_board):
    for row in TTT_board:
        print(" | ".join(row))


def check_rows(TTT_board):
    for row in TTT_board:
        if (len(set(row)) == 1) and (row[0] != "-"):
            return f"{row[0]} is the winner"
    return False
        
def check_columns(TTT_board):
    for i in range(3):
        column = [row[i] for row in TTT_board]
        if (len(set(column)) == 1) and (column[0] != "-"):
            return f"{column[0]} is the winner"
    return False

def check_diagonals(TTT_board):
    diagonal1 = [TTT_board[i][i] for i in range(3)]
    if (len(set(diagonal1)) == 1) and (diagonal1[0] != "-"):
        return f"{diagonal1[0]} is the winner"
    
    diagonal2 = [TTT_board[-(i + 1)][i] for i in range(3)]
    if (len(set(diagonal2)) == 1) and (diagonal2[0] != "-"):
        return f"{diagonal2[0]} is the winner"
    return False



def board_state_checker(TTT_board, turn):
    state = check_rows(TTT_board) or check_columns(TTT_board) or check_diagonals(TTT_board)

    if state:
        print(state)
        return True
    
    if turn == 9:
        print("The result is a draw")
        return True
    
    return False


current_player = "x"
game_turn = 0
game_over = False

print_board(board)

while not game_over:

    choice = int(input(f"Current player is {current_player}, Choose a spot: ")) - 1

    row = choice // 3
    column = choice % 3

    if board[row][column] != "-":
        print("Invalid input, redo your choice")
    else:
        board[row][column] = current_player
        if current_player == "o":
            current_player = "x"
        else:
            current_player = "o"
        
        game_turn += 1
        print_board(board)
        game_over = board_state_checker(board, game_turn)