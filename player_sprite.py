import arcade
import constants as c


class PlayerSprite(arcade.Sprite):
    """
    Sprite controlled by the player
    """
    def __init__(self):
        super(PlayerSprite, self).__init__()

        self.scale = c.SPRITE_SCALING
        self.face_direction = c.RIGHT_FACING

        self.idle_texture_pair = arcade.load_texture_pair(
            f'{c.PLAYER_SPRITE_PATH}_idle.png'
        )

        self.texture = self.idle_texture_pair[self.face_direction]
