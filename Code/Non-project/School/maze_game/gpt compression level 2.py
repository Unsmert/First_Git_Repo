import copy
from random import randint
Amount_of_floors=4;Floor_size=5;room_nums={1:'sword',2:'monster',3:'empty'}
def validate_map_requirements(m):
    s=mon=ms=0
    for f in m:
        for r in f:
            if r=='sword':s+=1
            elif r=='monster':mon+=1
            elif r=='magic stones':ms+=1
    return s>=4 and mon>=3 and ms>=1
def create_floor(u,d,n):
    f=[room_nums[randint(1,3)]for _ in range(n-2)];f.insert(u,'stairs up');f.insert(d,'stairs down');return f
def create_first_floor():
    f=create_floor(randint(0,Floor_size-2),0,Floor_size);f[0]='empty';return f
def create_last_2_floors(p):
    s=create_floor(randint(2,Floor_size-2),p,Floor_size);p=s.index('stairs up');l=create_floor(0,p-1,Floor_size-1);l[0]='prize';l.insert(1,'boss monster');return s,l
def randomize_map(n):
    m=[create_first_floor()];p=m[0].index('stairs up')
    if n-3>0:
        for _ in range(n-3):
            f=create_floor(randint(0,Floor_size-2),p,Floor_size);p=f.index('stairs up');m.append(f)
    s,l=create_last_2_floors(p);m+=[s,l];fi=ri=0
    while m[fi][ri] in ['prize','boss monster','stairs up','stairs down'] or (fi==0 and ri==0):
        fi,ri=randint(0,n-1),randint(0,Floor_size-1)
    m[fi][ri]='magic stones';return m[::-1]
def check_floor(floor,start_pointer,end_pointer,step,sword_count):
    fc=copy.deepcopy(floor);cs=sword_count;iteration_improved=False;Best_floor_config=floor;Best_config_index=start_pointer;floor_is_beatable=False
    for room_index in range(start_pointer,end_pointer,step):
        if room_index<0 or room_index>=len(fc):break
        room=fc[room_index]
        if room=='sword':cs+=1;fc[room_index]='empty'
        elif room in ['monster','boss monster']:cs-=1;fc[room_index]='empty'
        elif room in ['stairs up','prize']:floor_is_beatable=True;Best_floor_config=fc;Best_config_index=room_index;break
        if cs<0:break
        if cs>sword_count:Best_floor_config=fc;Best_config_index=room_index;sword_count=cs;iteration_improved=True
    return Best_floor_config,Best_config_index,iteration_improved,floor_is_beatable,sword_count
def confirmation_floor_check(floor,start_pointer,sword_count):
    fc=copy.deepcopy(floor);cs=sword_count;magic_stone_sword_cost=-1
    for room_index in range(start_pointer,-1,-1):
        if fc[room_index]=='sword':cs+=1;fc[room_index]='empty'
        elif fc[room_index]=='monster':cs-=1;fc[room_index]='empty'
        if cs<0:break
        if cs>sword_count:sword_count=cs
    for room_index in range(start_pointer,Floor_size):
        if fc[room_index]=='sword':cs+=1;fc[room_index]='empty'
        elif fc[room_index]=='monster':cs-=1;fc[room_index]='empty'
        if cs<0:break
        if cs>sword_count:sword_count=cs
    if 'magic stones' in fc:
        magic_stone_sword_cost=0
        if fc.index('magic stones')<start_pointer:
            for room_index in range(start_pointer,-1,-1):
                if fc[room_index]=='sword':magic_stone_sword_cost-=1
                elif fc[room_index]=='monster':magic_stone_sword_cost+=1
        else:
            for room_index in range(start_pointer,Floor_size):
                if fc[room_index]=='sword':magic_stone_sword_cost-=1
                elif fc[room_index]=='monster':magic_stone_sword_cost+=1
    return sword_count,magic_stone_sword_cost
def change_direction(direction):return(-1,-1) if direction==1 else (Floor_size,1)
def check_winnability(m):
    m=copy.deepcopy(m)
    if not validate_map_requirements(m):return False
    sword_count=0;current_magic_stone_cost=-1
    for index in range(len(m)-1,-1,-1):
        floor=m[index];end_pointer=Floor_size;start_pointer=floor.index('stairs down') if 'stairs down' in floor else 0;Best_floor_config=floor;Best_config_index=start_pointer;step=1
        while 1:
            Best_floor_config,Best_config_index,iteration_improved,floor_is_beatable,sword_count=check_floor(Best_floor_config,start_pointer,end_pointer,step,sword_count)
            if floor_is_beatable:
                sword_count,new_magic_stone_cost=confirmation_floor_check(Best_floor_config,Best_config_index,sword_count);current_magic_stone_cost=new_magic_stone_cost if new_magic_stone_cost>current_magic_stone_cost else current_magic_stone_cost;break
            end_pointer,step=change_direction(step)
            if iteration_improved:continue
            Best_floor_config,Best_config_index,iteration_improved,floor_is_beatable,sword_count=check_floor(Best_floor_config,start_pointer,end_pointer,step,sword_count)
            end_pointer,step=change_direction(step)
            if iteration_improved:continue
            return False
    return sword_count-current_magic_stone_cost>=0
map_winnable=False
while not map_winnable:map=randomize_map(Amount_of_floors);map_winnable=check_winnability(map)
inventory=[];currentFloor=Amount_of_floors-1;currentRoom=0;gameOver=False
def print_help():print('left: Takes you to the room to your left\nright: Takes you to the room to your right\nup: Takes you to the floor above you only if there are stairs up in your room\ndown: Takes you to the floor below you only if there are stairs down in your room\nfight: Allowd you to fight the monster if there is one in your room\ngrab: Allows you to grab the item in the room\ninventory: Allows you to see the items you have')
def general_action(r,a):
    if a=='help':print_help()
    if a=='end':return'!'
    if a=='inventory':print(f"You have: {', '.join(inventory)}")
    if a in ['left','right']:return move_horizontally(r,a)
    if a in ['fight','grab']:print(f"There is nothing to {a}")
    if a in ['up','down']:print(f"You cannot go {a}")
    else:print('That is an invalid action');return r
def move_horizontally(r,d):
    if d=='left'and currentRoom>0:return r-1
    if d=='right'and currentRoom<Floor_size-1:return r+1
    print('There is no room in that direction');return r
def empty_room(r):print('You are in an empty room.');return general_action(r,input('Command? '))
def monster_room(t):
    req=['sword'] if t=='monster' else ['sword','magic stones']
    print("There is an intimidating beast in this room."if t=='monster'else"You sense menacing silhouette in this room...")
    a=input('Command? ')
    if a not in ['help','fight','left','right']:print('That is an invalid action');return False
    if a=='help':print_help();return False
    if a!='fight':print(f'You attempted to flee from the {t} and failed!');return True
    if all(i in inventory for i in req):print(f'You defeated the {t}!');[inventory.remove(i) for i in req];map[currentFloor][currentRoom]='empty';return False
def item_room(r,i):
    print("There is a trusty blade in this room."if i=='sword'else'There are magical stones resonating this room.')
    a=input('Command? ')
    if a=='grab':
        if len(inventory)>=3:print('You cannot carry any more items')
        else:inventory.append(i);print(f'[{i} has been added to inventory]');map[currentFloor][currentRoom]='empty';return r
    return general_action(r,a)
def stair_room(f,r,d):
    print(f'There are stairs in this room going {d}')
    a=input('Command? ')
    if a==d and d=='up':return (f-1,r)
    if a==d and d=='down':return (f+1,r)
    return (f,general_action(r,a))
while not gameOver:
    for f in map:print(f)
    room=map[currentFloor][currentRoom]
    if room=='empty':currentRoom=empty_room(currentRoom)
    elif room in ['sword','magic stones']:currentRoom=item_room(currentRoom,room)
    elif room=='stairs up':currentFloor,currentRoom=stair_room(currentFloor,currentRoom,'up')
    elif room=='stairs down':currentFloor,currentRoom=stair_room(currentFloor,currentRoom,'down')
    elif room in ['monster','boss monster']:gameOver=monster_room(room)
    elif room=='prize':print('You have won!!!');gameOver=True