import sys
import pygame
import random
import time
import threading
import pygame.mixer
from settings import Settings
from player import Player
from bullet import BulletPlayer
from bullet import BulletVertical
from comet import Comet
from comet import CometSmall
from skill import Skill
from enemies import EnemyGreen
from enemies import EnemyBlue
from enemies import EnemyRed
from boss import Boss
from menu import Menu
from leaderboard import Leaderboard


class SpaceShooter:
    """Class for the game in whole"""

    def __init__(self):
        """Game initialization"""
        pygame.init()
        pygame.mixer.init()

        # Game and screen settings
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.running = True

        # Font set
        self.level_font = pygame.font.Font(None, 12)
        self.level_font_outline = pygame.font.Font(None, 14)

        # Music settings
        pygame.mixer.set_num_channels(4)
        self.songs = self.settings.songs
        self.menu_music = self.settings.menu_music
        self.boss_song = self.settings.boss_song
        self.song_channel = self.settings.song_channel
        self.sound_player_channel = self.settings.sound_player_channel
        self.sound_enemy_channel = self.settings.sound_enemy_channel
        self.sound_environment_channel = self.settings.sound_environment_channel
        self.previous_song = None
        self.play_menu_song()

        # Creating ship object and it's attributes
        self.ship = Player(self)
        self.last_shot_time = 0
        self.bullet_move = False

        # Defining a sprite groups
        self.bullets = pygame.sprite.Group()
        self.comets = pygame.sprite.Group()
        self.skills = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()

        # Skill selection boolean variables and skill list initialization
        self.left = False
        self.mid = False
        self.right = False
        self.once = True
        self.once2 = True
        self.skill_list = []

        # Game time track init
        self.start_time = time.time()
        self.spawn_time = 0
        self.spawn_interval = 0
        self.enemy_spawn_time = pygame.time.get_ticks()

        self.selected = 1
        self.selected_skill_index = 1

        # Background transition
        self.background = self.settings.background
        self.bg_height = self.background.get_height()
        self.scroll = - self.bg_height + self.settings.screen_height
        self.scroll2 = - self.bg_height + self.settings.screen_height

        # Menu and leaderboard initialization
        self.menu = Menu(self)
        self.leaderboard = Leaderboard(self)

    def run_game(self):
        """Main game loop"""

        while self.running:
            self.settings.clock.tick(self.settings.FPS)
            self._check_events()
            if not self.settings.game_frozen and not self.settings.in_menu and not self.settings.in_leaderboard:
                self.elapsed_time = time.time() - self.start_time
                self.boss_elapsed_time = time.time() - self.start_time
                self.ship.update()
                self._bullet_update()
                self.environment_respawn()
                self.comets.update()
                self.enemies.update()
                self.bosses.update()
                self.level_management()
            elif self.settings.game_frozen:
                self.attribute_draw()
            self._update_screen()

    def _check_events(self):
        """Key press triggers different operations"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Check when key is pressed it can move in four directions"""

        # Spaceship movement and shooting
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self.bullet_move = True

        # Game quit and skill picking
        elif event.key == pygame.K_q:
            pygame.mixer.quit()
            sys.exit()
        if self.settings.game_frozen:
            self.settings.sound_swipe.set_volume(100.0)
            if event.key == pygame.K_LEFT:
                for skill in self.skills:
                    self.sound_environment_channel.play(self.settings.sound_swipe)
                    skill.selected = False
                self.selected_skill_index = (self.selected_skill_index - 1) % len(self.skill_list)
                self.skills.sprites()[self.selected_skill_index].selected = True
            elif event.key == pygame.K_RIGHT:
                for skill in self.skills:
                    self.sound_environment_channel.play(self.settings.sound_swipe)
                    skill.selected = False
                self.selected_skill_index = (self.selected_skill_index + 1) % len(self.skill_list)
                self.skills.sprites()[self.selected_skill_index].selected = True
            elif event.key == pygame.K_RETURN:
                self.sound_environment_channel.play(self.settings.sound_menu_interaction)
                if self.selected_skill_index == 0:
                    self.left = True
                if self.selected_skill_index == 1:
                    self.mid = True
                elif self.selected_skill_index == 2:
                    self.right = True

        # Exiting a leaderboard by pressing ESC key input
        if self.settings.in_leaderboard:
            if event.key == pygame.K_ESCAPE:
                self.sound_environment_channel.play(self.settings.sound_menu_interaction)
                self.settings.in_leaderboard = False
                self.settings.in_menu = True

        # Starting a game
        if self.settings.in_menu:
            if self.menu.handle_events(event):
                self.settings.in_menu = False
                self.play_random_song()
                self.sound_environment_channel.play(self.settings.sound_game_start)
                self._reset_game()

    def _check_keyup_events(self, event):
        """Check when key is not pressed it stops moving in any direction"""

        # Stop of a spaceship movement and shooting
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_SPACE:
            self.bullet_move = False

    def play_random_song(self):
        """Plays randomly chosen song"""

        self.available_songs = list(set(self.songs) - {self.previous_song})
        if self.available_songs:
            random_song = random.choice(self.available_songs)
            self.song_channel.set_volume(0.2)
            self.song_channel.play(random_song, 0, 0, 0)
        else:
            self.available_songs = self.songs
            self.previous_song = None

    def play_menu_song(self):
        """Plays menu song"""

        self.song_channel.set_volume(1.0)
        self.menu_music.set_volume(0.4)
        self.song_channel.play(self.menu_music, 1, 0, 5000)

    def attribute_draw(self):
        """Drawing skill and skill pick management"""

        # Randomly skill picking
        while self.once:
            self.skill_list = []
            while len(self.skill_list) < 3:
                skill = self.skill_lottery()
                if skill < 10 and skill not in self.skill_list:
                    self.skill_list.append(skill)

            # Drawing skills on a screen
            left = Skill(self, self.skill_list[0], -400, -300)
            self.skills.add(left)
            mid = Skill(self, self.skill_list[1])
            # mid.selected = True
            self.skills.add(mid)
            right = Skill(self, self.skill_list[2], 200, -900)
            self.skills.add(right)

            self.once = False

        self.attribute_pick()

    def attribute_pick(self):
        """Let user pick a skill"""

        # Pick option
        if self.left:
            self.left = False
            self.skills.sprites()[0].selected = True
            self.ship.skill_choice(self.skill_list[0])
            self.skills.empty()
        if self.mid:
            self.mid = False
            self.skills.sprites()[1].selected = True
            self.ship.skill_choice(self.skill_list[1])
            self.skills.empty()
        if self.right:
            self.right = False
            self.skills.sprites()[2].selected = True
            self.ship.skill_choice(self.skill_list[2])
            self.skills.empty()

        # Update the selection using arrows
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    for skill in self.skills:
                        skill.selected = False
                    self.skills.sprites()[0].selected = True
                elif event.key == pygame.K_RIGHT:
                    for skill in self.skills:
                        skill.selected = False
                    self.skills.sprites()[2].selected = True
                elif event.key == pygame.K_RETURN:
                    if self.selected == 0:
                        self.left = True
                    if self.selected == 1:
                        self.mid = True
                    elif self.selected == 2:
                        self.right = True

    def fire_bullet(self):
        """Function that creates bullet"""

        if self.settings.double:
            left_bullet = BulletPlayer(self, self.ship.rect_bullet_fire)
            right_bullet = BulletPlayer(self, 2.5 * self.ship.rect_bullet_fire)
            self.bullets.add(left_bullet)
            self.bullets.add(right_bullet)
            if self.settings.vertical:
                self._bullet_vertical()
        else:
            bullet = BulletPlayer(self, self.ship.rect_bullet_fire * 1.75)
            self.bullets.add(bullet)
            if self.settings.vertical:
                self._bullet_vertical()

    def _bullet_vertical(self):
        """Function which makes player shoot bullets vertically"""

        left_vertical = BulletVertical(self)
        right_vertical = BulletVertical(self, 0, -10, True)
        self.bullets.add(left_vertical)
        self.bullets.add(right_vertical)

    def fire_enemy_bullet(self):
        """Function that creates enemy bullets and time delay between boss shots"""

        time_since_last_shot = pygame.time.get_ticks() - self.settings.boss_last_shot_time
        for enemy in self.enemies.sprites():
            self.enemy_bullets.add(enemy.shoot())
        if self.settings.boss_bullet_move and time_since_last_shot > self.settings.boss_fire_rate:
            for boss in self.bosses.sprites():
                self.enemy_bullets.add(boss.shoot())
                self.enemy_bullets.add(boss.shoot())
                self.enemy_bullets.add(boss.shoot())
                self.enemy_bullets.add(boss.shoot())
                self.settings.boss_last_shot_time = pygame.time.get_ticks()

    def _bullet_update(self):
        """Creating bullets and time delay between shots"""

        self.bullets.update()
        time_since_last_shot = pygame.time.get_ticks() - self.last_shot_time
        if self.bullet_move and time_since_last_shot > self.settings.fire_rate:
            self.fire_bullet()
            self.last_shot_time = pygame.time.get_ticks()
        self._bullet_clear()
        self._enemy_bullet_update()

    def _enemy_bullet_update(self):
        """Creating enemy bullets and time delay between shots"""

        self.enemy_bullets.update()
        time_since_last_shot = pygame.time.get_ticks() - self.settings.enemy_last_shot_time
        if self.settings.enemy_bullet_move and \
                time_since_last_shot > self.settings.enemy_fire_rate / self.settings.scale:
            self.fire_enemy_bullet()
            self.settings.enemy_last_shot_time = pygame.time.get_ticks()
        self._enemy_bullet_clear()

    def _bullet_clear(self):
        """Removing bullets that went out a screen"""

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            if bullet.rect.left >= 1600:
                self.bullets.remove(bullet)
            if bullet.rect.right <= 0:
                self.bullets.remove(bullet)

    def _enemy_bullet_clear(self):
        """Removing enemy bullets that went out a screen"""

        for bullet in self.enemy_bullets.copy():
            if bullet.rect.top >= 1000:
                self.enemy_bullets.remove(bullet)

    def boss_spawn(self):
        """Spawning boss if defined time elapsed"""
        if self.boss_elapsed_time >= self.settings.boss_spawn_time - 10 and self.settings.boss_not_alive \
                and not self.settings.endless_mode and self.once:
            self.song_channel.fadeout(5500)
            self.once = False
        if self.boss_elapsed_time >= self.settings.boss_spawn_time - 4.5 and self.settings.boss_not_alive \
                and not self.settings.endless_mode and self.once2:
            self.boss_song.set_volume(1.5)
            self.song_channel.play(self.boss_song, 1, 0, 5000)
            self.once2 = False
        if self.boss_elapsed_time >= self.settings.boss_spawn_time and self.settings.boss_not_alive \
                and not self.settings.endless_mode:
            self.settings.boss_not_alive = False
            self.once = True
            self.once2 = True
            boss = Boss(self)
            self.bosses.add(boss)

    def comet_create(self):
        """Creating x comets and showing them to a screen"""

        for comet in self.comets.sprites():
            comet.draw_comet()

    def enemy_create(self):
        """Creating enemies and showing them in to a screen"""

        for enemy in self.enemies.sprites():
            enemy.draw_enemy()

    def _comet_add(self):
        """Simple function that add comet"""

        comet = Comet(self)
        self.comets.add(comet)

    def _comet_small_add(self):
        """Simple function that add small comet"""

        comet = CometSmall(self)
        self.comets.add(comet)

    def enemy_counter(self):
        """Function that is creating enemies and checking their collision"""

        # Spawn random enemy if defined elapsed time will pass
        current_time = pygame.time.get_ticks()
        if current_time - self.enemy_spawn_time >= self.spawn_interval and self.settings.boss_not_alive:
            self.enemy_spawn_time = current_time
            self.spawn_interval = 20000
            i = random.randint(1, 3)
            if i == 1:
                enemy = EnemyGreen(self)
                self.enemies.add(enemy)
            elif i == 2:
                enemy = EnemyBlue(self)
                self.enemies.add(enemy)
            elif i == 3:
                enemy = EnemyRed(self)
                self.enemies.add(enemy)

        # Check for an enemy and bullet collision
        for bullet in self.bullets:
            collisions = pygame.sprite.groupcollide(
                self.enemies, self.bullets, False, self.settings.vertical)
            for enemy in collisions:
                enemy.hit()
                self.bullets.remove(bullet)

        # Check for a boss and bullet collision
        for bullet in self.bullets:
            collisions = pygame.sprite.groupcollide(
                self.bosses, self.bullets, False, self.settings.vertical)
            for boss in collisions:
                boss.hit()
                self.elapsed_time = 0
                self.bullets.remove(bullet)

        # Check for a boss and enemy collision
        pygame.sprite.groupcollide(self.bosses, self.enemies, False, True)

    def comet_counter(self):
        """Function that is creating comet if there is not x of them on a screen"""

        # Spawns missing comets after every comet destroyed
        if len(self.comets) < self.settings.comet_spawn_num + self.settings.comet_small_spawn_num \
                and self.settings.boss_not_alive:
            for i in range(self.settings.comet_small_spawn_num):
                self._comet_small_add()
            for i in range(self.settings.comet_spawn_num):
                self._comet_add()

        # Detecting comet collisions with bullets
        for bullet in self.bullets:
            collisions = pygame.sprite.groupcollide(
                self.comets, self.bullets, False, self.settings.vertical)
            for comet in collisions:
                comet.hit()
                self.bullets.remove(bullet)

        # Comet will destroy when they will cross bottom of a screen
        for comet in self.comets.copy():
            if comet.rect.top >= self.settings.screen_height:
                self.comets.remove(comet)

    def player_collisions(self):
        """Function that detects player collisions"""

        # Check for collisions between ship and comets
        collisions = pygame.sprite.spritecollide(
            self.ship, self.comets, True)
        if collisions:
            self.ship.get_damage(self.settings.collision_damage)
            self.player_game_validate()

        # Check for collisions between ship and enemies
        collisions = pygame.sprite.spritecollide(
            self.ship, self.enemies, True)
        if collisions:
            self.ship.get_damage(self.settings.collision_damage)
            self.player_game_validate()

        # Check for collisions between ship and enemy bullets
        for bullet in self.enemy_bullets:
            collisions = pygame.sprite.spritecollide(
                self.ship, self.enemy_bullets, True)
            if collisions:
                self.ship.get_damage(self.settings.enemy_dmg)
                self.bullets.remove(bullet)
                self.player_game_validate()

    def player_game_validate(self):
        """Checking if player is still alive"""

        if self.ship.health <= 0:
            self.sound_player_channel.play(self.settings.sound_player_death)
            if self.settings.second_life:
                self.settings.second_life = False
                self.ship.get_health(self.settings.max_health / 2)
            else:
                self.settings.in_leaderboard = True
                self.settings.in_leaderboard_sign = True
                self.play_menu_song()

    def level_management(self):
        """Level management, and level update function"""

        self.ship.target_exp = self.settings.target_exp
        if self.ship.target_exp >= self.settings.exp_need:
            self.sound_player_channel.play(self.settings.sound_level_up)
            self.settings.level += 1
            self.settings.scale += 0.25
            if self.settings.endless_mode:
                self.settings.scale += 0.25
            self.settings.target_exp -= self.settings.exp_need
            self.settings.exp_need = self.settings.exp_need * self.settings.exp_need_multiplier
            self.ship.exp_ratio = self.settings.exp_bar_width / self.settings.exp_need
            self.settings.game_frozen = True
            self.once = True

    def skill_lottery(self):
        """Three skills will be randomly chosen to pick from"""

        i = random.randint(1, 9)
        # DMG bonus
        if i == 1:
            return i
        # MAX Health bonus
        elif i == 2:
            return i
        # Heal bonus
        elif i == 3:
            return i
        # Critical Chance bonus
        elif i == 4:
            return i
        # Attack Speed bonus
        elif i == 5:
            return i
        # Double Shot bonus
        elif i == 6 and not self.settings.double and not self.settings.vertical:
            return i
        # If double shot or vertical are turned on, then skill will be randomly chosen again
        elif i == 6 and self.settings.double or self.settings.vertical:
            return i * 2
        # Diagonal Shot bonus
        elif i == 7 and not self.settings.vertical and not self.settings.double:
            return i
        # If vertical shot or double are turned on, then skill will be randomly chosen again
        elif i == 7 and self.settings.vertical or not self.settings.double:
            return i * 2
        # Headshot bonus
        if i == 8 and not self.settings.headshot:
            return i
        # If headshot is turned on it cannot be chosen again
        elif i == 8 and self.settings.headshot:
            return i * 2
        # Second life bonus
        elif i == 9 and not self.settings.second_life:
            return i
        # If second life bonus was chosen before it cannot be once again
        elif i == 9 and self.settings.second_life:
            return i * 2
        else:
            return i * 100

    def bonus_message_drawing(self):
        """Temporary function for drawing a message on a screen about recently picked skill"""

        if self.settings.message_var == 1:
            self.ship.message_bonus("DMG BONUS")
        if self.settings.message_var == 2:
            self.ship.message_bonus("MAX HP BONUS")
        if self.settings.message_var == 3:
            self.ship.message_bonus("HEAL BONUS")
        if self.settings.message_var == 4:
            self.ship.message_bonus("CRITICAL CHANCE BONUS")
        if self.settings.message_var == 5:
            self.ship.message_bonus("ATTACK SPEED BONUS")
        if self.settings.message_var == 6:
            self.ship.message_bonus("DOUBLE SHOT BONUS")
        if self.settings.message_var == 7:
            self.ship.message_bonus("DIAGONAL SHOT BONUS")
        if self.settings.message_var == 8:
            self.ship.message_bonus("HEADSHOT BONUS")
        if self.settings.message_var == 9:
            self.ship.message_bonus("SECOND LIFE BONUS")

    def environment_respawn(self):
        """Clean function that spawn environment"""

        thread1 = threading.Thread(self.comet_counter())
        thread1.start()
        self.enemy_counter()
        self.player_collisions()
        self.boss_spawn()
        thread1.join()


    def _reset_game(self):
        """Reset game initializations"""

        self.settings.level = self.settings.level_res
        self.settings.damage = self.settings.damage_res
        self.settings.critical_chance = self.settings.critical_chance_res
        self.ship.health = self.settings.health_res
        self.ship.target_health = self.settings.target_health_res
        self.settings.max_health = self.settings.max_health_res
        self.settings.target_exp = self.settings.target_exp_res
        self.settings.exp_points = self.settings.exp_points_res
        self.settings.exp_need = self.settings.exp_need_res
        self.settings.message_var = self.settings.message_var_res
        self.settings.fire_rate = self.settings.fire_rate_res
        self.settings.double = self.settings.double_res
        self.settings.vertical = self.settings.vertical_res
        self.settings.headshot = self.settings.headshot_res
        self.settings.second_life = self.settings.second_life_res
        self.settings.comet_health = self.settings.comet_health_res
        self.settings.comet_small_health = self.settings.comet_small_health_res
        self.settings.enemy_health = self.settings.enemy_health_res
        self.settings.enemy_fire_rate = self.settings.enemy_fire_rate_res
        self.settings.enemy_bullet_move = self.settings.enemy_bullet_move_res
        self.settings.enemy_bullet_speed = self.settings.enemy_bullet_speed_res
        self.settings.enemyblue_health = self.settings.enemyblue_health_res
        self.settings.enemyred_health = self.settings.enemyred_health_res
        self.settings.scale = self.settings.scale_res
        self.settings.endless_mode = self.settings.endless_mode_res
        self.settings.boss_spawn_time = self.settings.boss_spawn_time_res
        self.settings.boss_not_alive = self.settings.boss_not_alive_res

        self.ship.reset_position()
        self.comets.empty()
        self.enemies.empty()
        self.bullets.empty()
        self.bosses.empty()
        self.enemy_bullets.empty()

        self.enemy_spawn_time = pygame.time.get_ticks()
        self.start_time = time.time()
        self.settings.boss_elapsed_time = None
        self.spawn_interval = self.settings.spawn_interval_res

    def _background_transition(self):
        """Function responsible for scrolling a background"""

        self.screen.blit(self.background, (0, self.scroll))
        self.screen.blit(self.background, (0, self.scroll2))

        self.scroll += 0.5
        if self.scroll == 0:
            self.scroll2 = - self.bg_height

        self.scroll2 += 0.5
        if self.scroll2 == 0:
            self.scroll = - self.bg_height

    def _update_screen(self):
        """Showing updates of a screen"""

        # Background and environment drawing
        self._background_transition()
        self.ship.blit_me()
        self.comet_create()
        self.enemy_create()

        # Drawing of boss
        if not self.settings.boss_not_alive:
            for boss in self.bosses.sprites():
                boss.draw_boss()

        # Drawing bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Drawing enemy bullets
        for bullet in self.enemy_bullets.sprites():
            bullet.draw_bullet()

        # Level and health bar draw
        self.ship.health_bar()
        self.ship.level_bar()
        self.bonus_message_drawing()

        # Playing a song when one just finished playing
        if not pygame.mixer.Channel(0).get_busy():
            self.play_random_song()

        if self.settings.endless_mode and self.once2:
            self.play_random_song()
            self.once2 = False

        # Drawing skill boxes on a screen
        if self.settings.game_frozen:
            self.skills.update()

        if self.settings.in_menu and not self.settings.in_leaderboard:
            self.menu.draw_menu()

        if self.settings.in_leaderboard and not self.settings.in_leaderboard_sign:
            self.leaderboard.show()

        if self.settings.in_leaderboard and self.settings.in_leaderboard_sign:
            self.leaderboard.show()
            score = (self.settings.level - 1) * self.settings.exp_need / self.settings.exp_need_multiplier \
                    + self.ship.target_exp
            self.leaderboard.add_score(self.leaderboard.get_player_nickname(), score)
            self.leaderboard.save_scores()

        # Showing last modified screen
        pygame.display.flip()


if __name__ == '__main__':
    """Creating and executing a game"""
    ai = SpaceShooter()
    ai.run_game()
