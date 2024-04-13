import arcade
import constants as c


class StartView(arcade.View):
    """
    Opening screen for the game that displays the title and instructions.
    """
    def on_show_view(self):
        """
        Set the start screen's background color and sets the viewport to match
        the screen dimensions.
        :return:
        """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """
        Display the game title and instructions on the start screen.
        :return:
        """
        self.clear()

        arcade.draw_text(
            c.TITLE,
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.WHITE,
            font_size=50,
            anchor_x='center'
        )

        arcade.draw_text(
            c.INSTRUCTIONS,
            self.window.width / 2,
            self.window.height / 2 - 75,
            arcade.color.WHITE,
            font_size=20,
            anchor_x='center'
        )
