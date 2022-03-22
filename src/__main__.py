import arcade

import menu
from constants import *

if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = menu.Menu()
    window.show_view(menu_view)
    arcade.run()
