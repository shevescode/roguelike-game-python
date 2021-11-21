import util
import engine
import ui

PLAYER_ICON = '@'
PLAYER_START_X = 23
PLAYER_START_Y = 5
attack = 10
armor = 10
health = 100
total_health = 150
inventory = ["Your Inventory: "]

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
    board = engine.create_board(BOARD_WIDTH, BOARD_HEIGHT)
    # floor_1 = engine.read_board("maps/test_floor.txt")
    # engine.place_items(floor_1)
    util.clear_screen()
    floor_0, floor_1, floor_2 = engine.prepare_floors()
    floors = floor_0, floor_1, floor_2
    is_running = True
    while is_running:
        engine.put_player_on_board(board, player, floors)
        ui.display_board(board)
        ui.display_stats()
        key = util.key_pressed()
        if key == 'q':
            is_running = False
        else:
            board = engine.player_movement(key, board, floors)
        util.clear_screen()


if __name__ == '__main__':
    main()
