import sys
import pygame.font
import re

class Leaderboard:
    """Class for managing and displaying the leaderboard"""

    def __init__(self, ai_game):
        """Initialize leaderboard attributes"""

        # Game settings and screen initialization
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Font settings
        self.text_color = self.settings.white
        self.font = pygame.font.SysFont(self.settings.font_name, 48)

        # Load scores from file
        self.scores = []
        self.load_scores()

    def load_scores(self):
        """Load scores from file"""

        try:
            with open('scores.txt', 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        nickname, score = parts
                        self.scores.append((nickname, int(float(score))))
        except FileNotFoundError:
            pass

    def save_scores(self):
        """Save scores to file"""

        with open('scores.txt', 'w') as file:
            for nickname, score in self.scores:
                file.write(f"{nickname},{int(score)}\n")

    def add_score(self, nickname, score):
        """Add a new score to the leaderboard"""

        self.scores.append((nickname, int(score)))
        self.scores.sort(key=lambda x: x[1], reverse=True)
        self.scores = self.scores[:10]
        self.save_scores()

    def show(self):
        """Draw the leaderboard on the screen"""

        # Title of a leaderboard
        title_font = pygame.font.Font(self.settings.font_name, 56)
        title_text = title_font.render("Leaderboard", True, self.text_color)
        title_rect = title_text.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.top = 50

        # Names and scores settings and positions
        nickname_font = pygame.font.Font(self.settings.font_name, 32)
        score_font = pygame.font.Font(self.settings.font_name, 32)
        nicknames = [score[0] for score in self.scores]
        scores = [str(score[1]) for score in self.scores]
        nickname_labels = [nickname_font.render(nickname, True, self.text_color) for nickname in nicknames]
        score_labels = [score_font.render(score, True, self.text_color) for score in scores]
        x = self.screen_rect.right / 2 - 250
        y = title_rect.bottom + 50

        # Draw names and scores on a screen
        for i in range(len(self.scores)):
            nickname_label = nickname_labels[i]
            score_label = score_labels[i]

            self.screen.blit(nickname_label, (x + 10, y))
            self.screen.blit(score_label, (x + 335, y))

            y += nickname_label.get_height() + 10

        # Draw a table
        self.screen.blit(title_text, title_rect)
        pygame.draw.rect(self.screen, self.text_color, (x, title_rect.bottom + 30, 500, y - title_rect.bottom - 20)
                         , 3)

        # Draw the escape 'button'
        esc_text = nickname_font.render("<-ESC", True, self.text_color)
        esc_rect = esc_text.get_rect()
        esc_rect.bottom = self.screen_rect.bottom - 10
        esc_rect.left = 10
        self.screen.blit(esc_text, esc_rect)

        pygame.display.flip()

    def get_player_nickname(self):
        """Prompt the player to enter their nickname and return it"""
        nickname_rect = pygame.Rect(self.screen_rect.right / 2 - 250, self.screen_rect.bottom - 150, 500, 80)
        nickname = ""

        # Check key inputs from a user, also regex used so that the nickname only consists of letters and numbers
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.settings.sound_environment_channel.play(self.settings.sound_menu_interaction)
                        self.settings.in_leaderboard_sign = False
                        return nickname
                    elif event.key == pygame.K_BACKSPACE:
                        nickname = nickname[:-1]
                    else:
                        char = event.unicode
                        if re.match(r"[a-zA-Z0-9]", char) and len(nickname) < 10:
                            nickname += char

            # Draw the nickname entry rectangular
            pygame.draw.rect(self.screen, self.settings.black, nickname_rect)
            pygame.draw.rect(self.screen, self.settings.white, nickname_rect, 3)

            # Render and draw the current nickname being entered
            font = pygame.font.Font(self.settings.font_name, 32)
            text_surface = font.render(nickname, True, self.settings.white)
            text_rect = text_surface.get_rect()
            text_rect.center = nickname_rect.center
            self.screen.blit(text_surface, text_rect)

            # Update the screen
            pygame.display.flip()
