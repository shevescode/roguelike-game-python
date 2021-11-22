from main import BOARD_HEIGHT, BOARD_WIDTH
import main
import random
import os
floor = 0
discovered_floor_0 = None
discovered_floor_1 = None
discovered_floor_2 = None
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
    count_x = -2
    count_y = -2
    for i in range(5):
        for j in range(5):
            if x + count_x in range(-1, BOARD_HEIGHT) and y + count_y in range(-1, BOARD_WIDTH):
                board[x + count_x][y + count_y] = floors[floor][x + count_x][y + count_y]
                count_y += 1
        count_x += 1
        count_y = -2

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


# wywolane 1 raz w main na początku gry, ustawia przedmioty na 3 poziomach
def prepare_floors():
    floor_1 = read_board("maps/test_floor.txt")
    floor_2 = read_board("maps/test_floor2.txt")
    floor_3 = read_board("maps/test_floor3.txt")
    place_items(floor_1)
    place_items(floor_2)
    place_items(floor_3)
    return floor_1, floor_2, floor_3

"""
parameters: floors
potwory poruszaja sie po mapie nawet ktorej nie widac
return: floors
"""
def monsters_movement(floors):
    monsters_xy_list = check_monster_position(floors)
    directions = ["w", "s", "a", "d"]
    for i in monsters_xy_list:
        random_direction = random.choice(directions)
        x, y = i
        if random_direction == "w":
            if (floors[floor])[x - 1][y] == "#" or (floors[floor])[x - 1][y] == "X" or (floors[floor])[x - 1][y] == " ":
                continue
            else:
                (floors[floor])[x - 1][y] = "M"
                (floors[floor])[x][y] = "."
        elif random_direction == "s":
            if (floors[floor])[x + 1][y] == "#" or (floors[floor])[x + 1][y] == "X" or (floors[floor])[x + 1][y] == " ":
                continue
            else:
                (floors[floor])[x + 1][y] = "M"
                (floors[floor])[x][y] = "."
        elif random_direction == "a":
            if (floors[floor])[x][y - 1] == "#" or (floors[floor])[x][y - 1] == "X" or (floors[floor])[x][y - 1] == " ":
                continue
            else:
                (floors[floor])[x][y - 1] = "M"
                (floors[floor])[x][y] = "."
        elif random_direction == "d":
            if (floors[floor])[x][y + 1] == "#" or (floors[floor])[x][y + 1] == "X" or (floors[floor])[x][y + 1] == " ":
                continue
            else:
                (floors[floor])[x][y + 1] = "M"
                (floors[floor])[x][y] = "."
    return floors

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