import pygame

pygame.font.init()

class Button():
    
    def __init__(self, game, x, y, text):
       self.screen = game.screen
       self.settings = game.settings
       self.height = self.settings.btn_height
       self.width = self.settings.btn_width
       self.image = pygame.Surface((self.width, self.height))
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y
       self.image.fill(self.settings.btn_color)
       self.text = text
       self.font = pygame.font.SysFont("Consolas", 20)
       self.font_size = self.font.size(self.text)
       font_surface = self.font.render(self.text, True, self.settings.font_color)
       text_rect = font_surface.get_rect()
       text_rect.center = (self.width//2, self.height//2)
       self.image.blit(font_surface, text_rect) 

    def blitme(self):
        self.screen.blit(self.image, self.rect)