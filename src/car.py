#length:
#a: 2, p: 3, x:2, q: 3, o: 3, c: 2, r:3, b: 2

import pygame
from pygame.sprite import Sprite

class Car(Sprite):

    def __init__(self, game, category, lines, x, y):
        super().__init__()
        self.playing_area = game.playing_area
        self.settings = game.settings
        self.tile_size = self.settings.tile_size
        self.cate = category
        self.lines = lines
        self.start_x, self.start_y = x, y
        self.end_x, self.end_y = self.start_x, self.start_y
        self.image = pygame.image.load('assets/'+str(self.cate)+'.png')
        length = [('a', 2), ('p', 3), ('x', 2), ('q', 3), ('o', 3), ('c', 2), ('r', 3), ('b', 2)]
        self.length = 1
        for i in length:
            if i[0] == self.cate:
                self.length = i[1]
        self.image = pygame.transform.scale(self.image, (self.length*self.tile_size, self.tile_size))
        if self.lines == 'v':
            self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.choose = 0
        self.rect.x = (self.start_x+1)*self.tile_size
        self.rect.y = (self.start_y+1)*self.tile_size
        self.map = game.map

    def update(self):
        u = self.start_y+1
        v = self.start_x+1
        self.map[u][v] = self.cate
        if self.lines == 'h':
            self.end_x = self.start_x + self.length-1
        else:
            self.end_y = self.start_y + self.length-1 
        for i in range(1, self.length):
            if self.lines == 'h':
                self.map[u][v+i] = self.cate
            else:
                self.map[u+i][v] = self.cate

    def draw(self):
        self.playing_area.image.blit(self.image, self.rect)

    def click(self, mouse_x, mouse_y):
        left = self.rect.left
        top = self.rect.top
        right = self.rect.right
        bottom = self.rect.bottom
        return left <= mouse_x <= right and top <= mouse_y <= bottom
    
    def move_left(self):
        self.map[self.end_x+1][self.end_y+1] = 0
        if self.choose and self.lines == 'h':
            self.rect.x-=self.tile_size
            self.start_x -= 1

    def move_right(self):
        self.map[self.start_y+1][self.start_x+1] = 0
        if self.choose and self.lines == 'h':
            self.rect.x += self.tile_size
            self.start_x += 1

    def move_up(self):
        self.map[self.end_x+1][self.end_y+1] = 0
        if self.choose and self.lines == 'v':
            self.rect.y -= self.tile_size
            self.start_y -= 1

    def move_down(self):
        self.map[self.start_y+1][self.start_x+1] = 0
        if self.choose and self.lines == 'v':
            self.rect.y += self.tile_size
            self.start_y += 1