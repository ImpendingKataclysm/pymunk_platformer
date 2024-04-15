import arcade
import constants as c
from typing import Optional
from player_sprite import PlayerSprite
import utils


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

        # Track key inputs
        self.left_pressed: bool = False
        self.right_pressed: bool = False

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
        }
        tile_map = arcade.load_tilemap(c.MAP_SRC, c.SPRITE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(tile_map)

        # Get sprite lists from the tile map
        self.moving_platforms = tile_map.sprite_lists[c.LAYER_MOVING_PLATFORMS]

        # Set the background color
        if tile_map.background_color:
            arcade.set_background_color(tile_map.background_color)
        else:
            arcade.set_background_color(arcade.color.COLUMBIA_BLUE)

        # Create the physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(
            damping=c.DEFAULT_DAMPING,
            gravity=(0, -c.GRAVITY)
        )

        # Add sprites to the physics engine
        self.create_player_sprite()

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

    def on_update(self, delta_time: float):
        """
        Update the sprite movement and game logic.
        :param delta_time:
        :return:
        """
        # Update the moving platforms
        self.update_moving_platforms(delta_time)

        # Update the physics engine
        self.physics_engine.step()

    def on_draw(self):
        """
        Render the game map and sprites.
        :return:
        """
        self.clear()
        self.scene.draw()

    def create_player_sprite(self):
        """
        Create the player sprite and add it to the map and physics engine.
        :return:
        """
        self.player_sprite = PlayerSprite()
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
