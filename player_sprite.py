import arcade
import constants as c


class PlayerSprite(arcade.Sprite):
    """
    Sprite controlled by the player
    """

    def __init__(self, ladder_list):
        super(PlayerSprite, self).__init__()

        self.scale = c.SPRITE_SCALING
        self.face_direction = c.RIGHT_FACING

        self.idle_texture_pair = arcade.load_texture_pair(
            f'{c.PLAYER_SPRITE_PATH}_idle.png'
        )

        self.texture = self.idle_texture_pair[self.face_direction]
        self.is_on_ladder = False
        self.ladder_list = ladder_list

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """
        Handle movement from pymunk engine and set animation textures.
        :param physics_engine:
        :param dx:
        :param dy:
        :param d_angle:
        :return:
        """
        # Check if the sprite is on a ladder
        ladders = arcade.check_for_collision_with_list(self, self.ladder_list)

        if len(ladders) > 0:
            if not self.is_on_ladder:
                self.is_on_ladder = True
                self.pymunk.gravity = (0, 0)
                self.pymunk.damping = c.DAMPING_LADDERS
                self.pymunk.max_vertical_velocity = c.MAX_SPEED_X_PLAYER
        else:
            if self.is_on_ladder:
                self.is_on_ladder = False
                self.pymunk.gravity = (0, -c.GRAVITY)
                self.pymunk.damping = c.DAMPING_DEFAULT
                self.pymunk.max_vertical_velocity = c.MAX_SPEED_Y_PLAYER
