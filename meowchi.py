import pygame
import os
from bullet import Bullet

class Meowchi:
    def __init__(self, x, y):   
        # Gambar idle, attack, dan hit
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

        # Default image dan rect
        self.image = self.image_idle
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3

        # HP dimulai dari 10 dan maksimal 10
        self.hp = 10
        self.max_hp = 10

        # List peluru
        self.bullets = []
        self.shoot_delay = 15
        self.timer = 0

        self.attack_timer = 0
        self.attack_duration = 10
        self.shoot_sound = pygame.mixer.Sound("Assets/sound_effect/shoot.mp3")
        self.shoot_sound.set_volume(5)  # Sesuaikan volume jika perlu
        # Load gambar health bar
        self.health_images = []
        for i in range(1, 12):
            path = os.path.join("Assets/healtbar", f"health bar {i}.png")
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, (250, 75))
            self.health_images.append(image)

        # Mask untuk deteksi tabrakan
        self.mask = pygame.mask.from_surface(self.image)

        # Timer untuk efek hit (berkedip)
        self.hit_timer = 0
        self.hit_duration = 17  # Durasi berkedip

    def follow_mouse(self, mouse_x, mouse_y):
        """Menjaga Meowchi mengikuti posisi mouse."""
        self.rect.centerx = mouse_x
        self.rect.centery = mouse_y

    def shoot(self, target_pos):
        """Menembakkan peluru tomat ke target yang ditentukan."""
        if self.timer >= self.shoot_delay:
            bullet_x, bullet_y = self.get_tomat_position()
            bullet = Bullet(bullet_x, bullet_y, target_pos)
            self.bullets.append(bullet)
            self.timer = 0

            # Ubah gambar ketika menyerang
            self.image = self.image_attack
            self.attack_timer = self.attack_duration
            self.shoot_sound.play()

    def take_damage(self, amount): 
        """Mengurangi HP Meowchi ketika terkena serangan."""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        if self.hp == 0:
            print("Meowchi kalah!")
        
        # Ganti gambar menjadi meowchi3.png ketika terkena damage
        self.image = self.image_hit
        self.hit_timer = self.hit_duration  # Set timer untuk efek hit

    def get_tomat_position(self):
        """Mengambil posisi tembakan tomat dari Meowchi."""
        return self.rect.centerx + 25, self.rect.centery

    def update(self):
        """Update timer dan status Meowchi serta peluru-pelurunya."""
        self.timer += 1
        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer == 0:
                self.image = self.image_idle  # Kembali ke gambar idle setelah menyerang
        
        # Logika untuk mengembalikan gambar setelah Meowchi terkena damage
        if self.hp > 0 and self.image == self.image_hit:
            # Mengatur Meowchi kembali ke gambar idle setelah beberapa detik atau saat HP lebih dari 0
            if self.hit_timer > 0:
                self.hit_timer -= 1
            else:
                self.image = self.image_idle  # Kembali ke gambar idle setelah efek hit selesai

        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.alive]

    def draw_health_bar_top_left(self, screen):
        """Menampilkan health bar di kiri atas layar."""
        hit_count = self.max_hp - self.hp
        index = min(hit_count, 10)  # Index 0 sampai 10
        health_image = self.health_images[index]
        screen.blit(health_image, (20, 20))

    def draw(self, screen):
        """Menggambar Meowchi dan peluru-pelurunya ke layar."""
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)
        self.draw_health_bar_top_left(screen)

    def check_collision(self, other):
        """Cek tabrakan menggunakan mask."""
        offset = (other.rect.x - self.rect.x, other.rect.y - self.rect.y)
        if self.mask.overlap(other.mask, offset):
            return True
        return False
