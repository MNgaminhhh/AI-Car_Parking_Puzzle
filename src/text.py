import pygame

class Text:
    
    def __init__(self, game, x, y, text):
        self.settings = game.settings
        self.screen = game.screen
        self.x, self.y = x, y
        self.text = text
    
    def update(self):
        # Load the background image
        background_image = pygame.image.load('assets/button.png')
        background_image = pygame.transform.scale(background_image, (230, 83))  # Adjust the size as needed
        
        # Blit the background image onto the screen
        self.screen.blit(background_image, (self.x, self.y))
        
        # Render the text
        self.font = pygame.font.SysFont('Consolas', 32)
        self.image = self.font.render(self.text, True, (0, 0, 0)) 
        self.rect = self.image.get_rect()
        # Adjust the position of the text based on the background image's position and size
        self.rect.x = self.x + (background_image.get_width() - self.image.get_width()) // 2
        self.rect.y = self.y + (background_image.get_height() - self.image.get_height()) // 2
        self.screen.blit(self.image, self.rect)
