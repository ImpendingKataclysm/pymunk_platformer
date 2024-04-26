import arcade
import constants as c
from character_sprite import CharacterSprite


class EnemySprite(CharacterSprite):
    def __init__(self):
        super(EnemySprite, self).__init__(c.ENEMY_SPRITE_FOLDER, c.ENEMY_SPRITE_FILE)

        self.health = c.ENEMY_HEALTH
        self.points = c.ENEMY_POINTS
