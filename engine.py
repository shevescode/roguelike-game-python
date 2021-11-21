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


    count_x = -2
    count_y = -2
    for i in range(5):
        for j in range(5):
            if x + count_x in range(BOARD_HEIGHT) and y + count_y in range(BOARD_WIDTH):
                board[x + count_x][y + count_y] = floors[floor][x + count_x][y + count_y]
                count_y += 1
        count_x += 1
        count_y = -2

    board[x][y] = player["icon"]


# def change_floor():

#     if floor == 0:
#         return "maps/test_floor.txt"
#     if floor == 1:
#         return "maps/second_floor.txt"
#     if floor == 2:
#         return "maps/third_floor.txt"
#     if floor == 3:
#         return "maps/fourth_floor.txt"
#     if floor == 4:
#         return "maps/fifth_floor.txt"


# and x + count_x <= BOARD_HEIGHT and  and y +count_y <= BOARD_WIDTH

def check_player_position(board):
    player_x, player_y = -1, -1
    for x, i in enumerate(board):
        for y, j in enumerate(i):
            if j == "@":
                player_x = x
                player_y = y
    return player_x, player_y

# zapisac board po zmianie na nastepny floor i przywrocic go przy powrocie
def player_movement(key, board, floors):
    global floor
    global discovered_floor_0
    global discovered_floor_1
    global discovered_floor_2
    player_x, player_y = check_player_position(board)
# przechodzenie pomiedzy floorami
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

    # if floor == 0 and board[2][29] == "@":
    #     floor = 1
    #     board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    #     board[2][0] = "@"
    #     board[2][29] == "#"
    #     return board
    # if floor == 1 and board[19][14] == "@":
    #     floor = 2
    #     board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    #     board[0][14] = "@"
    #     board[19][14] == "#"
    #     return board
    # if floor == 2 and board[19][22] == "@":
    #     floor = 3
    #     board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    #     board[0][22] = "@"
    #     board[19][22] == "#"
    #     return board
    # if floor == 3 and board[19][1] == "@":
    #     floor = 4
    #     board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    #     board[0][1] = "@"
    #     board[19][1] == "#"
    #     return board
    # if floor == 4 and board[19][14] == "@":
    #     floor = 5
    #     board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    #     board[0][14] = "@"
    #     board[19][14] == "#"
    #     return board

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
    number = random.randint(0, 10)
    hp_number = random.randint(0, 100)
    adjective = ""
    if number <= 3:
        adjective = "chujowy "
    elif number <= 6:
        adjective = "normalny "
    elif number <= 9:
        adjective = "zajebisty "
    elif number >= 10:
        adjective = "magic "
    if select_dict == items_food:
        print(f"You found {items_food[item]['name']}. It recovers you {items_food[item]['hp']} health.")
        main.health += items_food[item]['hp']
    if select_dict == items_att:
        print(f"You found {adjective}{items_att[item]['name']}. It has {number} attack. It was added to your inventory.")
        main.inventory.append(f"{items_att[item]['name']} - attack + {number}.")
        main.attack += number
    if select_dict == items_deff:
        print(f"You found {adjective}{items_deff[item]['name']}. It has {number} armor. It was added to your inventory.")
        main.inventory.append(f"{items_deff[item]['name']} - armor + {number}.")
        main.armor += number
    if select_dict == items_spc:
        if items_spc[item]['name'] == "helmet":
            print(f"You found a helmet. It increase your total health by {hp_number}. It was added to your inventory.")
            main.inventory.append(f"Helmet - total health + {hp_number}.")
            main.total_health += hp_number
        if items_spc[item]['name'] == "key":
            print("You found a key! It was added to your inventory.")
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


items_food = {
    1: {"type": "food", "name": "an apple", "hp": 1},
    2: {"type": "food", "name": "a bread", "hp": 2},
    3: {"type": "food", "name": "a chicken leg", "hp": 3},
    4: {"type": "food", "name": "a cake", "hp": 4},
    5: {"type": "food", "name": "a sweet roll", "hp": 5},
    6: {"type": "food", "name": "a chicken", "hp": 6},
}

# items_food[1]['type'] - znika/pojawia sie z mapy, nie idzie do inventory
# items_food[1]['hp'] - znika/pojawia sie z mapy, zmienia staty gracza
# items_food[1]['name'] - informacja dla gracza, co podniosl

items_att = {
    1: {"type": "inv", "name": "sword"},
    6: {"type": "inv", "name": "artifact", "att": 20},
}
items_deff = {
    2: {"type": "inv", "name": "shield"},
    3: {"type": "inv", "name": "armor"},
}
items_spc = {
    4: {"type": "inv", "name": "key", "open": 1},
    5: {"type": "inv", "name": "helmet"},
}


# NASZA LISTA SLOWNIKOW
item_list = [items_food, items_att, items_deff, items_spc]


# items_eq[1]['type'] - znika/pojawia sie z mapy, idzie do inventory
# items_eq[1]['att'/'def'] - znika/pojawia sie z mapy, zmienia staty gracza
# items_eq[1]['name'] - informacja dla gracza, co podniosl

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
    for i in range(10):
        x = random.choice(list_of_coordinates)
        selected_coordinates.append(x)

    for i in selected_coordinates:
        floor[i[0]][i[1]] = "X"


# wywolane 1 raz w main na początku gry, ustawia przedmioty na 3 poziomach
def prepare_floors():
    floor_1 = read_board("maps/test_floor.txt")
    floor_2 = read_board("maps/test_floor2.txt")
    floor_3 = read_board("maps/test_floor3.txt")
    place_items(floor_1)
    place_items(floor_2)
    place_items(floor_3)
    return floor_1, floor_2, floor_3

