import pathlib
import webbrowser

import arcade
import arcade.gui

import game
from constants import SCREEN_TITLE


class Menu(arcade.View):
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

        red_style = {
            "font_name": ("Kenney Pixel", "arial"),
            "font_size": 32,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.REDWOOD,

            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.RED,
            "font_color_pressed": arcade.color.RED,
        }

        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        start_button = arcade.gui.UIFlatButton(text="START", width=200, style=default_style)
        quit_button = arcade.gui.UIFlatButton(text="QUIT", width=200, style=red_style)

        ui_text_label = arcade.gui.UITextArea(text=SCREEN_TITLE,
                                              width=900,
                                              height=80,
                                              font_size=72,
                                              font_name=("Kenney Pixel", "arial"))

        self.v_box.add(ui_text_label.with_space_around(bottom=0))
        self.v_box.add(start_button)
        self.v_box.add(quit_button)

        @start_button.event("on_click")
        def on_click_start(event):
            self.window.show_view(game.Game())
        @quit_button.event("on_click")
        def on_click_quit(event):
            webbrowser.open_new_tab("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            arcade.exit()

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_draw(self):
        self.clear()
        self.manager.draw()
