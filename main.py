import arcade
import constants as c
from start_view import StartView


def main():
    window = arcade.Window(
        width=c.SCREEN_WIDTH_PX,
        height=c.SCREEN_HEIGHT_PX,
        title=c.TITLE
    )

    start_view = StartView()
    window.show_view(start_view)

    arcade.run()


if __name__ == '__main__':
    main()
