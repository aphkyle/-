import arcade
from arcade.gui.mixins import UIMouseFilterMixin
from arcade.gui.widgets import (
    UILayout,
    UIAnchorWidget,
    UITextArea,
    UIFlatButton,
    UIBoxLayout,
)
from ui_sprite import CustomSpriteWidget


class UIMessageBox(UIMouseFilterMixin, UIAnchorWidget):
    def __init__(
        self,
        *,
        width: float,
        height: float,
        sprite: arcade.Sprite,
        message_text: str,
        buttons=("Ok",),
        callback=None
    ):

        space = 10

        self._text_area = UITextArea(
            text=message_text,
            width=width - space,
            height=height - space,
            font_name=("Kenney Pixel"),
            font_size=36,
            text_color=arcade.color.BLACK,
        )

        self._image = CustomSpriteWidget(sprite=sprite)

        button_group = UIBoxLayout(vertical=False)
        for button_text in buttons:
            button = UIFlatButton(
                text=button_text, style={"font_size": 36, "font_name": ("Kenney Pixel")}
            )
            button_group.add(button.with_space_around(left=10))
            button.on_click = self.on_ok  # type: ignore

        self._bg_tex = arcade.load_texture(
            ":resources:gui_basic_assets/window/grey_panel.png"
        )

        self._callback = callback  # type: ignore

        group = UILayout(
            width=width,
            height=height,
            children=[
                UIAnchorWidget(
                    child=self._image,
                    anchor_x="left",
                    anchor_y="top",
                    align_x=20,
                    align_y=-10,
                ),
                UIAnchorWidget(
                    child=self._text_area,
                    anchor_x="left",
                    anchor_y="center",
                    align_x=130,
                    align_y=-20,
                ),
                UIAnchorWidget(
                    child=button_group,
                    anchor_x="right",
                    anchor_y="bottom",
                    align_x=-10,
                    align_y=10,
                ),
            ],
        ).with_background(self._bg_tex)

        super().__init__(child=group)
        self.anchor_y = "bottom"

    def on_ok(self, event):
        self.parent.remove(self)
        if self._callback is not None:
            self._callback(event.source.text)
