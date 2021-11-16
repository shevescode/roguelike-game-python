

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
            if j == 0 or j == height - 1:
                temp_list.append("#")
            elif i == 0 or i == width - 1:
                temp_list.append("#")
            else:
                temp_list.append(" ")
        board.append(temp_list)
        temp_list = []
    return board

def put_player_on_board(board, player):
    '''
    Modifies the game board by placing the player icon at its coordinates.

    Args:
    list: The game board
    dictionary: The player information containing the icon and coordinates

    Returns:
    Nothing
    '''
    x = player["x"]
    y = player["y"]


    floor = read_board("maps/first_floor.txt")

    count_x = -2
    count_y = -2
    for i in range(5):
        for j in range(5):
            board[x + count_x][y + count_y] = floor[x + count_x][y + count_y]
            count_y += 1
        count_x += 1
        count_y = -2

    board[x][y] = player["icon"]




def player_movement(key, board):
    for x, i in enumerate(board):
        for y, j in enumerate(i):
            if j == "@":
                player_x = x
                player_y = y
    
    if key == "w":
        board[player_x - 1][player_y] = "@"
    if key == "s":
        board[player_x + 1][player_y] = "@"
    if key == "a":
        board[player_x][player_y - 1] = "@"
    if key == "d":
        board[player_x][player_y + 1] = "@"




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
    1: {"type": "food", "name": "apple", "hp": 1},
    2: {"type": "food", "name": "bread", "hp": 2},
    3: {"type": "food", "name": "chicken leg", "hp": 3},
    4: {"type": "food", "name": "cake", "hp": 4},
    5: {"type": "food", "name": "sweet roll", "hp": 5},
    6: {"type": "food", "name": "chicken", "hp": 6},
}

# items_food[1]['type'] - znika/pojawia sie z mapy, nie idzie do inventory
# items_food[1]['hp'] - znika/pojawia sie z mapy, zmienia staty gracza
# items_food[1]['name'] - informacja dla gracza, co podniosl

items_eq = {
    1: {"type": "inv", "name": "sword", "att": 1},
    2: {"type": "inv", "name": "shield", "def": 2},
    3: {"type": "inv", "name": "chest armor", "def": 3},
    4: {"type": "inv", "name": "key", "open": 1/0},
    5: {"type": "inv", "name": "helmet", "hp": 1},
    6: {"type": "inv", "name": "artifact", "att": 4},
}

# items_eq[1]['type'] - znika/pojawia sie z mapy, idzie do inventory
# items_eq[1]['att'/'def'] - znika/pojawia sie z mapy, zmienia staty gracza
# items_eq[1]['name'] - informacja dla gracza, co podniosl