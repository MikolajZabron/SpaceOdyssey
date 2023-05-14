import pygame

class Menu:
    """Class for handling menu of a game"""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.font_title = pygame.font.Font("images/Bruno_Ace_SC/BrunoAceSC-Regular.ttf", 72)
        self.font = pygame.font.Font("images/Bruno_Ace_SC/BrunoAceSC-Regular.ttf", 56)
        self.menu_items = ['Play', 'Leaderboard', 'Exit']
        self.selected_item = 0

    def draw_menu(self):
        """Draws menu on a screen"""

        # Draws title of a game
        text = self.font_title.render("The Void Crew", True, self.settings.white)
        rect = text.get_rect(center=self.screen_rect.center)
        rect.y -= self.screen_rect.centery / 2 + 75
        self.screen.blit(text, rect)

        # Draws buttons on menu
        for i, item in enumerate(self.menu_items):
            if i == self.selected_item:
                color = self.settings.white
            else:
                color = (128, 128, 128)
            text = self.font.render(item, True, color)
            rect = text.get_rect(center=self.screen_rect.center)
            rect.y += i * 75
            self.screen.blit(text, rect)

    def handle_events(self, event):

        self.settings.sound_swipe.set_volume(100.0)
        if event.key == pygame.K_UP:
            self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            self.settings.sound_environment_channel.play(self.settings.sound_swipe)
        elif event.key == pygame.K_DOWN:
            self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            self.settings.sound_environment_channel.play(self.settings.sound_swipe)
        elif event.key == pygame.K_RETURN:
            if self.selected_item == 0:
                return True
            elif self.selected_item == 1:
                self.settings.sound_environment_channel.play(self.settings.sound_menu_interaction)
                self.settings.in_leaderboard = True
            elif self.selected_item == 2:
                pygame.mixer.quit()
                pygame.quit()
                quit()

