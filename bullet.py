import pygame
import random
from graphical import Graphical


class Bullet(Graphical):
    """Main bullet class, other bullets will inherit from that class"""

    def __init__(self, ai_game):
        """Initialization of a bullet object"""
        super().__init__(ai_game)

        # Bullet image load and it's dimension and position
        self.bullet_img = self.settings.bullet_img
        self.rect = self.bullet_img.get_rect()
        self.y = float(self.rect.y)

    def draw_bullet(self):
        """Bullet draw on a screen"""

        self.screen.blit(self.bullet_img, self.rect)


class BulletPlayer(Bullet):
    """Player bullet class, other player's bullets will inherit from that class"""

    def __init__(self, ai_game, x=0, y=-10, side=None):
        """Initialization of a player bullet"""
        super().__init__(ai_game)

        # Bullet player position
        self.settings.sound_player_channel.play(self.settings.sound_player_shot)
        self.rect.x = ai_game.ship.rect.x + x
        self.rect.y = ai_game.ship.rect.y + y
        self.y = float(self.rect.y)
        self.moving = False
        self.enemy_hit = False

    def update(self):
        """Moving a bullet"""

        self.y -= self.settings.bullet_speed
        self.rect.y = self.y


class BulletVertical(BulletPlayer):
    """Subclass that defines bullet for vertical bonus"""

    def __init__(self, ai_game, x=0, y=-10, side=None):
        """Initialization of a vertical bullet"""
        super().__init__(ai_game, x, y, side)

        # Position and statistics of a vertical bullet mode
        self.x_speed = self.settings.bullet_speed
        self.side = side
        self.y = float(self.rect.y)

    def update(self):
        """Bullets moving vertical"""

        self.rect.y = self.y
        if self.side:
            self.rect.x += self.x_speed
        else:
            self.rect.x -= self.x_speed

    def draw_bullet(self):
        """Diagonal bullet draw on a screen"""

        rotated_bullet = pygame.transform.rotate(self.bullet_img, 90)
        self.screen.blit(rotated_bullet, self.rect)


class BulletEnemy(Bullet):
    """Subclass for enemy bullets management"""

    def __init__(self, ai_game, x=0, y=-10):
        """Initialization of enemy bullet"""
        super().__init__(ai_game)

        # Position of an enemy bullet and it's statistics
        self.bullet_img = self.settings.enemy_bullet_img
        self.settings.sound_enemy_channel.play(self.settings.sound_enemy_shot)
        self.rect.x = x
        self.rect.y = y
        self.speed = self.settings.enemy_bullet_speed
        self.y = float(self.rect.y)
        if self.settings.boss_bullet_move:
            self.speed = random.randrange(1, 5)

    def update(self):
        """BulletEnemy falling down a screen"""
        self.y += self.speed * self.settings.scale
        self.rect.y = self.y

