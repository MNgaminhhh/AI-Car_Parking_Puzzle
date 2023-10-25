import sys
import pygame
from settings import Settings
from playing_area import PlayingArea
from button import Button

class MyGame:
    pygame.init()

    def __init__(self):
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.playing_area = PlayingArea(self)
        self.btn_count = 0
        #self.btn_newgame = BtnNewGame(self, self.settings.tab_x_btn, self.playing_area.rect.y, "New game")
        #self.btn_create = BtnNewGame(self, self.settings.tab_x_btn, 
                                    #self.playing_area.rect.y + self.settings.tab_y_btn + self.settings.btn_height, "Create")
        pygame.display.set_caption("Car Parking Puzzle")
        
    def new_game(self):
        self.btn_init()

    def draw(self):
        for i in self.btn_list:
            i.blitme()

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.playing_area.draw()
        self.draw()
        pygame.display.flip()

    def btn_init(self):
        self.btn_list = []
        list_btn = ['New Game', 'Create', 'Reset']
        tab_x = self.settings.tab_x_btn
        tab_y = self.settings.tab_y_btn
        height = self.settings.btn_height
        for i, text in enumerate(list_btn):
            self.btn_list.append(Button(self, tab_x, (tab_y + height)*i + self.playing_area.rect.y, text))

    def check_event(self):
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                sys.exit()

    def run_game(self):
        while True: 
            self.update_screen()
            self.check_event()

if __name__ == '__main__':
    MG = MyGame()
    MG.new_game()
    MG.run_game()