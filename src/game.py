import random
import time

import arcade
import arcade.gui

import pyglet
import pyglet.clock

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SCALING, CHARACTER_SCALING, ASSETS
from misc import pop, check, check_lose
from end import End

UP = (arcade.key.UP, arcade.key.W)
LEFT = (arcade.key.LEFT, arcade.key.A)
DOWN = (arcade.key.DOWN, arcade.key.S)
RIGHT = (arcade.key.RIGHT, arcade.key.D)

INDOOR = ASSETS / "indoor"
RANDOM = ASSETS / "random"
SFX = ASSETS / "sfx"
background = arcade.Sound(RANDOM / "background.wav")
unlock_door = arcade.Sound(SFX / "114250__godofph__door-unlock.wav")
pop_sound = arcade.Sound(SFX / "22763__franciscopadilla__60-high-bongo.wav")


class Game(arcade.View):
    def on_show(self):
        self.background_player = background.play(loop=1)
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.start = time.time()
        self.setup()

    def setup(self):
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        map_name = INDOOR / "map1.json"
        layer_options = {
            "walls": {
                "use_spatial_hash": True,
            },
            "doors": {
                "use_spatial_hash": True,
            },
            "stealable_top": {
                "use_spatial_hash": True,
            },
            "stealable_base": {
                "use_spatial_hash": True,
            },
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.player_sprite = arcade.Sprite(RANDOM / "player.png", CHARACTER_SCALING)
        self.player_sprite.center_x = 256
        self.player_sprite.center_y = 700
        self.player_circle = arcade.SpriteCircle(128, (244, 119, 125))
        self.player_circle.center_x = 256
        self.player_circle.center_y = 700
        self.scene.add_sprite("player_circle", self.player_circle)
        self.scene.add_sprite("player", self.player_sprite)

        self.enemy_sprite = arcade.Sprite(RANDOM / "player.png", CHARACTER_SCALING)
        self.enemy_sprite.center_x = 1650
        self.enemy_sprite.center_y = 1250
        self.enemy_circle = arcade.SpriteCircle(128, (11, 136, 130))
        self.enemy_circle.center_x = 1650
        self.enemy_circle.center_y = 1250

        self.scene.add_sprite("enemy_circle", self.enemy_circle)
        self.scene.add_sprite("enemy", self.enemy_sprite)


        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            [
                self.scene["doors"],
                self.scene["stealable_top"],
                self.scene["stealable_base"],
                self.scene["walls"],
            ],
        )
        self.physics_engine_2_electric_boogaloo = arcade.PhysicsEngineSimple(
            self.enemy_sprite,
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
        self.last_money = 0
        self.grab_time_text = arcade.gui.UITextArea(
            width=300,
            height=45,
            font_size=36,
            text='',
            font_name="Kenney Pixel",
            )
        self.money_text = arcade.gui.UITextArea(
            x=self.window.width - 125,
            width=125,
            height=45,
            font_size=36,
            text='$0',
            font_name='Kenney Pixel',
        )
        self.manager.add(self.grab_time_text)
        self.manager.add(self.money_text)

    def on_key_press(self, key, modifiers):
        if key in UP:
            self.player_sprite.change_y = 5
            self.enemy_sprite.change_y = 5
        if key in LEFT:
            self.player_sprite.change_x = -5
            self.enemy_sprite.change_x = -5
        if key in DOWN:
            self.player_sprite.change_y = -5
            self.enemy_sprite.change_y = -5
        if key in RIGHT:
            self.player_sprite.change_x = 5
            self.enemy_sprite.change_x = 5

    def on_key_release(self, key, modifiers):
        if key in (*LEFT, *RIGHT):  # basically LEFT or RIGHT
            self.player_sprite.change_x = 0
            self.enemy_sprite.change_x = 0
        elif key in (*UP, *DOWN):  # ^^ same as the comment above but it's up and downs
            self.player_sprite.change_y = 0
            self.enemy_sprite.change_y = 0

    def center_camera_to_player(self):
        # https://api.arcade.academy/en/latest/examples/platform_tutorial/step_09.html
        self.player_circle.position = self.player_sprite.position
        self.enemy_circle.position = self.enemy_sprite.position
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
        self.scene["player_circle"].draw(pixelated=True)
        self.scene["enemy_circle"].draw(pixelated=True)
        self.scene["walls"].draw(pixelated=True)
        self.scene["doors"].draw(pixelated=True)
        self.scene["stealable_base"].draw(pixelated=True)
        self.scene["stealable_top"].draw(pixelated=True)
        self.scene["player"].draw(pixelated=True)  # ordering = zindex :sunglassses:
        self.scene["enemy"].draw(pixelated=True)

        self.manager.draw()

    def on_update(self, delta_time):
        # `ST` in short of 'stealable_top'
        # `SB` in short of 'stealable_base'
        if self.scene["stealable_base"]:
            SB_sprite, SB_distance = arcade.get_closest_sprite(
                self.player_circle, self.scene["stealable_base"]
            )
            if SB_distance < 128:
                self.success_type = "SB"
                self.success = SB_sprite
        if self.scene["stealable_top"]:
            ST_sprite, ST_distance = arcade.get_closest_sprite(
                self.player_circle, self.scene["stealable_top"]
            )
            if ST_distance < 128:
                self.success_type = "ST"
                self.success = ST_sprite
        if self.scene["doors"]:
            D_sprite, D_distance = arcade.get_closest_sprite(
                self.player_sprite, self.scene["doors"]
            )
            if D_distance < 128:
                self.success_type = "D"
                self.success = D_sprite
        pop(self)
        self.last_money = self.money
        self.physics_engine.update()
        self.physics_engine_2_electric_boogaloo.update()
        self.center_camera_to_player()

        check(self)
        if check_lose(self):
            end = time.time()
            self.window.show_view(End(end - self.start, self.money, 0))
            self.clear()
            self.scene.name_mapping = None

    def on_message_box_close(self, dt, bt_text, exit=0):
        self.time -= 100 # debug
        self.time -= 0.1
        self.time = round(self.time, 1)
        self.grab_time_text.text = f"{bt_text}ING: {round(self.time, 1)}"
        if self.time <= 0:
            if exit == "EXIT":
                end = time.time()
                self.window.show_view(End(end - self.start, self.money, 1))
                self.clear()
                background.stop(self.background_player)
                self.scene.name_mapping = None
                pyglet.clock.unschedule(self.on_message_box_close)
            if bt_text == "LOCKPICK":
                unlock_door.play()
            elif bt_text == "STEAL":
                pop_sound.play()
            self.money += self.info.get("price", 0)
            if self.success:
                self.success.kill()
            self.success = False
            self.grab_time_text.text = ''
            pyglet.clock.unschedule(self.on_message_box_close)

    def load(self, button_text):
        # if button_text == "STEAL":
        #     self.time = self.info["grab_time"]
        #     self.t = multiprocessing.Process(target=self.on_message_box_close)
        #     self.t.daemon = True
        #     self.t.run()

        if button_text == "STEAL":
            self.time = self.info["grab_time"]
            pyglet.clock.schedule_interval(self.on_message_box_close, 0.1, button_text, self.info["name"])
        elif button_text == "LOCKPICK":
            self.time = round(random.uniform(*self.info["lockpick_time"]), 1)
            pyglet.clock.schedule_interval(self.on_message_box_close, 0.1, button_text)