import pygame
class DialogBox:
    def __init__(self, image, name, dialog_text, font, screen, box_bg_path=None):
        self.portrait = pygame.image.load(image).convert_alpha()
        self.portrait = pygame.transform.scale(self.portrait, (300, 300))

        self.name = name
        self.full_text = dialog_text
        self.displayed_text = ""
        self.font = font
        self.screen = screen
        self.text_index = 0
        self.finished = False

        if box_bg_path:
            self.box_image = pygame.image.load(box_bg_path).convert_alpha()
            self.box_image = pygame.transform.scale(self.box_image, (screen.get_width() - 20, 200))
        else:
            self.box_image = pygame.Surface((screen.get_width() - 20, 200))
            self.box_image.fill((255, 105, 180))
        self.box_rect = self.box_image.get_rect(center=(screen.get_width() // 2, screen.get_height() - 70))

        self.name_surface = self.font.render(self.name, True, (100, 200, 255))

        self.text_timer = 0
        self.typing_speed = 40  # ms per char
        
    def update(self, dt):
        if self.text_index < len(self.full_text):
            self.text_timer += dt
            if self.text_timer >= self.typing_speed:
                self.displayed_text += self.full_text[self.text_index]
                self.text_index += 1
                self.text_timer = 0
        else:
            self.finished = True

    def draw(self):
        self.screen.blit(self.box_image, self.box_rect)

    # Mengatur posisi portrait di kiri dan tengah vertikal kotak
        portrait_rect = self.portrait.get_rect()
        portrait_rect.left = self.box_rect.left + 100
        portrait_rect.centery = self.box_rect.top + self.box_rect.height // 2
        self.screen.blit(self.portrait, portrait_rect)

    # Posisi nama dan teks bergeser ke kanan setelah portrait
        name_x = portrait_rect.right - 40
        name_y = self.box_rect.top + 70
        self.name_surface = self.font.render(self.name, True, (100, 200, 255))
        self.screen.blit(self.name_surface, (name_x, name_y))

    # Teks dialog muncul di bawah nama
        text_surface = self.font.render(self.displayed_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (name_x, name_y + self.name_surface.get_height() + 10))
        # self.screen.blit(text_surface, (name_x, name_y + 30))

