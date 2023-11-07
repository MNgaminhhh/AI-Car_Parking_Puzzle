import sys
import pygame
import random
from src.settings import Settings
from src.playing_area import PlayingArea
from src.button import Button
from src.car import Car
from src.text import Text

class MyGame:
    pygame.init()

    def __init__(self):
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.init_map()
        self.playing_area = PlayingArea(self)
        self.btn_count = 0
        options = [
            ['a00h' ,'p01v' ,'b04v', 'x12h' ,'q31v' ,'c44h' ,'o50v','r25h'],
            ['a00v' ,'x02h' ,'q03h' ,'f05h' ,'d24v' ,'b31v' ,'c42v' ,'e44h' ,'g35h' ,'o30h' ,'p51v'],
            ['a13h' ,'b14v' ,'c25h' ,'x12h' ,'o32v' ,'p53v'],
            ['a23v' ,'b54v' ,'x12h' ,'o00v' ,'p03v' ,'q33h' ,'r25h'],
            ['a00h' ,'b50v' ,'d04v' ,'e44h' ,'f45h' ,'g52v' ,'x12h' ,'o30v' ,'p01v' ,'q41v', 'r13h'],
            ['a00h' ,'b30v' ,'c01h' ,'d03h' ,'e23v' ,'f04v', 'x12h' ,'o42v' ,'p51v' ,'q32v', 'r35h'],
            ['a10v' ,'b20h' ,'c40v' ,'d50v' ,'e31v' ,'f52v' ,'g34v' ,'i23h' ,'x12h'],
            ['a30h' ,'b21h' ,'c41v' ,'d22v' ,'e32v' ,'f03h' ,'g43h' ,'h04h', 'i24v' ,'k05h' ,'o50v' ,'p34h' ,'q35h' ,'x02h'],
            ['a10v' ,'b20h' ,'c40h' ,'d31v', 'e41h' ,'f52v' ,'g24v' ,'h54v' ,'x02h' ,'o42v' ,'p03v' ,'q13h'],
            ['a00h' ,'b20v' ,'c40h' ,'d01h' ,'e34v' ,'f44h' ,'g05h' ,'h45h' ,'x12h' ,'o51v' ,'p02v' ,'q13h'],
            ['a00h' ,'b20h' ,'c40v' ,'d01v' ,'e21h' ,'f12v' ,'g05h' ,'o50v' ,'p22v' ,'q33h', 'x32h'],
            ['a20v' ,'b41h' ,'c13v' ,'d43h', 'e04v' ,'f24h' ,'g54v', 'o30h' ,'p31v' ,'q15h' ,'x12h'],
            ['a10h' ,'b30h' ,'c01h' ,'d21h' ,'e23v' ,'f33v' ,'g44h' ,'h15h' ,'i35h' ,'o41v' ,'p51v' ,'q02v' ,'r12v' ,'x22h'],
            ['a20v' ,'b01h' ,'c41v' ,'d02v' ,'e13v' ,'f23v' ,'g33h' ,'i34h' ,'o30h' ,'p53v' ,'q15h', 'x12h'],
            ['a10h' ,'b23v' ,'e54v' ,'o00v' ,'p30v' ,'q33h' ,'r25h' ,'x12h'],
            ['a10h' ,'b30v' ,'c40h' ,'d11h' ,'e51v' ,'f03h' ,'g04v' ,'h15h' ,'i35h' ,'o22v' ,'p53v' ,'x32h'],
            ['a10v' ,'b20h' ,'c40h' ,'d13h' ,'e33h' ,'f24v' ,'g34v' ,'h44h' ,'i05h' ,'o01v' ,'p51v' ,'x12h'],
            ['a30v' ,'b40h' ,'c32v' ,'d42v' ,'e14v' ,'f24v' ,'g34h' ,'o00v' ,'p03h' ,'q53v' ,'x12h'],
            ['a10v' ,'b40h' ,'c41h' ,'d03v' ,'e14h' ,'f34v' ,'g45h' ,'o20v' ,'p52v' ,'q13h' ,'x02h'],
            ['a20v' ,'b40h' ,'c01v' ,'d31h', 'e03h' ,'f23v' ,'g33v' ,'h44h' ,'i15h' ,'j35h' ,'o10v' ,'p51v' ,'x22h'],
            ['a00h' ,'b20v' ,'c40h' ,'d01h' ,'e42v' ,'f14v' ,'g34v' ,'h44h', 'i45h' ,'o51v' ,'p02v' ,'q13h' ,'x12h'],
            ['a00v','b10h','c11h' ,'d22v' ,'e33h' ,'f24v' ,'o30v' ,'p52v' ,'r35h' ,'x02h'],
            ['a00h' ,'b20v' ,'c11v' ,'d34v' ,'e44h' ,'f05h' ,'g45h' ,'o01v' ,'p41v' ,'q51v' ,'r13h' ,'x22h'],
            ['a10h' ,'b30v' ,'c40v' ,'d11v', 'e33v' ,'f24v' ,'g44h' ,'h05h' ,'i35h' ,'o00v' ,'p51v' ,'q03h' ,'x32h'],
            ['a00h' ,'b20v' ,'c40h' ,'d42v' ,'e34v' ,'f44h' ,'g05h' ,'o01v' ,'p51v' ,'q13h' ,'x22h'],
            ['a20v' ,'b31h' ,'c51v' ,'d32v' ,'e42v' ,'f03h' ,'g34v' ,'h44h' ,'i54h' ,'o00v' ,'p30h' ,'x12h'],
            ['a10v' ,'b20h' ,'c40v' ,'d21v' ,'e51v' ,'f03h' ,'g23v' ,'h33h' ,'i04v' ,'j34h' ,'o53v' ,'p25h' ,'x02h'],
            ['a40v' ,'b50v' ,'c52v' ,'d13v' ,'e24v' ,'f34v' ,'g44h' ,'i45h' ,'o00h' ,'p02v' ,'q23h' ,'x12h'],
            ['a21v' ,'b52v' ,'c03v' ,'d13h' ,'e33h' ,'f14h' ,'g34v' ,'h54v' ,'o00h' ,'p40v' ,'r05h' ,'x02h'],
            ['a20v' ,'b01h' ,'c41v' ,'d02v' ,'e43h' ,'f04h' ,'g24h' ,'h54v' ,'i05h' ,'j25h' ,'o30h' ,'p31v' ,'x12h']
        ]
        selected_options = random.choice(options)
        self.problem_text = selected_options
        #self.problem_text = ['a20v' ,'b01h' ,'c41v', 'd02v' ,'e43h' ,'f04h' ,'g24h' ,'h54v' ,'i05h' ,'j25h' ,'o30h' ,'p31v' ,'x12h']
        self.all_btn = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.goal = (0, 0)
        pygame.display.set_caption("Car Parking Puzzle")
        
    def shuffle_problem():
        pass
        
    def init_map(self):
        self.map = [[0 for _ in range(self.settings.map_width)] for _ in range(self.settings.map_height)]
    
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
        self.step = 0
        self.expense = Text(self, 1000, 50, 'Step: 0')
        for car in self.cars:
            car.kill()
        for btn in self.all_btn:
            btn.kill()
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
        self.expense.update()
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
                    self.init_map()
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
        
    def expense_move(self):
        self.step += 1
        self.expense.text = "Step: " + str(self.step)

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