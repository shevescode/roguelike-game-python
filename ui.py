# import engine

# board = engine.create_board(30,20)
import main


def display_board(board):
    '''
    Displays complete game board on the screen

    Returns:
    Nothing
    '''
    for index, i in enumerate(board):
        # for x in range(50):
        #     print(" ", end="")
        # moves board 50 " " to right
        for j in i:
            print(f"{j} ", end="")
        if len(main.inventory) > index:
            print(main.inventory[index])
        else:
            print()



def display_stats():
    print(f"HEALTH: {main.health}/{main.total_health} ATTACK: {main.attack} ARMOUR: {main.armour}")
