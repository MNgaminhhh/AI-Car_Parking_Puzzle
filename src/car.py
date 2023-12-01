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
        self.update()
    def rotate(self):
        if self.lines == 'h':
            self.lines = 'v'
        else:
            self.lines = 'h'
        return self.lines
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
        self.rect.x = (self.start_x+1)*self.tile_size
        self.rect.y = (self.start_y+1)*self.tile_size

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

    def turn_left(self, dir):
        if self.choose:
            if self.lines == 'v':
                if dir == 'ul':
                    if self.can_move('ul'):
                        self.rotate_image = pygame.transform.rotate(self.image, 30)
                        rotate_rect = self.rotate_image.get_rect()
                        rotate_rect.center = self.rect.center
                        rotate_rect.y -= 0.9*self.tile_size
                        rotate_rect.x -= 0.3*self.tile_size
                        self.playing_area.image.blit(self.rotate_image, rotate_rect)
                        self.game.expense_move()
                        self.image = pygame.transform.rotate(self.image, 90)
                        self.rect = self.image.get_rect()
                        for i in range(self.length):
                            self.map[self.start_y+1+i][self.start_x+1] = 0
                        self.start_x -= self.length-1 
                        self.start_y -= 1
                        self.lines = 'h'
                        self.game.expense_move()
                        self.update()
                if dir == 'dl':
                    if self.can_move('dl'):
                        print('Move')
                        self.rotate_image = pygame.transform.rotate(self.image, -30)
                        rotate_rect = self.rotate_image.get_rect()
                        rotate_rect.center = self.rect.center
                        rotate_rect.y += 0.9*self.tile_size
                        rotate_rect.x -= 0.3*self.tile_size
                        self.playing_area.image.blit(self.rotate_image, rotate_rect)
                        self.game.expense_move()
                        self.image = pygame.transform.rotate(self.image, -90)
                        self.rect = self.image.get_rect()
                        for i in range(self.length):
                            self.map[self.start_y+1+i][self.start_x+1] = 0
                        self.start_x -= self.length-1 
                        self.start_y += self.length
                        self.lines = 'h'
                        self.game.expense_move()
                        self.update()

            else:
                if dir == 'ru':
                    if self.can_move('ru'):
                        self.rotate_image = pygame.transform.rotate(self.image, 30)
                        rotate_rect = self.rotate_image.get_rect()
                        rotate_rect.center = self.rect.center
                        rotate_rect.y -= 0.3*self.tile_size
                        rotate_rect.x += 1.2*self.tile_size
                        self.playing_area.image.blit(self.rotate_image, rotate_rect)
                        self.game.expense_move()
                        self.image = pygame.transform.rotate(self.image, 90)
                        self.rect = self.image.get_rect()
                        for i in range(self.length):
                            self.map[self.start_y+1][self.start_x+1+i] = 0
                        self.start_x += self.length 
                        self.start_y -= 1
                        self.lines = 'v'
                        self.game.expense_move()
                        self.update()
                if dir == 'lu':
                    if self.can_move('lu'):
                        self.rotate_image = pygame.transform.rotate(self.image, -30)
                        rotate_rect = self.rotate_image.get_rect()
                        rotate_rect.center = self.rect.center
                        rotate_rect.y -= 0.3*self.tile_size
                        rotate_rect.x -= 0.9*self.tile_size
                        self.playing_area.image.blit(self.rotate_image, rotate_rect)
                        self.game.expense_move()
                        self.image = pygame.transform.rotate(self.image, -90)
                        self.rect = self.image.get_rect()
                        for i in range(self.length):
                            self.map[self.start_y+1][self.start_x+1+i] = 0
                        self.start_x -= self.length - 1
                        self.start_y -= 1
                        self.lines = 'v'
                        self.game.expense_move()
                        self.update()

            for i in range(8):
                for j in range(9):
                    print(self.map[i][j], end=' ')
                print()
        
    def turn_right(self, dir):  
        if self.choose:
            #Xe dọc
            #1.
            if self.lines == 'v':
                if dir == 'ur':
                    if self.can_move('ur'):
                        self.rotate_image = pygame.transform.rotate(self.image, -30)
                        rotate_rect = self.rotate_image.get_rect()
                        rotate_rect.center = self.rect.center
                        rotate_rect.y -= 1.2*self.tile_size
                        rotate_rect.x += 0.3*self.tile_size
                        self.playing_area.image.blit(self.rotate_image, rotate_rect)
                        self.game.expense_move()
                        
                        self.image = pygame.transform.rotate(self.image, -90)
                        self.rect = self.image.get_rect()
                        #map
                        for i in range(self.length):
                            self.map[self.start_y+1+i][self.start_x+1] = 0

                        self.start_y -= 1
                        self.lines = 'h'
                        self.game.expense_move()
                        self.update()
            #2
            if self.lines == 'v':
                if dir == 'dr':
                    if self.can_move('dr'):
                        self.rotate_image = pygame.transform.rotate(self.image, 30)
                        rotate_rect = self.rotate_image.get_rect()
                        rotate_rect.center = self.rect.center
                        rotate_rect.x += 0.3*self.tile_size
                        rotate_rect.y += 0.9*self.tile_size
                        self.playing_area.image.blit(self.rotate_image, rotate_rect)
                        self.game.expense_move()
                        
                        self.image = pygame.transform.rotate(self.image, 90)
                        self.rect = self.image.get_rect()
                        #map
                        for i in range(self.length):
                            self.map[self.start_y+1+i][self.start_x+1] = 0

                        self.start_y += self.length
                        self.lines = 'h'
                        self.game.expense_move()
                        self.update()
            #Xe ngang
            else:
                if dir == 'rd':
                    if self.can_move('rd'):
                        self.rotate_image = pygame.transform.rotate(self.image, -30)
                        rotate_rect = self.rotate_image.get_rect()
                        rotate_rect.center = self.rect.center
                        rotate_rect.x += 1.2*self.tile_size
                        rotate_rect.y += 0.3*self.tile_size
                        self.playing_area.image.blit(self.rotate_image, rotate_rect)
                        self.game.expense_move()
                        
                        self.image = pygame.transform.rotate(self.image, -90)
                        self.rect = self.image.get_rect()
                        #map
                        for i in range(self.length):
                            self.map[self.start_y+1][self.start_x+1+i] = 0
                        
                        self.start_x += self.length
                        self.lines = 'v'
                        self.game.expense_move()
                        self.update()
                elif dir == 'ld':
                    if self.can_move('ld'):
                        self.rotate_image = pygame.transform.rotate(self.image, 30)
                        rotate_rect = self.rotate_image.get_rect()
                        rotate_rect.center = self.rect.center
                        rotate_rect.x -= 0.7*self.tile_size
                        rotate_rect.y += 1.2*self.tile_size
                        self.playing_area.image.blit(self.rotate_image, rotate_rect)
                        self.game.expense_move()
                        
                        self.image = pygame.transform.rotate(self.image, 90)
                        self.rect = self.image.get_rect()
                        #map
                        for i in range(self.length):
                            self.map[self.start_y+1][self.start_x+1+i] = 0
                        
                        self.start_x -= 1
                        self.lines = 'v'
                        self.game.expense_move()
                        self.update()
            
            for i in range(8):
                for j in range(9):
                    print(self.map[i][j], end=' ')
                print()


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
        #Xe nằm dọc:
        if dir == 'ul':
            print('ul')
            for i in range(self.length):
                if self.map[self.start_y][self.start_x+1-i] != 0:
                    return False 
        if dir == 'ur':
            print('ur')
            for i in range(self.length):
                print(self.start_y, self.start_x+1+i)
                if self.map[self.start_y][self.start_x+1+i] != 0:
                    return False       
        if dir == 'dr':
            print('dr')
            for i in range(self.length):
                print(self.end_y+2, self.end_x+1+i)
                if self.map[self.end_y+2][self.end_x+1+i] != 0:
                    return False 
        if dir == 'dl':
            print('dl')
            for i in range(self.length):
                print(self.end_y+1, self.end_x+1)
                print(self.end_y+2, self.end_x+1-i)
                if self.map[self.end_y+2][self.end_x+1-i] != 0:
                    return False
        #Xe nằm ngang:
        if dir == 'ru':
            print('ru')
            for i in range(self.length):
                print(self.end_y+1+i, self.end_x+2)
                if self.map[self.end_y+1-i][self.end_x+2] != 0:
                    return False
        if dir == 'lu':
            print('lu')
            for i in range(self.length):
                if self.map[self.start_y+1-i][self.start_x] != 0:
                    return False
        if dir == 'rd':
            print('rd')
            for i in range(self.length):
                if self.map[self.end_y+1+i][self.end_x+2] != 0:
                    return False
        if dir == 'ld':
            print('ld')
            for i in range(self.length):
                if self.map[self.start_y+1+i][self.start_x]:
                    return False
        return True  

    def blitme(self, surface):
        surface.blit(self.image, self.rect)