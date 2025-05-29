import pygame

class ImageButton:
    def __init__(self, image_path, x, y, callback, size=(200, 80)):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.callback = callback

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def handle_event(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.callback()
