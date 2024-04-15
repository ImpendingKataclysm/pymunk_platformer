# Start screen info
TITLE = 'Platforming with Python'
INSTRUCTIONS = 'Click to start playing'

# Screen sizing
SCREEN_WIDTH_PX = 1920
SCREEN_HEIGHT_PX = 1080

# Tile Map
MAP_SRC = ':resources:tiled_maps/pymunk_test_map.json'
LAYER_PLATFORMS = 'Platforms'
LAYER_MOVING_PLATFORMS = 'Moving Platforms'
LAYER_DYNAMIC_ITEMS = 'Dynamic Items'
LAYER_LADDERS = 'Ladders'
LAYER_PLAYER = 'Player'

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

# Physics engine forces
GRAVITY = 1500
DEFAULT_DAMPING = 1.0
FRICTION_PLAYER = 1.0
FRICTION_WALL = 0.7
FRICTION_DYNAMIC_ITEM = 0.6
MASS_PLAYER = 2.0
MAX_SPEED_X_PLAYER = 450
MAX_SPEED_Y_PLAYER = 1600

# Collision tracking
COLLISION_PLAYER = 'player'
COLLISION_WALL = 'wall'
COLLISION_DYNAMIC_ITEM = 'item'
