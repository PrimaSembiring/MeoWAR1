import pygame
import os
import random
from bullet import DogBone

class Enemy:
    def __init__(self, screen_width, screen_height, image_path, dead_image_path, hp,size):
        # Ukuran gambar default bisa diubah lewat parameter `size`
        self.size = size
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.dead_image = pygame.image.load(dead_image_path).convert_alpha()
        self.dead_image = pygame.transform.scale(self.dead_image, size)

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(screen_width, screen_width + 300)
        self.rect.y = random.randint(0, screen_height - self.rect.height)

        self.speed = 5
        self.alive = True
        self.hp = hp

        self.death_timer = 0
        self.DEATH_DURATION = 60
        self.score_awarded = False

    def update(self, meowchi):
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            return

        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.alive = False
            self.death_timer = 0

    def draw(self, screen, debug=False):
        if self.alive:
            screen.blit(self.image, self.rect)
        elif self.death_timer > 0:
            screen.blit(self.dead_image, self.rect)
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def take_damage(self):
        self.hp -= 1
        if self.hp <= 0 and self.alive:
            self.alive = False
            self.death_timer = self.DEATH_DURATION
            return True
        return False


class TikusDapur(Enemy):
    def __init__(self, screen_width, screen_height):
        image_path = os.path.join("Assets/tikus/tikus.png")
        dead_image_path = os.path.join("Assets/tikus/tikus_mati.png")
        super().__init__(screen_width, screen_height, image_path, dead_image_path, hp=1, size = (250, 250))


class TikusPutih(Enemy):
    def __init__(self, screen_width, screen_height):
        image_path = os.path.join("Assets/tikus/tikusputih.png")
        dead_image_path = os.path.join("Assets/tikus/tikusputih_mati.png")
        super().__init__(screen_width, screen_height, image_path, dead_image_path, hp=2, size = (250, 250))

class Anjing(Enemy):
    def __init__(self, screen_width, screen_height):
        image_path = os.path.join("Assets/Anjing/guguk imut1.png")
        dead_image_path = os.path.join("Assets/Anjing/anjing_mati.png")
        super().__init__(screen_width, screen_height, image_path, dead_image_path, hp=8, size=(300, 300))
        self.speed = 1.5
        self.attack_timer = 0
        self.attack_interval = 120
        self.bullets = []

        # Menyimpan sejarah posisi Meowchi
        self.meowchi_positions = []
        self.position_delay = 15  # Jumlah frame delay

    def update(self, meowchi):
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            return

        # Simpan posisi terbaru Meowchi ke dalam list
        self.meowchi_positions.append(meowchi.rect.center)
        if len(self.meowchi_positions) > self.position_delay:
            target_x, target_y = self.meowchi_positions.pop(0)
        else:
            target_x, target_y = meowchi.rect.center  # Jika belum cukup data, kejar posisi langsung

        # Gerak ke arah posisi delay
        if self.rect.centerx < target_x:
            self.rect.x += self.speed
        elif self.rect.centerx > target_x:
            self.rect.x -= self.speed

        if self.rect.centery < target_y:
            self.rect.y += self.speed
        elif self.rect.centery > target_y:
            self.rect.y -= self.speed

        # Menyerang setiap interval
        self.attack_timer += 1
        if self.attack_timer >= self.attack_interval:
            self.attack_timer = 0
            self.shoot(meowchi)

        # Update peluru
        for bullet in self.bullets:
            bullet.update()
            if bullet.check_collision(meowchi):
                print("Meowchi terkena tulang!")

        self.bullets = [b for b in self.bullets if b.alive]

    def shoot(self, meowchi):
        start_x = self.rect.centerx
        start_y = self.rect.centery
        target_pos = meowchi.rect.center
        self.bullets.append(DogBone(start_x, start_y, target_pos))

    def draw(self, screen, debug=False):
        super().draw(screen, debug)
        for bullet in self.bullets:
            bullet.draw(screen)

