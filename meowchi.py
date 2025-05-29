import pygame
import os
from bullet import Tomat

class Meowchi:
    def __init__(self, x, y):
        self.image_idle = pygame.transform.scale(
            pygame.image.load(os.path.join("Assets/meowchi/meowchi1.png")),
            (575, 575)
        )
        self.image_attack = pygame.transform.scale(
            pygame.image.load(os.path.join("Assets/meowchi/meowchi2.png")),
            (575, 575)
        )
        self.image_hit = pygame.transform.scale(
            pygame.image.load(os.path.join("Assets/meowchi/meowchi3.png")),
            (575, 575)
        )

        self.image = self.image_idle
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3

        self.__max_hp = 10
        self.__hp = 10

        self.bullets = []
        self.shoot_delay = 15
        self.timer = 0

        self.attack_timer = 0
        self.attack_duration = 10
        self.shoot_sound = pygame.mixer.Sound("Assets/sound_effect/shoot.mp3")
        self.shoot_sound.set_volume(0.5)  # Sesuaikan volume jika perlu

        # Load gambar health bar
        self.health_images = []
        for i in range(1, 12):
            path = os.path.join("Assets/healtbar", f"health bar {i}.png")
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, (250, 100))
            self.health_images.append(image)

        self.mask = pygame.mask.from_surface(self.image)
        self.hit_timer = 0
        self.hit_duration = 17  # Durasi berkedip

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, value):
        if value < 0:
            self.__hp = 0
        elif value > self.__max_hp:
            self.__hp = self.__max_hp
        else:
            self.__hp = value

    @property
    def max_hp(self):
        return self.__max_hp

    def follow_mouse(self, mouse_x, mouse_y):
        self.rect.centerx = mouse_x
        self.rect.centery = mouse_y

    def shoot(self, target_pos):
        if self.timer >= self.shoot_delay:
            bullet_x, bullet_y = self.get_tomat_position()
            bullet = Tomat(bullet_x, bullet_y, target_pos) #objek
            self.bullets.append(bullet)
            self.timer = 0

            # Ubah gambar ketika menyerang
            self.image = self.image_attack
            self.attack_timer = self.attack_duration
            self.shoot_sound.play()

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp == 0:
            print("Meowchi kalah!")

        # Ganti gambar menjadi meowchi3.png ketika terkena damage
        self.image = self.image_hit
        self.hit_timer = self.hit_duration  # Set timer untuk efek hit

    def get_tomat_position(self):
        return self.rect.centerx + 25, self.rect.centery

    def update(self):
        self.timer += 1
        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer == 0:
                self.image = self.image_idle  # Kembali ke gambar idle setelah menyerang

        if self.hp > 0 and self.image == self.image_hit:
            if self.hit_timer > 0:
                self.hit_timer -= 1
            else:
                self.image = self.image_idle  # Kembali ke gambar idle setelah efek hit selesai

        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.alive]

    def draw_health_bar_top_left(self, screen):
        hit_count = self.max_hp - self.hp
        index = min(hit_count, 10)  # Index 0 sampai 10
        health_image = self.health_images[index]
        screen.blit(health_image, (20, 20))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)
        self.draw_health_bar_top_left(screen)

    def check_collision(self, other):
        offset = (other.rect.x - self.rect.x, other.rect.y - self.rect.y)
        return self.mask.overlap(other.mask, offset) is not None
