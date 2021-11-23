# import engine

# board = engine.create_board(30,20)
import os
import main

def display_board(board, inv):
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
        if len(main.inventory) > index and inv == 1:
            print(main.inventory[index])
        else:
            print()


# def display_inventory(key):
#     '''
#     Displays inventory on the screen

#     Returns:
#     Nothing
#     '''
#     if key == "i":
#         print("\nYour inventory: ")
#         if len(main.inventory) == 0:
#             print("Your inventory is empty.")
#         else:
#             for equipment in main.inventory:
#                 print(equipment)

#     print()
#     os.system("pause")


def display_stats():
    print(f"HEALTH: {main.health}/{main.total_health} ATTACK: {main.attack} ARMOUR: {main.armour}")

def display_message(message):
    print(message)

def get_user_input(message):
    user_input = input(message)
    return user_input
