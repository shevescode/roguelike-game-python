# import engine

# board = engine.create_board(30,20)
import main


def display_board(board):
    '''
    Displays complete game board on the screen

    Returns:
    Nothing
    '''
    for i in board:
        # for x in range(50):
        #     print(" ", end="")
        # moves board 50 " " to right
        for j in i:
            print(f"{j} ", end="")
        print()



def display_stats():
    pass

def display_inventory():
    pass