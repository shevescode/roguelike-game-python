


def create_board(width, height):
    '''
    Creates a new game board based on input parameters.

    Args:
    int: The width of the board
    int: The height of the board

    Returns:
    list: Game board
    '''
    pass


def put_player_on_board(board, player):
    '''
    Modifies the game board by placing the player icon at its coordinates.

    Args:
    list: The game board
    dictionary: The player information containing the icon and coordinates

    Returns:
    Nothing
    '''
    pass


x = """# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
. . . . . . . . . # # # # # # # # # . . . . . . . . . . # #
# # . . . . . . . # # # # # # # # # . # # # # # # # # . # #
# # . . . . . . . # # # # . . . . . . # # # # # # # # . # #
# # . . . . . . . # # # # . . . . . . # # . . . . # . . . #
# # # # # . # # # # # # # . . . . . . # # . . . . # . . . #
# # # # # . . . . . . . . . . . . . . # # . . . . . . . . #
# # # # # # # # # # . # # # # # # # # # # . . . . # . . . #
# # # # # # # # # # . # # # # . . . # # # . . . . # . . . #
# # # # # # . . . . . . . . . . # . # # # # # . # # # # # #
# # # # # # # # # # # # # # # . . . # # # # # . # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # . # # # # # #
# # # # # # # # # # # # # # . . . . . . . . . . # # # # # #
# . . . . . . # # # # # # # . . . . . . # # # # # # # # # #
# . . . . . . # # # # # # # . . . . . . # # # # # # # # # #
# . . . . . . # # # # # # # . . . . . . # # # # # # # # # #
# . . . . . . . . . . . . . . . . . . . # # # # # # # # # #
# . . . . . . # # # # # # # # # # # # # # # # # # # # # # #
# . . . . . . # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #"""



list = []
temp_list = []
count = 0
str = ""
for i in x:
    if i != " " and i != "\n":
        temp_list.append(i)
        count += 1
        if count % 30 == 0:
            list.append(temp_list)
            temp_list = []
            count = 0

print(list)