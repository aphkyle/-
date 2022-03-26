import datetime

import arcade
import arcade.gui

import menu


class End(arcade.View):
    def __init__(self, time_elapsed, money, win):
        self.time_elapsed = datetime.timedelta(seconds=round(time_elapsed))
        self.win = win
        self.money = money    
        super().__init__()
    
    def on_show(self):
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        default_style = {
            "font_name": ("Kenney Pixel", "arial"),
            "font_size": 32,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": (21, 19, 21),
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.WHITE,
            "font_color_pressed": arcade.color.BLACK,
        }

        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        game_title = arcade.gui.UITextArea(
            text="YOU WON" if self.win else "YOU LOST",
            width=900,
            height=80,
            font_size=72,
            font_name=("Kenney Pixel", "Arial"),
        )
        stats = arcade.gui.UITextArea(
            text=f"TIME USED: {self.time_elapsed}\nMONEY STOLE: {self.money} ({round(self.money/443.5, 2)}%)",
            width=900,
            height=80,
            font_size=36,
            font_name=("Kenney Pixel", "Arial"),
        )
        restart_button = arcade.gui.UIFlatButton(
            text="RESTART", width=200, style=default_style
        )

        self.v_box.add(game_title.with_space_around(left=400))
        self.v_box.add(stats.with_space_around(left=400))
        self.v_box.add(restart_button)

        @restart_button.event("on_click")
        def on_click_start(event):
            self.window.show_view(menu.Menu())
            self.v_box.clear()
            self.manager.remove(self.v_box)
            self.manager = None  

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box
            )
        )

    def on_draw(self):
        self.clear()
        self.manager.draw()
