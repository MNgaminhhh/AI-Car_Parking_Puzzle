import sys
import pygame
from src.settings import Settings
from src.playing_area import PlayingArea
from src.button import Button
from src.car import Car

class MyGame:
    pygame.init()

    def __init__(self):
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.map = []
        self.playing_area = PlayingArea(self)
        self.btn_count = 0
        self.problem_text = ['a00h' , 'p01v','b04v', 'x12h', 'q31v', 'c44h', 'o50v', 'r25h']
        self.cars = pygame.sprite.Group()
        pygame.display.set_caption("Car Parking Puzzle")
    
    def create_car(self):
        for car in self.problem_text:
            new_car = Car(self, car[0], car[3], int(car[1]), int(car[2]))
            self.cars.add(new_car)

    def create_map(self):
        m = self.settings.map_height
        n = self.settings.map_width
        for i in range(m):
            self.map.append([])
            for j in range(n):
                if i == 0 or i == m-1 or j == 0 or j == n-1 or j == n - 2:
                    self.map[i].append(-1)
                else:
                    self.map[i].append(0)
        for car in self.problem_text:
            if car[0] == 'x':
                if car[3] == 'h':
                    col = int(car[2])+1
                    self.map[col][n-1] = 0
                    self.map[col][n-2] = 0
                else:
                    row = int(car[1])+1
                    self.map[m-1][row] = 0
                    self.map[m-2][row] = 0

        
    def new_game(self):
        self.btn_init()
        self.create_car()
        self.create_map()

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
        list_btn = ['assets/buttonNewGame.png', 'assets/buttonCreate.png', 'assets/buttonReset.png']
        tab_x = self.settings.tab_x_btn
        tab_y = self.settings.tab_y_btn
        height = self.settings.btn_height
        button_spacing = 100
        for i, image_path in enumerate(list_btn):
            y_position = (tab_y + height + button_spacing) * i + self.playing_area.rect.y
            self.btn_list.append(Button(self, tab_x, y_position, image_path))

    def check_event(self):
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                relative_mouse_x = mouse_x - self.playing_area.rect.x
                relative_mouse_y = mouse_y - self.playing_area.rect.y
                print(self.map)
                for car in self.cars.sprites():
                    if car.click(relative_mouse_x, relative_mouse_y):
                        car.choose = 1
                        print(car.cate)
                    else:
                        car.choose = 0
            if event.type == pygame.KEYDOWN:
                for car in self.cars.sprites():
                    if car.choose == 1:
                        if event.key == pygame.K_RIGHT:
                            car.move_right()
                        if event.key == pygame.K_LEFT:
                            car.move_left()
                        if event.key == pygame.K_UP:
                            car.move_up()
                        if event.key == pygame.K_DOWN:
                            car.move_down()

    def run_game(self):
        while True: 
            self.update_screen()
            self.check_event()

if __name__ == '__main__':
    MG = MyGame()
    MG.new_game()
    MG.run_game()