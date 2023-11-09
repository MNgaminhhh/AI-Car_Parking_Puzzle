import pygame

class ComboBox:
    def __init__(self, x, y, width, height, image_path, options=[]):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.options = options
        self.selected_option_index = 0
        self.font = pygame.font.Font(None, 42)
        self.txt_surface = self.font.render(self.options[self.selected_option_index], True, (0, 0, 0))
        self.active = False
        self.is_open = False
        self.color = (255, 255, 255)
        self.option_rects = []
        for i in range(len(options)):
            option_rect = pygame.Rect(x, y + (i + 1) * height, width, height)
            self.option_rects.append(option_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_open = not self.is_open
                self.active = True
            else:
                self.is_open = False
                self.active = False
            if self.is_open:
                for i, option_rect in enumerate(self.option_rects):
                    if option_rect.collidepoint(event.pos):
                        self.selected_option_index = i
                        self.txt_surface = self.font.render(self.options[self.selected_option_index], True, (0, 0, 0))
                        self.active = False
                        self.is_open = False
                        break
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_UP:
                    self.selected_option_index = max(0, self.selected_option_index - 1)
                elif event.key == pygame.K_DOWN:
                    self.selected_option_index = min(len(self.options) - 1, self.selected_option_index + 1)
                self.txt_surface = self.font.render(self.options[self.selected_option_index], True, (0, 0, 0))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        selected_text = self.options[self.selected_option_index]
        text_surface = pygame.font.Font(None, 42).render(selected_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        transparent_color = (200, 200, 200, 100)
        if self.is_open:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                transparent_surface = pygame.Surface((option_rect.width, option_rect.height), pygame.SRCALPHA)
                transparent_surface.fill(transparent_color)
                screen.blit(transparent_surface, option_rect)
                option_surface = pygame.font.Font(None, 32).render(option, True, (0, 0, 0))
                screen.blit(option_surface, (option_rect.x + 5, option_rect.y + 5))
