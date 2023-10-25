#length:
#a: 2, p: 3, x:2, q: 3, o: 3, c: 2, r:3, b: 2

import pygame
from pygame.sprite import Sprite

class Car(Sprite):

    def __init__(self, game, category, lines, x, y):
        super().__init__()
        self.playing_area = game.playing_area
        self.settings = game.settings
        self.cate = category
        self.lines = lines
        self.x, self.y = x, y
        self.image = pygame.image.load('assets/'+str(self.cate)+'.png')
        self.rect = self.image.get_rect()
        self.length = [('a', 2), ('p', 3), ('x', 2), ('q', 3), ('o', 3), ('c', 2), ('r', 3), ('b', 2)]
        size = 1
        for i in self.length:
            if i[0] == self.cate:
                size = i[1]
        self.image = pygame.transform.scale(self.image, (size*self.settings.tile_size, self.settings.tile_size))
        if self.lines == 'v':
            self.image = pygame.transform.rotate(self.image, 90)

    def draw(self):
        self.rect.x = (self.x+1)*self.settings.tile_size
        self.rect.y = (self.y+1)*self.settings.tile_size
        self.playing_area.image.blit(self.image, self.rect)