import pygame
import os
import math
from abc import ABC, abstractmethod

class Peluru(ABC):
    def __init__(self, x, y, target_pos, image_path, size, speed, damage, horizontal_only=False):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.__speed = speed
        self.__damage = damage

        dx = target_pos[0] - x
        dy = target_pos[1] - y
        if horizontal_only:
            direction = dx / abs(dx) if dx != 0 else 1
            self.__velocity = (direction * speed, 0)
        else:
            dist = math.hypot(dx, dy) or 1
            self.__velocity = (dx / dist * speed, dy / dist * speed)

        self.__alive = True
        self.__hit = False

    @property
    def speed(self):
        return self.__speed

    @property
    def damage(self):
        return self.__damage

    @property
    def velocity(self):
        return self.__velocity

    @property
    def alive(self):
        return self.__alive

    @alive.setter
    def alive(self, value):
        self.__alive = value

    @property
    def hit(self):
        return self.__hit

    @hit.setter
    def hit(self, value):
        self.__hit = value

    def update(self):
        self.rect.x += self.__velocity[0]
        self.rect.y += self.__velocity[1]
        w, h = pygame.display.get_surface().get_size()
        if (self.rect.right < 0 or self.rect.left > w or
            self.rect.bottom < 0 or self.rect.top > h):
            self.__alive = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    @abstractmethod
    def check_collision(self, target):
        pass

class Tomat(Peluru):
    def __init__(self, x, y, target_pos):
        image_path = os.path.join("Assets/bumbu/bumbu dapurr1.png")
        super().__init__(x, y, target_pos, image_path=image_path, size=(55, 55), speed=15, damage=1, horizontal_only=False)

    def check_collision(self, enemy):
        if self.hit or not enemy.alive:
            return False
        offset = (enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y)
        if self.mask.overlap(enemy.mask, offset):
            enemy.take_damage(self.damage)
            self.hit = True
            self.alive = False
            return True
        return False

class DogBone(Peluru):
    def __init__(self, x, y, target_pos):
        image_path = os.path.join("Assets/Anjing/tulang guguk.png")
        super().__init__(x, y, target_pos, image_path=image_path, size=(65, 65), speed=20, damage=3, horizontal_only=True)

    def check_collision(self, meowchi):
        offset = (meowchi.rect.x - self.rect.x, meowchi.rect.y - self.rect.y)
        if self.mask.overlap(meowchi.mask, offset):
            self.alive = False
            meowchi.take_damage(self.damage)
            return True
        return False

class Chili(Peluru):
    def __init__(self, x, y, target_pos):
        image_path = os.path.join("Assets/Meowzho/Chili.png")
        super().__init__(x, y, target_pos, image_path=image_path, size=(65, 65), speed=25, damage=5, horizontal_only=True)

    def check_collision(self, meowchi):
        offset = (meowchi.rect.x - self.rect.x, meowchi.rect.y - self.rect.y)
        if self.mask.overlap(meowchi.mask, offset):
            self.alive = False
            meowchi.take_damage(self.damage)
            return True
        return False

# pengujuan aja :v (opsional)
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    tomat = Tomat(100, 300, (700, 300))
    dog_bone = DogBone(700, 400, (100, 400))
    chili = Chili(700, 500, (100, 500))

    bullets = [tomat, dog_bone, chili]

    running = True
    while running:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for b in bullets:
            b.update()
            b.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
