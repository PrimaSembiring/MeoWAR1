import pygame
import sys
import random
import os
from button import Button
from meowchi import Meowchi
from enemy import TikusDapur, TikusPutih, Anjing
from image_button import ImageButton

pygame.init()
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("MeoWar")
clock = pygame.time.Clock()

title_font = pygame.font.SysFont("comicsansms", 72)
button_font = pygame.font.SysFont("comicsansms", 36)

menu_bg = pygame.image.load("Assets/Background/main_menu.png")
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

pygame.mixer.init()

def play_music(music_path):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)

class MainMenu:
    def __init__(self):
        self.title_image = pygame.image.load("Assets/title/titlee.png").convert_alpha()
        self.title_image = pygame.transform.scale(self.title_image, (1200, 1000))
        self.title_rect = self.title_image.get_rect(center=(WIDTH // 2, 250))

        self.buttons = [
            ImageButton("Assets/button/play_button_lv3.png", WIDTH // 2 - 100, HEIGHT // 2 - 100, self.start_game, size=(200, 200)),
            ImageButton("Assets/button/exit_button_lv3.png", WIDTH // 2 - 95, HEIGHT // 2 + 100, self.quit_game, size=(200, 200))
        ]
        self.running = True
        self.bg_images = [menu_bg]
        self.current_bg_index = 0
        self.bg_x = 0
        self.scroll_speed = 1

    def start_game(self):
        game = GameManager(1)
        game.run()
        self.running = True

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def scroll_background(self):
        self.bg_x -= self.scroll_speed
        current_bg = self.bg_images[self.current_bg_index]
        next_bg = self.bg_images[(self.current_bg_index + 1) % len(self.bg_images)]
        screen.blit(current_bg, (self.bg_x, 0))
        screen.blit(next_bg, (self.bg_x + current_bg.get_width(), 0))
        if self.bg_x <= -current_bg.get_width():
            self.bg_x = 0
            self.current_bg_index = (self.current_bg_index + 1) % len(self.bg_images)

    def run(self):
        play_music("Assets/Music/regrowth.wav")
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                for button in self.buttons:
                    button.handle_event(event)
            self.scroll_background()
            screen.blit(self.title_image, self.title_rect)
            for button in self.buttons:
                button.draw(screen)
            pygame.display.flip()
            clock.tick(60)


class GameManager:
    def __init__(self, level=1):
        self.level = level
        self.score = 0
        self.bg_x = 0
        self.bg_speed = 3 + level
        self.meowchi = Meowchi(200, HEIGHT // 2)
        self.game_over = False
        self.win = False

        if self.level == 1:
            play_music("Assets/Music/start.wav")
            self.bg_image = pygame.image.load("Assets/Background/background1.png")
            self.enemy_list = [TikusDapur(WIDTH, HEIGHT) for _ in range(2)] + [TikusPutih(WIDTH, HEIGHT) for _ in range(3)]
        elif self.level == 2:
            play_music("Assets/Music/level_2.wav")
            self.bg_image = pygame.image.load("Assets/Background/BG2.png")
            self.enemy_list = [Anjing(WIDTH, HEIGHT) for _ in range(2)]  # Awal hanya 2 anjing
        elif self.level == 3:
            play_music("Assets/Music/boss battle.wav")
            self.bg_image = pygame.image.load("Assets/Background/background3.png")
            self.enemy_list = []

        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))
        self.running = True

        self.next_button = ImageButton("Assets/button/next_button_lv1.png", WIDTH // 2 - 95, HEIGHT // 2 + 100, self.next_level, size=(200, 200))
        self.try_again_button = ImageButton("Assets/button/tryagain_button_lv1.png", WIDTH // 2 - 95, HEIGHT // 2 + 100, self.restart_game, size=(200, 200))
        self.show_next_button = False

        self.game_over_image = pygame.image.load("Assets/title/game_over.png")
        self.game_over_image = pygame.transform.scale(self.game_over_image, (600, 400))
        self.game_over_rect = self.game_over_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

        self.win_image = pygame.image.load("Assets/title/win.png")
        self.win_image = pygame.transform.scale(self.win_image, (600, 400))
        self.win_rect = self.win_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

    def next_level(self):
        if self.level < 3:
            self.level += 1
            self.__init__(self.level)
        else:
            self.win = True

    def restart_game(self):
        self.__init__(1)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                if self.game_over:
                    self.try_again_button.handle_event(event)
                elif self.show_next_button and not self.win:
                    self.next_button.handle_event(event)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over and not self.win:
                    target_pos = (WIDTH + 100, self.meowchi.rect.centery)
                    self.meowchi.shoot(target_pos)

            if self.meowchi.hp <= 0:
                self.game_over = True

            if not self.game_over and not self.win:
                if self.score >= 100:
                    self.show_next_button = True
                    pygame.mouse.set_visible(True)
                else:
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
                                break

                    self.enemy_list = [e for e in self.enemy_list if e.alive or e.death_timer > 0]

                    # PEMBATASAN ANJING AKTIF di Level 2
                    if self.level == 2:
                        alive_dogs = [e for e in self.enemy_list if isinstance(e, Anjing) and e.alive]
                        if len(alive_dogs) < 2:
                            self.enemy_list.append(Anjing(WIDTH, HEIGHT))
                    elif self.level == 1:
                        if len(self.enemy_list) < 5:
                            self.enemy_list.append(random.choice([TikusDapur, TikusPutih])(WIDTH, HEIGHT))

            if self.game_over or self.win:
                self.bg_speed = 0

            if not self.win:
                self.bg_x -= self.bg_speed
                if self.bg_x <= -WIDTH:
                    self.bg_x = 0

            screen.blit(self.bg_image, (self.bg_x, 0))
            screen.blit(self.bg_image, (self.bg_x + WIDTH, 0))

            self.meowchi.draw(screen)
            for enemy in self.enemy_list:
                enemy.draw(screen)

            self.meowchi.draw_health_bar_top_left(screen)

            score_text = pygame.font.SysFont("comicsansms", 36).render(f"Score: {self.score}", True, (255, 255, 255))
            screen.blit(score_text, (280, 30))

            if self.show_next_button and not self.game_over and not self.win:
                screen.blit(self.win_image, self.win_rect)
                self.next_button.draw(screen)

            if self.win:
                screen.blit(self.win_image, self.win_rect)
                pygame.mouse.set_visible(True)

            if self.game_over:
                screen.blit(self.game_over_image, self.game_over_rect)
                self.try_again_button.draw(screen)
                pygame.mouse.set_visible(True)

            pygame.display.flip()
            clock.tick(60)


def main():
    menu = MainMenu()
    menu.run()


if __name__ == "__main__":
    main()
