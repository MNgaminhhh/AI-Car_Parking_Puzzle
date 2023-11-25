from src.node import Node
from src.priority_queue import priority_queue
import copy

class Hill_climbing:

    def __init__(self, game):
        self.quizz = game.map
        self.goal = game.goal
        self.cars = game.cars
        self.game = game

    def init_cars(self):
        self.cars = []
        for car in self.game.cars:
            cate = car.cate
            lines = car.lines
            start_x = car.start_x
            start_y = car.start_y
            end_x = car.end_x
            end_y = car.end_y
            self.cars.append({"cate": cate, "lines": lines, "start_x": start_x, "start_y": start_y, "end_x": end_x, "end_y": end_y})

    def can_move(self, quizz, car, dir):
        if dir == 'l':
            if (quizz[car["start_y"]+1][car["start_x"]] == 0 and car["start_x"]>0):
                return True
        if dir == 'r':
            if (car["end_x"]+1 < self.game.settings.map_width - 1):
                if (quizz[car["end_y"]+1][car["end_x"]+2] == 0 ):
                    return True
        if dir == 'u':
            if (quizz[car["start_y"]][car["start_x"]+1] == 0):
                return True
        if dir =='d':
            if (quizz[car["end_y"]+2][car["end_x"]+1] == 0):
                return True
        return False
    
    def convert_to_key(self, state):
        key = ''.join([str(i) for list in state for i in list])
        key = key.replace('-1', '')
        return key
    
    def create_neighbors(self, parent, cars):
        neighbors = []
        print("parent: ",self.convert_to_key(parent));
        for index in range(len(cars)):
            if cars[index]["lines"] == 'h':
                if self.can_move(parent, cars[index], 'l'):
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_state[new_car[index]["start_y"]+1][new_car[index]["start_x"]] = new_car[index]["cate"]
                    new_state[new_car[index]["end_y"]+1][new_car[index]["end_x"]+1] = 0
                    new_car[index]
                    new_car[index]["start_x"] -= 1
                    new_car[index]["end_x"] -=1
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'l'))
                if self.can_move(parent, cars[index], 'r'):
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_state[new_car[index]["end_y"]+1][new_car[index]["end_x"]+2] = new_car[index]["cate"]
                    new_state[new_car[index]["start_y"]+1][new_car[index]["start_x"]+1] = 0
                    new_car[index]["start_x"] += 1
                    new_car[index]["end_x"] +=1
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'r'))
            if cars[index]["lines"] == 'v':
                if self.can_move(parent, cars[index], 'u'):
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_state[new_car[index]["start_y"]][new_car[index]["start_x"]+1] = new_car[index]["cate"]
                    new_state[new_car[index]["end_y"]+1][new_car[index]["end_x"]+1] = 0
                    new_car[index]["start_y"] -= 1
                    new_car[index]["end_y"] -=1
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'u'))
                if self.can_move(parent, cars[index], 'd'):
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_state[new_car[index]["end_y"]+2][new_car[index]["end_x"]+1] = new_car[index]["cate"]
                    new_state[new_car[index]["start_y"]+1][new_car[index]["start_x"]+1] = 0
                    new_car[index]["start_y"] += 1
                    new_car[index]["end_y"] +=1
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'd'))
        return neighbors
    
    def heuristic_distance(self, node):
        cars = node.all_cars
        for car in cars:
            if car['cate'] == 'x':
                distance = self.goal[1] - car['start_x'] - 1
        return distance
    
    def heuristic_obstacle(self, node):
        state = node.state
        cars = node.all_cars
        row = 0
        obstacle = 0
        for car in cars:
            if car['cate'] == 'x':
                row = car['start_y']+1
                end_index = car['end_x']+1
                break
        for col in range(self.game.settings.map_width-2):
            if col > end_index:
                val = state[row][col]
                if val != 0 and val != 'x':
                    obstacle += 1
        return obstacle
    
    def solve(self):
        self.init_cars()
        start_node = Node(self.quizz, None, self.cars, None, None, None)
        visited = set()
        
    
    def test(self):
        self.init_cars()
        node = Node(self.quizz, None, self.cars, None, None, None)
        distance = self.heuristic_distance(node)
        obstacle = self.heuristic_obstacle(node)
        print('Distance: ', distance)
        print('Obstacle: ', obstacle)