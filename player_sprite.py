import arcade
import constants as c


class PlayerSprite(arcade.Sprite):
    """
    Sprite controlled by the player
    """
    def __init__(self, ladder_list, coin_list, gem_list, flag_list, star_list):
        super(PlayerSprite, self).__init__()

        self.scale = c.SPRITE_SCALING
        self.face_direction = c.RIGHT_FACING

        self.idle_texture_pair = arcade.load_texture_pair(
            f'{c.PLAYER_SPRITE_PATH}_idle.png'
        )

        self.jump_texture_pair = arcade.load_texture_pair(
            f'{c.PLAYER_SPRITE_PATH}_jump.png'
        )

        self.fall_texture_pair = arcade.load_texture_pair(
            f'{c.PLAYER_SPRITE_PATH}_fall.png'
        )

        self.walk_texture_pairs = []
        self.climb_textures = []

        for i in range(c.WALK_TEXTURES_TOTAL):
            texture_pair = arcade.load_texture_pair(
                f'{c.PLAYER_SPRITE_PATH}_walk{i}.png'
            )

            self.walk_texture_pairs.append(texture_pair)

        for i in range(c.CLIMB_TEXTURES_TOTAL):
            texture = arcade.load_texture(
                f'{c.PLAYER_SPRITE_PATH}_climb{i}.png'
            )

            self.climb_textures.append(texture)

        self.texture = self.idle_texture_pair[self.face_direction]
        self.cur_texture_index = 0
        self.is_on_ladder = False
        self.is_on_ground = False
        self.ladder_list = ladder_list
        self.coin_list = coin_list
        self.gem_list = gem_list
        self.flag_list = flag_list
        self.star_list = star_list
        self.coins_left = len(coin_list)
        self.gems_left = len(gem_list)
        self.flags_left = len(flag_list)
        self.stars_left = len(star_list)
        self.odometer_x = 0
        self.odometer_y = 0
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

        if abs(dx) <= c.STATIONARY_ZONE and not self.is_on_ladder:
            self.texture = self.idle_texture_pair[self.face_direction]
            return

        self.animate_walking()

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

                if sprite in self.coin_list:
                    self.coins_left -= 1
                elif sprite in self.gem_list:
                    self.gems_left -= 1
                elif sprite in self.flag_list:
                    self.flags_left -= 1
                elif sprite in self.star_list:
                    self.stars_left -= 1

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
