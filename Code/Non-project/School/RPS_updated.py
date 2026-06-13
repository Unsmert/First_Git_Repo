import os
from pprint import pprint
from copy import deepcopy

def clear():
    """Utility function that clears the terminal GUI's screen - takes no arguments"""
    try:
        os.system('cls')
    except:
        #If nothing else works, a hacky, non optimal solution
        for i in range(50): print("")

class game_piece():
    def __init__(self, player, orientation):
        self.player = player
        self.orientation = orientation # [top, back, right]
        
    def vertical_move(self):
        self.orientation[0], self.orientation[1] = self.orientation[1], self.orientation[0]
    
    def horizontal_move(self):
        self.orientation[0], self.orientation[2] = self.orientation[2], self.orientation[0]

scissors = 3
rock = 4
paper = 5

def main():
    Player1_turn = True
    Game_over = False
    p1_end_case_counter = 0
    p2_end_case_counter = 0

    while not Game_over:
        if Player1_turn:
            Game_over, p1_end_case_counter, p2_end_case_counter = Turn('1', Game_over, p1_end_case_counter, p2_end_case_counter)
            Player1_turn = False
        else:
            Game_over, p1_end_case_counter, p2_end_case_counter = Turn('2', Game_over, p1_end_case_counter, p2_end_case_counter)
            Player1_turn = True

def initBoard():
    board_size = 8
    board = [["*" for j in range(board_size)] for i in range(board_size)]
    for index in range(board_size):
        if index%2 == 0:
            board[-1][index] = game_piece("1", [3 + (-index) % 3, 3 + ((-index)+1) % 3, 3 + ((-index)+2) % 3])
    for index in range(board_size):
        if index%2 == 1:
            board[0][index] = game_piece("2", [3 + (index - 1) % 3, 3 + (index) % 3, 3 + (index + 1) % 3])
    return board

def print_board(board):
    for row in board:
        for square in row:
            if square != "*":
                print(f"p{square.player}, {square.orientation}", end=" | ")
            else:
                print(square, end=" | ")
        print()

def adjacency_checker(y, x):
    global game_board
    piece_1 = game_board[y][x]
    squares = [[(0, -1), "*"], [(0, 1), "*"], [(-1, 0), "*"], [(1, 0), "*"]]
    if x > 0:
        squares[0][1] = game_board[y][x - 1]
    if x < 7:
        squares[1][1] = game_board[y][x + 1]
    if y > 0:
        squares[2][1] = game_board[y - 1][x]
    if y < 7:
        squares[3][1] = game_board[y + 1][x]
    
    piece_2 = [square for square in squares if square[1] != "*"]
    amount_of_pieces = len(piece_2)
    
    if amount_of_pieces > 1:
        game_board[y][x] = "*"
        return
    if amount_of_pieces == 0:
        return
    
    piece_2 = piece_2[0]
    
    game_board[y][x], game_board[y + piece_2[0][0]][x + piece_2[0][1]] = comparison(piece1= piece_1, piece2= piece_2[1])
    
def comparison(piece1, piece2):
    piece1_orientation = piece1.orientation[0]
    piece2_orientation = piece2.orientation[0]

    if piece1_orientation == piece2_orientation:
        return (piece1, piece2)
    if (piece1_orientation == scissors) and (piece2_orientation == paper):
        return (piece1, "*")
    if (piece1_orientation == rock) and (piece2_orientation == scissors):
        return (piece1, "*")
    if (piece1_orientation == paper) and (piece2_orientation == rock):
        return (piece1, "*")
    else:
        return ("*", piece2)   

def Check_game_over(player_1_counter, player_2_counter, whos_turn):
    piece_counter_1 = 0
    piece_counter_2 = 0
    global board
    for row in board:
        for square in row:
            piece_counter_1, piece_counter_2 = (piece_counter_1 + (not(square == "*") and square.player == "1"), piece_counter_2 + (not(square == "*") and square.player == "2"))
            continue
    if piece_counter_1 == 0:
        print("player 2 wins")
        return True, 0, 0
    if piece_counter_2 == 0:
        print("player 1 wins")
        return True, 0, 0
    if piece_counter_1 == 1 and piece_counter_2 == 1:
        if whos_turn == "1" and not all(square == "*" for square in board[0]):
            player_1_counter += 1
            if player_1_counter == 2:
                print("player 2 wins")
                return True, 0, 0
        if whos_turn == "2" and not all(square == "*" for square in board[-1]):
            player_2_counter += 1
            if player_2_counter == 2:
                print("player 2 wins")
                return True, 0, 0
    return False, player_1_counter, piece_counter_2

def Turn(whos_turn, game_over, p1_turn_counter, p2_turn_counter):
    global game_board
    clear()
    print_board(game_board)
    
    while True:
        try:
            move = input(f"Player {whos_turn}, which piece do you want to move? \n").split(", ")
            x, y = int(move[0]) - 1, 8 - int(move[1])
            assert not (0 >= x >= 7 and 0 >= y >= 7)
            if game_board[y][x].player == whos_turn:
                chosen_piece = game_board[y][x]
                break
            else:
                print("Has to be a valid square")
        except:
            print("Input should be in the form: {x}, {y}")
    
    invalid_direction = ""

    for i in range(chosen_piece.orientation[0]):
        while True:
            direction = input("Up, down, left, or right? (u/d/l/r) \n")

            if direction == invalid_direction:
                print("You picked an invalid direction")
                print("The piece will be removed")
                board[y][x] = '*'
                return

            elif direction == "u" and y > 0:
                game_board[y][x].vertical_move()
                game_board[y-1][x], game_board[y][x] = game_board[y][x], game_board[y-1][x]
                y -= 1
                invalid_direction = "d"
                break
            
            elif direction == "d" and y < 7:
                game_board[y][x].vertical_move()
                game_board[y+1][x], game_board[y][x] = game_board[y][x], game_board[y+1][x]
                y += 1
                invalid_direction = "u"
                break
            
            elif direction == "r" and x < 7:
                game_board[y][x].horizontal_move()
                game_board[y][x+1], game_board[y][x] = game_board[y][x], game_board[y][x+1]
                x += 1
                invalid_direction = "l"
                break
            
            elif direction == "l" and x > 0:
                game_board[y][x].horizontal_move()
                game_board[y][x-1], game_board[y][x] = game_board[y][x], game_board[y][x-1]
                x -= 1
                invalid_direction = "r"
                break
            
            else:
                print("The chosen direction is invalid. Choose another direction.")
    adjacency_checker(y= y, x= x)
    return Check_game_over(game_over, p1_turn_counter, p2_turn_counter)

def apply_die_rotation(current_orientation, delta_row, delta_col):
    """Swap top face with the correct adjacent face based on roll direction."""
    orient = list(current_orientation)
    directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]  # right, up, left, down
    direction_index = directions.index((delta_row, delta_col))
    swap_index = ((direction_index + 1) % 2) + 1  # 2 for back, 3 for right
    orient[0], orient[swap_index] = orient[swap_index], orient[0]
    return orient

def explore_all_paths(board, current_row, current_col, steps_remaining, previous_direction, current_orientation, valid_end_states, turn):
    """
    Recursively explore all valid 4-step paths.
    - board: 8x8 grid
    - current_row, current_col: current position
    - steps_remaining: how many rolls left (3, 4, or 5)
    - previous_direction: (dr, dc) of last move, or None at start
    - current_orientation: [top, back, right]
    - valid_end_states: set of (final_row, final_col, (top, back, right))
    """
    if steps_remaining == 0:
        dcopy_board = deepcopy(board)
        dcopy_board[current_row][current_col] = game_piece(turn, current_orientation)
        valid_end_states.add(tuple(tuple(row) for row in dcopy_board))
        return

    for delta_row, delta_col in [(0, 1), (-1, 0), (0, -1), (1, 0)]:  # right, up, left, down
        # Prevent immediate backtracking
        if previous_direction is not None and (delta_row, delta_col) == (-previous_direction[0], -previous_direction[1]):
            continue
        next_row = current_row + delta_row
        next_col = current_col + delta_col
        # Check bounds and empty space
        if not (0 <= next_row <= 7 and 0 <= next_col <= 7):
            continue
        if board[next_row][next_col] != "*":
            continue

        # Apply rotation and recurse
        new_orientation = apply_die_rotation(current_orientation, delta_row, delta_col)
        explore_all_paths(board, next_row, next_col, steps_remaining - 1, (delta_row, delta_col), new_orientation, valid_end_states, turn)

def possible_moves_for_piece(board, piece, start_row, start_col, turn):
    """Main function: find all valid end positions and orientations after N rolls."""
    valid_end_states = set()
    original_cell = board[start_row][start_col]
    board[start_row][start_col] = "*"  # Temporarily free the starting square
    steps_to_take = piece.orientation[0]  # top face = number of rolls
    explore_all_paths(board=board, current_row=start_row, current_col=start_col, steps_remaining=steps_to_take, previous_direction=None, current_orientation=piece.orientation, valid_end_states=valid_end_states, turn= turn)

    board[start_row][start_col] = original_cell  # Restore
    return valid_end_states

def explore_all_moves(board):
    for y in range(8):
        for x in range(8):
            if board[y][x] != "*":
                pass
game_board = initBoard()

print("\n")
for board in possible_moves_for_piece(game_board, game_board[7][0], 7, 0, "1"):
    print_board(board)
    print()
# print("\n")
# pprint(possible_moves_for_piece(game_board, game_board[7][2], 7, 2, "1"))
print("\n")
pprint(len(possible_moves_for_piece(game_board, game_board[7][4], 7, 4, "1")))