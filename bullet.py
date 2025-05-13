import pygame
import os
import math

class Bullet:
    def __init__(self, x, y, target_pos):
        # Muat gambar peluru dan tentukan ukuran
        image_path = os.path.join("Assets/bumbu/bumbu dapurr1.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (55, 55))
        self.rect = self.image.get_rect(center=(x, y))

        # Membuat mask dari gambar peluru untuk tabrakan berbasis piksel
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 15

        # Hitung kecepatan peluru menuju target
        dx = target_pos[0] - x
        dy = target_pos[1] - y
        distance = math.hypot(dx, dy)
        if distance == 0:
            distance = 1
        self.velocity = (dx / distance * self.speed, dy / distance * self.speed)

        self.alive = True
        self.hit = False

    def update(self):
        """Update posisi peluru."""
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # Hapus peluru jika keluar dari layar
        if (self.rect.right < 0 or self.rect.left > 1920 or
                self.rect.bottom < 0 or self.rect.top > 1080):
            self.alive = False

    def draw(self, screen):
        """Gambar peluru ke layar."""
        screen.blit(self.image, self.rect)

    def check_collision(self, enemy):
        """Cek tabrakan peluru dengan musuh."""
        if self.hit or not enemy.alive:
            return False
        
        # Jika musuh tidak memiliki mask, buatkan mask
        if not hasattr(enemy, 'mask'):
            enemy.mask = pygame.mask.from_surface(enemy.image)

        # Cek tabrakan berbasis piksel antara peluru dan musuh
        offset = (enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y)
        if self.mask.overlap(enemy.mask, offset):
            enemy.take_damage()  # Misalnya memanggil metode untuk mengurangi HP musuh
            self.hit = True
            self.alive = False
            return True
        return False


class DogBone:
    def __init__(self, x, y, target_pos):
        # Muat gambar tulang dan tentukan ukuran
        image_path = os.path.join("Assets/Anjing/tulang guguk.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (65, 65))
        self.rect = self.image.get_rect(center=(x, y))

        # Membuat mask dari gambar tulang untuk tabrakan berbasis piksel
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 8

        # Hitung kecepatan peluru tulang menuju target
        dx = target_pos[0] - x
        dy = target_pos[1] - y
        distance = math.hypot(dx, dy)
        if distance == 0:
            distance = 1
        self.velocity = (dx / distance * self.speed, dy / distance * self.speed)

        self.alive = True

    def update(self):
        """Update posisi tulang."""
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # Hapus tulang jika keluar dari layar
        if (self.rect.right < 0 or self.rect.left > 1920 or
                self.rect.bottom < 0 or self.rect.top > 1080):
            self.alive = False

    def draw(self, screen):
        """Gambar tulang ke layar."""
        screen.blit(self.image, self.rect)

    def check_collision(self, meowchi):
        """Cek tabrakan antara tulang dan Meowchi."""
        offset = (meowchi.rect.x - self.rect.x, meowchi.rect.y - self.rect.y)
        if self.mask.overlap(meowchi.mask, offset):
            self.alive = False  # Hapus tulang jika mengenai Meowchi
            meowchi.take_damage(1)  # Misalnya mengurangi HP Meowchi
            return True
        return False
