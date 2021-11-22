import os
import util
import engine
import ui

PLAYER_ICON = '@'
PLAYER_START_X = 23
PLAYER_START_Y = 5
attack = 10
armour = 10
health = 100
total_health = 150
inventory = ["YOUR INVENTORY: "]

BOARD_WIDTH = 64
BOARD_HEIGHT = 36


def create_player():
    '''
    Creates a 'player' dictionary for storing all player related informations - i.e. player icon, player position.
    Fell free to extend this dictionary!

    Returns:
    dictionary
    '''
    player = {
        "icon": PLAYER_ICON,
        "x": PLAYER_START_X,
        "y": PLAYER_START_Y
    }

    return player

def main():
    player = create_player()
    show_inventory = 0
    board = engine.create_board(BOARD_WIDTH, BOARD_HEIGHT)
    util.clear_screen()
    floor_0, floor_1, floor_2 = engine.prepare_floors()
    floors = floor_0, floor_1, floor_2
    is_running = True
    while is_running:
        engine.put_player_on_board(board, player, floors)
        ui.display_board(board, show_inventory)
        ui.display_stats()
        key = util.key_pressed()
        if key == 'q':
            is_running = False
        elif key == "i":
            show_inventory = 1

        else:
            board = engine.player_movement(key, board, floors)
            floors = engine.monsters_movement(floors)
            show_inventory = 0
        util.clear_screen()
        print(show_inventory)


if __name__ == '__main__':
    main()
