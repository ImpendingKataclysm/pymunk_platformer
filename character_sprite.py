import arcade
import constants as c
import utils


class CharacterSprite(arcade.Sprite):
    """
    Animated character sprite (can be a player or an enemy).
    """
    def __init__(self, name_folder, name_file):
        super(CharacterSprite, self).__init__()

        self.sprite_path = f'{c.CHARACTER_SPRITE_PATH}/{name_folder}/{name_file}'
        self.scale = c.SPRITE_SCALING
        self.face_direction = c.RIGHT_FACING
        self.is_on_ladder = False
        self.odometer_x = 0
        self.odometer_y = 0

        self.idle_texture_pair = arcade.load_texture_pair(
            f'{self.sprite_path}_idle.png'
        )

        self.walk_texture_pairs = []

        for i in range(c.WALK_TEXTURES_TOTAL):
            texture_pair = arcade.load_texture_pair(
                f'{c.PLAYER_SPRITE_PATH}_walk{i}.png'
            )

            self.walk_texture_pairs.append(texture_pair)

        self.texture = self.idle_texture_pair[self.face_direction]
        self.cur_texture_index = 0

    def set_sprite_direction(self, dx):
        """
        Change the sprite's facing direction to match its direction of movement.
        :param dx: horizontal displacement of the sprite
        :return:
        """
        if (
                dx < -c.STATIONARY_ZONE
                and self.face_direction == c.RIGHT_FACING
        ):
            self.face_direction = c.LEFT_FACING
        elif (
                dx > c.STATIONARY_ZONE
                and self.face_direction == c.LEFT_FACING
        ):
            self.face_direction = c.RIGHT_FACING

    def animate_walking(self):
        """
        Update the sprite's walking animation.
        :return:
        """
        if (
            abs(self.odometer_x) > c.DISTANCE_PX_TO_CHANGE_TEXTURE
            and not self.is_on_ladder
        ):
            self.odometer_x = 0
            self.cur_texture_index += 1

            if self.cur_texture_index >= c.WALK_TEXTURES_TOTAL:
                self.cur_texture_index = 0

            self.texture = self.walk_texture_pairs[
                self.cur_texture_index
            ][
                self.face_direction
            ]

    def animate_idle(self, dx):
        """
        Update the sprite's texture to an idle texture if its horizontal
        displacement reaches the value of STATIONARY_ZONE.
        :param dx: The sprite's horizontal displacement
        :return:
        """
        if abs(dx) <= c.STATIONARY_ZONE and not self.is_on_ladder:
            self.texture = self.idle_texture_pair[self.face_direction]
