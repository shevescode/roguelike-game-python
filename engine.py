from main import BOARD_HEIGHT, BOARD_WIDTH
floor = 0

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

def put_player_on_board(board, player):
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

    current_floor = read_board(change_floor())

    count_x = -1
    count_y = -1
    for i in range(3):
        for j in range(3):
            if x + count_x in range(BOARD_HEIGHT) and y + count_y in range(BOARD_WIDTH):
                board[x + count_x][y + count_y] = current_floor[x + count_x][y + count_y]
                count_y += 1
        count_x += 1
        count_y = -1

    board[x][y] = player["icon"]


def change_floor():
    if floor == 0:
        return "maps/first_floor.txt"
    if floor == 1:
        return "maps/second_floor.txt"
    if floor == 2:
        return "maps/third_floor.txt"
    if floor == 3:
        return "maps/fourth_floor.txt"
    if floor == 4:
        return "maps/fifth_floor.txt"


# and x + count_x <= BOARD_HEIGHT and  and y +count_y <= BOARD_WIDTH

def check_player_position(board):
    player_x, player_y = -1, -1
    for x, i in enumerate(board):
        for y, j in enumerate(i):
            if j == "@":
                player_x = x
                player_y = y
    return player_x, player_y


def player_movement(key, board):
    global floor
    player_x, player_y = check_player_position(board)

    if floor == 0 and board[2][29] == "@":
        floor = 1
        board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
        board[2][0] = "@"
        board[2][29] == "#"
        return board
    if floor == 1 and board[19][14] == "@":
        floor = 2
        board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
        board[0][14] = "@"
        board[19][14] == "#"
        return board
    if floor == 2 and board[19][22] == "@":
        floor = 3
        board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
        board[0][22] = "@"
        board[19][22] == "#"
        return board
    if floor == 3 and board[19][1] == "@":
        floor = 4
        board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
        board[0][1] = "@"
        board[19][1] == "#"
        return board
    if floor == 4 and board[19][14] == "@":
        floor = 5
        board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
        board[0][14] = "@"
        board[19][14] == "#"
        return board

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
