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
import time

class MyGame:
    pygame.init()

    def __init__(self):
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.map=[]
        self.init_map()
        self.combobox = ComboBox(71, 660, 230, 83, 'assets/combobox2.png', ['BFS', 'UCS', 'IDS', 'A*', 'BEAM', 'Hill climbing', 'GREEDY'])
        self.checkbox_button = Button(self, 71, 820, 'checkbox', 0.21)
        self.playing_area = PlayingArea(self)
        self.btn_count = 0
        self.problems = []
        self.problem = []
        self.car_cate = []
        self.selected_car = 'x'
        self.all_btn = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.goal = (0, 0)
        self.initialize_buttons() 
        self.in_start_menu = True
        self.newgame = True
        self.settings_visible = False
        self.checkbox_checked = False
        pygame.display.set_caption("Car Parking Puzzle")

    # Problem
    def shuffle_problem(self):
        max_int = len(self.problems)
        index = random.randint(0,max_int-1)
        
        print(index)
        self.problem = self.problems[index]

    def load_problem(self):
        self.problems = []
        if self.checkbox_checked:
            print("7x7")
            with open('problem/problem_7x7.txt', 'r') as f:
                lines = f.readlines()
            for line in lines:
                line = line.rstrip()
                problem = line.split(" ")
                self.problems.append(problem)
        else:
            print("6x6")
            with open('problem/problem_set.txt', 'r') as f:
                lines = f.readlines()
            for line in lines:
                line = line.rstrip()
                problem = line.split(" ")
                self.problems.append(problem)
    # Map
    def init_map(self):
        map_width = self.settings.map_width
        map_height = self.settings.map_height
        for i in range(map_height):
            self.map.append([])
            for j in range(map_width):
                if i == 0 or i == map_height-1 or j == 0 or ((j == map_width-1 or j == map_width-2) and i != 3):
                    self.map[i].append(-1)
                else:  
                    self.map[i].append(0)

    def create_map(self):
        self.map=[]
        self.init_map()

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
        self.draw()
        self.combobox.draw(self.screen)
        self.combobox_car.draw2(self.screen)
        self.expense.update()
        self.visited_text.update2()
        self.time_text.update2()
        self.sevenseven_text.update3()
        self.cars.update()
        self.playing_area.draw(self.map)
        for car in self.cars.sprites():
            car.draw()
        self.checkbox_button.blitme()
        pygame.display.flip()

    # Car
    def create_car(self):
        for car in self.problem:
            new_car = Car(self, car[0], car[3], int(car[1]), int(car[2]))
            self.cars.add(new_car)

    # Buttons
    def btn_init(self):
        self.btn_list = []
        list_btn = ['buttonNewGame', 'buttonReset', 'buttonStart2','backtomenu']
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
        self.car_cate = []
        self.step = 0
        self.expense = Text(self, 730, 820, 'Step: 0')
        self.visited = 0
        self.visited_text = Text(self, 430, 820, 'Visited States: 0')
        self.time_text = Text(self, 980, 820, 'Time: 0')
        self.sevenseven_text = Text(self, 165, 840, '7x7')
        for car in self.cars:
            car.kill()
        for btn in self.all_btn:
            btn.kill()
        if self.newgame:
            self.shuffle_problem()
            self.newgame=False
        if self.checkbox_checked:
            self.settings.map_height = 9
            self.settings.map_width = 10
        else:
            self.settings.map_height = 8
            self.settings.map_width = 9
        self.btn_init()
        self.create_map()
        self.create_car()
        for car in self.cars.sprites():
            self.car_cate.append(car.cate)
        print(self.car_cate)
        self.combobox_car = ComboBox(71, 500, 230, 83, 'assets/combobox2.png', self.car_cate)
        for car in self.cars:
            if car.cate == 'x':
                start_y = car.start_y
                self.goal = (start_y+1, self.settings.map_width-4)
                self.map[start_y+1][self.settings.map_width-2] = 0
                self.map[start_y+1][self.settings.map_width-1] = 0
    
    def check_back_to_menu(self):
        self.in_start_menu = True 
    
    def check_event(self):
        for event in pygame.event.get() :
            self.combobox.handle_event(event)
            self.combobox_car.handle_event(event)
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(self.settings.map_height):
                    for j in range(self.settings.map_width):
                        print(self.map[i][j],end=" ")
                    print() 
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_car_click(mouse_x, mouse_y)
                self.check_btn_click(mouse_x, mouse_y)
                if self.checkbox_button.click(mouse_x, mouse_y):
                    self.checkbox_checked = not self.checkbox_checked
                    if self.checkbox_checked:
                        self.settings.map_height = 9
                        self.settings.map_width = 10
                        self.init_game()    
                        self.sevenseven_text.text = '6x6'
                        checkbox_image_path = 'assets/checkbox2.png'
                        print(self.settings.map_height)
                    else:
                        self.settings.map_height = 8
                        self.settings.map_width = 9
                        checkbox_image_path = 'assets/checkbox.png'
                        self.init_game()
                        self.sevenseven_text.text = '7x7'
                        print(self.settings.map_height)
                    # self.playing_area = PlayingArea(self)
                    self.load_problem()
                    self.create_map()
                    checkbox_image = pygame.image.load(checkbox_image_path)
                    self.checkbox_button.image = pygame.transform.scale(checkbox_image, self.checkbox_button.rect.size)
            if event.type == pygame.KEYDOWN:
                self.move_car(event)
                if event.key == pygame.K_b:
                    self.bfs = BFS(self)
                    self.bfs.solve()  
                if event.key == pygame.K_g:
                    # self.greedy = GREEDY(self)
                    self.greedy = ASTAR(self)
                    #self.run_greedy_solver()
                    self.greedy.test()
                if event.key == pygame.K_h: 
                    self.run_hillclimbing_solver()
                if event.key == pygame.K_j:
                    self.run_astar_solver()
                if event.key == pygame.K_k:
                    self.run_beam_solver()
                if event.key == pygame.K_m:
                    self.run_greedy_solver()


    def check_car_click(self, mouse_x, mouse_y):
        relative_mouse_x = mouse_x - self.playing_area.rect.x
        relative_mouse_y = mouse_y - self.playing_area.rect.y
        print(relative_mouse_x, relative_mouse_y)
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

                    if event.key == pygame.K_q:
                        car.turn_left('lu')
                    if event.key == pygame.K_e:
                        car.turn_left('ru')
                    if event.key == pygame.K_z:
                        car.turn_right('ld')
                    if event.key == pygame.K_c:
                        car.turn_right('rd')

                    if event.key == pygame.K_7:
                        car.turn_left('ul')
                    if event.key == pygame.K_9:
                        car.turn_right('ur')
                    if event.key == pygame.K_1:
                        car.turn_left('dl')
                    if event.key == pygame.K_3:
                        car.turn_right('dr')
                    

                    print(car.cate, car.start_x, car.start_y)
        self.update_screen()
    def check_btn_click(self, mouse_x, mouse_y):
        for btn in self.all_btn:
            if btn.click(mouse_x, mouse_y):
                if btn.name == "buttonNewGame":
                    self.newgame = True
                    self.map_settings = False
                    self.problem_settings = []
                    
                    self.combobox_car = ComboBox(71, 500, 230, 83, 'assets/combobox2.png', self.car_cate)
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
                    self.selected_car = self.combobox_car.get_selected_option_car()
                    
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
        start_time = time.time()
        bfs = BFS(self)
        path = bfs.solve()
        self.visited = bfs.visited_states_count
        self.visited_text.text = "Visited States: " + str(self.visited)
        end_time = time.time()
        self.time_text.text = "Time: {:.6f}".format(end_time - start_time)
        print(f"BFS took {end_time - start_time:.6f} seconds")
        self.AI_playing(path)

    def run_beam_solver(self):
        start_time = time.time()
        beam = BEAM(self, 100)
        path = beam.solve()
        self.visited = beam.visited_states_count
        self.visited_text.text = "Visited States: " + str(self.visited)
        end_time = time.time()
        self.time_text.text = "Time: {:.6f}".format(end_time - start_time)
        print(f"BFS took {end_time - start_time:.6f} seconds")
        self.AI_playing(path)
    
    def run_IDS_solver(self):
        start_time = time.time()
        ids = IDS(self)
        path = ids.solve()
        self.visited = ids.visited_states_count
        self.visited_text.text = "Visited States: " + str(self.visited)
        end_time = time.time()
        self.time_text.text = "Time: {:.6f}".format(end_time - start_time)
        print(f"BFS took {end_time - start_time:.6f} seconds")
        self.AI_playing(path)

    def run_ucs_solver(self):
        start_time = time.time()
        ucs = UCS(self)
        path = ucs.solve()
        self.visited = ucs.visited_states_count
        self.visited_text.text = "Visited States: " + str(self.visited)
        end_time = time.time()
        self.time_text.text = "Time: {:.6f}".format(end_time - start_time)
        print(f"BFS took {end_time - start_time:.6f} seconds")
        self.AI_playing(path)
    
    def run_greedy_solver(self):
        start_time = time.time()
        greedy = GREEDY(self)
        path = greedy.solve()
        self.visited = greedy.visited_states_count
        self.visited_text.text = "Visited States: " + str(self.visited)
        end_time = time.time()
        self.time_text.text = "Time: {:.6f}".format(end_time - start_time)
        print(f"BFS took {end_time - start_time:.6f} seconds")
        self.AI_playing(path)

    def run_astar_solver(self):
        start_time = time.time()
        astar = ASTAR(self)
        path = astar.solve(self.selected_car)
        self.visited = astar.visited_states_count
        self.visited_text.text = "Visited States: " + str(self.visited)
        end_time = time.time()
        self.time_text.text = "Time: {:.6f}".format(end_time - start_time)
        print(f"BFS took {end_time - start_time:.6f} seconds")
        self.AI_playing(path)


    def run_hillclimbing_solver(self):
        start_time = time.time()
        hill = Hill_climbing(self)
        path = hill.solve()
        if (len(path)>1):
            self.visited = hill.visited_states_count
            self.visited_text.text = "Visited States: " + str(self.visited)
            end_time = time.time()
            self.time_text.text = "Time: {:.6f}".format(end_time - start_time)
            print(f"BFS took {end_time - start_time:.6f} seconds")
            self.AI_playing(path)
        else:
            self.visited = hill.visited_states_count
            self.visited_text.text = "Visited States: " + str(self.visited)
            end_time = time.time()
            self.time_text.text = "Time: {:.6f}".format(end_time - start_time)
            print(f"BFS took {end_time - start_time:.6f} seconds")
            print('Maximum local: ',path[0])

    def AI_playing(self, path):
        print(self.goal)
        if path:
            for i, node in enumerate(path):
                print(f"Step {i}:")
                print("Selected Car:", node.car_choose)
                print("Action:", node.action)
                # print("path:", node.state)
                for a in range(self.settings.map_height):
                    for b in range(self.settings.map_width):
                        print(node.state[a][b], end= ' ')
                    print()
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
                            if node.action == 'r':
                                print("Moving Right")
                                chosen_car.choose = 1
                                chosen_car.move_right()
                            if node.action == 'lu':
                                print("Moving Left up")
                                chosen_car.choose = 1
                                chosen_car.turn_left('lu')
                            if node.action == 'ru':
                                print("Moving Right up")
                                chosen_car.choose = 1
                                chosen_car.turn_left('ru')
                            if node.action == 'ld':
                                print("Moving Left down")
                                chosen_car.choose = 1
                                chosen_car.turn_right('ld')
                            if node.action == 'rd':
                                print("Moving Right down")
                                chosen_car.choose = 1
                                chosen_car.turn_right('rd')     
                        elif chosen_car.lines == 'v':
                            if node.action == 'u':
                                print("Moving Up")
                                chosen_car.choose = 1
                                chosen_car.move_up()
                            if node.action == 'd':
                                print("Moving Down")
                                chosen_car.choose = 1
                                chosen_car.move_down()
                            if node.action == 'ul':
                                print("Moving up left")
                                chosen_car.choose = 1
                                chosen_car.turn_left('ul')
                            if node.action == 'ur':
                                print("Moving up right")
                                chosen_car.choose = 1
                                chosen_car.turn_right('ur')
                            if node.action == 'dl':
                                print("Moving down left")
                                chosen_car.choose = 1
                                chosen_car.turn_left('dl')
                            if node.action == 'dr':
                                print("Moving Down right")
                                chosen_car.choose = 1
                                chosen_car.turn_right('dr')
                        self.update_screen()
                        pygame.time.Clock().tick(60)
                print("---------------")
        else:
            print("No solution found.") 

    def check_end_game(self):
        for car in self.cars:
            if car.cate == 'x':
                if car.start_y + 1 == self.goal[0] and car.start_x + 1 == self.goal[1] and car.lines == 'h':
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
            # pygame.time.Clock().tick(24000)
            if self.in_start_menu:
                self.show_start_menu()
            else:
                self.selected_car = self.combobox_car.get_selected_option_car()
                self.update_screen()
                self.all_btn.update()
                self.check_event()
                self.check_end_game()
    
    def show_start_menu(self):
        background_image = pygame.image.load('assets/background_menu.png')
        background_image = pygame.transform.scale(background_image, (self.settings.screen_width, self.settings.screen_height))
        self.screen.blit(background_image, [0, 0])
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
                        self.settings_visible = not self.settings_visible
                        self.show_settings()
                    elif self.quit_button.click(mouse_x, mouse_y):
                        sys.exit()
            self.cars.update()
            pygame.display.flip() 
    
    def show_settings(self):
        if self.settings_visible:
            problems = ['x02h']
            screen_width = self.settings.screen_width
            screen_height = self.settings.screen_height
            map_width = self.settings.map_width
            map_height = self.settings.map_height
            map = []
            hello_font = pygame.font.SysFont(None, 40)
            hello_text = hello_font.render('<= OR => MOVE CAR PLAYING', True, (255, 255, 255))
            hello_rect = hello_text.get_rect()
            line2_text = hello_font.render('DRAG CAR TO MAP TO SETTING MAP PRESS SPACE ROTATE CAR', True, (255, 255, 255))
            line2_rect = line2_text.get_rect()
            line2_rect.center = (screen_width // 2, screen_height - 90)
            hello_rect.center = (screen_width // 2, screen_height - 130)
            back_to_menu_button = Button(self, 100, 110, 'backtomenu', 0.21)
            acc_button = Button(self, 200, 110, 'buttonAcc', 0.20)
            for i in range(map_height):
                map.append([])
                for j in range(map_width):
                    if i == 0 or i == map_height-1  or j == 0 or ((j == map_width-1 or j==map_width-2) and i!=3):
                        map[i].append(-1) 
                    else:
                        map[i].append(0)
            map[3][1] = 'x'
            map[3][2] = 'x'
            settings_background = pygame.image.load('assets/background_setting2.png')
            settings_background = pygame.transform.scale(settings_background, (screen_width, screen_height))
            all_car = [Car(self, 'x', 'h', 0, 2)]
            for btn in self.all_btn:
                btn.blitme()
                cars = [('a', 2), ('b', 2),('r', 3), ('c', 2), ('d', 2), ('e', 2), ('f', 2), ('g', 2), ('h', 2),
                        ('i', 2), ('j', 2), ('k', 2), ('l', 2), ('m', 2), ('n', 2), ('o', 2), ('p', 3), ('q', 3)]
                car_objects = []
                for car_info in cars:
                    category, length = car_info
                    car = Car(self, category, 'h', 0, 0)
                    car_objects.append((car, length))
                num_columns = 3
            dragging_car = None
            offset_x, offset_y = 0, 0
            dragging_image = None
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for (car, _), i in zip(car_objects, range(len(car_objects))):
                            row = i // num_columns
                            col = i % num_columns
                            car_rect = pygame.Rect(100 + col * 120, 200 + row * 80, int(car.length * car.tile_size * scaling_factor), int(car.tile_size * scaling_factor))

                            if car_rect.collidepoint(event.pos):
                                dragging_car = Car(self, car.cate, 'h', 0, 0)
                                offset_x = event.pos[0] - car.rect.x
                                offset_y = event.pos[1] - car.rect.y
                                dragging_image = pygame.image.load(f'assets/{dragging_car.cate}.png')
                                scaling_factor = 0.7
                                dragging_image = pygame.transform.scale(dragging_image, (int(dragging_car.length * dragging_car.tile_size * scaling_factor), int(dragging_car.tile_size * scaling_factor)))
                        if back_to_menu_button.rect.collidepoint(event.pos):
                            self.show_start_menu()
                            # print(self.settings_visible)
                       
                        if acc_button.rect.collidepoint(event.pos):
                            self.in_start_menu=False
                            isVisible=False
                            self.problem=problems 
                            self.newgame=False
                            self.init_game()
                            return
                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_SPACE and dragging_car is not None:
                            dragging_car.rotate()
                            dragging_image = pygame.transform.rotate(dragging_image, 90)
                        if event.key == pygame.K_s:
                            self.in_start_menu=False
                            isVisible=False
                            self.problem=problems
                            self.newgame=False
                            self.init_game()
                            return
                        if event.key == pygame.K_RIGHT:
                            for i in all_car:
                                if i.cate == 'x':
                                    if (map[i.end_y+1][i.end_x+2])==0 and i.end_x+1 < map_width-3:
                                        map[i.start_y+1][i.start_x+1] = 0
                                        map[i.end_y+1][i.end_x+2]='x'
                                        i.start_x += 1
                                        i.update()
                                        p = i.cate+str(i.start_x)+str(i.start_y)+'h'
                                        problems.pop(0)
                                        problems.insert(0, p)
                        if event.key == pygame.K_LEFT:
                            for i in all_car:
                                if i.cate == 'x':
                                    if map[i.start_y+1][i.start_x] == 0:
                                        map[i.end_y+1][i.end_x+1] = 0
                                        map[i.start_y+1][i.start_x] = 'x'
                                        i.start_x -= 1
                                        i.update()
                                        p = i.cate+str(i.start_x)+str(i.start_y)+'h'
                                        problems.pop(0)
                                        problems.insert(0, p)
                                    print(map)
                        for i in all_car:
                            print(i.cate, i.start_x)
                    if event.type == pygame.MOUSEMOTION:
                        if dragging_car is not None:
                            dragging_car.rect.x = event.pos[0] - offset_x
                            dragging_car.rect.y = event.pos[1] - offset_y
                    if event.type == pygame.MOUSEBUTTONUP:
                        if dragging_car is not None:
                            map_col = (event.pos[0] - self.playing_area.rect.topleft[0]) // self.playing_area.tile_size - 1
                            map_row = (event.pos[1] - self.playing_area.rect.topleft[1]) // self.playing_area.tile_size - 1 
                            self.map[map_row][map_col] = dragging_car.cate
                            print(f"Dropped car {dragging_car.cate} into map at row {map_row}, column {map_col} {dragging_car.lines}")
                            if ((map_col>=0 and map_col<map_width-1) and (map_row>=0 and map_row<map_height-1) and (map[map_row+1][map_col+1]==0)):
                                new_car = Car(self, dragging_car.cate, dragging_car.lines, map_col, map_row)
                                all_car.append(new_car)
                                new_car.update()
                                start_x = new_car.start_x
                                start_y = new_car.start_y
                                end_x = new_car.end_x
                                end_y = new_car.end_y
                                if (map[end_y+1][end_x+1] != 0 or (start_y+1 == 3 and new_car.lines == 'h')):
                                    all_car.pop()
                                else:
                                    map[start_y+1][start_x+1]=new_car.cate
                                    map[end_y+1][end_x+1]=new_car.cate
                                    problem = new_car.cate+str(new_car.start_x)+str(new_car.start_y)+new_car.lines
                                    problems.append(problem)
                                    for (car, _), i in zip(car_objects, range(len(car_objects))):
                                        if car.cate==new_car.cate:
                                            car_objects.pop(i)
                            dragging_car = None
                            dragging_image = None
                    if self.checkbox_checked:
                        checkbox_image = pygame.image.load('assets/checkbox2.png')
                    else:
                        checkbox_image = pygame.image.load('assets/checkbox.png')
                self.screen.fill((255, 255, 255))
                self.screen.blit(settings_background, [0, 0])
                self.screen.blit(self.playing_area.image, self.playing_area.rect.topleft)
                self.playing_area.draw(map)
                for i in all_car:
                    i.blitme(self.playing_area.image)
                for (car, _), i in zip(car_objects, range(len(car_objects))):
                    row = i // num_columns
                    col = i % num_columns
                    car_image = pygame.image.load(f'assets/{car.cate}.png')
                    scaling_factor = 0.7
                    car_image = pygame.transform.scale(car_image, (int(car.length * car.tile_size * scaling_factor), int(car.tile_size * scaling_factor)))
                    if car.cate != 'q' and car.cate != 'r':
                        car.rect.topleft = (100 + col * 120, 200 + row * 80)
                    else:
                        car.rect.topleft = (100 + col*120+40, 200 + row * 80)
                    self.screen.blit(car_image, car.rect)
                if dragging_image is not None:
                    self.screen.blit(dragging_image, (pygame.mouse.get_pos()[0] - offset_x, pygame.mouse.get_pos()[1] - offset_y))
                self.screen.blit(hello_text, hello_rect)
                # button back to menu
                back_to_menu_button.blitme()
                self.screen.blit(line2_text, line2_rect)
                # tick button
                acc_button.blitme()
                for car in all_car:
                    car.update()
                pygame.display.flip()
                pygame.time.Clock().tick(60)
if __name__ == '__main__':
    MG = MyGame()
    MG.load_problem()
    MG.init_game()
    MG.run_game()