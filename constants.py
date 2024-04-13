# Start screen info
TITLE = 'Platforming with Python'
INSTRUCTIONS = 'Click to start playing'

# Screen sizing
SCREEN_WIDTH_PX = 1920
SCREEN_HEIGHT_PX = 1080

# Tile Map
MAP_SRC = ':resources:tiled_maps/pymunk_test_map.json'
PLATFORMS_LAYER = 'Platforms'
LADDERS_LAYER = 'Ladders'
PLAYER_LAYER = 'Player'

# Sprite sizing and scaling
SPRITE_SCALING = 0.5
SPRITE_IMAGE_SIZE = 128
SPRITE_SCALED_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING)

# Sprite textures
CHARACTER_SPRITE_PATH = ':resources:images/animated_characters/'
PLAYER_SPRITE_PATH = f'{CHARACTER_SPRITE_PATH}female_adventurer/femaleAdventurer'

# Sprite animations
RIGHT_FACING = 0
LEFT_FACING = 1
