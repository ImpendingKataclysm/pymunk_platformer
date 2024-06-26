import arcade
import math
import constants as c
import utils
from typing import Optional
from player_sprite import PlayerSprite
from enemy_sprite import EnemySprite
from pyglet.math import Vec2


class GameView(arcade.View):
    """
    Main application screen that displays the game map.
    """
    def __init__(self):
        super(GameView, self).__init__()

        self.scene: Optional[arcade.Scene] = None
        self.player_sprite: Optional[arcade.Sprite] = None
        self.physics_engine: Optional[arcade.PymunkPhysicsEngine] = None
        self.moving_platforms: Optional[arcade.SpriteList] = None
        self.ladders: Optional[arcade.SpriteList] = None
        self.coins: Optional[arcade.SpriteList] = None
        self.gems: Optional[arcade.SpriteList] = None
        self.flags: Optional[arcade.SpriteList] = None
        self.stars: Optional[arcade.SpriteList] = None
        self.main_camera: Optional[arcade.Camera] = None
        self.gui_camera: Optional[arcade.Camera] = None

        # Track key inputs
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False

    def on_show_view(self):
        """
        Create the game environment and sprites and display them in their
        initial state
        :return:
        """
        # Load the tile map and create the starting Scene
        layer_options = {
            c.LAYER_PLATFORMS: {
                'use_spatial_hash': True,
            },
            c.LAYER_MOVING_PLATFORMS: {
                'use_spatial_hash': False,
            },
            c.LAYER_LADDERS: {
                'use_spatial_hash': True,
            },
            c.LAYER_COINS: {
                'use_spatial_hash': True,
            },
            c.LAYER_FLAGS: {
                'use_spatial_hash': True,
            },
            c.LAYER_GEMS: {
                'use_spatial_hash': True,
            },
            c.LAYER_STARS: {
                'use_spatial_hash': True,
            },
        }
        tile_map = arcade.load_tilemap(
            c.MAP_SRC,
            c.SPRITE_SCALING,
            layer_options
        )

        self.scene = arcade.Scene.from_tilemap(tile_map)

        # Set up the cameras
        self.main_camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        # Get sprite lists from the tile map
        self.moving_platforms = tile_map.sprite_lists[c.LAYER_MOVING_PLATFORMS]
        self.ladders = tile_map.sprite_lists[c.LAYER_LADDERS]
        self.coins = tile_map.sprite_lists[c.LAYER_COINS]
        self.gems = tile_map.sprite_lists[c.LAYER_GEMS]
        self.flags = tile_map.sprite_lists[c.LAYER_FLAGS]
        self.stars = tile_map.sprite_lists[c.LAYER_STARS]

        # Set the background color
        if tile_map.background_color:
            arcade.set_background_color(tile_map.background_color)
        else:
            arcade.set_background_color(arcade.color.COLUMBIA_BLUE)

        # Create the physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=c.DAMPING_DEFAULT,
            gravity=(0, -c.GRAVITY)
        )

        # Add sprites to the physics engine
        self.create_player_sprite()

        # Reset score
        self.player_sprite.score = 0

        self.physics_engine.add_sprite_list(
            tile_map.sprite_lists[c.LAYER_PLATFORMS],
            friction=c.FRICTION_WALL,
            collision_type=c.COLLISION_WALL,
            body_type=arcade.PymunkPhysicsEngine.STATIC
        )

        self.physics_engine.add_sprite_list(
            tile_map.sprite_lists[c.LAYER_DYNAMIC_ITEMS],
            friction=c.FRICTION_DYNAMIC_ITEM,
            collision_type=c.COLLISION_DYNAMIC_ITEM
        )

        self.physics_engine.add_sprite_list(
            self.moving_platforms,
            body_type=arcade.PymunkPhysicsEngine.KINEMATIC
        )

        # Get enemies layer from the tile map
        enemies_layer = tile_map.object_lists[c.LAYER_ENEMIES]

        for enemy in enemies_layer:
            # Get the enemy's coordinates from the map
            cartesian = tile_map.get_cartesian(
                enemy.shape[0],
                enemy.shape[1]
            )

            # Create an enemy sprite
            enemy_sprite = EnemySprite()

            # Set the enemy sprite's position
            enemy_sprite.center_x = math.floor(c.SPRITE_SCALING * tile_map.tile_width * cartesian[0])
            enemy_sprite.center_y = math.floor(c.SPRITE_SCALING * tile_map.tile_height * (cartesian[1] + 0.5))

            self.scene.add_sprite(c.LAYER_ENEMIES, enemy_sprite)

        # Add enemy sprites to the physics engine
        self.physics_engine.add_sprite_list(
            self.scene.get_sprite_list(c.LAYER_ENEMIES),
            friction=c.FRICTION_PLAYER,
            collision_type=c.COLLISION_ENEMY
        )

    def on_update(self, delta_time: float):
        """
        Update the sprite movement and game logic.
        :param delta_time:
        :return:
        """
        self.update_moving_platforms(delta_time)
        self.update_player_sprite()

        # Game over if the player sprite is out of bounds
        if self.player_sprite.center_y < c.OUT_OF_BOUNDS:
            game_over = self.GameOverView()
            self.window.show_view(game_over)

        self.center_camera_to_player()

        self.physics_engine.step()

    def on_key_press(self, symbol: int, modifiers: int):
        """
        Updates player movement based on keyboard input.
        :param symbol:
        :param modifiers:
        :return:
        """
        if symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.left_pressed = True
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.right_pressed = True
        elif symbol == arcade.key.UP or symbol == arcade.key.W:
            self.up_pressed = True
        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.down_pressed = True

    def on_key_release(self, _symbol: int, _modifiers: int):
        """
        Tracks which movement inputs are no longer active.
        :param _symbol:
        :param _modifiers:
        :return:
        """
        if _symbol == arcade.key.LEFT or _symbol == arcade.key.A:
            self.left_pressed = False
        elif _symbol == arcade.key.RIGHT or _symbol == arcade.key.D:
            self.right_pressed = False
        elif _symbol == arcade.key.UP or _symbol == arcade.key.W:
            self.up_pressed = False
        elif _symbol == arcade.key.DOWN or _symbol == arcade.key.S:
            self.down_pressed = False

    def on_draw(self):
        """
        Render the game map and sprites.
        :return:
        """
        self.clear()
        self.main_camera.use()
        self.scene.draw()
        self.gui_camera.use()

        utils.write_gui_text(
            c.SCORE_LABEL,
            self.player_sprite.score,
            c.SCORE_START_X
        )

        utils.write_gui_text(
            c.LAYER_COINS,
            len(self.scene[c.LAYER_COINS]),
            c.COINS_START_X
        )

        utils.write_gui_text(
            c.LAYER_GEMS,
            len(self.scene[c.LAYER_GEMS]),
            c.GEMS_START_X
        )

        utils.write_gui_text(
            c.LAYER_FLAGS,
            len(self.scene[c.LAYER_FLAGS]),
            c.FLAGS_START_X
        )

        utils.write_gui_text(
            c.LAYER_STARS,
            len(self.scene[c.LAYER_STARS]),
            c.STARS_START_X
        )

    def create_player_sprite(self):
        """
        Create the player sprite and add it to the map and physics engine.
        :return:
        """
        self.player_sprite = PlayerSprite(
            self.ladders,
            self.coins,
            self.gems,
            self.flags,
            self.stars
        )

        self.player_sprite.center_x = c.SPRITE_SCALED_SIZE + c.SPRITE_SCALED_SIZE / 2
        self.player_sprite.center_y = c.SPRITE_SCALED_SIZE + c.SPRITE_SCALED_SIZE / 2

        self.scene.add_sprite(c.LAYER_PLAYER, self.player_sprite)

        self.physics_engine.add_sprite(
            self.player_sprite,
            friction=c.FRICTION_PLAYER,
            mass=c.MASS_PLAYER,
            moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
            collision_type=c.COLLISION_PLAYER,
            max_horizontal_velocity=c.MAX_SPEED_X_PLAYER,
            max_vertical_velocity=c.MAX_SPEED_Y_PLAYER
        )

    def update_player_sprite(self):
        """
        Update player sprite movement on the ground and in the air based on
        user inputs.
        :return:
        """
        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)
        force = (0, 0)
        friction = 0

        if self.left_pressed and not self.right_pressed:
            if is_on_ground or self.player_sprite.is_on_ladder:
                force = (-c.MOVE_FORCE_GROUND_PLAYER, 0)
            else:
                force = (-c.MOVE_FORCE_AIR_PLAYER, 0)
        elif self.right_pressed and not self.left_pressed:
            if is_on_ground or self.player_sprite.is_on_ladder:
                force = (c.MOVE_FORCE_GROUND_PLAYER, 0)
            else:
                force = (c.MOVE_FORCE_AIR_PLAYER, 0)

        if self.up_pressed and not self.down_pressed:
            if is_on_ground and not self.player_sprite.is_on_ladder:
                impulse = (0, c.JUMP_IMPULSE_PLAYER)
                self.physics_engine.apply_impulse(self.player_sprite, impulse)
            elif self.player_sprite.is_on_ladder:
                friction = c.FRICTION_PLAYER
                force = (0, c.MOVE_FORCE_GROUND_PLAYER)
        elif self.down_pressed and not self.up_pressed:
            if self.player_sprite.is_on_ladder:
                friction = c.FRICTION_PLAYER
                force = (0, -c.MOVE_FORCE_GROUND_PLAYER)

        if (
            not self.up_pressed
            and not self.down_pressed
            and not self.right_pressed
            and not self.left_pressed
        ):
            friction = c.FRICTION_PLAYER

        self.physics_engine.set_friction(self.player_sprite, friction)
        self.physics_engine.apply_force(self.player_sprite, force)

    def center_camera_to_player(self):
        """
        Scroll the viewport to keep up with the player sprite
        :return:
        """
        screen_center_x = self.player_sprite.center_x - (
                self.main_camera.viewport_width / 2
        )

        screen_center_y = self.player_sprite.center_y - (
                self.main_camera.viewport_height / 2
        )

        if screen_center_x < 0:
            screen_center_x = 0

        if screen_center_y < 0:
            screen_center_y = 0

        player_center = Vec2(screen_center_x, screen_center_y)

        self.main_camera.move_to(player_center)

    def update_moving_platforms(self, delta_time: float):
        """
        Update the velocity for any moving platforms in the map.
        :param delta_time:
        :return:
        """
        for platform in self.moving_platforms:
            velocity_x = 0
            velocity_y = 0

            if platform.change_x:
                utils.check_boundary_x(platform)
                velocity_x = platform.change_x / delta_time

            if platform.change_y:
                utils.check_boundary_y(platform)
                velocity_y = platform.change_y / delta_time

            platform_velocity = (velocity_x, velocity_y)

            self.physics_engine.set_velocity(platform, platform_velocity)

    class GameOverView(arcade.View):
        """
        Game over screen. User may click anywhere on the screen to restart.
        """
        def __init__(self):
            super(GameView.GameOverView, self).__init__()
            self.texture = arcade.load_texture(c.GAME_OVER_SCREEN)
            arcade.set_viewport(
                left=0,
                right=c.SCREEN_WIDTH_PX - 1,
                bottom=0,
                top=c.SCREEN_HEIGHT_PX - 1
            )

        def on_draw(self):
            """
            Render the game over screen.
            :return:
            """
            self.clear()
            self.texture.draw_sized(
                c.SCREEN_WIDTH_PX / 2,
                c.SCREEN_HEIGHT_PX / 2,
                c.SCREEN_WIDTH_PX,
                c.SCREEN_HEIGHT_PX
            )

        def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
            """
            Restart the game when the user clicks the screen
            :param x:
            :param y:
            :param button:
            :param modifiers:
            :return:
            """
            game_view = GameView()
            self.window.show_view(game_view)
