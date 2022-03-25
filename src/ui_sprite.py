import arcade
from arcade.gui.surface import Surface
from arcade.gui.widgets import UISpriteWidget


class CustomSurface(Surface):
    def draw_sprite(self, x, y, width, height, sprite: arcade.Sprite):
        sprite.set_position(x + width // 2, y + height // 2)
        sprite.width = width
        sprite.height = height
        sprite.draw(pixelated=True)


class CustomSpriteWidget(UISpriteWidget):
    def do_render(self, surface: CustomSurface):
        surface.__class__ = CustomSurface
        self.prepare_render(surface)
        # surface.clear(color=(0, 0, 0, 0))
        surface.draw_sprite(0, 0, self.width, self.height, self._sprite)
