import util
import engine
import ui

PLAYER_ICON = '@'
PLAYER_START_X = 1
PLAYER_START_Y = 1

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
    floor_1 = engine.read_board("maps/test_floor.txt")
    engine.place_items(floor_1)
    util.clear_screen()
    is_running = True
    print(floor_1)
    while is_running:
        engine.put_player_on_board(board, player, floor_1)
        ui.display_board(board)

        key = util.key_pressed()
        if key == 'q':
            is_running = False
        else:
            board = engine.player_movement(key, board)
        util.clear_screen()


if __name__ == '__main__':
    main()
