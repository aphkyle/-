import arcade
import arcade.gui

import game


class Story(arcade.View):
    def on_show(self):
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.RED_DEVIL)


        story_text = arcade.gui.UITextArea(
            text="""\
        You, J. Doe were a twin of a rich person - J. Dope.

        They took away your life, all your money is now theirs.

        To take back your revenge,

        steal things from their house without them knowing

        Who's evil? I guess you both are.

                (Click anywhere on the window to continue)
            """,
            width=900,
            height=500,
            font_size=36,
            font_name=("Kenney Pixel", "Arial"),
        )

        self.manager.add(
            story_text
        )

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_mouse_press(self, *_):
        self.window.show_view(game.Game())
        self.manager = None  