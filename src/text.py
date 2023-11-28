import pygame

class Text:
    
    def __init__(self, game, x, y, text):
        self.settings = game.settings
        self.screen = game.screen
        self.x, self.y = x, y
        self.text = text
    
    def update(self):
        background_image = pygame.image.load('assets/button.png')
        background_image = pygame.transform.scale(background_image, (230, 83))
        self.screen.blit(background_image, (self.x, self.y))
        self.font = pygame.font.SysFont(None, 40)
        self.image = self.font.render(self.text, True, (0, 0, 0)) 
        self.rect = self.image.get_rect()
        self.rect.x = self.x + (background_image.get_width() - self.image.get_width()) // 2
        self.rect.y = self.y + (background_image.get_height() - self.image.get_height()) // 2
        self.screen.blit(self.image, self.rect)
    def update2(self):
        background_image = pygame.image.load('assets/button2.png')
        background_image = pygame.transform.scale(background_image, (280, 83))
        self.screen.blit(background_image, (self.x, self.y))
        self.font = pygame.font.SysFont(None, 38)
        self.image = self.font.render(self.text, True, (0, 0, 0)) 
        self.rect = self.image.get_rect()
        self.rect.x = self.x + (background_image.get_width() - self.image.get_width()) // 2
        self.rect.y = self.y + (background_image.get_height() - self.image.get_height()) // 2
        self.screen.blit(self.image, self.rect)
    def update3(self):
        background_image = pygame.image.load('assets/backtomenu.png')
        background_image = pygame.transform.scale(background_image, (83, 83))
        self.screen.blit(background_image, (self.x, self.y))
        self.font = pygame.font.SysFont(None, 38)
        self.image = self.font.render(self.text, True, (0, 0, 0)) 
        self.rect = self.image.get_rect()
        self.rect.x = self.x + (background_image.get_width() - self.image.get_width()) // 2
        self.rect.y = self.y + (background_image.get_height() - self.image.get_height()) // 2
        self.screen.blit(self.image, self.rect)
