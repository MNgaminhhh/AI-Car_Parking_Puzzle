import sys
import pygame
import random
from src.settings import Settings
from src.playing_area import PlayingArea
from src.button import Button
from src.car import Car
from src.text import Text
from src.combobox import ComboBox

class MyGame:
    pygame.init()

    def __init__(self):
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.init_map()
        self.combobox = ComboBox(71, 430, 230, 83, 'assets/combobox.png', ['BFS', 'DFS'])
        self.playing_area = PlayingArea(self)
        self.btn_count = 0
        self.problems = []
        self.problem = []
        self.all_btn = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.goal = (0, 0)
        self.initialize_buttons()
        self.in_start_menu = True
        pygame.display.set_caption("Car Parking Puzzle")

    # Problem
    def shuffle_problem(self):
        max_int = len(self.problems)
        index = random.randint(0,max_int-1)
        print(index)
        self.problem =  self.problems[index]

    def load_problem(self):
        with open('problem/problem_set.txt', 'r') as f:
            lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            problem = line.split(" ")
            self.problems.append(problem) 
    # Map  
    def init_map(self):
        self.map = [[0 for _ in range(self.settings.map_width)] for _ in range(self.settings.map_height)]

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
    def initialize_buttons(self):
        buttons = [('buttonStart', self.settings.menu_btn_margin), ('buttonSetting', self.settings.menu_btn_margin), ('buttonQuit', self.settings.menu_btn_margin)]
        tab_x = self.settings.menu_x_btn
        tab_y = self.settings.menu_y_btn
        height = self.settings.menu_btn_height
        self.all_btn.empty()
        for i, (btn_name, offset) in enumerate(buttons):
            y_position = (tab_y + height) * i + offset
            new_btn = Button(self, tab_x, y_position, btn_name, 0.65)
            self.all_btn.add(new_btn)
        self.start_button, self.settings_button, self.quit_button = self.all_btn.sprites()

    def draw(self):
        for btn in self.all_btn:
            btn.blitme()

    def update_screen(self):
        background_image = pygame.image.load('assets/background_game.png')
        background_image = pygame.transform.scale(background_image, (self.settings.screen_width, self.settings.screen_height))
        self.screen.blit(background_image, (0, 0))
        self.playing_area.draw()
        self.draw()
        self.combobox.draw(self.screen)
        self.expense.update()
        for car in self.cars.sprites():
            car.draw()
        pygame.display.flip()

    
    # Car
    def create_car(self):
        for car in self.problem:
            new_car = Car(self, car[0], car[3], int(car[1]), int(car[2]))
            self.cars.add(new_car)

    # Buttons
    def btn_init(self):
        self.btn_list = []
        list_btn = ['buttonNewGame', 'buttonReset']
        tab_x = self.settings.tab_x_btn
        tab_y = self.settings.tab_y_btn
        height = self.settings.btn_height
        for i, image_path in enumerate(list_btn):
            y_position = (tab_y + height) * i + self.playing_area.rect.y
            new_btn = Button(self, tab_x, y_position, image_path, 0.215)
            self.all_btn.add(new_btn)
    
    #Game
    def init_game(self):
        self.step = 0
        self.expense = Text(self, 100, 720, 'Step: 0')
        for car in self.cars:
            car.kill()
        for btn in self.all_btn:
            btn.kill()
        self.btn_init()
        self.create_car()
        self.create_map()

    def check_event(self):
        for event in pygame.event.get() :
            self.combobox.handle_event(event)
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print(mouse_x, mouse_y)
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
                    self.shuffle_problem()
                    self.init_map()
                    self.init_game()
                if btn.name == "buttonReset":
                    self.init_map()
                    self.init_game()

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
        
    def expense_move(self):
        self.step += 1
        self.expense.text = "Step: " + str(self.step)

    def run_game(self):
        while True:
            if self.in_start_menu:
                self.show_start_menu()
            else:
                self.update_screen()
                self.all_btn.update()
                self.cars.update()
                self.check_event()
                self.check_end_game()
    def show_start_menu(self):
        background_image = pygame.image.load('assets/background_menu.png').convert()
        background_image = pygame.transform.scale(background_image, (self.settings.screen_width, self.settings.screen_height))
        self.screen.blit(background_image, [0, 0])
        self.start_button.blitme()
        self.settings_button.blitme()
        self.quit_button.blitme()
        pygame.display.flip() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.start_button.click(mouse_x, mouse_y):
                    self.in_start_menu = False 
                elif self.settings_button.click(mouse_x, mouse_y):
                    print("Settings button clicked")
                elif self.quit_button.click(mouse_x, mouse_y):
                    sys.exit()

if __name__ == '__main__':
    MG = MyGame()
    MG.load_problem()
    MG.shuffle_problem()
    MG.init_game()
    MG.run_game()