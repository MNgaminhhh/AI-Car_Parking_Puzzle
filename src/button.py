import pygame
from pygame.sprite import Sprite

pygame.font.init()

class Button(Sprite):
    
    def __init__(self, game, x, y, btn_name, scale=1):
        super().__init__()
        self.screen = game.screen
        self.name = btn_name
        self.image = pygame.image.load('assets/' + btn_name + '.png')
        self.image = pygame.transform.rotozoom(self.image, 0, scale)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def blitme(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom