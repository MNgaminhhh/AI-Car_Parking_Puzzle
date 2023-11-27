#length:
#a: 2, b: 2, c: 2, d:2, e: 2, p: 3, x:2, q: 3, o: 3, r:3

import pygame
from pygame.sprite import Sprite

class Car(Sprite):

    def __init__(self, game, category, lines, x, y):
        super().__init__()
        self.game = game
        self.playing_area = game.playing_area
        self.settings = game.settings
        self.tile_size = self.settings.tile_size
        self.cate = category
        self.lines = lines
        self.start_x, self.start_y = x, y
        self.end_x, self.end_y = self.start_x, self.start_y
        self.image = pygame.image.load('assets/'+str(self.cate)+'.png')
        length = [('x', 2),('a', 2),('b', 2),('c', 2),('d', 2),('e', 2),('f', 2),('g', 2),('h', 2),
                  ('i', 2),('j', 2),('k', 2),('l', 2),('m', 2),('n', 2),('o', 2),('p', 3),('q', 3),('r', 3)]
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
        if self.choose and self.lines == 'h' and self.can_move('l'):
            self.map[self.end_y+1][self.end_x+1] = 0
            self.rect.x-=self.tile_size
            self.start_x -= 1
            self.game.expense_move()

    def move_right(self):
        if self.choose and self.lines == 'h' and self.can_move('r'):
            self.map[self.start_y+1][self.start_x+1] = 0
            self.rect.x += self.tile_size
            self.start_x += 1
            self.game.expense_move()

    def move_up(self):
        if self.choose and self.lines == 'v' and self.can_move('u'):
            self.map[self.end_y+1][self.end_x+1] = 0
            self.rect.y -= self.tile_size
            self.start_y -= 1
            self.game.expense_move()

    def move_down(self):
        if self.choose and self.lines == 'v' and self.can_move('d'):
            self.map[self.start_y+1][self.start_x+1] = 0
            self.rect.y += self.tile_size
            self.start_y += 1
            self.game.expense_move()

    def can_move(self, dir):
        if dir == 'l':
            if (self.map[self.start_y+1][self.start_x] != 0):
                return False
        if dir == 'r':
            if (self.map[self.end_y+1][self.end_x+2] != 0):
                return False
        if dir == 'u':
            if (self.map[self.start_y][self.start_x+1] != 0):
                return False
        if dir == 'd':
            if (self.map[self.end_y+2][self.end_x+1] != 0):
                return False                  
        return True
