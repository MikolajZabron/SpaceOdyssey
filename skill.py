import pygame.image
from graphical import Graphical


class Skill(Graphical):
    """Class made for skill showcase"""

    def __init__(self, ai_game, skill, x=-100, y=-600):
        """Initialization of a skill box object"""
        super().__init__(ai_game)

        # Skill object image load and it's dimensions
        self.image = pygame.image.load(f"images/skill_{skill}.png").convert()
        self.rect = self.image.get_rect()

        # Skill object statistics and position on a screen
        self.speed = self.settings.skill_transition_speed
        self.rect.x = self.screen_rect.right / 2 + x
        self.rect.y = y

        # Drawing a skill while initializing a object
        self.draw_skill()

    def update(self):
        """Function responsible for skill box animation"""

        if self.rect.y >= self.screen_rect.bottom / 2 - 100:
            self.rect.y = self.screen_rect.bottom / 2 - 100
            self.speed = 0
        else:
            self.rect.y += self.speed
        self.draw_skill()

    def draw_skill(self):
        """Function responsible for drawing a skill box onto a screen"""

        self.screen.blit(self.image, self.rect)
