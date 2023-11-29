import sys
import pygame
import random
from src.IDS import IDS
from src.BFS import BFS
from src.UCS import UCS
from src.Beam import BEAM
from src.Greedy import GREEDY
from src.Astar import ASTAR
from src.Hill_climbing import Hill_climbing
from src.settings import Settings
from src.playing_area import PlayingArea
from src.button import Button
from src.car import Car
from src.text import Text
from src.combobox import ComboBox
from src.node import Node
#from src.priority_queue import QueueElement
class MyGame:
    pygame.init()

    def __init__(self):
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.init_map()
        self.combobox = ComboBox(71, 495, 230, 83, 'assets/combobox.png', ['BFS', 'UCS', 'IDS', 'A*', 'BEAM', 'Hill climbing', 'Greedy'])
        self.playing_area = PlayingArea(self)
        self.btn_count = 0
        self.problems = []
        self.problem = []
        self.all_btn = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.goal = (0, 0)
        self.initialize_buttons() 
        self.in_start_menu = True
        self.buttons_visible = True
        pygame.display.set_caption("Car Parking Puzzle")

    # Problem
    def shuffle_problem(self):
        max_int = len(self.problems)
        index = random.randint(0,max_int-1)
        print(index)
        self.problem = self.problems[4]

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
        self.goal = (y+1, n-4)

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
        self.visited_text.update2()
        self.cars.update()
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
        list_btn = ['buttonNewGame', 'buttonReset', 'buttonStart2', 'buttonstop','backtomenu']
        tab_x = self.settings.tab_x_btn
        tab_y = self.settings.tab_y_btn
        height = self.settings.btn_height
        padding = self.settings.btn_padding_top
        for i, image_path in enumerate(list_btn):
            y_position = (tab_y + height) * i + padding
            new_btn = Button(self, tab_x, y_position, image_path, 0.215)
            self.all_btn.add(new_btn)
    
    #Game
    def init_game(self):
        self.step = 0
        self.expense = Text(self, 71, 580, 'Step: 0')
        self.visited = 0
        self.visited_text = Text(self, 49, 670, 'Visited States: 0')
        for car in self.cars:
            car.kill()
        for btn in self.all_btn:
            btn.kill()
        self.btn_init()
        self.create_car()
        self.create_map()
    def check_back_to_menu(self):
        self.in_start_menu = True 
    def check_event(self):
        for event in pygame.event.get() :
            self.combobox.handle_event(event)
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_car_click(mouse_x, mouse_y)
                self.check_btn_click(mouse_x, mouse_y)
            if event.type == pygame.KEYDOWN:
                self.move_car(event)
                if event.key == pygame.K_b:
                    self.bfs = BFS(self)
                    self.bfs.solve()      
                if event.key == pygame.K_u:
                    self.ucs = UCS(self)
                    self.ucs.test()  
                if event.key == pygame.K_g:
                    self.greedy = GREEDY(self)
                    self.greedy.test()
                if event.key == pygame.K_h: 
                    self.run_hillclimbing_solver()
                if event.key == pygame.K_j:
                    self.run_astar_solver()
                if event.key == pygame.K_k:
                    self.run_beam_solver()


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
                    print(car.cate, car.start_x, car.start_y)
        self.update_screen()
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
                if btn.name == "buttonstop":
                    self.init_map()
                    self.init_game()
                if btn.name == "backtomenu":
                    self.check_back_to_menu()
                if btn.name == "buttonStart2":
                    selected_algorithm = self.combobox.get_selected_option()
                    if selected_algorithm == 'BFS':
                        self.run_bfs_solver()   
                    elif selected_algorithm == 'GREEDY':
                        self.run_greedy_solver()
                    elif selected_algorithm == 'A*':
                        self.run_astar_solver()
                    elif selected_algorithm == 'BEAM':
                        self.run_beam_solver()
                    elif selected_algorithm == 'Hill climbing':
                        self.run_hillclimbing_solver()
                    elif selected_algorithm == 'UCS':
                        self.run_ucs_solver()
                    elif selected_algorithm == 'IDS':
                        self.run_IDS_solver()
          
    def run_bfs_solver(self):
        bfs = BFS(self)
        path = bfs.solve()
        self.visited = bfs.visited_states_count
        self.visited_text.text = "Visited States: " + str(self.visited)
        self.AI_playing(path)
    
    def run_beam_solver(self):
        beam = BEAM(self, 100)
        path = beam.solve()
        self.visited = beam.visited_states_count
        self.visited_text.text = "Visited States: " + str(self.visited)
        self.AI_playing(path)
    
    def run_IDS_solver(self):
        ids = IDS(self)
        path = ids.solve()
        self.visited = ids.visited_states_count
        self.visited_text.text = "Visited States: " + str(self.visited)
        self.AI_playing(path)

    def run_ucs_solver(self):
        ucs = UCS(self)
        path = ucs.solve()
        self.visited = ucs.visited_states_count
        self.visited_text.text = "Visited States: " + str(self.visited)
        self.AI_playing(path)
    
    def run_greedy_solver(self):
        greedy = GREEDY(self)
        path = greedy.solve()
        self.visited = greedy.visited_states_count
        self.visited_text.text = "Visited States: " + str(self.visited)
        self.AI_playing(path)
    def run_astar_solver(self):
        astar = ASTAR(self)
        path = astar.solve()
        self.visited = astar.visited_states_count
        self.visited_text.text = "Visited States: " + str(self.visited)
        self.AI_playing(path)

    def run_hillclimbing_solver(self):
        hill = Hill_climbing(self)
        path = hill.solve()
        if (len(path)>1):
            self.visited = hill.visited_states_count
            self.visited_text.text = "Visited States: " + str(self.visited)
            self.AI_playing(path)
        else:
            print('Maximum local: ',path[0])

    def print_heuristic_values(self, node):
        distance = node.heuristic_distance
        obstacle = node.heuristic_obstacle
        print(f'Khoảng cách: {distance}, Số lượng vật cản: {obstacle}')

    def AI_playing(self, path):
        if path:
            for i, node in enumerate(path):
                print(f"Step {i}:")
                print("Selected Car:", node.car_choose)
                print("Action:", node.action)
                if node.car_choose is not None:
                    chosen_car = None
                    for car in self.cars:
                        if car.cate == node.car_choose:
                            chosen_car = car
                            break
                    if chosen_car:
                        if chosen_car.lines == 'h':
                            if node.action == 'l':
                                print("Moving Left")
                                chosen_car.choose = 1
                                chosen_car.move_left()
                            
                            elif node.action == 'r':
                                print("Moving Right")
                                chosen_car.choose = 1
                                chosen_car.move_right()
                                
                        elif chosen_car.lines == 'v':
                            if node.action == 'u':
                                print("Moving Up")
                                chosen_car.choose = 1
                                chosen_car.move_up()
                                
                            elif node.action == 'd':
                                print("Moving Down")
                                chosen_car.choose = 1
                                chosen_car.move_down()
                        self.update_screen()
                        pygame.time.wait(100) 
                        self.update_screen()
                print("---------------")
        else:
            print("No solution found.") 

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
                self.check_event()
                self.check_end_game()
    
    def show_start_menu(self):
        show_settings = True
        background_image = pygame.image.load('assets/background_menu.png').convert()
        background_image = pygame.transform.scale(background_image, (self.settings.screen_width, self.settings.screen_height))
        self.screen.blit(background_image, [0, 0])
        if self.buttons_visible:
            self.start_button.blitme()
            self.settings_button.blitme()
            self.quit_button.blitme()
        while self.in_start_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.start_button.click(mouse_x, mouse_y):
                        self.in_start_menu = False 
                    elif self.settings_button.click(mouse_x, mouse_y):
                        self.show_settings(show_settings)
                        self.buttons_visible = False
                    elif self.quit_button.click(mouse_x, mouse_y):
                        sys.exit()
            self.cars.update()
            pygame.display.flip() 
    
    def show_settings(self, isVisible):
        screen_width = self.settings.screen_width
        screen_height = self.settings.screen_height
        if isVisible:
            settings_background = pygame.image.load('assets/background_setting.png')
            settings_background = pygame.transform.scale(settings_background, (screen_width, screen_height))
            self.screen.blit(settings_background, [0, 0])
            menu_width = screen_width * 1
            menu_height = screen_height * 1
            menu_x = (screen_width - menu_width) // 2
            menu_y = (screen_height - menu_height) // 2
            self.board = pygame.Surface((menu_width, menu_height))
            self.board_rect = self.board.get_rect()
            self.board_rect.topleft = (menu_x, menu_y)
            pygame.display.flip()

if __name__ == '__main__':
    MG = MyGame()
    MG.load_problem()
    MG.shuffle_problem()
    MG.init_game()
    MG.run_game()