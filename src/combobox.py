import pygame

class ComboBox:
    def __init__(self, x, y, width, height, image_path, options=[]):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.options = options
        self.selected_option_index = 0
        self.font = pygame.font.Font(None, 40)
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
                if event.key == pygame.K_LEFT:
                    self.selected_option_index = max(0, self.selected_option_index - 1)
                elif event.key == pygame.K_RIGHT:
                    self.selected_option_index = min(len(self.options) - 1, self.selected_option_index + 1)
                self.txt_surface = self.font.render(self.options[self.selected_option_index], True, (0, 0, 0))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        selected_text = self.options[self.selected_option_index]
        text_surface = pygame.font.Font(None, 42).render(selected_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        transparent_color = (200, 200, 200, 100)
    def draw2(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        selected_option = self.options[self.selected_option_index]
        selected_image_path = 'assets/' + selected_option + '.png'
        original_image = pygame.image.load(selected_image_path)
        selected_image = pygame.transform.scale(original_image, (int(self.rect.width * 0.5), int(self.rect.height * 0.65)))
        x = (self.rect.width - selected_image.get_width()) // 2 + self.rect.x
        y = (self.rect.height - selected_image.get_height()) // 2 + self.rect.y
        screen.blit(selected_image, (x, y))

    def get_selected_option(self):
        return self.options[self.selected_option_index]
    def get_selected_option_car(self):
        return self.options[self.selected_option_index]

