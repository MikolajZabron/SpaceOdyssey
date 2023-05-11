import pygame.image
import random
from graphical import Graphical


class Comet(Graphical):
    """Class used to manage comets"""

    def __init__(self, ai_game):
        """Initialization of comet"""
        super().__init__(ai_game)

        # Comet image load and it's dimensions
        self.image = self.settings.comet_image
        self.image = pygame.transform.scale(self.image, (80, 59))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(self.screen_rect.right - self.rect.width)
        self.rect.y = random.randrange(-500, -100)

        # Comet statistics
        self.comet_speed = random.randrange(1, 3)
        self.health = self.settings.comet_health * self.settings.scale

    def update(self):
        """Comet moving down the screen"""

        self.rect.y += self.comet_speed

    def hit(self):
        """Function executed when a comet is being hit"""

        # Checking if it was a critical shot
        i = random.randint(1, 10)
        if i < self.settings.critical_chance:
            self.health -= self.settings.damage * 2

        # Checking if it was a headshot, if not normal damage applied
        if self.settings.headshot:
            j = random.randint(1, 20)
            if j == 1:
                self.kill()
                self.settings.target_exp += self.settings.comet_exp
            else:
                self.health -= self.settings.damage
        else:
            self.health -= self.settings.damage

        # Checking if comet is destroyed
        if self.health <= 0:
            self.settings.sound_environment_channel.play(self.settings.sound_comet_death)
            self.kill()
            self.settings.target_exp += self.settings.comet_exp

    def draw_comet(self):
        """Function responsible for drawing a comet on a screen"""

        self.screen.blit(self.image, self.rect)


class CometSmall(Comet):
    """Subclass for small comets management"""

    def __init__(self, ai_game):
        """Initialization of small comet"""
        super().__init__(ai_game)

        # Small comet image transform and it's dimensions
        self.image = pygame.transform.scale(self.settings.comet_image, (60, 45))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(self.screen_rect.right - self.rect.width)
        self.rect.y = random.randrange(-200, -100)

        # Small comet statistics
        self.health = self.settings.comet_small_health * self.settings.scale
        self.comet_speed = random.randrange(2, 4)

    def hit(self):
        """Function executed when a comet is being hit"""

        # Checking if it was a critical shot
        i = random.randint(1, 10)
        if i < self.settings.critical_chance:
            self.health -= self.settings.damage * 2

        # Checking if it was a headshot, if not normal damage applied
        if self.settings.headshot:
            j = random.randint(1, 20)
            if j == 1:
                self.kill()
                self.settings.target_exp += self.settings.comet_small_exp
        else:
            self.health -= self.settings.damage

        # Checking if comet is destroyed
        if self.health <= 0:
            self.settings.sound_environment_channel.play(self.settings.sound_comet_death)
            self.kill()
            self.settings.target_exp += self.settings.comet_small_exp
