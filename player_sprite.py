import arcade
import constants as c
from character_sprite import CharacterSprite


class PlayerSprite(CharacterSprite):
    """
    Sprite controlled by the player
    """
    def __init__(self, ladder_list, coin_list, gem_list, flag_list, star_list):
        super(PlayerSprite, self).__init__(
            c.PLAYER_SPRITE_FOLDER,
            c.PLAYER_SPRITE_FILE
        )

        self.jump_texture_pair = arcade.load_texture_pair(
            f'{self.sprite_path}_jump.png'
        )

        self.fall_texture_pair = arcade.load_texture_pair(
            f'{self.sprite_path}_fall.png'
        )

        self.climb_textures = []

        for i in range(c.CLIMB_TEXTURES_TOTAL):
            texture = arcade.load_texture(
                f'{self.sprite_path}_climb{i}.png'
            )

            self.climb_textures.append(texture)

        self.is_on_ground = False
        self.ladder_list = ladder_list
        self.coin_list = coin_list
        self.gem_list = gem_list
        self.flag_list = flag_list
        self.star_list = star_list
        self.score = 0

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """
        Handle movement from pymunk engine and set animation textures.
        :param physics_engine:
        :param dx:
        :param dy:
        :param d_angle:
        :return:
        """
        self.set_sprite_direction(dx)
        self.check_ladder_collision()
        self.check_collectible_collision()

        # Check if the sprite is on the ground
        self.is_on_ground = physics_engine.is_on_ground(self)

        # Increment the odometers by the horizontal and vertical displacement
        self.odometer_x += dx
        self.odometer_y += dy

        # Update animations
        if self.is_on_ladder and not self.is_on_ground:
            if self.animate_climbing():
                return

        if self.animate_jumping(dy):
            return

        if self.animate_idle(dx):
            return

        self.animate_walking()

    def check_ladder_collision(self):
        """
        Check if the sprite is on a ladder and update the physics engine
        accordingly.
        :return:
        """
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

    def check_collectible_collision(self):
        """
        Checks whether the player sprite has collided with a collectible object
        e.g. a coin, gem or flag, and increases the score accordingly as well
        as tracking how many of each collectible are left.
        :return:
        """
        collectibles = arcade.check_for_collision_with_list(self, self.coin_list)

        if len(collectibles) == 0:
            collectibles = arcade.check_for_collision_with_list(self, self.gem_list)

        if len(collectibles) == 0:
            collectibles = arcade.check_for_collision_with_list(self, self.flag_list)

        if len(collectibles) == 0:
            collectibles = arcade.check_for_collision_with_list(self, self.star_list)

        if len(collectibles) > 0:
            for sprite in collectibles:
                points = int(sprite.properties[c.PROP_POINTS])
                self.score += points
                sprite.remove_from_sprite_lists()

    def animate_climbing(self):
        """
        Update the sprite's climbing animation.
        :return: Boolean indicating whether to update the animation
        """
        animating = False
        if abs(self.odometer_y) > c.DISTANCE_PX_TO_CHANGE_TEXTURE:
            self.odometer_y = 0
            self.cur_texture_index += 1

            if self.cur_texture_index >= c.CLIMB_TEXTURES_TOTAL:
                self.cur_texture_index = 0

            self.texture = self.climb_textures[self.cur_texture_index]
            animating = True

        return animating

    def animate_jumping(self, dy):
        """
        Update the sprite's jumping and falling animations.
        :param dy: The sprite's vertical displacement
        :return: Boolean indicating whether to update the animation
        """
        animating = False

        if not self.is_on_ground and not self.is_on_ladder:
            if dy > c.STATIONARY_ZONE:
                self.texture = self.jump_texture_pair[self.face_direction]
                animating = True
            elif dy < -c.STATIONARY_ZONE:
                self.texture = self.fall_texture_pair[self.face_direction]
                animating = True

        return animating
