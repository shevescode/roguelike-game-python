# import engine

# board = engine.create_board(30,20)
import os
import main
from util import clear_screen


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


def display_message(message):
    print(message)

def display_stats(health, total_health, attack, armour):
    """
    This function displays player's statistics.
    """
    print(f"HEALTH: {health}/{total_health} ATTACK: {attack} ARMOUR: {armour}")

def display_message(message):
    """
    This function displays chosen message in the terminal.
    """
    print(message)

def get_user_numeric_input(message):
    """
    This function gets and returns user numeric input or returns False if the input is not an integer.
    """
    try:
        user_input = int(input(message))
        return user_input
    except ValueError:
        return False


def personalisation_menu():
    """
    This function dispalys information about character's race option for the user
    and returns an integer connected with one of the races described in user_race dictionary.
    """
    clear_screen()
    display_message("""Before the game begins, decide who do you want to play as.

Your options are:
    1. Elf (low HP, low defence, high attack)
    2. Human (medium HP, medium defence, medium attack)
    3. Dwarf (high HP, high defence, low attack)
    """)
    return get_user_numeric_input("Enter 1, 2 or 3 to choose: ")

def get_user_name():
    """
    This function ask for and returns user name, and if left blank, sets it to 'stranger'.
    """
    clear_screen()
    display_message("Now, all significant matter has its name. What is yours?\n")
    name = input("Enter your name: ")
    if name.strip() == "":
        name = "stranger"
    return name