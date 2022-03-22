import pathlib

import arcade
from arcade.pymunk_physics_engine import PymunkPhysicsEngine

from constants import *


ASSETS = pathlib.Path("assets")
if not ASSETS.exists():
    ASSETS = pathlib.Path('..') / "assets"
DUNGEON_BLOCKS = ASSETS / "dungeon_blocks"

class Game(arcade.View):
    def on_show(self):
        self.setup()

    def setup(self):
        self.up_pressed = None
        self.down_pressed = None
        self.left_pressed = None
        self.right_pressed = None
        self.player_speed = 50
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.physics_engine = PymunkPhysicsEngine()

        map_name = ASSETS / "map1.json"
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        print(self.scene.name_mapping)

        image_source = DUNGEON_BLOCKS / "player.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 256
        self.player_sprite.center_y = 512
        self.scene.add_sprite("Player", self.player_sprite)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=0.6,
                                       moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
                                       damping=0.01,
                                       collision_type="player",
                                       max_velocity=400)
        self.physics_engine.add_sprite_list(self.scene["walls"],
                                            friction=0.6,
                                            collision_type="wall",
                                            body_type=PymunkPhysicsEngine.STATIC)
        self.physics_engine.add_sprite_list(self.scene["doorsNshit"],
                                            friction=0.6,
                                            collision_type="wall",
                                            body_type=PymunkPhysicsEngine.STATIC)


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.SPACE:
            bullet = arcade.SpriteSolidColor(9, 9, arcade.color.RED)
            bullet.position = self.player_sprite.position
            bullet.center_x += 30
            self.bullet_list.append(bullet)
            self.physics_engine.add_sprite(bullet,
                                           mass=0.2,
                                           damping=1.0,
                                           friction=0.6,
                                           collision_type="bullet")
            force = (3000, 0)
            self.physics_engine.apply_force(bullet, force)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def center_camera_to_player(self):
        # https://api.arcade.academy/en/latest/examples/platform_tutorial/step_09.html
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
        # self.scene["doorsNshit"].draw_hit_boxes()
        # self.scene["walls"].draw_hit_boxes()
        self.player_sprite.draw_hit_box()
        self.scene.draw(pixelated=True)
        self.player_sprite.draw()

    def on_update(self, delta_time):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            force = (0, 2000)
            self.physics_engine.apply_force(self.player_sprite, force)
        elif self.down_pressed and not self.up_pressed:
            force = (0, -2000)
            self.physics_engine.apply_force(self.player_sprite, force)
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
            force = (-2000, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
        elif self.right_pressed and not self.left_pressed:
            force = (2000, 0)
            self.physics_engine.apply_force(self.player_sprite, force)

        self.physics_engine.step()
        self.center_camera_to_player()