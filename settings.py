import pygame


class Settings:
    """Class where ale settings and constants are being kept"""

    def __init__(self):
        """Game settings initialization"""

        # FPS and clock settings
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.game_frozen = False
        self.game_paused = False

        # Screen settings
        self.screen_width = 1920
        self.screen_height = 1080
        pygame.display.set_caption("Space Shooter")
        self.bg_color = (255, 255, 255)

        # Player's spaceship settings
        self.ship_speed = 13
        self.level = 1
        self.damage = 10
        self.critical_chance = 1

        # Player's health settings
        self.health = 0
        self.max_health = 200

        # Player's transition set up
        self.transition_change_speed = 5
        self.target_health = 200
        self.target_exp = 0

        self.skill_transition_speed = 12

        # Player's experience settings
        self.exp_points = 0
        self.exp_need = 1000
        self.exp_need_multiplier = 1.5
        self.exp_bar_width = 600
        self.exp_ratio = self.exp_need / self.exp_bar_width
        self.message_var = 0

        # BulletPlayer settings
        self.bullet_speed = 15.0
        self.fire_rate = 450
        self.double = False
        self.vertical = False

        # Headshot
        self.headshot = False

        # Second life
        self.second_life = False

        # Comet settings
        self.comet_health = 30
        self.comet_exp = 100
        self.collision_damage = 100
        self.comet_spawn_num = 6

        # Comet Small settings
        self.comet_small_health = 15
        self.comet_small_exp = 50
        self.comet_small_spawn_num = 3

        # Green enemy settings
        self.enemy_health = 120
        self.enemy_spawn_time = 20
        self.enemy_exp = 500
        self.enemy_last_shot_time = 0
        self.enemy_fire_rate = 1000
        self.enemy_bullet_move = False
        self.enemy_bullet_speed = 5
        self.enemy_dmg = 100

        # Blue enemy settings
        self.enemyblue_health = 80

        # Red enemy settings
        self.enemyred_health = 100

        # Boss settings
        self.boss_health = 2000
        self.boss_speed = 1
        self.boss_last_shot_time = 0
        self.boss_fire_rate = 40
        self.boss_bullet_move = False
        self.boss_bullet_speed = 3
        self.boss_dmg = 100
        self.boss_not_alive = True
        self.boss_spawn_time = 150

        # Scaling difficulty level
        self.scale = 1
        self.endless_mode = False

        # Colours
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)

        # Level bar settings
        self.bar_width = 500
        self.bar_height = 10
