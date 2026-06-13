## NAMES: Ruohan Xu, Mohamed M, Lishanth
## Period: 2
## Date Last Edited: 10/3

## Check for +6: Randomization
from random import randint

# Feel free to adapt and design your own level. The whole map must be at least 3 floors and 15 rooms total, though.

"""
Only 15 rooms total sounds wrong so I'm assuming that's not the actual direction

OPTIONAL CODE BELOW
  -  lets the player adjust map dimensions based on input

while True:
    try:
        Amount_of_floors = int(input("Amount of floors? (Must be at least 4) ")) # Strictly must be at least 2 to prevent code errors
        if Amount_of_floors >= 4:
            break
        print("Invalid input, enter an integer equal to or greater than 4")
    except:
        print("Invalid input, enter an integer")

while True:
    try:
        Floor_size = int(input("Floor size? (Must be at least 5) ")) # Strictly must be at least 4 to prevent code errors
        if Floor_size >= 5:
            break
        print("Invalid input, enter an integer equal to or greater than 5")
    except:
        print("Invalid input, enter an integer")
"""

Amount_of_floors = 4
Floor_size = 5
room_nums = {
    1: 'sword',
    2: 'monster',
    3: 'empty'
}

"Just a function to ensure that the code follows assignment directions"

def validate_map_requirements(map):
    sword_count = 0
    monster_count = 0
    magic_stone_count = 0
    for floor in map:
        for room in floor:
            if room == 'sword':
                sword_count += 1
            elif room == 'monster':
                monster_count += 1
            elif room == 'magic stones':
                magic_stone_count += 1
    
    return sword_count >= 4 and monster_count >= 3 and magic_stone_count >= 1

"""
The following 5 functions are to randomize the map
  -  The first 4 of them are purely for function abstraction

The algorithm: 
  1)  Create the first floor
        -  ensure the first room is empty (start room)
        -  insert the 'stairs up' room last
  2)  For each floor in the middle, similar thing as the first floor
        -  Insert 'stairs up' THEN 'stairs down' because they can interfere with each other's indicies
        -  'stairs down' needs to be exact while 'stairs up' has more freedom
        -  Obtain the current index of 'stairs up' through [floor.index('stairs up)] because the index can be affected
  3)  Create the last 2 floors
        -  Ensure that the index of 'stairs down' on the last floor is to the right of boss monster
            -  That implies that 'stairs up' on the previous floor is also past the index of the boss monster
        -  Add 'prize' and 'boss monster' to the front of the last floor
  4)  Change one of the 'empty', 'monster', or 'sword' rooms to 'magic stones'
"""

def create_floor(new_up_stairs_index, down_stairs_index, floor_size):
    floor = []

    for j in range(floor_size - 2):
        floor.append(room_nums[randint(1, 3)])
    
    floor.insert(new_up_stairs_index, "stairs up")
    floor.insert(down_stairs_index, "stairs down")

    return floor

def create_first_floor():
    floor = create_floor(randint(0, Floor_size - 2), 0, Floor_size)

    floor[0] = 'empty'

    return floor

def create_middle_floors(previous_up_stairs_index, floors):

    middle_floors = []

    for i in range(floors):
        floor = create_floor(randint(0, Floor_size - 2), previous_up_stairs_index, Floor_size)
        previous_up_stairs_index = floor.index("stairs up")
        middle_floors.append(floor)
    
    return middle_floors

def create_last_2_floors(previous_up_stairs_index):
    second_to_last_floor = create_floor(randint(2, Floor_size - 2), previous_up_stairs_index, Floor_size)
    previous_up_stairs_index = second_to_last_floor.index("stairs up")

    last_floor = create_floor(0, previous_up_stairs_index - 1, Floor_size - 1)
    last_floor[0] = 'prize'
    last_floor.insert(1, 'boss monster')

    return (second_to_last_floor, last_floor)

def randomize_map(Amount_of_floors):
    map = []

    floor_rooms = create_first_floor()
    previous_up_stairs_index = floor_rooms.index("stairs up")
    map.append(floor_rooms)

    if Amount_of_floors - 3 > 0:
        middle_floors = create_middle_floors(previous_up_stairs_index, Amount_of_floors - 3)
        previous_up_stairs_index = middle_floors[-1].index("stairs up")
        for floor in middle_floors:
            map.append(floor)
    
    second_to_last_floor, last_floor = create_last_2_floors(previous_up_stairs_index)
    map.append(second_to_last_floor)
    map.append(last_floor)

    floor_index = 0
    room_index = 0

    while map[floor_index][room_index] in ['prize', 'boss monster', 'stairs up', 'stairs down'] or (floor_index == 0 and room_index == 0):
        floor_index = randint(0, Amount_of_floors - 1)
        room_index = randint(0, Floor_size - 1)
    
    map[floor_index][room_index] = 'magic stones'

    return map[::-1]

"""
The following 4 functions are to check if the map is beatable
They essentially define the algorithm for which it checks the map
  -  The first 3 are purely for function abstraction

Trick for this algorithm:
  -  Because the player can backtrack, you don't need to keep track of inventory space 
     because the amount of swords the player can access at any given time is just
     the surplus of swords accessible by that floor
  -  Therefore, just need make sure that at no time does the amount of monsters blocking 
     the path be greater than the swords accessible
  -  Then just check whether the cost (amount of swords) it takes to access the magic stones
     is small enough such that the player can beat the boss

A randomly generated example of back-tracking I noticed (and liked):
['prize', 'boss monster', 'monster', 'stairs down', 'sword']
['empty', 'stairs down', 'monster', 'stairs up', 'monster']
['sword', 'stairs up', 'stairs down', 'sword', 'sword']
['empty', 'empty', 'stairs up', 'monster', 'magic stones']

The fact that a [for loop] actually gives a reference to the floor from the map and editing it actually edits the map directly made me mald
https://stackoverflow.com/questions/8997559/yet-another-list-aliasing-conundrum?
https://stackoverflow.com/questions/2612802/how-do-i-clone-a-list-so-that-it-doesnt-change-unexpectedly-after-assignment

LMK if you want me to put an explanation of the algorithm and not just my insight here
"""

def check_floor(floor, start_pointer, end_pointer, step, sword_count):
    "Like why is the list here necessary cringeeeeeee"
    "Dont remove it though"
    floor_copy = list(floor)
    current_sword_count = sword_count

    iteration_improved = False
    Best_floor_config = floor
    Best_config_index = start_pointer
    floor_is_beatable = False

    for room_index in range(start_pointer, end_pointer, step):
        if room_index < 0 or room_index >= len(floor_copy):  # Prevent index errors
            break

        room = floor_copy[room_index]
        if room == 'sword':
            current_sword_count += 1
            floor_copy[room_index] = 'empty'
        elif room in ['monster', 'boss monster']:
            current_sword_count -= 1
            floor_copy[room_index] = 'empty'
        elif room in ['stairs up', 'prize']:
            floor_is_beatable = True
            Best_floor_config = floor_copy
            Best_config_index = room_index
            break

        if current_sword_count < 0:
            break
        if current_sword_count > sword_count:
            Best_floor_config = floor_copy
            Best_config_index = room_index
            sword_count = current_sword_count
            iteration_improved = True

    return (Best_floor_config, Best_config_index, iteration_improved, floor_is_beatable, sword_count)

def confirmation_floor_check(floor, start_pointer, sword_count):
    "Like why is the list here necessary cringeeeeeee"
    "Dont remove it though"
    floor_copy = list(floor)
    current_sword_count = sword_count

    magic_stone_sword_cost = -1

    for room_index in range(start_pointer, -1, -1):
        if floor_copy[room_index] == 'sword':
            current_sword_count += 1
            floor_copy[room_index] = 'empty'
        elif floor_copy[room_index] == 'monster':
            current_sword_count -= 1
            floor_copy[room_index] = 'empty'

        if current_sword_count < 0:
            break
        if current_sword_count > sword_count:
            sword_count = current_sword_count
    
    for room_index in range(start_pointer, Floor_size):
        if floor_copy[room_index] == 'sword':
            current_sword_count += 1
            floor_copy[room_index] = 'empty'
        elif floor_copy[room_index] == 'monster':
            current_sword_count -= 1
            floor_copy[room_index] = 'empty'

        if current_sword_count < 0:
            break
        if current_sword_count > sword_count:
            sword_count = current_sword_count

    if 'magic stones' in floor_copy:
        magic_stone_sword_cost = 0
        if floor_copy.index('magic stones') < start_pointer:
            for room_index in range(start_pointer, -1, -1):
                if floor_copy[room_index] == 'sword':
                    magic_stone_sword_cost -= 1
                elif floor_copy[room_index] == 'monster':
                    magic_stone_sword_cost += 1
        else:
            for room_index in range(start_pointer, Floor_size):
                if floor_copy[room_index] == 'sword':
                    magic_stone_sword_cost -= 1
                elif floor_copy[room_index] == 'monster':
                    magic_stone_sword_cost += 1
    
    return (sword_count, magic_stone_sword_cost)

def change_direction(direction):
    if direction == 1:
        return -1, -1
    else:
        return Floor_size, 1

def check_winnability(map):
    "Like why is the list here necessary cringeeeeeee"
    "Dont remove it though"
    map = list(map)
    # Need to change code in case magic stones are in that floor
    if not validate_map_requirements(map):
        return False
    
    sword_count = 0

    current_magic_stone_cost = -1

    for index in range(len(map) - 1, -1, -1):
        floor = map[index]

        floor_is_beatable = False
        end_pointer = Floor_size
        start_pointer = floor.index("stairs down") if "stairs down" in floor else 0 # sets the index to 0 if on the first floor

        Best_floor_config = floor
        Best_config_index = start_pointer
        step = 1
        
        flag = True

        while flag:
            iteration_improved = False
            Best_floor_config, Best_config_index, iteration_improved, floor_is_beatable, sword_count = check_floor(Best_floor_config, start_pointer, end_pointer, step, sword_count)

            if floor_is_beatable:
                sword_count, new_magic_stone_cost = confirmation_floor_check(Best_floor_config, Best_config_index, sword_count)
                current_magic_stone_cost = new_magic_stone_cost if new_magic_stone_cost > current_magic_stone_cost else current_magic_stone_cost
                break

            end_pointer, step = change_direction(step)

            if iteration_improved:
                continue
            Best_floor_config, Best_config_index, iteration_improved, floor_is_beatable, sword_count = check_floor(Best_floor_config, start_pointer, end_pointer, step, sword_count)

            end_pointer, step = change_direction(step)

            if iteration_improved:
                continue
            return False
    
    if sword_count - current_magic_stone_cost >= 0:
        return True
    return False

map_winnable = False
while not map_winnable:
    map = randomize_map(Amount_of_floors)
    map_winnable = check_winnability(map)

# Items in the player's possession
inventory = []

# Player's current position in the dungeon
# The player starts in the first room on the bottom floor
currentFloor = Amount_of_floors - 1 # This is the bottom floor
currentRoom = 0 # This is the first empty room on the bottom floor

gameOver = False # Keeps track of whether the game is in progress or over (to know when to stop the game loop)

"""
The code below is what actually runs the game

The main running code is in the [while not gameOver: ] under all the functions
  -  All of the functions are function abstraction
  -  Separated each category of room so that a simple [match - case] can be run in the loop
  -  Defined [print_help()] to reduce lines in [general_action()], optional and doesn't reduce indent level
  -  Added [match - case] to both [general_action()] and [monster_room()] for readability

In the end the code below is pretty simple, pretty easy to understand
"""

def print_help():
    print("""
    left: Takes you to the room to your left
    right: Takes you to the room to your right
    up: Takes you to the floor above you only if there are stairs up in your room
    down: Takes you to the floor below you only if there are stairs down in your room
    fight: Allowd you to fight the monster if there is one in your room
    grab: Allows you to grab the item in the room
    inventory: Allows you to see the items you have
""")

def general_action(room_column, action):
    match action:
        case 'help':
            print_help()

        case 'end':
            return "Something that isn't room_column so there is an error"
        
        case 'inventory':
            print(f"You have: {", ".join(inventory)}")

        case 'left' | 'right':
            return move_horizontally(room_column, action)
        
        case 'fight' | 'grab':
            print(f"There is nothing to {action}")

        case 'up' | 'down':
            print(f"You cannot go {action}")

        case _:
            print("That is an invalid action")
    return room_column

def move_horizontally(room_column, left_or_right):
    if left_or_right == "left" and currentRoom > 0:
        return room_column - 1
    elif left_or_right == 'right' and currentRoom < Floor_size - 1:
        return room_column + 1
    print("There is no room in that direction")
    return room_column

def empty_room(room_column):
    print('You are in an empty room.')
    action = input('Command? ')
    return general_action(room_column, action)

def monster_room(type_of_monster):
    Game_is_over, Game_isnt_over = True, False

    if type_of_monster == 'monster':
        print("There is an monster in this room.")
        required_items = ['sword']
    
    elif type_of_monster == 'boss monster':
        print("You sense powerful monster in this room...")
        required_items = ['sword', 'magic stones']

    action = input('Command? ')

    match action:
        case 'help':
            print_help()
            return Game_isnt_over
        
        case 'fight' if all(item in inventory for item in required_items):
            print(f"You defeated the {type_of_monster}!")
            for item in required_items:
                inventory.remove(item)
            map[currentFloor][currentRoom] = "empty"
            return Game_isnt_over
        
        case 'fight':
            print(f"You attempted to fight {type_of_monster} without a required item and lost! ")
            print(f"You had: {", ".join(inventory)}")
            print(f"You needed: a {" and ".join(required_items)}")
            return Game_is_over
        
        case 'left' | 'right':
            print(f"You attempted to flee from the {type_of_monster} and failed!")
            return Game_is_over
        
        case _:
            print("That is an invalid action")
            return False

def item_room(room_column, item):

    if item == 'sword':
        print("There is a trusty blade in this room.")
    elif item == 'magic stones':
        print("There are magical stones resonating this room.")
    
    action = input('Command? ')

    if action == 'grab':
        if len(inventory) >= 3:
            print("You cannot carry any more items")
        else:
            inventory.append(item)
            print(f"[{item} has been added to inventory]")
            map[currentFloor][currentRoom] = "empty"
        return room_column
    return general_action(room_column, action)
    
def stair_room(floor_level, room_column, up_or_down):

    print(f"There are stairs in this room going {up_or_down}")
    action = input('Command? ')
    if action == up_or_down and up_or_down == "up":
        return (floor_level - 1, room_column)
    elif action == up_or_down and up_or_down == "down":
        return (floor_level + 1, room_column)
    return (floor_level, general_action(room_column, action))

while not gameOver:
    "CODE THAT NEEDS TO BE REMOVED - SOLELY FOR DEBUGGING"
    for floor in map:
        print(floor)

    "CODE THAT SHOULD STAY"
    # Describe the room the player is in
    room = map[currentFloor][currentRoom]

    match room:
        case 'empty':
            currentRoom = empty_room(currentRoom)

        case 'sword' | 'magic stones':
            currentRoom = item_room(currentRoom, room)

        case 'stairs up':
            currentFloor, currentRoom = stair_room(currentFloor, currentRoom, 'up')

        case 'stairs down':
            currentFloor, currentRoom = stair_room(currentFloor, currentRoom, 'down')

        case 'monster' | 'boss monster':
            gameOver = monster_room(room)

        case 'prize':
            print("In front of you is a treasure chest")
            print("You get 100 fictional currency! ")
            inventory.append("100 fictional currency")
            map[currentFloor][currentRoom] = 'opening'
        
        case 'opening':
            print("In front of you is an opening")
            action = input("Would you like to leave the maze? ")
            if action == 'yes':
                print("You have won the game!")
                gameOver = True
            else:
                print("You take a step back. ")
                currentRoom += 1 # 500 LINES OF CODE EXACTLY!!!!!