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
        self.map = [[0 for _ in range(self.settings.map_width)] for _ in range(self.settings.map_height)]
        self.playing_area = PlayingArea(self)
        self.btn_count = 0
        self.problem_text = ['a00h' , 'p01v','b04v', 'x12h', 'q31v', 'c44h', 'o50v', 'r25h']
        self.all_btn = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.goal = (0, 0)
        pygame.display.set_caption("Car Parking Puzzle")
    
    def create_car(self):
        for car in self.problem_text:
            new_car = Car(self, car[0], car[3], int(car[1]), int(car[2]))
            self.cars.add(new_car)

    def create_map(self):
        m = self.settings.map_height
        n = self.settings.map_width
        y = 0
        for car in self.cars:
            if car.cate == 'x':
                y = car.start_y
        for i in range(m):
            for j in range(n):
                if i == 0 or i == m-1 or j == 0 or (i != y+1 and j == n-1) or (i!= y+1 and j == n-2):
                    self.map[i][j] = -1
        self.goal = (y+1, n-2)
        
    def new_game(self):
        for car in self.cars:
            car.kill()
        self.btn_init()
        self.create_car()
        self.create_map()

    def draw(self):
        for btn in self.all_btn:
            btn.blitme()

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.playing_area.draw()
        self.draw()
        for car in self.cars.sprites():
            car.draw()
        pygame.display.flip()

    def btn_init(self):
        self.btn_list = []
        list_btn = ['buttonNewGame', 'buttonCreate', 'buttonReset']
        tab_x = self.settings.tab_x_btn
        tab_y = self.settings.tab_y_btn
        height = self.settings.btn_height
        for i, image_path in enumerate(list_btn):
            y_position = (tab_y + height) * i + self.playing_area.rect.y
            new_btn = Button(self, tab_x, y_position, image_path)
            self.all_btn.add(new_btn)

    def check_event(self):
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_car_click(mouse_x, mouse_y)
                self.check_btn_click(mouse_x, mouse_y)
            if event.type == pygame.KEYDOWN:
                self.move_car(event)         

    def check_car_click(self, mouse_x, mouse_y):
        relative_mouse_x = mouse_x - self.playing_area.rect.x
        relative_mouse_y = mouse_y - self.playing_area.rect.y
        for car in self.cars.sprites():
            if car.click(relative_mouse_x, relative_mouse_y):
                car.choose = 1
            else:
                car.choose = 0

    def move_car(self, event):
        if not self.check_end_game():
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

    def check_btn_click(self, mouse_x, mouse_y):
        for btn in self.all_btn:
            if btn.click(mouse_x, mouse_y):
                if btn.name == "buttonNewGame":
                    self.new_game()

    def check_end_game(self):
        for car in self.cars:
            if car.cate == 'x':
                if car.start_y + 1 == self.goal[0] and car.start_x + 1 == self.goal[1]:
                    self.message("Win")
                    return True
        return False
    
    def message(self, text):
        image = pygame.Surface((200, 100))
        image.fill((255, 255, 255))
        image_rect = image.get_rect()
        image_rect.center = self.playing_area.image.get_rect().center
        font = pygame.font.SysFont('Consolas', 40)
        text = font.render('Win', True, (0, 0, 0))
        rect = text.get_rect()
        rect.center = (100, 50)
        image.blit(text, rect)
        self.playing_area.image.blit(image, image_rect)

    def run_game(self):
        while True:
            self.update_screen()
            self.all_btn.update()
            self.cars.update()
            self.check_event()
            self.check_end_game()

if __name__ == '__main__':
    MG = MyGame()
    MG.new_game()
    MG.run_game()