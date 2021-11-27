from main import BOARD_HEIGHT, BOARD_WIDTH
import main
import random
import os
import ui
import time
import util
floor = 0
discovered_floor_0 = None
discovered_floor_1 = None
discovered_floor_2 = None
icanseeyou = 0
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
    player_attack_monster(player_x, player_y, key, board, floors)
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
        util.health += items_food[item]['hp']

    if select_dict == eq_items:
        if eq_items[item]['name'] != "key" and eq_items[item]['name'] != "artifact":
            print(
                f"You found {adjective}{eq_items[item]['name']}. It's increasing {eq_items[item]['function']} by {number}. It was added to your inventory.")
            main.inventory.append(
                f"{adjective}{eq_items[item]['name']} - {eq_items[item]['function']} + {number}.")
#FIXME: zapisać printy do UI
            if eq_items[item]['name'] == "sword":
                util.attack += number
            if eq_items[item]['name'] == "shield":
                util.armour += number
            if eq_items[item]['name'] == "armour":
                util.armour += number
            if eq_items[item]['name'] == "helmet":
                util.total_health += number
        elif eq_items[item]['name'] == "artifact":
            print(
                f"You found {eq_items[item]['name']}. It's increasing {ability} by {number}. It was added to your inventory.")
            if ability == "defence points":
                util.armour += number
                main.inventory.append(f"The fucking horn of defence + {number}")
            else:
                util.attack += number
                main.inventory.append(
                    f"The fucking horn of attack + {number}")
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

'''
Items on board dictionaries: eq_items, items_food, boos
'''
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
    2: {"type": "inv", "name": "shield", "function": "defence points"},
    3: {"type": "inv", "name": "armour", "function": "defence points"},
    4: {"type": "inv", "name": "key", "function": "possibilities", "open": 1},
    5: {"type": "inv", "name": "helmet", "function": "total healt points"},
    6: {"type": "inv", "name": "artifact", "function": "defence", "att": 20},
}

boss = {"type": "boss", "hp": 200, "attack": 30, "defence": 30, "feature": "invincible"}



'''List for random choice the item on map/ list for random choice the artifact feature'''
item_list = [eq_items, items_food]
artifact_ability_list = ["attack points", "defence points"]


def find_empty_space(floor):
    free_spots = []
    for x, i in enumerate(floor):
        for y, j in enumerate(i):
            if j == ".":
                temp = x, y
                free_spots.append(temp)

    return free_spots


def place_items(floor):
    '''
    Placing items "X"/moobs "M" on the board'''
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
    '''
    parameters: key, board, player_x, player_y
    Checking if boss is opposite to us, if yes -> invoke fight_with_boss()
    return: Boolean value
    '''
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


def play_again():
    global floor
    '''
    parameter: -
    Asking player for playing again or quit.
    returns: -
    '''
    ui.display_message("""Would you like to play again?

    1. Yes

    2. No
    """)
    while True:
        again = input().strip()
        if again == "":
            continue
        if again == "1":
            floor = 0
            main.main()
        if again == "2":
            ui.display_message(f"\nGoodbye! See you next time!\n")
            quit()
        else:
            print("\nInvalid input! Try again!\n")
            continue


def fight_with_boss():
    """
    parameters: -
    Function displays to user actuall stats during fighting with BOSS, ending the game when player or boss have 0 hp.
    return: -
    """
    boss["hp"] -= util.attack
    util.health -= boss["attack"]
    if util.health >= boss["attack"] and boss["hp"] > 0:
        ui.display_message(f"""You have been attacked by {boss['feature']} {boss['type']}!
The {boss['type']} attacked you with {boss['attack']} attack points.
You have left {util.health} health points.""")
        time.sleep(2)

    elif 0 < util.health <= boss['attack'] and boss["hp"] > 0:
        ui.display_message(f"""You have been attacked by {boss['feature']} {boss['type']}!
The {boss['type']} attacked you with {boss['attack']} attack points.
You have left {util.health} health points.""")
        time.sleep(2)

    elif util.health <= 0:
        util.health = 0
        ui.display_message(f"""You have been attacked by {boss['feature']} {boss['type']}!
The {boss['type']} attacked you with {boss['attack']} attack points. \nYou have left {util.health} health points.
You were defeated by the {boss['feature']} {boss['type']} :(.""")
        time.sleep(2)
        print()
        play_again()

    elif boss['hp'] <= 0:
        boss['hp'] = 0
        ui.display_message(f"The {boss['feature']} {boss['type']} was defeated! You have won the game. \nCongratulations! :)")
        time.sleep(2)
        print()
        play_again()

def check_monster_position(floors):
    """
    parameters: floors
    zbiera liste koordynatow potworow
    return: lista koordynatow potworow
    """
    monsters_xy_list = []
    for x, i in enumerate(floors[floor]):
        for y, j in enumerate(i):
            if j == "M":
                temp = x, y
                monsters_xy_list.append(temp)
    return monsters_xy_list

#Monsters dictionaries
monsters_list = {
    1: {"type": "monster", "name": "rat", "activity": "fight", "hp": 50},
    2: {"type": "monster", "name": "skeleton", "activity": "fight", "hp": 55},
    3: {"type": "monster", "name": "archer", "activity": "fight", "hp": 60},
    4: {"type": "monster", "name": "warrior", "activity": "fight", "hp": 60},
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
    attack = random.randrange(0, 5)
    if attack == 0:
        hit = "missed"
        print(f"Your opponent {hit}. Your hp level didn't change")
    if monsters_list[monster]["name"] == "rat":
        rat_hp = monsters_list[monster]["hp"]
        while  util.health > 0:
            util.health -= attack
            attack = random.randrange(1, 4)
            print(f"HEALTH: {util.health}/{util.total_health}")
            print(f"You got bitten by a {monsters_list[monster]['name']}. Your hp is lowered by {attack} points.\n Monsters hp got lowered by {util.attack}. Monster hp is {rat_hp}")
            rat_hp -= util.attack
            time.sleep(3)
            if util.health <= 0:
                print(f"\nYou died. You are noob.\n")
                play_again()
            if rat_hp <= 0:
                print(f"\nYou won the fight!\n")
                time.sleep(3)
                break
    if monsters_list[monster]["name"] == "skeleton":
        skeleton_hp = monsters_list[monster]["hp"]
        while util.health > 0:
            util.health -= attack
            attack = random.randrange(5, 8)
            print(f"HEALTH: {util.health}/{util.total_health}")
            print(f"You got scratched by a {monsters_list[monster]['name']}. Your hp is lowered by {attack} points.\n Monsters hp got lowered by {util.attack}. Monster hp is {skeleton_hp}")
            skeleton_hp -= util.attack
            time.sleep(3)
            if util.health <= 0:
                print(f"\nYou died. You are noob.\n")
                play_again()
            if skeleton_hp <= 0:
                print(f"\nYou won the fight!\n")
                time.sleep(3)
                break
    if monsters_list[monster]["name"] == "archer":
        archer_hp = monsters_list[monster]["hp"]
        while util.health > 0:
            util.health -= attack
            attack = random.randrange(9, 12)
            print(f"HEALTH: {util.health}/{util.total_health}")
            print(f"You got shot by a {monsters_list[monster]['name']}. Your hp is lowered by {attack} points.\n Monsters hp got lowered by {util.attack}. Monster hp is {archer_hp}")
            archer_hp -= util.attack
            time.sleep(3)
            if util.health <= 0:
                print(f"\nYou died. You are noob.\n")
                play_again()
            if archer_hp <= 0:
                print(f"\nYou won the fight!\n")
                time.sleep(3)
                break

    if monsters_list[monster]["name"] == "warrior":
        warrior_hp = monsters_list[monster]["hp"]
        while util.health > 0:
            util.health -= attack
            attack = random.randrange(13, 15)
            print(f"HEALTH: {util.health}/{util.total_health}")
            print(f"You got hit by a {monsters_list[monster]['name']}. Your hp is lowered by {attack} points.\n Monsters hp got lowered by {util.attack}. Monster hp is {warrior_hp}")
            warrior_hp -= util.attack
            time.sleep(3)
            if util.health <= 0:
                print(f"\nYou died. You are noob.\n")
                play_again()
            if warrior_hp <= 0:
                print(f"\nYou won the fight!\n")
                time.sleep(3)
                break


def player_attack_monster(player_x, player_y, key, board, floors):
    if key == "w":
        if board[player_x - 1][player_y] == "M":
            monster_attack(monster=True)
            (floors[floor])[player_x - 1][player_y] = "D"
    elif key == "s":
        if board[player_x + 1][player_y] == "M":
            monster_attack(monster=True)
            (floors[floor])[player_x + 1][player_y] = "D"
    elif key == "a":
        if board[player_x][player_y - 1] == "M":
            monster_attack(monster=True)
            (floors[floor])[player_x][player_y - 1] = "D"
    elif key == "d":
        if board[player_x][player_y + 1] == "M":
            monster_attack(monster=True)
            (floors[floor])[player_x][player_y + 1] = "D"


def cheats_module(key):
    """
    parameters: key
    modyfikuje statystyki i zmienia zmiennia globalna icanseeyou
    no return
    """
    global icanseeyou
    if key == "h":
        user_input = input(">")
        if user_input == "spameggs":
            util.health += 10
            util.attack += 10
            util.armour += 10
            util.total_health += 10
        if user_input == "icanseeyou" and icanseeyou == 0:
            icanseeyou = 1
        elif user_input == "icanseeyou" and icanseeyou == 1:
            icanseeyou = 0


user_race = {
    1: {"name": "Elf", "hp": 80, "armor": 8, "attack": 12, "ability": None},
    2: {"name": "Human", "hp": 100, "armor": 10, "attack": 10, "ability": None},
    3: {"name": "Dwarf", "hp": 120, "armor": 12, "attack": 8, "ability": None},
    4: {"name": "Orc", "hp": 120, "armor": 12, "attack": 12, "ability": "low_drop"},
    5: {"name": "Rouge", "hp": 80, "armor": 12, "attack": 8, "ability": "keys"},
    6: {"name": "Pumpkin", "hp": 10, "armor": 5, "attack": 20, "ability": "high_vis"},
    7: {"name": "Own", "hp": "?", "armor": "?", "attack": "?", "ability": None}
    }

def implement_user_choosen_race_option(user_input):
    """
    This function connects user input with dictionary user_race and returns its chosen element.
    """
    if user_input in range(4):
        if user_input == 1:
            return user_race[1]
        if user_input == 2:
            return user_race[2]
        if user_input == 3:
            return user_race[3]
    else:
        return False

