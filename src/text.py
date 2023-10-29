import pygame
class Text:
    
    def __init__(self, game, x, y, text):
        self.settings = game.settings
        self.screen = game.screen
        self.x, self.y = x, y
        self.text = text
    
    def update(self):
        self.font = pygame.font.SysFont('Consolas', 40)
        self.image = self.font.render(self.text, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.screen.blit(self.image, self.rect)