import pygame
import sys
import random
import os
from meowchi import Meowchi
from enemy import TikusDapur, TikusPutih, Anjing, Meowzho
from image_button import ImageButton
from dialogbox import DialogBox


class GameManager:
    def __init__(self, screen, WIDTH, HEIGHT):
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.score = 0
        self.dialog_box = None
        self.show_dialog = False

        try:
            pygame.mixer.init()
            pygame.mouse.set_visible(False)
            self.button_font = pygame.font.Font("Assets/font/PixelPurl.ttf", 36)
            self.score_font = pygame.font.Font("Assets/font/PixelPurl.ttf", 64)  
            self.cursor_image = pygame.image.load("Assets/meowchi/cursor.png").convert_alpha()
            self.cursor_image = pygame.transform.scale(self.cursor_image, (32, 32))
            self.menu_bg = pygame.image.load(os.path.join("Assets/Background/background_menu.png"))
            self.menu_bg = pygame.transform.scale(self.menu_bg, (WIDTH, HEIGHT))
        except Exception as e:
            print(f"[ERROR loading assets in __init__]: {e}")

        self.state = "menu"  # state: "menu", "game", "endgame"
        self.running = True

        self.bg_x = 0
        self.scroll_speed = 1

        self.init_menu()
        self.init_game(1)
        self.dogs_killed = 0
        self.cats_killed = 0
        
        self.fade_alpha = 0
        self.fade_done = False
        self.endgame_text = [
            "We did it... Meowzho has been defeated.",
            "The kitchen is safe once again, thanks to you.",
            "But I will keep my chef hat ready...just in case another war brews.",
            "Until then... see you in the next MeoWAR!"
        ]
        self.endgame_text_index = 0
        self.endgame_text_timer = 0

        self.prologue_text = [
            "The kitchen was once a place of harmony, filled with the aroma of spices and the warmth of teamwork.",
            "But peace did not last long. A sudden betrayal shattered it all.",
            "An uprising has begun...led by Meowzho, the former ally turned rival.",
            "Now, Meowchi must fight to reclaim the heart of the home...the kitchen."
        ]
        self.prologue_text_index = 0
        self.prologue_text_timer = 0
        self.prologue_fade_alpha = 255  # Mulai dari hitam penuh (fade in)
        self.prologue_fade_done = False
        self.state = "menu"

    def play_music(self, music_file):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)

    def init_menu(self):
        self.title_image = pygame.image.load(os.path.join("Assets/title/titlee.png")).convert_alpha()
        self.title_image = pygame.transform.scale(self.title_image, (1200, 1000))
        self.title_rect = self.title_image.get_rect(center=(self.WIDTH // 2, 250))

        self.buttons = [
            ImageButton(os.path.join("Assets/Button/play_button_lv3.png"), self.WIDTH // 2 - 100, self.HEIGHT // 2 - 100, self.start_game, size=(200, 200)),
            ImageButton(os.path.join("Assets/Button/exit_button_lv3.png"), self.WIDTH // 2 - 95, self.HEIGHT // 2 + 100, self.quit_game, size=(200, 200))
        ]

    def start_game(self):
        self.state = "prologue"
        self.prologue_text_index = 0
        self.prologue_text_timer = pygame.time.get_ticks()
        self.prologue_fade_alpha = 255
        self.prologue_fade_done = False

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def scroll_background(self):
        self.bg_x -= self.scroll_speed
        screen_width = self.menu_bg.get_width()
        self.screen.blit(self.menu_bg, (self.bg_x, 0))
        self.screen.blit(self.menu_bg, (self.bg_x + screen_width, 0))
        if self.bg_x <= -screen_width:
            self.bg_x = 0

    def init_game(self, level):
        self.enemy_list = []
        self.level = level
        self.score = 0
        self.bg_speed = 3 + level
        self.meowchi = Meowchi(200, self.HEIGHT // 2)
        self.game_over = False
        self.win = False
        self.show_next_button = False
        self.dogs_killed = 0
        self.cats_killed = 0

        # --- Dialog sequence untuk tiap level ---
        if self.level == 1:
            self.play_music(os.path.join("Assets/Music/start.wav"))
            self.bg_image = pygame.image.load(os.path.join("Assets/Background/background1.png"))
            self.enemy_list = [TikusDapur(self.WIDTH, self.HEIGHT) for _ in range(2)] + [TikusPutih(self.WIDTH, self.HEIGHT) for _ in range(3)]
            self.dialog_sequence = [
                ("Meowchi", "Assets/meowchi/meowchidialog.png", "Huh? Where this rat come from??!", "Assets/meowchi/storyboard.png"),
                ("Meowchi", "Assets/meowchi/meowchidialog.png", "I have to drive them out before this kitchen becomes more chaotic!", "Assets/meowchi/storyboard.png"),
            ]
            self.dialog_index = 0
            self.show_dialog = True
            name, img, text, bg = self.dialog_sequence[self.dialog_index]
            self.dialog_box = DialogBox(img, name, text, self.button_font, self.screen, box_bg_path=bg)

        elif self.level == 2:
            self.play_music(os.path.join("Assets/Music/level_2.wav"))
            self.bg_image = pygame.image.load(os.path.join("Assets/Background/background2.png"))
            self.enemy_list = [Anjing(self.WIDTH, self.HEIGHT) for _ in range(2)]
            self.dialog_sequence = [
                ("Meowchi", "Assets/meowchi/meowchidialog.png", "Now i have to beat that me*ow dog..!", "Assets/meowchi/storyboard.png"),
                ("Meowchi", "Assets/meowchi/meowchidialog.png", "Why they come like already know that this kichen was ruined?", "Assets/meowchi/storyboard.png"),
                ("Meowchi", "Assets/meowchi/meowchidialog.png", "I wonder who tells them about this...?", "Assets/meowchi/storyboard.png"),
            ]
            self.dialog_index = 0
            self.show_dialog = True
            name, img, text, bg = self.dialog_sequence[self.dialog_index]
            self.dialog_box = DialogBox(img, name, text, self.button_font, self.screen, box_bg_path=bg)

        elif self.level == 3:
            self.play_music(os.path.join("Assets/Music/boss battle.wav"))
            self.bg_image = pygame.image.load(os.path.join("Assets/Background/background3.png"))
            self.enemy_list = [Meowzho(self.WIDTH, self.HEIGHT)]
            self.dialog_sequence = [
                ("Meowchi", "Assets/meowchi/meowchidialog.png", "What the me*ow is that?!", "Assets/meowchi/storyboard.png"),
                ("Meowchi", "Assets/meowchi/meowchidialog.png", "That....is MEOWZHO?! My BestFriend???!", "Assets/meowchi/storyboard.png"),
                ("Meowchi", "Assets/meowchi/meowchidialog.png", "MEOWZHO! WHYY?! I Must Stop you from ruining this place!", "Assets/meowchi/storyboard.png"),
                ("Meowchi", "Assets/meowchi/meowchidialog.png", "MEOWWWWWWW!", "Assets/meowchi/storyboard.png"),
            ]
            self.dialog_index = 0
            self.show_dialog = True
            name, img, text, bg = self.dialog_sequence[self.dialog_index]
            self.dialog_box = DialogBox(img, name, text, self.button_font, self.screen, box_bg_path=bg)

        self.bg_image = pygame.transform.scale(self.bg_image, (self.WIDTH, self.HEIGHT))

        self.next_button = ImageButton(os.path.join("Assets/Button/next_button_lv1.png"), self.WIDTH // 2 - 95, self.HEIGHT // 2 + 100, self.next_level, size=(200, 200))
        self.try_again_button = ImageButton(os.path.join("Assets/Button/tryagain_button_lv1.png"), self.WIDTH // 2 - 95, self.HEIGHT // 2 + 100, self.restart_game, size=(200, 200))

        self.game_over_image = pygame.image.load(os.path.join("Assets/title/game_over.png"))
        self.game_over_image = pygame.transform.scale(self.game_over_image, (600, 400))
        self.game_over_rect = self.game_over_image.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 100))

        self.win_image = pygame.image.load(os.path.join("Assets/title/win.png"))
        self.win_image = pygame.transform.scale(self.win_image, (600, 400))
        self.win_rect = self.win_image.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 100))

    def next_level(self):
        if self.level < 3:
            self.init_game(self.level + 1)
        else:
            # Mulai endgame
            self.state = "endgame"
            self.fade_alpha = 0
            self.fade_done = False
            self.endgame_text_index = 0
            self.endgame_text_timer = 0

    def restart_game(self):
        self.init_game(1)
        self.state = "game"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            if self.state == "menu":
                for button in self.buttons:
                    button.handle_event(event)

            elif self.state == "game":
                if self.show_dialog and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.dialog_index += 1
                    if self.dialog_index < len(self.dialog_sequence):
                        name, img, text, bg = self.dialog_sequence[self.dialog_index]
                        self.dialog_box = DialogBox(img, name, text, self.button_font, self.screen, box_bg_path=bg)
                    else:
                        self.show_dialog = False
                        # lanjutkan ke next state/gameplay
                elif self.game_over:
                    self.try_again_button.handle_event(event)
                elif self.show_next_button and not self.win:
                    self.next_button.handle_event(event)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over and not self.win:
                    target_pos = (self.WIDTH + 100, self.meowchi.rect.centery)
                    self.meowchi.shoot(target_pos)
               
            elif self.state == "endgame":
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = "menu"
            elif self.state == "prologue":
                if self.prologue_fade_done and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                    self.state = "game"
                    self.init_game(1)

    def update_game(self):
        if self.show_dialog:
            self.dialog_box.update(pygame.time.get_ticks() // 10)
            return
        
        if self.meowchi.hp <= 0:
            if not self.game_over:
                self.game_over = True
                pygame.mixer.music.stop()
                pygame.mixer.Sound(os.path.join("Assets/sound_effect/lose.mp3")).play()

        if self.game_over or self.win or self.show_next_button:
            pass
        
        elif not self.win:
            pygame.mouse.set_visible(False)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.meowchi.follow_mouse(mouse_x, mouse_y)
            self.meowchi.update()

            for enemy in self.enemy_list:
                enemy.update(self.meowchi)
                if isinstance(enemy, Anjing):
                    for bullet in enemy.bullets:
                        if bullet.check_collision(self.meowchi):
                            self.meowchi.take_damage(1)
                for bullet in self.meowchi.bullets:
                    if bullet.check_collision(enemy):
                        self.score += 5
                        if isinstance(enemy, Anjing) and not enemy.alive and not enemy.score_awarded:
                            self.dogs_killed += 1
                            enemy.score_awarded = True  # agar tidak dihitung ganda
                        break
                    
            if isinstance(enemy, Meowzho):
                    for bullet in enemy.bullets:
                        if bullet.check_collision(self.meowchi):
                            self.meowchi.take_damage(1)
                    for bullet in self.meowchi.bullets:
                        if bullet.check_collision(enemy):
                            self.score += 5
                        if isinstance(enemy, Meowzho) and not enemy.alive and not enemy.score_awarded:
                            self.cats_killed += 1
                            enemy.score_awarded = True  # agar tidak dihitung ganda
                        break
        
            self.enemy_list = [e for e in self.enemy_list if e.alive or e.death_timer > 0]
            if self.level == 1:
                if len(self.enemy_list) < 5:
                    self.enemy_list.append(random.choice([TikusDapur, TikusPutih])(self.WIDTH, self.HEIGHT))

            if self.score >= 100 and self.level == 1:
                self.show_next_button = True 
            elif self.level == 2 and self.dogs_killed >= 5:
                self.show_next_button = True
            elif self.level == 3 and self.cats_killed >= 1:
                self.show_next_button = True
            # self.win = True
            elif self.level == 2:
                active_dogs = [e for e in self.enemy_list if isinstance(e, Anjing) and (e.alive or e.death_timer > 0)]
                if len(active_dogs) < 2:
                    self.enemy_list.append(Anjing(self.WIDTH, self.HEIGHT))
            
            elif self.level == 3:
               pass

        if self.win:
            pass

        if self.game_over or self.win:
            self.bg_speed = 0

        if not self.win:
            self.bg_x -= self.bg_speed
            if self.bg_x <= -self.WIDTH:
                self.bg_x = 0
        if self.show_next_button:
            self.bg_speed = 0
            
    def draw(self):
        if self.state == "menu":
            self.scroll_background()
            self.screen.blit(self.title_image, self.title_rect)
            for button in self.buttons:
                button.draw(self.screen)

        elif self.state == "game":
            self.screen.blit(self.bg_image, (self.bg_x, 0))
            self.screen.blit(self.bg_image, (self.bg_x + self.WIDTH, 0))

            self.meowchi.draw(self.screen)

            for enemy in self.enemy_list:
                enemy.draw(self.screen)

            self.draw_score()
            # self.draw_hp()

            if self.game_over:
                self.screen.blit(self.game_over_image, self.game_over_rect)
                self.try_again_button.draw(self.screen)         
            elif self.win:
                self.screen.blit(self.win_image, self.win_rect)
                self.next_button.draw(self.screen)
            elif self.show_next_button and not self.win :
                self.screen.blit(self.win_image, self.win_rect)
                self.next_button.draw(self.screen)
            if self.show_dialog:
                self.dialog_box.draw()
        elif self.state == "endgame":
            # Fade out
            if not self.fade_done:
                fade_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
                fade_surface.fill((0, 0, 0))
                self.fade_alpha = min(self.fade_alpha + 4, 255)
                fade_surface.set_alpha(self.fade_alpha)
                self.screen.blit(fade_surface, (0, 0))
                if self.fade_alpha >= 255:
                    self.fade_done = True
            else:
                self.screen.fill((0, 0, 0))
                # Tampilkan teks satu per satu
                if self.endgame_text_index < len(self.endgame_text):
                    if pygame.time.get_ticks() - self.endgame_text_timer > 1200:  # 1.2 detik per baris
                        self.endgame_text_index += 1
                        self.endgame_text_timer = pygame.time.get_ticks()
                for i in range(self.endgame_text_index):
                    text = self.score_font.render(self.endgame_text[i], True, (255, 255, 255))
                    rect = text.get_rect(center=(self.WIDTH // 2, 200 + i * 80))
                    self.screen.blit(text, rect)
        elif self.state == "prologue":
            # Fade in dari hitam ke terang
            if not self.prologue_fade_done:
                self.screen.fill((0, 0, 0))
                self.prologue_fade_alpha = max(self.prologue_fade_alpha - 20, 0)
                fade_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
                fade_surface.set_alpha(self.prologue_fade_alpha)
                fade_surface.fill((0, 0, 0))
                self.screen.blit(fade_surface, (0, 0))
                if self.prologue_fade_alpha == 0:
                    self.prologue_fade_done = True
                    self.prologue_text_timer = pygame.time.get_ticks()
            else:
                self.screen.fill((0, 0, 0))
                # Tampilkan teks satu per satu
                if self.prologue_text_index < len(self.prologue_text):
                    if pygame.time.get_ticks() - self.prologue_text_timer > 1200:
                        self.prologue_text_index += 1
                        self.prologue_text_timer = pygame.time.get_ticks()
                for i in range(self.prologue_text_index):
                    text = self.button_font.render(self.prologue_text[i], True, (255, 255, 255))
                    rect = text.get_rect(center=(self.WIDTH // 2, 200 + i * 60))
                    self.screen.blit(text, rect)
                    
        show_cursor = (
        self.state in ["menu", "endgame", "prologue"]
        or (self.state == "game" and (self.show_dialog or self.show_next_button or self.win or self.game_over))
    )
        if show_cursor:
            pygame.mouse.set_visible(False)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.screen.blit(self.cursor_image, (mouse_x, mouse_y))
     
           
    def draw_score(self):
        score_text = self.score_font.render(f"Score: {self.score}", True, (0, 0, 0))
        score_rect = score_text.get_rect(topright=(self.WIDTH - 20, 20))
        self.screen.blit(score_text, score_rect)
        # self.screen.blit(score_text, (-20, -20))

    def run(self, clock):
        while self.running:
            self.handle_events()
            if self.state == "game":
                self.update_game()
            self.draw()
            pygame.display.flip()
            clock.tick(60)
