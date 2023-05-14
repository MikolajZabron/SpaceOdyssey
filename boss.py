import pygame
import random
from graphical import Graphical
from bullet import BulletEnemy


class Boss(Graphical):
    """Boss Class that manages a boss object"""

    def __init__(self, ai_game):
        """Initialization of a boss object"""
        super().__init__(ai_game)

        # Boss image load and set of it's dimensions
        self.image = self.settings.boss_image
        self.rect = self.image.get_rect()
        self.rect.x = self.screen_rect.right / 2 - self.rect.width / 2
        self.rect.y = -1200

        # Boss statistics
        self.speed = self.settings.boss_speed
        self.health = self.settings.boss_health
        self.not_alive = self.settings.boss_not_alive

    def update(self):
        """Makes boss object fly down a screen until his top side is 500 pixels over a screen"""

        if self.rect.y >= -550:
            self.rect.y = -550
            self.speed = 0
            self.settings.boss_bullet_move = True
        else:
            self.rect.y += self.speed
            self.settings.boss_bullet_move = False

    def shoot(self):
        """Function which makes boss shoot a bullets"""

        bullet = BulletEnemy(self, random.randrange(0, self.screen_rect.right), self.rect.bottom)
        return bullet

    def hit(self):
        """Function that is being executed when boss object is taking damage"""

        # Critical chance check
        i = random.randint(1, 10)
        if i < self.settings.critical_chance:
            self.health -= self.settings.damage * 2
        else:
            self.health -= self.settings.damage

        # Check if boss is still having health points
        if self.health <= 0:
            self.settings.sound_boss_death.set_volume(0.7)
            self.settings.sound_enemy_channel.play(self.settings.sound_boss_death)
            self.settings.boss_not_alive = True
            self.settings.target_exp = self.settings.exp_need
            self.settings.endless_mode = True
            self.settings.enemy_bullet_speed = 5
            self.settings.boss_bullet_move = False
            self.kill()

    def draw_boss(self):
        """Draw boss on a screen"""

        self.screen.blit(self.image, self.rect)
