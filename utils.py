import arcade
import constants as c


def check_boundary_y(sprite: arcade.Sprite):
    """
    Reverses a moving sprite's vertical velocity if it has reached its top or
    bottom boundary.
    :param sprite: Moving sprite
    :return:
    """
    if(
        sprite.boundary_top
        and sprite.change_y > 0
        and sprite.top > sprite.boundary_top
    ) or (
        sprite.boundary_bottom
        and sprite.change_y < 0
        and sprite.bottom < sprite.boundary_bottom
    ):
        sprite.change_y *= -1


def check_boundary_x(sprite: arcade.Sprite):
    """
    Reverses a moving sprite's horizontal velocity if it has reached its left
    or right boundary.
    :param sprite: Moving sprite
    :return:
    """
    if (
        sprite.boundary_right
        and sprite.change_x > 0
        and sprite.right > sprite.boundary_right
    ) or (
        sprite.boundary_left
        and sprite.change_x < 0
        and sprite.left < sprite.boundary_left
    ):
        sprite.change_x *= -1


def write_gui_text(label: str, value: int, start_x: int):
    """
    Display information in the GUI
    :param label:
    :param value:
    :param start_x:
    :return:
    """
    gui_text = f'{label}: {value}'
    arcade.draw_text(
        gui_text,
        start_x,
        c.GUI_START_Y,
        arcade.csscolor.WHITE,
        c.GUI_FONT_SIZE
    )
