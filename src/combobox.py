import pygame

class ComboBox:
    def __init__(self, x, y, width, height, color, options=[]):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.options = options
        self.selected_option_index = 0
        self.txt_surface = pygame.font.Font(None, 32).render(self.options[self.selected_option_index], True, self.color)
        self.active = False
        self.is_open = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Toggle the active state and also whether the combo box is open
                self.active = not self.active
                self.is_open = not self.is_open
            else:
                self.active = False
                self.is_open = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_UP:
                    self.selected_option_index = max(0, self.selected_option_index - 1)
                elif event.key == pygame.K_DOWN:
                    self.selected_option_index = min(len(self.options) - 1, self.selected_option_index + 1)
                self.txt_surface = pygame.font.Font(None, 32).render(self.options[self.selected_option_index], True, self.color)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        if self.is_open:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i+1) * self.rect.height, self.rect.width, self.rect.height)
                pygame.draw.rect(screen, self.color, option_rect, 2)
                option_surface = pygame.font.Font(None, 32).render(option, True, self.color)
                screen.blit(option_surface, (option_rect.x+5, option_rect.y+5))
