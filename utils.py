import arcade


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
