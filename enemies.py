import pygame
import random
from graphical import Graphical
from bullet import BulletEnemy


class Enemies(Graphical):
    """Class that other EnemyGreen classes will inherit from"""

    def __init__(self, ai_game):
        """Enemies initialization"""
        super().__init__(ai_game)

        # Enemies image load
        self.image = self.settings.enemy_image
        self.image = pygame.transform.scale(self.image, (160, 81))

        # Enemies set dimensions
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(self.screen_rect.right - self.rect.width)
        self.rect.y = random.randrange(-1000, -200)
        self.rand_y = random.randrange(5, 162)

        # Enemies statistics
        self.speed = random.randint(2, 4)
        self.health = self.settings.enemy_health * self.settings.scale

    def shoot(self):
        """Makes enemies shoot bullet"""

        bullet = BulletEnemy(self, self.rect.centerx, self.rect.bottom)
        return bullet

    def hit(self):
        """Function executed when a enemy is being hit"""

        # Checking if it was a critical shot
        i = random.randint(1, 10)
        if i < self.settings.critical_chance:
            self.health -= self.settings.damage * 2

        # Checking if it was a headshot, if not normal damage applied
        if self.settings.headshot:
            j = random.randint(1, 60)
            if j == 1:
                self.kill()
                self.settings.target_exp += self.settings.enemy_exp
            else:
                self.health -= self.settings.damage
        else:
            self.health -= self.settings.damage

        # Checking if enemy is destroyed
        if self.health <= 0:
            self.settings.sound_enemy_death.set_volume(0.4)
            self.settings.sound_enemy_channel.play(self.settings.sound_enemy_death)
            self.kill()
            self.settings.target_exp += self.settings.enemy_exp

    def draw_enemy(self):
        """Drawing enemy function"""

        self.screen.blit(self.image, self.rect)


class EnemyGreen(Enemies):
    """Subclass that is used for green enemy management"""

    def __init__(self, ai_game):
        """Initialization of EnemyGreen object"""

        super().__init__(ai_game)
        self.health = self.settings.enemy_health * self.settings.scale

    def update(self):
        """Ship moving down the screen and shooting from some point"""

        if self.rect.y >= self.rand_y:
            self.rect.y = self.rand_y
            self.speed = 0
            self.settings.enemy_bullet_move = True
        else:
            self.rect.y += self.speed


class EnemyBlue(Enemies):
    """Subclass that is used for blue enemy management"""

    def __init__(self, ai_game):
        """Initialization of EnemyBlue object"""

        super().__init__(ai_game)
        self.speed = random.randrange(2, 4)
        self.health = self.settings.enemyblue_health * self.settings.scale
        self.starting_front = random.randint(1, 2)
        self.not_executed = True
        self.enemy_bullet_move = self.settings.enemy_bullet_move

    def update(self):
        """Enemy moving down to a certain point and then randomly goes right or left
            and while it reaches end of a screen it turns back"""

        if self.rect.y >= self.rand_y:
            self.rect.y = self.rand_y
            self.settings.enemy_bullet_move = True
            if self.starting_front == 1 and self.not_executed:
                self.speed = -self.speed
                self.not_executed = False
            if self.rect.x >= self.screen_rect.right - 160:
                self.speed = -self.speed
            elif self.rect.x <= 0:
                self.speed = -self.speed
            self.rect.x -= self.speed
        else:
            self.rect.y += self.speed


class EnemyRed(EnemyBlue):
    """Subclass that is used for red enemy management"""

    def __init__(self, ai_game):
        """Initialization of EnemyRed object which inherits from EnemyBlue"""

        super().__init__(ai_game)
        self.health = self.settings.enemyred_health * self.settings.scale

    def update(self):
        """Enemy moving down to a certain point and then randomly goes right or left
            and while it reaches end of a screen it disappears and shows on the other side of a screen"""

        if self.rect.y >= self.rand_y:
            self.rect.y = self.rand_y
            self.settings.enemy_bullet_move = True
            if self.starting_front == 1 and self.not_executed:
                self.speed = -self.speed
                self.not_executed = False
            if self.rect.x >= self.screen_rect.right - 10:
                self.rect.x = -150
                self.rect.x += self.speed
            elif self.rect.x <= -150:
                self.rect.x = self.screen_rect.right - 10
                self.rect.x += self.speed
            else:
                self.rect.x += self.speed
        else:
            self.rect.y += self.speed
