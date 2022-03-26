import arcade

import pyglet.clock

from sort_sprite import SortName 
from message_box import UIMessageBox

def pop(self):
    if self.success and self.time <= 0:
        self.info = SortName(self.success.texture.name).get_sprite_info()
        if self.success != self.last_sprite:
            if self.message_box:
                self.manager.remove(self.message_box)
            if self.success_type in ("ST", "SB"):
                self.message_box = UIMessageBox(
                    width=500,
                    height=200,
                    sprite=arcade.Sprite(texture=self.success.texture),
                    message_text=f"{self.info['name']}\nVALUE:{self.info['price']}",
                    buttons=("STEAL",),
                    callback=self.load,
                )
            elif self.success_type == "D":
                self.message_box = UIMessageBox(
                    width=500,
                    height=200,
                    sprite=arcade.Sprite(texture=self.success.texture),
                    message_text=f"{self.info['name']}\nTIME:{self.info['lockpick_time']}",
                    buttons=("LOCKPICK",),
                    callback=self.load,
                )
            self.manager.add(self.message_box)
        self.last_sprite = self.success
    elif self.message_box:
        self.manager.remove(self.message_box)
        self.last_sprite = None
    if self.money != self.last_money:
        self.money_text.text = f"${self.money}"
    self.last_money = self.money

def check(self):
    D = ST = arcade.get_closest_sprite(self.player_sprite, self.scene["doors"])
    ST = arcade.get_closest_sprite(self.player_sprite, self.scene["stealable_top"])
    SB = arcade.get_closest_sprite(self.player_sprite, self.scene["stealable_base"])
    if self.success_type == "D":
        if not D or (D[1] > 128 or D[0] != self.success):
            self.time = 0
            self.success = False
    elif self.success_type == "ST":
        if not ST or (ST[1] > 128 or ST[0] != self.success):
            self.time = 0
            self.success = False
    elif self.success_type == "SB":
        if not SB or (SB[1] > 128 or SB[0] != self.success):
            self.time = 0
            self.success = False
            pyglet.clock.unschedule(self.on_message_box_close)
    if self.success == False:
        self.manager.remove(self.message_box)

def check_lose(self):
    return arcade.check_for_collision(self.player_sprite, self.enemy_circle)

