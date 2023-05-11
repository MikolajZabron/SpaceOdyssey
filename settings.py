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
        self.in_menu = True
        self.in_leaderboard = False
        self.in_leaderboard_sign = False
        self.reset_game = False

        # Screen settings
        self.screen_width = 1920
        self.screen_height = 1080
        pygame.display.set_caption("Space Shooter")
        self.background = pygame.image.load("images/background_3.jpg")
        self.bg_color = (255, 255, 255)
        self.font = pygame.font.Font("images/Bruno_Ace_SC/BrunoAceSC-Regular.ttf", 56)
        self.font_name = "images/Bruno_Ace_SC/BrunoAceSC-Regular.ttf"

        # Channels Initializer
        self.song_channel = pygame.mixer.Channel(0)
        self.sound_player_channel = pygame.mixer.Channel(1)
        self.sound_enemy_channel = pygame.mixer.Channel(2)
        self.sound_environment_channel = pygame.mixer.Channel(3)
        self.song_channel.set_volume(0.5)
        self.sound_player_channel.set_volume(0.4)
        self.sound_enemy_channel.set_volume(0.4)
        self.sound_environment_channel.set_volume(0.4)

        # Songs Initializer
        self.songs = []
        for i in range(1, 6):
            song = pygame.mixer.Sound(f"sounds/game_music_{i}.mp3")
            self.songs.append(song)
        self.menu_music = pygame.mixer.Sound("sounds/menu_music.mp3")

        # Sounds Initializer
        self.sound_game_start = pygame.mixer.Sound("sounds/game_start.mp3")
        self.sound_level_up = pygame.mixer.Sound("sounds/level_up.mp3")
        self.sound_menu_interaction = pygame.mixer.Sound("sounds/menu_interaction.mp3")
        self.sound_player_death = pygame.mixer.Sound("sounds/player_death.mp3")
        self.sound_player_shot = pygame.mixer.Sound("sounds/player_shot2.mp3")
        self.sound_swipe = pygame.mixer.Sound("sounds/swipe.mp3")
        self.sound_comet_death = pygame.mixer.Sound("sounds/comet_death_2.mp3")
        self.sound_enemy_death = pygame.mixer.Sound("sounds/enemy_death.mp3")
        self.sound_enemy_shot = pygame.mixer.Sound("sounds/enemy_shot.mp3")
        self.sound_boss_death = pygame.mixer.Sound("sounds/boss_explosion.mp3")
        self.sound_player_shot.set_volume(0.2)

        # Player's spaceship settings
        self.player_image = pygame.image.load("images/player_1.png")
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

        # Skill settings
        self.skill_transition_speed = 12

        # Player's experience settings
        self.exp_points = 0
        self.exp_need = 1000
        self.exp_need_multiplier = 1.5
        self.exp_bar_width = 600
        self.exp_ratio = self.exp_need / self.exp_bar_width
        self.message_var = 0

        # BulletPlayer settings
        self.bullet_img = pygame.image.load("images/bullet.png")
        self.bullet_speed = 15.0
        self.fire_rate = 450
        self.double = False
        self.vertical = False

        # Headshot
        self.headshot = False

        # Second life
        self.second_life = False

        # Comet settings
        self.comet_image = pygame.image.load("images/comet.png")
        self.comet_health = 30
        self.comet_exp = 100
        self.collision_damage = 100
        self.comet_spawn_num = 6

        # Comet Small settings
        self.comet_small_health = 15
        self.comet_small_exp = 50
        self.comet_small_spawn_num = 3

        # Green enemy settings
        self.enemy_image = pygame.image.load("images/enemy.png")
        self.enemy_bullet_img = pygame.image.load("images/enemy_bullet.png")
        self.enemy_health = 120
        self.enemy_spawn_time = 15
        self.spawn_interval = 0
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
        self.boss_image = pygame.image.load("images/Boss.png")
        self.boss_song = pygame.mixer.Sound("sounds/game_music_boss.mp3")
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

        # Reset game storage variables
        self.level_res = self.level
        self.damage_res = self.damage
        self.critical_chance_res = self.critical_chance
        self.health_res = self.health
        self.target_health_res = self.target_health
        self.max_health_res = self.max_health
        self.target_exp_res = self.target_exp
        self.exp_points_res = self.exp_points
        self.exp_need_res = self.exp_need
        self.message_var_res = self.message_var
        self.fire_rate_res = self.fire_rate
        self.double_res = self.double
        self.vertical_res = self.vertical
        self.headshot_res = self.headshot
        self.second_life_res = self.second_life
        self.comet_health_res = self.comet_health
        self.comet_small_health_res = self.comet_small_health
        self.enemy_health_res = self.enemy_health
        self.enemy_fire_rate_res = self.enemy_fire_rate
        self.enemy_bullet_move_res = self.enemy_bullet_move
        self.enemy_bullet_speed_res = self.enemy_bullet_speed
        self.enemyblue_health_res = self.enemyblue_health
        self.enemyred_health_res = self.enemyred_health
        self.scale_res = self.scale
        self.endless_mode_res = self.endless_mode
        self.boss_spawn_time_res = self.boss_spawn_time
        self.boss_not_alive_res = self.boss_not_alive
        self.spawn_interval_res = self.spawn_interval

        # Colours
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.white = (255, 255, 255)

        # Level bar settings
        self.bar_width = 500
        self.bar_height = 10
