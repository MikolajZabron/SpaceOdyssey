import pygame
from graphical import Graphical


class Player(Graphical):
    """Class made for defining a player's ship and manipulating it"""

    def __init__(self, ai_game):
        """Player's spaceship initialization"""
        super().__init__(ai_game)

        # Font set
        self.font = pygame.font.Font("images/Bruno_Ace_SC/BrunoAceSC-Regular.ttf", 32)
        self.level_font_outline = pygame.font.Font("images/Bruno_Ace_SC/BrunoAceSC-Regular.ttf", 20)

        # Spaceship image load
        self.image = self.settings.player_image
        self.image = pygame.transform.scale(self.image, (60, 120))
        self.rect = self.image.get_rect()

        # Health
        self.health = self.settings.health

        # Experience and health transition
        self.transition_change_speed = self.settings.transition_change_speed
        self.target_health = self.settings.target_health
        self.target_exp = self.settings.target_exp

        # Experience
        self.exp = self.settings.exp_points
        self.exp_ratio = self.settings.exp_bar_width / self.settings.exp_need

        # Position of a bullets
        self.rect_bullet_fire = self.rect.centerx / 2

        # Position of a player's spaceship
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y = self.screen_rect.bottom - 164
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Player's movement boolean variables
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Player's spaceship position update"""

        if self.moving_right:
            self.x += self.settings.ship_speed
        if self.x > self.screen_rect.right - 30:
            self.x = - 30
        if self.moving_left:
            self.x -= self.settings.ship_speed
        if self.x < - 30:
            self.x = self.screen_rect.right - 30
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        self.rect.x = self.x
        self.rect.y = self.y

        self.health_bar()
        self.level_bar()

    def get_damage(self, amount):
        """Player damage function"""

        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health <= 0:
            self.target_health = 0

    def get_health(self, amount):
        """Player heal function"""

        if self.target_health < self.settings.max_health:
            self.target_health += amount
        if self.target_health >= self.settings.max_health:
            self.target_health = self.settings.max_health

    def health_bar(self):
        """Drawing of a health bar"""
        if not self.settings.in_menu:

            # Animation of a health bar
            if self.health < self.target_health:
                self.health += self.transition_change_speed
            if self.health > self.target_health:
                self.health -= self.transition_change_speed

            # Drawing on a screen a health bar
            pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_rect.right / 2 - self.health / 2, 839, self.health, 4))
            pygame.draw.rect(self.screen, (76, 72, 76), (self.screen_rect.right / 2 - self.settings.max_health / 2, 838,
                                                         self.settings.max_health, 6), 1, 5)

    def level_bar(self):
        """Level bar drawing function"""

        if not self.settings.in_menu:

            # Animation of a level bar
            if self.exp < self.target_exp:
                self.exp += self.transition_change_speed
            if self.exp > self.target_exp:
                self.exp -= self.transition_change_speed

            # Drawing on a screen a level_bar
            pygame.draw.rect(self.screen, (0, 255, 0), (self.screen_rect.right / 2 - (self.exp * self.exp_ratio) / 2,
                                                        851, self.exp * self.exp_ratio, 6))
            pygame.draw.rect(self.screen, (76, 72, 76), (self.screen_rect.right / 2 - self.settings.exp_bar_width / 2,
                                                         850, self.settings.exp_bar_width, 8), 1, 5)

            # Drawing on a screen a level number
            text = self.level_font_outline.render(str(self.settings.level), True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (self.screen_rect.right / 2, 854)
            self.screen.blit(text, text_rect)

    def skill_choice(self, i):
        """Function which selects bonus coming with currently picked skill"""

        if i == 1:
            self.skill_damage(i)
        elif i == 2:
            self.skill_hp_max(i)
        elif i == 3:
            self.skill_hp_resp(i)
        elif i == 4:
            self.skill_critic(i)
        elif i == 5:
            self.skill_atk_speed(i)
        elif i == 6:
            self.skill_double(i)
        elif i == 7:
            self.skill_diagonal(i)
        elif i == 8:
            self.skill_hs(i)
        elif i == 9:
            self.skill_sl(i)
        self.settings.game_frozen = False

    def skill_damage(self, i):
        """Function which adds damage"""

        self.settings.damage += self.settings.damage * 0.5
        self.settings.message_var = i

    def skill_hp_max(self, i):
        """Function which increases max health"""

        self.settings.max_health += self.settings.max_health * 0.5
        self.settings.message_var = i

    def skill_hp_resp(self, i):
        """Function which restores missing health"""

        if self.target_health < self.settings.max_health:
            self.target_health += self.settings.max_health * 0.5
        self.settings.message_var = i

    def skill_critic(self, i):
        """Function which increase critical chance"""

        if self.settings.critical_chance < 10:
            self.settings.critical_chance = self.settings.critical_chance * 2
        else:
            self.settings.critical_chance = 10
        self.settings.message_var = i

    def skill_atk_speed(self, i):
        """Function which increases fire rate of a player's ship"""

        self.settings.fire_rate -= self.settings.fire_rate * 0.2
        self.settings.message_var = i

    def skill_double(self, i):
        """Function which turns on a double shot"""

        self.settings.double = True
        self.settings.message_var = i

    def skill_diagonal(self, i):
        """Function which turns on a vertical shot"""

        self.settings.vertical = True
        self.settings.message_var = i

    def skill_hs(self, i):
        """Function which turns on a headshot chance"""

        self.settings.headshot = True
        self.settings.message_var = i

    def skill_sl(self, i):
        """Function which gives a player a second life"""

        self.settings.second_life = True
        self.settings.message_var = i

    def message_bonus(self, message):
        """Printing message when leveling up(Temporary)"""

        text = self.font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(centery=self.screen_rect.bottom - 50)
        text_rect.right = self.screen_rect.right - 20
        self.screen.blit(text, text_rect)

    def reset_position(self):
        """Resets ship position when playing again a game"""

        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y = self.screen_rect.bottom - 164

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def blit_me(self):
        """Drawing spaceship on a screen"""

        self.screen.blit(self.image, self.rect)
