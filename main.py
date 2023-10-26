import sys
import pygame
from settings import Settings
from playing_area import PlayingArea
from button import Button
from car import Car

class MyGame:
    pygame.init()

    def __init__(self):
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.playing_area = PlayingArea(self)
        self.btn_count = 0
        self.problem_text = ['a00h', 'p01v', 'x11h']
        self.cars = pygame.sprite.Group()
        pygame.display.set_caption("Car Parking Puzzle")
    
    def create_car(self):
        for car in self.problem_text:
            new_car = Car(self, car[0], car[3], int(car[1]), int(car[2]))
            self.cars.add(new_car)
        
    def new_game(self):
        self.btn_init()
        self.create_car()

    def draw(self):
        for i in self.btn_list:
            i.blitme()

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.playing_area.draw()
        self.draw()
        for car in self.cars.sprites():
            car.draw()
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