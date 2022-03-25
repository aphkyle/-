from pathlib import Path

import arcade
import arcade.gui

import pyglet
import pyglet.clock

from constants import *
from sort_sprite import SortName
from message_box import UIMessageBox

UP = (arcade.key.UP, arcade.key.W)
LEFT = (arcade.key.LEFT, arcade.key.A)
DOWN = (arcade.key.DOWN, arcade.key.S)
RIGHT = (arcade.key.RIGHT, arcade.key.D)

ASSETS = Path("assets")
if not ASSETS.exists():
    ASSETS = Path("..") / "assets"
INDOOR = ASSETS / "indoor"
RANDOM = ASSETS / "random"


class Game(arcade.View):
    def on_show(self):
        self.setup()

    def setup(self):
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        map_name = INDOOR / "map1.json"
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.player_sprite = arcade.Sprite(RANDOM / "player.png", CHARACTER_SCALING)
        self.player_sprite.center_x = 256
        self.player_sprite.center_y = 700
        self.circle = arcade.SpriteCircle(128, (244, 119, 125))
        self.circle.center_x = 256
        self.circle.center_y = 700
        self.scene.add_sprite("circle", self.circle)
        self.scene.add_sprite("player", self.player_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            [
                self.scene["doors"],
                self.scene["stealable_top"],
                self.scene["stealable_base"],
                self.scene["walls"],
            ],
        )

        self.success = None
        self.last_sprite = None
        self.message_box = None
        self.time = 0
        self.money = 0
        self.textarea = None

    def on_key_press(self, key, modifiers):
        if key in UP:
            self.player_sprite.change_y = 5
        if key in LEFT:
            self.player_sprite.change_x = -5
        if key in DOWN:
            self.player_sprite.change_y = -5
        if key in RIGHT:
            self.player_sprite.change_x = 5
        # ST = arcade.get_closest_sprite(self.player_sprite, self.scene["stealable_top"])
        # SB = arcade.get_closest_sprite(self.player_sprite, self.scene["stealable_base"])
        # if self.success_type == "ST":
        #     if ST[1] > 128 or ST[0] != self.success:
        #         self.time = 0
        #         self.success = False
        # elif self.success_type == "SB":
        #     if SB[1] > 128 or SB[0] != self.success:
        #         self.time = 0
        #         self.success = False
        #         pyglet.clock.unschedule(self.on_message_box_close)

    def on_key_release(self, key, modifiers):
        if key in (*LEFT, *RIGHT):  # basically LEFT or RIGHT
            self.player_sprite.change_x = 0
        elif key in (*UP, *DOWN):  # ^^ same as the comment above but it's up and downs
            self.player_sprite.change_y = 0

    def center_camera_to_player(self):
        # https://api.arcade.academy/en/latest/examples/platform_tutorial/step_09.html
        self.circle.position = self.player_sprite.position
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_draw(self):
        self.clear()

        self.camera.use()
        self.scene["carpets"].draw(pixelated=True)
        self.scene["circle"].draw(pixelated=True)
        self.scene["walls"].draw(pixelated=True)
        self.scene["doors"].draw(pixelated=True)
        self.scene["stealable_base"].draw(pixelated=True)
        self.scene["stealable_top"].draw(pixelated=True)
        self.scene["player"].draw(pixelated=True)  # ordering = zindex :sunglassses:

        self.manager.draw()

    def on_update(self, delta_time):
        # `ST` in short of 'stealable_top'
        # `SB` in short of 'stealable_base'
        self.ST_sprite, self.ST_distance = arcade.get_closest_sprite(
            self.player_sprite, self.scene["stealable_top"]
        )
        self.SB_sprite, self.SB_distance = arcade.get_closest_sprite(
            self.player_sprite, self.scene["stealable_base"]
        )
        if self.SB_distance < 128:
            self.success_type = "SB"
            self.success = self.SB_sprite
        if self.ST_distance < 128:
            self.success_type = "ST"
            self.success = self.ST_sprite

        if self.success and self.time <= 0:
            self.info = SortName(self.success.texture.name).get_sprite_info()
            if self.success != self.last_sprite:
                if self.message_box:
                    self.manager.remove(self.message_box)
                self.message_box = UIMessageBox(
                    width=500,
                    height=200,
                    sprite=arcade.Sprite(texture=self.success.texture),
                    message_text=f"{self.info['name']}\nVALUE:{self.info['price']}",
                    buttons=("STEAL",),
                    callback=self.load,
                )
                self.manager.add(self.message_box)
            self.last_sprite = self.success
        elif self.message_box:
            self.manager.remove(self.message_box)
            self.last_sprite = None
        self.physics_engine.update()
        self.center_camera_to_player()

    def on_message_box_close(self, dt):
        self.time -= 0.1
        print(self.time)
        if self.textarea:
            self.manager.remove(self.textarea)
        self.textarea = arcade.gui.UITextArea(
            width=200,
            height=50,
            font_size=36,
            text=str(self.time)[0:3],
            font_name=("Kenney Pixel"),
        )
        self.manager.add(self.textarea)
        if self.time <= 0:
            self.money += self.info["price"]
            self.success.remove_from_sprite_lists()

            pyglet.clock.unschedule(self.on_message_box_close)

    def load(self, button_text):
        # if button_text == "STEAL":
        #     self.time = self.info["grab_time"]
        #     self.t = multiprocessing.Process(target=self.on_message_box_close)
        #     self.t.daemon = True
        #     self.t.run()

        if button_text == "STEAL":
            self.time = self.info["grab_time"]
            pyglet.clock.schedule_interval(self.on_message_box_close, 0.1)
