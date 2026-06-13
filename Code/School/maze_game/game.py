# NAMES: Mohammed Mohmedzain, Lishanth Payyavula, Ruohan Xu
# Period: 2
# Date Last Edited: 10/5

# Check for +6: Map Randomization
# Check for +4: Detailed Descriptions

# The whole map must be at least 3 floors and 15 rooms total, though.

from random import randint

Amount_of_floors = 4
Floor_size = 5
inventory_size = 3

"""
Only 15 rooms total sounds wrong so I'm assuming that's not the actual direction

OPTIONAL CODE BELOW
  -  lets the player adjust map dimensions based on input
"""

# while True:
#     try:
#         Amount_of_floors = int(input("Amount of floors? (Must be at least 4) ")) # Strictly must be at least 3 to prevent code errors
#         if Amount_of_floors >= 4:
#             break
#         print("Invalid input, enter an integer equal to or greater than 4")
#     except:
#         print("Invalid input, enter an integer")

# while True:
#     try:
#         Floor_size = int(input("Floor size? (Must be at least 5) ")) # Strictly must be at least 4 to prevent code errors
#         if Floor_size >= 5:
#             break
#         print("Invalid input, enter an integer equal to or greater than 5")
#     except:
#         print("Invalid input, enter an integer")

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
  4)  Take 2 of the 'empty', 'monster', or 'sword' rooms; change 1 to 'magic stones' and 1 to 'exit gate'
"""

room_nums = ['sword', 'monster', 'empty']

def create_floor(new_up_stairs_index, down_stairs_index, floor_size):
    floor = []

    for j in range(floor_size - 2):
        floor.append(room_nums[randint(0, 2)])
    
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
    second_to_last_floor = create_floor(randint(2, Floor_size - 2), previous_up_stairs_index, Floor_size) # this line technically leaves out a few possible map arrangements, but it's fineeee
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

    while map[floor_index][room_index] in ['prize', 'boss monster', 'stairs up', 'stairs down', 'magic stones'] or (floor_index == 0 and room_index == 0):
        floor_index = randint(0, Amount_of_floors - 1)
        room_index = randint(0, Floor_size - 1)
    map[floor_index][room_index] = 'exit gate'

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
  -  Then, make sure the cost (amount of swords) it takes to access the magic stones and 
     access the exit gate is smaller or equal to the sword surplus by the time you get to the boss monster

A randomly-generated example of back-tracking I noticed (and liked):
['prize', 'boss monster', 'monster', 'stairs down', 'sword']
['exit gate', 'stairs down', 'monster', 'stairs up', 'monster']
['sword', 'stairs up', 'stairs down', 'sword', 'sword']
['empty', 'empty', 'stairs up', 'monster', 'magic stones']

The fact that a [for loop] actually gives a reference to the floor from the map and editing it actually edits the map directly made me mald
https://stackoverflow.com/questions/8997559/yet-another-list-aliasing-conundrum?
https://stackoverflow.com/questions/2612802/how-do-i-clone-a-list-so-that-it-doesnt-change-unexpectedly-after-assignment

After a bit of time, I no longer understand my own code lol
"""

"Like why does list() have to be in these functions, that's so cringeeeeeeee"
def check_floor(floor, start_pointer, end_pointer, step, sword_count):
    floor_copy = list(floor)
    current_sword_count = sword_count

    iteration_improved = False
    Best_floor_config = floor
    Best_config_index = start_pointer
    floor_is_beatable = False

    for room_index in range(start_pointer, end_pointer, step):
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
    floor_copy = list(floor)
    current_sword_count = sword_count

    magic_stone_sword_cost = -1
    exit_gate_sword_cost = -1

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
    
    if 'exit gate' in floor_copy:
        exit_gate_sword_cost = 0
        if floor_copy.index('exit gate') < start_pointer:
            for room_index in range(start_pointer, -1, -1):
                if floor_copy[room_index] == 'sword':
                    exit_gate_sword_cost -= 1
                elif floor_copy[room_index] == 'monster':
                    exit_gate_sword_cost += 1
        else:
            for room_index in range(start_pointer, Floor_size):
                if floor_copy[room_index] == 'sword':
                    exit_gate_sword_cost -= 1
                elif floor_copy[room_index] == 'monster':
                    exit_gate_sword_cost += 1
    
    return (sword_count, magic_stone_sword_cost, exit_gate_sword_cost)
def change_direction(direction):
    if direction == 1:
        return -1, -1
    else:
        return Floor_size, 1
def check_winnability(map):
    if not validate_map_requirements(map):
        return False
    
    map_copy = list(map)

    sword_count = 0
    current_magic_stone_cost = -1
    current_exit_gate_cost = -1

    for index in range(len(map_copy) - 1, -1, -1):
        floor = map_copy[index]

        floor_is_beatable = False
        end_pointer = Floor_size
        start_pointer = floor.index("stairs down") if "stairs down" in floor else 0 # sets the index to 0 if on the first floor
        Best_floor_config = floor # What are the rooms on the best state of the floor
        Best_config_index = start_pointer
        step = 1

        while True:
            iteration_improved = False
            Best_floor_config, Best_config_index, iteration_improved, floor_is_beatable, sword_count = check_floor(Best_floor_config, start_pointer, end_pointer, step, sword_count)

            if floor_is_beatable:
                sword_count, new_magic_stone_cost, new_exit_gate_cost = confirmation_floor_check(Best_floor_config, Best_config_index, sword_count)
                current_magic_stone_cost = new_magic_stone_cost if new_magic_stone_cost > current_magic_stone_cost else current_magic_stone_cost
                current_exit_gate_cost = new_exit_gate_cost if new_exit_gate_cost > current_exit_gate_cost else current_exit_gate_cost
                break

            end_pointer, step = change_direction(step)

            if iteration_improved:
                continue
            Best_floor_config, Best_config_index, iteration_improved, floor_is_beatable, sword_count = check_floor(Best_floor_config, start_pointer, end_pointer, step, sword_count)

            end_pointer, step = change_direction(step)

            if iteration_improved:
                continue
            return False
    
    if sword_count - current_magic_stone_cost - current_exit_gate_cost >= 0:
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

"""
The code below is what actually runs the game

The main running code is in the [while not gameOver: ] loop under all the functions
  -  All of the functions are purely for function abstraction
  -  Separated each category of room so that a simple [match - case] can be run in the loop
  -  Defined [print_help()] to reduce lines in [general_action()], optional and doesn't reduce indent level
  -  Added [match - case] to both [general_action()] and [monster_room()] for readability

In the end the code below is pretty simple, pretty easy to understand
"""

playermap = [['?????' for i in range(Floor_size)] for j in range(Amount_of_floors)]

"The code below is what I wanted to add to the map, but it messes with the flavor text logic and I'm too lazy to adjust the logic since the fun part is over soooo yah..."
# playermap[0][0], playermap[0][1] = 'prize', 'boss monster'

def print_help():
    print("""
    left: Takes you to the room to your left
    right: Takes you to the room to your right
    up: Takes you to the floor above you only if there are stairs up in your room
    down: Takes you to the floor below you only if there are stairs down in your room
    fight: Allowd you to fight the monster if there is one in your room
    grab: Allows you to grab the item in the room
    inventory: Allows you to see the items you have
    map: Allows you to see the map of the maze with the rooms you have visited
    open: Used to open the exit gate with a key
    end: Quits the game
    """)
def print_player_map():
    for floor_index in range(Amount_of_floors):
        for room_index in range(Floor_size):
            if floor_index == currentFloor and room_index == currentRoom:
                print(f"[{'You':^14}]", end= "  ")
            else:
                print(f"[{playermap[floor_index][room_index]:^14}]", end= "  ")
        print()
def print_room_text():
    if entered_for_first_time:
        print(flavor_text)
    else:
        print(basic_text)
    
    return input('Command? ')
def get_room_text(parameter_room):
    match parameter_room:
        case 'empty':
            detailed_text = "A deafening silence fills the vicinity, all of the warmth and light stripped from the room. The surface is bare and have no company as you stand in this flavorless expanse."
            simple_text = "You are in an empty room"

        case 'sword': 
            detailed_text = "A seemingly reliable sword rests upright in a pedastal as you enter, though the oxidation dims the shine and glimmer. "
            simple_text = "There is a sword in this room."
        
        case 'magic stones':
            detailed_text = "A low hum vibrates through the air, rune-etched stones come into view. You feel raw and untamed energy emanating from the gems."
            simple_text = "There are magical stones in this room."

        case 'stairs up' :
            detailed_text = "The stone walls tremble slightly, cracked and crumbling from erosion. Ancient steps spiral upward into darkness, worn down by countless footsteps long since faded from memory."
            simple_text = "There are stairs in this room going up"
        
        case 'stairs down':
            detailed_text = "A chilling draft rises from the depths below. The steps descend into shadows, the darkness swalling the path whence you once came. "
            simple_text = "There are stairs in this room going down"
        case 'monster':
            detailed_text = "A dread comes over you as you enter this room. You can almost grasp the air from the musky energy. Your hands shake with anticipation as you encounter a ghastly beast"
            simple_text = "There is a monster in this room."

        case 'boss monster':
            detailed_text = "The room is curdled with a thick bloodlust, a low growl vibrates the floor as you eye an unsettling silhoutte. A harrowing brute emerges from the miserably thick ambience, making your blood run cold."
            simple_text = "There is a boss monster in this room. "

        case 'prize':
            detailed_text = "Your steps reverberate through the air, clanking on the medal, the atmosphere humming with reward and completion. This is it; the prize you've fought hard to claim. "
            simple_text = "There is a prize in this room. "
        
        case 'exit gate':
            detailed_text = "A tall wooden gate, weathered by time, stands sealed before you, emanating a faint magical pulse. An ornate iron keyhole lies carved into its center."
            simple_text = "Before you lies the exit gate. "
        
        case "Boss's Diary":
            detailed_text = 'This string is not used at all lol'
            simple_text = "In this room lies the Boss's Diary"
    
    return detailed_text, simple_text

def general_action(room_column, action):
    
    match action:
        case 'help':
            print_help()
        
        case 'map':
            print_player_map()

        case 'end':
            global gameOver
            gameOver = True
            print("You choose to give up. ")
        
        case 'inventory':
            print(f"You have: {', '.join(inventory)}")

        case 'left' | 'right':
            return move_horizontally(room_column, action)
        
        case 'fight' | 'grab' | 'open':
            print(f"Invalid Input - There is nothing to {action}")

        case 'up' | 'down':
            print(f"Invalid Input - You cannot go {action}")

        case _:
            print("Invalid Input - That is an invalid action")
    return (room_column, "N/A")

def move_horizontally(room_column, left_or_right):
    if left_or_right == "left" and currentRoom > 0:
        return (room_column - 1, 'left')
    elif left_or_right == 'right' and currentRoom < Floor_size - 1:
        return (room_column + 1, 'right')
    print("Invalid Input - There is no room in that direction")
    return room_column, 'N/A'

def empty_room(room_column):
    action = print_room_text()
    return general_action(room_column, action)

def enemy_room(type_of_monster, previous_move):
    Game_is_over, Game_isnt_over = True, False
    global currentRoom

    action = print_room_text()

    match action: 
        case 'fight' if all(item in inventory for item in required_items):
            print(f"You defeated the {type_of_monster}!")
            for item in required_items:
                inventory.remove(item)
            map[currentFloor][currentRoom] = "empty"
        
        case 'fight':
            print(f"You attempted to fight {type_of_monster} without a required item and lost! ")
            print(f"You had: {', '.join(inventory)}")
            print(f"You needed: a {' and '.join(required_items)}")
            return Game_is_over
        
        case 'left' if previous_move == 'right':
            currentRoom -= 1

        case 'right' if previous_move == 'left':
            currentRoom += 1
        
        case 'left' | 'right':
            print(f"You attempted to run past the {type_of_monster} and died")
            return Game_is_over
        
        case 'end':
            general_action(currentRoom, action)
            return Game_is_over
        
        case _:
            general_action(currentRoom, action)
    return Game_isnt_over
def item_room(room_column, item):
    action = print_room_text()

    if action == 'grab':
        if len(inventory) >= inventory_size:
            print("You cannot carry any more items")
        else:
            print(f"[{item} has been added to inventory]")
            inventory.append(item)
            map[currentFloor][currentRoom] = "empty"
        return room_column, 'N/A'
    return general_action(room_column, action)    
def stair_room(floor_level, room_column, up_or_down):
    action = print_room_text()

    if action == up_or_down and up_or_down == "up":
        return (floor_level - 1, room_column, 'N/A')
    elif action == up_or_down and up_or_down == "down":
        return (floor_level + 1, room_column, 'N/A')
    
    new_room_column, previous_action = general_action(room_column, action)
    return (floor_level, new_room_column, previous_action)
def prize_room(room_column):
    action = print_room_text()

    if action == 'grab':
        print("[key has been added to inventory]")
        inventory.insert(0, 'key')
        global inventory_size
        inventory_size += 1
        if len(inventory) >= inventory_size:
            print("You cannot carry any more items")
            new_room = "Boss's Diary"
        else:
            print("[The Boss's Diary has been added to inventory]")
            inventory.append("Boss's Diary")
            new_room = "empty"
        return room_column, 'N/A', new_room
        
    room_column, previous_action = general_action(room_column, action)
    return room_column, previous_action

def gate_room(room_column):
    action = print_room_text()

    if action == 'open' and 'key' in inventory:
        global gameOver
        gameOver = True
        print("You insert the key... \nThe gate groans open, and light floods in. \nYou step through — free at last. ")
        return room_column, 'N/A'
    if action == 'open' and 'key' not in inventory:
        print("You need a key to open the gate. ")
        return room_column, 'N/A'
    
    return general_action(room_column, action) 

currentFloor = Amount_of_floors - 1 # This is the bottom floor
currentRoom = 0 # This is the first empty room on the bottom floor

room = map[currentFloor][currentRoom]

gameOver = False # Keeps track of whether the game is in progress or over (to know when to stop the game loop)

while not gameOver:
    room = map[currentFloor][currentRoom]
    entered_for_first_time = playermap[currentFloor][currentRoom] == '?????'
    playermap[currentFloor][currentRoom] = room
    flavor_text, basic_text = get_room_text(room)

    match room:
        case 'empty':
            currentRoom, previous_action = empty_room(currentRoom)

        case 'sword' | 'magic stones' | "Boss's Diary": 
            currentRoom, previous_action = item_room(currentRoom, room)

        case 'stairs up' | 'stairs down':
            currentFloor, currentRoom, previous_action = stair_room(currentFloor, currentRoom, room[7:])

        case 'monster' | 'boss monster':
            required_items = ['sword'] if room == 'monster' else ['sword', 'magic stones']
            gameOver = enemy_room(room, previous_action)

        case 'prize':
            currentRoom, previous_action, map[0][0] = prize_room(currentRoom)
        
        case 'exit gate':
            currentRoom, previous_action = gate_room(currentRoom)