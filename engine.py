from main import BOARD_HEIGHT, BOARD_WIDTH
import main
import random
import os
import ui
import time
floor = 2
discovered_floor_0 = None
discovered_floor_1 = None
discovered_floor_2 = None
icanseeyou = 1
# board is based on rows / height = rows / width = elements in row

def create_board(width, height):
    '''
    Creates a new game board based on input parameters.

    Args:
    int: The width of the board
    int: The height of the board

    Returns:
    list: Game board
    '''
    board = []
    temp_list = []
    for j in range(height):
        for i in range(width):
            if (j == 0 or j == height - 1):
                temp_list.append("#")
            elif (i == 0 or i == width - 1):
                temp_list.append("#")
            else:
                temp_list.append(" ")
        board.append(temp_list)
        temp_list = []
    return board

def put_player_on_board(board, player, floors):
    '''
    Modifies the game board by placing the player icon at its coordinates.

    Args:
    list: The game board
    dictionary: The player information containing the icon and coordinates

    Returns:
    Nothing
    '''
    x, y = check_player_position(board)
    if x == -1 or y == -1:
        x = player["x"]
        y = player["y"]

    # current_floor = read_board(change_floor())
    remove_monsters_from_eyeshot(board)
    remove_boss_from_eyeshot(board)

    if icanseeyou == 0:
        count_x = -3
        count_y = -3
        for i in range(7):
            for j in range(7):
                if x + count_x in range(-1, BOARD_HEIGHT) and y + count_y in range(-1, BOARD_WIDTH):
                    board[x + count_x][y + count_y] = floors[floor][x + count_x][y + count_y]
                    count_y += 1
            count_x += 1
            count_y = -3
    if icanseeyou == 1:
        count_x = 0
        count_y = 0
        for i in range(36):
            for j in range(64):
                if count_x in range(-1, BOARD_HEIGHT) and count_y in range(-1, BOARD_WIDTH):
                    board[count_x][count_y] = floors[floor][count_x][count_y]
                    count_y += 1
            count_x += 1
            count_y = 0

    board[x][y] = player["icon"]



def check_player_position(board):
    player_x, player_y = -1, -1
    for x, i in enumerate(board):
        for y, j in enumerate(i):
            if j == "@":
                player_x = x
                player_y = y
    return player_x, player_y


def player_movement(key, board, floors):
    global floor
    global discovered_floor_0
    global discovered_floor_1
    global discovered_floor_2
    player_x, player_y = check_player_position(board)
# przechodzenie pomiedzy floorami
    cheats_module(key)

#TODO: zrobić w innej funkcji
    if floor == 0 and board[3][63] == "@" and key == "d":
        floor = 1
        discovered_floor_0 = board
        if discovered_floor_1 == None:
            board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
        else:
            board = discovered_floor_1
        board[3][0] = "@"
        return board
    elif floor == 1 and board[3][0] == "@" and key == "a":
        floor = 0
        discovered_floor_1 = board
        board = discovered_floor_0
        board[3][63] = "@"
        return board
    elif floor == 1 and board[35][1] == "@" and key == "s":
        floor = 2
        discovered_floor_1 = board
        if discovered_floor_2 == None:
            board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
        else:
            board = discovered_floor_2
        board[0][1] = "@"
        return board
    elif floor == 2 and board[0][1] == "@" and key == "w":
        floor = 1
        discovered_floor_2 = board
        board = discovered_floor_1
        board[35][1] = "@"
        return board

# znaleznienie itemu przez gracza
    player_stand_on_item(player_x, player_y, key, board, floors)
    if contact_with_boss(key, board, player_x, player_y) == True:
        return board
# ruch gracza
    if key == "w":
        if not board[player_x - 1][player_y] == "#":
            board[player_x - 1][player_y] = "@"
            board[player_x][player_y] = "."
    elif key == "s":
        if not board[player_x + 1][player_y] == "#":
            board[player_x + 1][player_y] = "@"
            board[player_x][player_y] = "."
    elif key == "a":
        if not board[player_x][player_y - 1] == "#":
            board[player_x][player_y - 1] = "@"
            board[player_x][player_y] = "."
    elif key == "d":
        if not board[player_x][player_y + 1] == "#":
            board[player_x][player_y + 1] = "@"
            board[player_x][player_y] = "."

    return board

def remove_monsters_from_eyeshot(board):
    for x, i in enumerate(board):
        for y, j in enumerate(i):
            if j == "M":
                board[x][y] = "."
    return board


def remove_boss_from_eyeshot(board):
    for x, i in enumerate(board):
        for y, j in enumerate(i):
            if j == "B":
                board[x][y] = "."
    return board

def player_stand_on_item(player_x, player_y, key, board, floors):
    if key == "w":
        if board[player_x - 1][player_y] == "X":
            (floors[floor])[player_x - 1][player_y] = "."
            draw_item()
            os.system('pause')
            return True
    elif key == "s":
        if board[player_x + 1][player_y] == "X":
            (floors[floor])[player_x + 1][player_y] = "."
            draw_item()
            os.system('pause')
            return True
    elif key == "a":
        if board[player_x][player_y - 1] == "X":
            (floors[floor])[player_x][player_y - 1] = "."
            draw_item()
            os.system('pause')
            return True
    elif key == "d":
        if board[player_x][player_y + 1] == "X":
            (floors[floor])[player_x][player_y + 1] = "."
            draw_item()
            os.system('pause')
            return True


def draw_item():
    select_dict = random.choice(item_list)
    item = random.choice(list(select_dict))
    number = random.randint(1, 10)
    ability = ""
    if select_dict == eq_items and eq_items[item]['name'] == "artifact":
        finall_ability = random.choice(artifact_ability_list)
        ability = finall_ability
        number = eq_items[item]['att']
    if select_dict == eq_items and eq_items[item]['name'] == "helmet":
        hp_number = random.randint(1, 100)
        number = hp_number

    adjective = ""
    if number <= 3:
        adjective = "basic "
    elif number <= 6:
        adjective = "improved "
    elif number <= 9:
        adjective = "magic "
    elif number >= 10:
        adjective = "unique "

    drew_item_informations(number, adjective, select_dict, item, ability)


def drew_item_informations(number, adjective, select_dict, item, ability):

    if select_dict == items_food:
        print(
            f"You found {items_food[item]['name']}. It recovers you {items_food[item]['hp']} {items_food[item]['function']}")
        main.health += items_food[item]['hp']

    if select_dict == eq_items:
        if eq_items[item]['name'] != "key" and eq_items[item]['name'] != "artifact":
            print(
                f"You found {adjective}{eq_items[item]['name']}. It's increasing {eq_items[item]['function']} by {number}. It was added to your inventory.")
            main.inventory.append(
                f"{adjective}{eq_items[item]['name']} - {eq_items[item]['function']} + {number}.")
#FIXME: zapisać printy do UI
            if eq_items[item]['name'] == "sword":
                main.attack += number
            if eq_items[item]['name'] == "shield":
                main.armour += number
            if eq_items[item]['name'] == "armour":
                main.armour += number
            if eq_items[item]['name'] == "helmet":
                main.total_health += number
        elif eq_items[item]['name'] == "artifact":
            print(
                f"You found {eq_items[item]['name']}. It's increasing {ability} by {number}. It was added to your inventory.")
            if ability == "deffence points":
                main.armour += number
                # main.inventory.append(f"{eq_items[item]['name']} + {number}") #DO USTALENIA - róg kurwa obrony 
            else:
                main.attack += number
                # main.inventory.append(f"{eq_items[item]['name']} + {number}") #DO USTALENIA - róg kurwa ataku
        elif eq_items[item]['name'] == "key":
            print(
                f"You've found an {eq_items[item]['name']}! It was added to your inventory.")
            main.inventory.append(f"Key")

# floor parameter is the path to txt file with boards
# ex. floor = "maps/first_floor.txt"
def read_board(floor):
    list = []
    temp_list = []
    with open(floor) as text_file:
        for line in text_file.readlines():
            for i in line:
                if i != "\n":
                    temp_list.append(i)
            list.append(temp_list)
            temp_list = []

    return list

#ITEM DICTIONARIES
items_food = {
    1: {"type": "food", "name": "an apple", "hp": 1, "function": "health point."},
    2: {"type": "food", "name": "a bread", "hp": 2, "function": "health points."},
    3: {"type": "food", "name": "a chicken leg", "hp": 3, "function": "health points."},
    4: {"type": "food", "name": "a cake", "hp": 4, "function": "health points."},
    5: {"type": "food", "name": "a sweet roll", "hp": 5, "function": "health points."},
    6: {"type": "food", "name": "a chicken", "hp": 6, "function": "health points."},
}
eq_items = {
    1: {"type": "inv", "name": "sword", "function": "attack points"},
    2: {"type": "inv", "name": "shield", "function": "deffence points"},
    3: {"type": "inv", "name": "armour", "function": "deffence points"},
    4: {"type": "inv", "name": "key", "function": "possibilities", "open": 1},
    5: {"type": "inv", "name": "helmet", "function": "total healt points"},
    6: {"type": "inv", "name": "artifact", "function": "deffence", "att": 20},
}


boss = {"type": "boss", "hp": 200, "attack": 30, "deffence": 25, "feature": "invincible"}



#LISTS TO RANDOM CHOICE
item_list = [eq_items]
artifact_ability_list = ["attack points", "deffence points"]


def find_empty_space(floor):
    free_spots = []
    for x, i in enumerate(floor):
        for y, j in enumerate(i):
            if j == ".":
                temp = x, y
                free_spots.append(temp)

    return free_spots


def place_items(floor):
    list_of_coordinates = find_empty_space(floor)
    selected_coordinates = []
    for i in range(20):
        x = random.choice(list_of_coordinates)
        selected_coordinates.append(x)
    count = 0
    for i in selected_coordinates:
        if count <= 10:
            floor[i[0]][i[1]] = "X"
        else:
            floor[i[0]][i[1]] = "M"
        count += 1

def place_boss(floor_3):
    '''
    Placing "B" letters on floor_3 immitating boss .

    Args:
    floor_3

    '''
    count_x = -2
    count_y = -2
    x, y = 26, 33
    for i in range(5):
        for j in range(5):
            if x + count_x in range(-1, BOARD_HEIGHT) and y + count_y in range(-1, BOARD_WIDTH):
                floor_3[x + count_x][y + count_y] = "B"
                count_y += 1
        count_x += 1
        count_y = -2


def get_boss_coordinates(floor_3):
    '''
    Getting list with coordinates which ale places where letter "B" is standing on floor_3
    Args:
    floor_3

    Returns:
    list: boss_coordinates
    '''
    boss_coordinates = []
    for x, i in enumerate(floor_3):
        for y, j in enumerate(i):
            if j == "B":
                temp = x, y
                boss_coordinates.append(temp)

    return boss_coordinates

# wywolane 1 raz w main na początku gry, ustawia przedmioty na 3 poziomach
def prepare_floors():
    floor_1 = read_board("maps/test_floor.txt")
    floor_2 = read_board("maps/test_floor2.txt")
    floor_3 = read_board("maps/test_floor3.txt")
    place_items(floor_1)
    place_items(floor_2)
    place_items(floor_3)
    place_boss(floor_3)
    return floor_1, floor_2, floor_3

"""
parameters: floors
potwory poruszaja sie po mapie nawet ktorej nie widac
return: floors
"""


def monsters_movement(floors):
    '''
    Creates a new game board based on input parameters.

    Args:
    int: The width of the board
    int: The height of the board

    Returns:
    list: Game board
    '''
    monsters_xy_list = check_monster_position(floors)
    directions = ["w", "s", "a", "d"]
    for i in monsters_xy_list:
        random_direction = random.choice(directions)
        x, y = i
        if random_direction == "w":
            if (x - 1) not in range(1, 35) or (floors[floor])[x - 1][y] == "#" or (floors[floor])[x - 1][y] == "X" or (floors[floor])[x - 1][y] == " " or (floors[floor])[x - 1][y] == "B" or (floors[floor])[x - 1][y] == "$":
                continue
            else:
                (floors[floor])[x - 1][y] = "M"
                (floors[floor])[x][y] = "."
        elif random_direction == "s":
            if (x + 1) not in range(1, 35) or (floors[floor])[x + 1][y] == "#" or (floors[floor])[x + 1][y] == "X" or (floors[floor])[x + 1][y] == " " or (floors[floor])[x + 1][y] == "B" or (floors[floor])[x + 1][y] == "$":
                continue
            else:
                (floors[floor])[x + 1][y] = "M"
                (floors[floor])[x][y] = "."
        elif random_direction == "a":
            if (y - 1) not in range(1, 63) or (floors[floor])[x][y - 1] == "#" or (floors[floor])[x][y - 1] == "X" or (floors[floor])[x][y - 1] == " " or (floors[floor])[x][y - 1] == "B" or (floors[floor])[x][y - 1] == "$":
                continue
            else:
                (floors[floor])[x][y - 1] = "M"
                (floors[floor])[x][y] = "."
        elif random_direction == "d":
            if (y + 1) not in range(1, 63) or (floors[floor])[x][y + 1] == "#" or (floors[floor])[x][y + 1] == "X" or (floors[floor])[x][y + 1] == " " or (floors[floor])[x][y + 1] == "B" or (floors[floor])[x][y + 1] == "$":
                continue
            else:
                (floors[floor])[x][y + 1] = "M"
                (floors[floor])[x][y] = "."
    return floors


def boss_movement(floors, board):
    '''
    Randomly choosing coordinates for making random boss movement, overwrite floor_3

    Args:
    floors -> floor_3

    Returns:
    floors
    '''
    boss_xy_list = get_boss_coordinates(floors[2])
    directions = ["w", "s", "a", "d"]
    random_direction = random.choice(directions)
    if random_direction == "w":
        if player_in_boss_range(floors, board, random_direction) == True:
            for index, value in enumerate(boss_xy_list):
                if index >= 20:
                    x, y = value
                    if not (x - 5) in range(1, 35) or (floors[2])[x - 5][y] == "#" or (floors[2])[x - 5][y] == " " or (floors[2])[x - 5][y] == "$":
                        continue
                    (floors[2])[x][y] = "."
                    (floors[2])[x - 5][y] = "B"
    elif random_direction == "s":
        if player_in_boss_range(floors, board, random_direction) == True:
            for index, value in enumerate(boss_xy_list):
                if index <= 4:
                    x, y = value
                    if not (x + 5) in range(1, 35) or (floors[2])[x + 5][y] == "#" or (floors[2])[x + 5][y] == " " or (floors[2])[x + 5][y] == "$":
                        continue
                    (floors[2])[x][y] = "."
                    (floors[2])[x + 5][y] = "B"
    elif random_direction == "a":
        if player_in_boss_range(floors, board, random_direction) == True:
            for index, value in enumerate(boss_xy_list):
                if index == 4 or index == 9 or index == 14 or index == 19 or index == 24:
                    x, y = value
                    if not (y - 5) in range(1, 64) or (floors[2])[x][y - 5] == "#" or (floors[2])[x][y - 5] == " " or (floors[2])[x][y - 5] == "$":
                        continue
                    (floors[2])[x][y] = "."
                    (floors[2])[x][y - 5] = "B"
    elif random_direction == "d":
        if player_in_boss_range(floors, board, random_direction) == True:
            for index, value in enumerate(boss_xy_list):
                if index == 0 or index == 5 or index == 10 or index == 15 or index == 20:
                    x, y = value
                    if not (y - 5) in range(1, 64) or (floors[2])[x][y + 5] == "#" or (floors[2])[x][y + 5] == " " or (floors[2])[x][y + 5] == "$":
                        continue
                    (floors[2])[x][y] = "."
                    (floors[2])[x][y + 5] = "B"
    return floors

# def player_in_range(floors, board):
#     boss_xy_list = get_boss_coordinates(floors[2])
#     for i in boss_xy_list:
#         x, y = i
#         if board[x - 1][y] == "@":
#             return False
#         if board[x + 1][y] == "@":
#             return False
#         if board[x][y - 1] == "@":
#             return False
#         if board[x][y + 1] == "@":
#             return False

def player_in_boss_range(floors, board, direction):
    boss_xy_list = get_boss_coordinates(floors[2])
    if direction == "w":
        for index, value in enumerate(boss_xy_list):
            if index >= 20:
                x, y = value
                if board[x - 5][y] == "@":
                    return False
        return True
    elif direction == "s":
        for index, value in enumerate(boss_xy_list):
            if index <= 4:
                x, y = value
                if board[x + 5][y] == "@":
                    return False
        return True
    elif direction == "a":
        for index, value in enumerate(boss_xy_list):
            if index == 4 or index == 9 or index == 14 or index == 19 or index == 24:
                x, y = value
                if board[x][y - 5] == "@":
                    return False
        return True
    elif direction == "d":
        for index, value in enumerate(boss_xy_list):
            if index == 0 or index == 5 or index == 10 or index == 15 or index == 20:
                x, y = value
                if board[x][y + 5] == "@":
                    return False
        return True

def contact_with_boss(key,board, player_x, player_y):
    if key == "w":
        if board[player_x - 1][player_y] == "B":
            fight_with_boss()
            return True
        return False
    elif key == "s":
        if board[player_x + 1][player_y] == "B":
            fight_with_boss()
            return True
        return False
    elif key == "a":
        if board[player_x][player_y - 1] == "B":
            fight_with_boss()
            return True
        return False
    elif key == "d":
        if board[player_x][player_y + 1] == "B":
            fight_with_boss()
            return True

        return False

def fight_with_boss():
    boss["hp"] -= main.attack
    main.health -= boss["attack"]
    if main.health >= boss["attack"]:
        ui.display_message(
            f"You have been attacked by {boss['feature']} {boss['type']}! \nThe {boss['type']} attacked you with {boss['attack']} attack points.")
        time.sleep(2)
        ui.display_message(
            f"You have left {main.health} health points.")
        time.sleep(2)

    elif 0 < main.health <= boss['attack']:
        ui.display_message(
            f"The {boss['type']} attacked you with {boss['attack']} attack points, now you have {main.health} health points.")
        main.health = 0
    elif main.health == 0:
        ui.display_message(
            f"The {boss['type']} attacked you with {boss['attack']} attack points, now you have {main.health} health points.")
        time.sleep(2)
        ui.display_message(
            f"You were defeated by the {boss['feature']} {boss['type']} :(.")
        time.sleep(1)
        quit()
        # dodać tutaj wywołanie funkcji która będzie nam pytać czy grasz dalej czy nie
        quit()
        # elif boss["hp"] <= 0:
        #     ui.display_message(f"The {boss['feature']} {boss['type']} has been defeated! You have won the game!")
        #     time.sleep(1)
"""
parameters: floors
zbiera liste koordynatow potworow
return: lista koordynatow potworow
"""
def check_monster_position(floors):
    monsters_xy_list = []
    for x, i in enumerate(floors[floor]):
        for y, j in enumerate(i):
            if j == "M":
                temp = x, y
                monsters_xy_list.append(temp)
    return monsters_xy_list

#Monsters dictionaries
monsters_list = {
    1: {"type": "monster", "name": "rat", "activity": "fight", "hp": 20},
    2: {"type": "monster", "name": "skeleton", "activity": "fight", "hp": 25},
    3: {"type": "monster", "name": "archer", "activity": "fight", "hp": 30},
    4: {"type": "monster", "name": "warrior", "activity": "fight", "hp": 35},
}

def monster_choose():
    """ chooses random monster from the provided dictionary """
    monster = random.choice(list(monsters_list))
    return monster

def monster_attack(monster):
    monster = monster_choose()
    """ implement hit and miss for each monster depending on their attack strength
        returns hit and attack points
     """
    # att_strength = random.randrange(0, 24)
    attack = random.randrange(0, 5)
    if attack == 0:
        hit = "missed"
        print(f"Your opponent {hit}. Your hp level didn't change")
    if monsters_list[monster]["name"] == "rat":
        x = monsters_list[monster]["name"]
        attack = random.randrange(1, 4)
        main.health -= attack
        print(f"You got bitten by a {x}. Your hp is lowered by {attack} points.")
    if monsters_list[monster]["name"] == "skeleton":
        x = monsters_list[monster]["name"]
        attack = random.randrange(5, 8)
        main.health -= attack
        print(f"You got scratched by a {x}. Your hp is lowered by {attack} points.")
    if monsters_list[monster]["name"] == "archer":
        x = monsters_list[monster]["name"]
        attack = random.randrange(9, 12)
        main.health -= attack
        print(f"You got shot by a {x}. Your hp is lowered by {attack} points.")
    if monsters_list[monster]["name"] == "warrior":
        x = monsters_list[monster]["name"]
        attack = random.randrange(13, 15)
        main.health -= attack
        print(f"You got hit by a {x}. Your hp is lowered by {attack} points.")


monster_attack(monster=True)

def player_attack_monster(player_x, player_y, key, board, floors):
    if key == "w":
        if board[player_x - 1][player_y] == "M":
            (floors[floor])[player_x - 1][player_y] = "D"
            print("dupa")
    elif key == "s":
        if board[player_x + 1][player_y] == "M":
            (floors[floor])[player_x + 1][player_y] = "D"
            print("dupa")
    elif key == "a":
        if board[player_x][player_y - 1] == "M":
            (floors[floor])[player_x][player_y - 1] = "D"
            print("dupa")
    elif key == "d":
        if board[player_x][player_y + 1] == "M":
            (floors[floor])[player_x][player_y + 1] = "D"
            print("dupa")

"""
parameters: key
modyfikuje statystyki i zmienia zmiennia globalna icanseeyou
no return
"""
def cheats_module(key):
    global icanseeyou
    if key == "h":
        user_input = input(">")
        if user_input == "spameggs":
            main.health += 10
            main.attack += 10
            main.armour += 10
            main.total_health += 10
        if user_input == "icanseeyou" and icanseeyou == 0:
            icanseeyou = 1
        elif user_input == "icanseeyou" and icanseeyou == 1:
            icanseeyou = 0


