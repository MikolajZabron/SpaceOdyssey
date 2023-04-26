from pygame.sprite import Sprite


class Graphical(Sprite):
    """Initialize class for graphical objects"""

    def __init__(self, ai_game):
        """Initialization of graphical objects"""
        super().__init__()

        # Game screen and settings initialization
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
    