import arcade
import constants as c
from typing import Optional
from player_sprite import PlayerSprite


class GameView(arcade.View):
    """
    Main application screen that displays the game map.
    """

    def __init__(self):
        super(GameView, self).__init__()

        self.scene: Optional[arcade.Scene] = None
        self.player_sprite: Optional[arcade.Sprite] = None

        # Set background color
        arcade.set_background_color(arcade.color.COLUMBIA_BLUE)

    def on_show_view(self):
        """
        Create the game environment and sprites and display them in their
        initial state
        :return:
        """
        layer_options = {
            c.PLATFORMS_LAYER: {
                'use_spatial_hash': True,
            },
            c.LADDERS_LAYER: {
                'use_spatial_hash': True,
            },
        }
        tile_map = arcade.load_tilemap(c.MAP_SRC, c.SPRITE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(tile_map)

        self.player_sprite = PlayerSprite()
        self.player_sprite.center_x = c.SPRITE_SCALED_SIZE + c.SPRITE_SCALED_SIZE / 2
        self.player_sprite.center_y = c.SPRITE_SCALED_SIZE + c.SPRITE_SCALED_SIZE / 2

        self.scene.add_sprite(c.PLAYER_LAYER, self.player_sprite)

    def on_draw(self):
        """
        Render the game map and sprites.
        :return:
        """
        self.clear()
        self.scene.draw()
