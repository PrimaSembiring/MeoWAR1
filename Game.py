import pygame
import random
from meowchi import Meowchi
from enemy import TikusDapur, TikusPutih, Anjing
from button import Button

class Game: 
    def __init__(self, screen, WIDTH, HEIGHT, level=1):
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.level = level

        self.background = pygame.image.load("Assets/bg/bg1.jpg")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.bg_x = 0
        self.bg_speed = 2

        self.meowchi = Meowchi(200, 400)
        self.enemies = []  # Tikus dan anjing biasa
        self.spawn_delay = 60
        self.spawn_timer = 0

        self.score = 0
        self.font = pygame.font.SysFont(None, 72)
        self.win = False

        self.next_button = Button("NEXT", WIDTH - 160, HEIGHT - 80, 140, 50, self.next_level)
        self.next_level_callback = None

        # # Untuk level 2, atur delay anjing kedua
        # if self.level == 2:
        #     self.active_dogs = []  # Tidak ada anjing yang muncul di awal
        #     self.dog_queue = [Anjing(self.WIDTH, self.HEIGHT) for _ in range(3)]  # Queue untuk anjing lainnya
        #     self.dog_2_delay = 0  # Timer untuk menunggu sebelum anjing kedua muncul

    def set_next_level_callback(self, callback):
        self.next_level_callback = callback

    def spawn_enemy(self):
        # Jika level 1, spawn TikusDapur dan TikusPutih dengan jarak minimal
        if self.level == 1:
            if random.random() < 0.7:
                self.enemies.append(TikusDapur(self.WIDTH, self.HEIGHT))
            else:
                self.enemies.append(TikusPutih(self.WIDTH, self.HEIGHT))
        # Jika level 2, spawn 2 Anjing dengan delay
        elif self.level == 2:
            # Tentukan posisi pertama untuk anjing
            x_pos1 = random.randint(self.WIDTH // 4, self.WIDTH // 2)
            y_pos1 = random.randint(100, self.HEIGHT - 100)
            dog1 = Anjing(x_pos1, y_pos1)
            self.active_dogs.append(dog1)  # Tambahkan anjing pertama ke list

    def update(self):
        if self.win:
            return

        self.bg_x -= self.bg_speed
        if self.bg_x <= -self.WIDTH:
            self.bg_x = 0

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.meowchi.follow_mouse(mouse_x, mouse_y)
        self.meowchi.update()

        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay and self.level != 2:
            self.spawn_timer = 0
            self.spawn_enemy()

        # 🔁 Perbarui anjing aktif jika ada yang mati
        if self.level == 2:
    # Hapus anjing yang sudah mati total
            self.active_dogs = [d for d in self.active_dogs if d.alive or d.death_timer > 0]

    # Jika tidak ada anjing aktif & masih ada di queue, spawn berikutnya setelah delay
        if len(self.active_dogs) == 0 and self.dog_queue:
            self.dog_2_delay += 0.2
        if self.dog_2_delay >= 1000:  # Tunggu 3 detik (180 frame)
            next_dog = self.dog_queue.pop(0)
            
            # Cegah spawn berdempetan: random ulang hingga posisi tidak terlalu dekat
            too_close = True
            attempt = 0
            while too_close and attempt < 10:
                next_dog.rect.x = random.randint(self.WIDTH // 3, self.WIDTH - 300)
                next_dog.rect.y = random.randint(100, self.HEIGHT - 100)
                too_close = any(
                    abs(next_dog.rect.x - d.rect.x) < 250 and abs(next_dog.rect.y - d.rect.y) < 250
                    for d in self.active_dogs
                )
                attempt += 1

            self.active_dogs.append(next_dog)
            self.dog_2_delay = 0  # Reset delay

    # Update semua anjing aktif
        for dog in self.active_dogs:
            dog.update(self.meowchi)

        # if self.level == 2:
        #     # Jika sudah 8 detik (480 frame), tambahkan anjing kedua
        #     self.dog_2_delay += 1
        #     if self.dog_2_delay >= 480 and len(self.active_dogs) == 1:  # Setelah 8 detik dan hanya ada 1 anjing
        #         # Tentukan posisi kedua untuk anjing, pastikan tidak terlalu dekat
        #         x_pos2 = random.randint(self.WIDTH // 2, self.WIDTH - self.WIDTH // 4)
        #         y_pos2 = random.randint(100, self.HEIGHT - 100)
        #         dog2 = Anjing(x_pos2, y_pos2)
        #         self.active_dogs.append(dog2)  # Tambahkan anjing kedua ke dalam list

            for dog in self.active_dogs:
                dog.update(self.meowchi)

        for enemy in self.enemies:
            enemy.update(self.meowchi)

        for bullet in self.meowchi.bullets[:]:
            # Cek tabrakan dengan musuh selain anjing aktif
            for enemy in self.enemies:
                if enemy.alive and bullet.check_collision(enemy):
                    if enemy.take_damage():
                        if not enemy.score_awarded:
                            self.score += 10
                        enemy.score_awarded = True
                    if bullet in self.meowchi.bullets:
                        self.meowchi.bullets.remove(bullet)
                    break

            # Cek tabrakan dengan anjing aktif
            if self.level == 2:
                for dog in self.active_dogs:
                    if dog.alive and bullet.check_collision(dog):
                        if dog.take_damage():
                            if not dog.score_awarded:
                                self.score += 10
                            dog.score_awarded = True
                        if bullet in self.meowchi.bullets:
                            self.meowchi.bullets.remove(bullet)
                        break

        self.enemies = [e for e in self.enemies if e.alive or e.death_timer > 0]
        if self.level == 2:
            self.active_dogs = [d for d in self.active_dogs if d.alive or d.death_timer > 0]

        if self.score >= 100 and not self.win:
            self.win = True

    def draw(self):
        self.screen.blit(self.background, (self.bg_x, 0))
        self.screen.blit(self.background, (self.bg_x + self.WIDTH, 0))

        self.meowchi.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        if self.level == 2:
            for dog in self.active_dogs:
                dog.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.WIDTH - 250, 30))

        if self.win:
            win_text = self.font.render("YOU WIN", True, (255, 255, 0))
            text_rect = win_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            self.screen.blit(win_text, text_rect)
            self.next_button.draw(self.screen)

    def handle_event(self, event):
        if self.win:
            self.next_button.handle_event(event)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.meowchi.shoot(pygame.mouse.get_pos())

    def next_level(self):
        self.level += 1
        if self.next_level_callback:
            self.next_level_callback()
