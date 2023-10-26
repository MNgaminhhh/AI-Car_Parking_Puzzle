import pygame
from pygame.sprite import Sprite

pygame.font.init()

class Button(Sprite):
    
    def __init__(self, game, x, y, image_path):
        self.screen = game.screen
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def blitme(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
