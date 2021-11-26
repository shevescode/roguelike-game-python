import os
import util
import engine
import ui

PLAYER_ICON = '@'
PLAYER_START_X = 23
PLAYER_START_Y = 5
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

def user_personalisation():
    # global util.attack, armour, health
    chosen_option = engine.implement_user_choosen_race_option(ui.personalisation_menu())
    print(util.attack, util.armour, util.health)
    if chosen_option:
        util.health = chosen_option["hp"]
        util.armour = chosen_option["armor"]
        util.attack = chosen_option["attack"]
        ui.display_message(f"You have chosen playing as {chosen_option['name']}.")
        os.system('pause')
        name = ui.get_user_name()
        util.clear_screen()
        ui.display_message(f"Welcome to Rougelike, {name}! \n\nSharpen your sword and polish your armour for the game begins NOW!\n")
        print(util.attack, util.armour, util.health)
        os.system('pause')
    else:
        ui.display_message("There is no such option. Try again.")
        os.system('pause')
        user_personalisation()

def main():
    # global attack, armour, health
    user_personalisation()
    player = create_player()
    show_inventory = 0
    board = engine.create_board(BOARD_WIDTH, BOARD_HEIGHT)
    util.clear_screen()
    print(util.attack, util.armour, util.health)
    floor_0, floor_1, floor_2 = engine.prepare_floors()
    floors = floor_0, floor_1, floor_2
    is_running = True
    while is_running:
        engine.put_player_on_board(board, player, floors)
        ui.display_board(board, show_inventory)
        print(util.attack, util.armour, util.health)
        ui.display_stats(util.health, util.total_health, util.attack, util.armour)
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


if __name__ == '__main__':
    main()
