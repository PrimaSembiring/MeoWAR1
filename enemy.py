import pygame
import os
import random
from abc import ABC, abstractmethod
from bullet import DogBone, Chili

class Enemy(ABC):
    def __init__(self, screen_width, screen_height, image_path, dead_image_path, hp, size):
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
        self.__hp = hp
        self.death_timer = 0
        self.DEATH_DURATION = 60
        self.score_awarded = False

    @abstractmethod
    def update(self, meowchi):
        pass

    @abstractmethod
    def draw(self, screen, debug=False):
        pass

    def take_damage(self, amount=1):
        self.__hp -= amount
        if self.__hp <= 0 and self.alive:
            self.alive = False
            self.death_timer = self.DEATH_DURATION
            self.image = self.dead_image
            return True
        return False

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, value):
        self.__hp = max(0, value)


class TikusDapur(Enemy):
    def __init__(self, screen_width, screen_height):
        image_path = os.path.join("Assets/tikus/tikus.png")
        dead_image_path = os.path.join("Assets/tikus/tikus_mati.png")
        super().__init__(screen_width, screen_height, image_path, dead_image_path, hp=1, size=(250, 250))
        self.speed = 5

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

class TikusPutih(Enemy):
    def __init__(self, screen_width, screen_height):
        image_path = os.path.join("Assets/tikus/tikusputih.png")
        dead_image_path = os.path.join("Assets/tikus/tikusputih_mati.png")
        super().__init__(screen_width, screen_height, image_path, dead_image_path, hp=2, size=(250, 250))
        self.speed = 5

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


class Anjing(Enemy):
    def __init__(self, screen_width, screen_height):
        image_idle_path = os.path.join("Assets/Anjing/guguk imut1.png")
        image_attack_path = os.path.join("Assets/Anjing/guguk imut2.png")
        image_dead_path = os.path.join("Assets/Anjing/guguk mati.png")
        super().__init__(screen_width, screen_height, image_idle_path, image_dead_path, hp=3, size=(375, 375))

        self.image_idle = self.image
        self.image_attack = pygame.image.load(image_attack_path).convert_alpha()
        self.image_attack = pygame.transform.scale(self.image_attack, self.size)

        self.image = self.image_idle
        self.speed = 1.5

        self.attack_timer = 0
        self.attack_interval = 60
        self.bullets = []

        self.meowchi_positions = []
        self.position_delay = 15

        self.attacking = False
        self.attack_duration = 15
        self.attack_anim_timer = 0

    def update(self, meowchi):
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            self.bullets.clear()
            return

        self.meowchi_positions.append(meowchi.rect.center)
        if len(self.meowchi_positions) > self.position_delay:
            target_x, target_y = self.meowchi_positions.pop(0)
        else:
            target_x, target_y = meowchi.rect.center

        if self.rect.centerx < target_x:
            self.rect.x += self.speed
        elif self.rect.centerx > target_x:
            self.rect.x -= self.speed

        if self.rect.centery < target_y:
            self.rect.y += self.speed
        elif self.rect.centery > target_y:
            self.rect.y -= self.speed

        if self.attacking:
            self.attack_anim_timer += 1
            if self.attack_anim_timer >= self.attack_duration:
                self.attacking = False
                self.attack_anim_timer = 0

        self.attack_timer += 1
        if self.attack_timer >= self.attack_interval:
            self.attack_timer = 0
            self.attacking = True
            self.shoot(meowchi)

        for bullet in self.bullets:
            bullet.update()
            if bullet.check_collision(meowchi):
                print("Meowchi terkena tulang!")

        self.bullets = [b for b in self.bullets if b.alive]
        self.image = self.image_attack if self.attacking else self.image_idle

    def shoot(self, meowchi):
        start_x = self.rect.centerx
        start_y = self.rect.centery
        target_pos = meowchi.rect.center
        self.bullets.append(DogBone(start_x, start_y, target_pos)) #objek Dogbone

    def take_damage(self, amount=1):
        return super().take_damage(amount)

    def draw(self, screen, debug=False):
        screen.blit(self.image, self.rect)
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        for bullet in self.bullets:
            bullet.draw(screen)


class Meowzho(Enemy):
    def __init__(self, screen_width, screen_height):
        image_idle_path = os.path.join("Assets/Meowzho/meowzho1.png")
        image_attack_path = os.path.join("Assets/Meowzho/meowzho2.png")
        image_dead_path = os.path.join("Assets/Meowzho/meowzho4.png")
        super().__init__(screen_width, screen_height, image_idle_path, image_dead_path, hp=20, size=(375, 375))

        self.image_idle = self.image
        self.image_attack = pygame.image.load(image_attack_path).convert_alpha()
        self.image_attack = pygame.transform.scale(self.image_attack, self.size)

        self.image = self.image_idle
        self.speed = 1.7

        self.attack_timer = 0
        self.attack_interval = 60
        self.bullets = []

        self.meowchi_positions = []
        self.position_delay = 15

        self.attacking = False
        self.attack_duration = 15
        self.attack_anim_timer = 0

    def update(self, meowchi):
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            self.bullets.clear()
            return

        self.meowchi_positions.append(meowchi.rect.center)
        if len(self.meowchi_positions) > self.position_delay:
            target_x, target_y = self.meowchi_positions.pop(0)
        else:
            target_x, target_y = meowchi.rect.center

        if self.rect.centerx < target_x:
            self.rect.x += self.speed
        elif self.rect.centerx > target_x:
            self.rect.x -= self.speed

        if self.rect.centery < target_y:
            self.rect.y += self.speed
        elif self.rect.centery > target_y:
            self.rect.y -= self.speed

        if self.attacking:
            self.attack_anim_timer += 1
            if self.attack_anim_timer >= self.attack_duration:
                self.attacking = False
                self.attack_anim_timer = 0

        self.attack_timer += 1
        if self.attack_timer >= self.attack_interval:
            self.attack_timer = 0
            self.attacking = True
            self.shoot(meowchi)

        for bullet in self.bullets:
            bullet.update()
            if bullet.check_collision(meowchi):
                print("Meowchi terkena Cabe!")

        self.bullets = [b for b in self.bullets if b.alive]
        self.image = self.image_attack if self.attacking else self.image_idle

    def shoot(self, meowchi):
        start_x = self.rect.centerx
        start_y = self.rect.centery
        target_pos = meowchi.rect.center
        self.bullets.append(Chili(start_x, start_y, target_pos)) #objek Chili

    def take_damage(self, amount=2):
        return super().take_damage(amount)

    def draw(self, screen, debug=False):
        screen.blit(self.image, self.rect)
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        for bullet in self.bullets:
            bullet.draw(screen)

# (opsional ini)
if __name__ == "__main__":
    pygame.init()
    screen_width, screen_height = 800, 600

    class DummyMeowchi:
        def __init__(self):
            self.rect = pygame.Rect(400, 300, 50, 50)

    meowchi = DummyMeowchi()

    tikus_dapur = TikusDapur(screen_width, screen_height)
    tikus_putih = TikusPutih(screen_width, screen_height)
    anjing = Anjing(screen_width, screen_height)
    meowzho = Meowzho(screen_width, screen_height)

    print("TikusDapur HP awal:", tikus_dapur.hp)
    tikus_dapur.take_damage()
    print("TikusDapur HP setelah damage:", tikus_dapur.hp)

    print("TikusPutih HP awal:", tikus_putih.hp)
    tikus_putih.take_damage()
    print("TikusPutih HP setelah damage:", tikus_putih.hp)

    print("Anjing HP awal:", anjing.hp)
    anjing.take_damage(3)
    print("Anjing HP setelah damage:", anjing.hp)

    print("Meowzho HP awal:", meowzho.hp)
    meowzho.take_damage(5)
    print("Meowzho HP setelah damage:", meowzho.hp)

    pygame.quit()