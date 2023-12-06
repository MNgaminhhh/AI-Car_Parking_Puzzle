from src.node import Node
from src.priority_queue import QueueElement
import copy
import queue
class ASTAR:
    def __init__(self, game):
        self.quizz = game.map
        self.goal = game.goal
        self.cars = game.cars
        self.game = game
        self.index_car = None
        self.settings = game.settings
        self.visited_states_count = 0

    def init_cars(self):
        self.cars = []
        for car in self.game.cars:
            cate = car.cate
            lines = car.lines
            start_x = car.start_x
            start_y = car.start_y
            end_x = car.end_x
            end_y = car.end_y
            length = car.length
            self.cars.append({"cate": cate, "lines": lines, "start_x": start_x, "start_y": start_y, "end_x": end_x, "end_y": end_y, "length":length})

    
    def can_move(self, quizz, car, dir):
        #Horizontal
        width = self.settings.map_width
        height = self.settings.map_height
        length = car['length']
        if car["lines"] == 'h':
            if dir == 'l':
                if (quizz[car["start_y"]+1][car["start_x"]] == 0):
                    return True
                return False
            if dir == 'r':
                if (car['start_x']+1+length >= width):
                    return False
                if (quizz[car["start_y"]+1][car['start_x']+1+length] == 0 ):
                    return True
                return False
            
            if dir == 'ru':
                for i in range(car['length']):
                    if (car["start_y"]+1-i>=height or car["start_x"]+1+length >= width):
                        return False
                    if quizz[car["start_y"]+1-i][car["start_x"]+1+length] != 0:
                        return False
                return True
            
            if dir == 'lu':
                for i in range(length):
                    if (car['start_y']+1-i >= height):
                        return False
                    if quizz[car['start_y']+1-i][car['start_x']] != 0:
                        return False
                return True
            
            if dir == 'rd':
                for i in range(length):
                    if (car['start_x']+length >= self.settings.map_width or car['start_y']+1+i >= height):
                        return False
                    if quizz[car['start_y']+1+i][car['start_x']+length] != 0:
                        return False
                return True
            
            if dir == 'ld':
                for i in range(length):
                    if (car["start_x"] >= width or car["start_y"]+1+i >= height):
                        return False
                    if quizz[car["start_y"]+1+i][car["start_x"]] != 0:
                        return False
                return True
        #Vertical
        else:
            if dir == 'u':
                if (quizz[car["start_y"]][car["start_x"]+1] == 0):
                    return True
                return False
            if dir =='d':
                if (quizz[car["start_y"]+length+1][car["start_x"]+1] == 0):
                    return True
                return False
            if dir == 'ul':
                for i in range(car['length']):
                    if quizz[car["start_y"]][car["start_x"]+1-i] != 0:
                        return False
                return True    
            
            if dir == 'ur':
                for i in range(car['length']):
                    if(car["start_x"]+1+i>= width):
                        return False
                    if quizz[car["start_y"]][car["start_x"]+1+i] != 0:
                        return False
                return True
                
            if dir == 'dr':
                for i in range(car["length"]):
                    if (car['start_x']+1+length+i >= width):
                        return False
                    if quizz[car['start_y']+1+length][car['start_x']+1+length+i] != 0:
                        return False
                return True 
            
            if dir == 'dl':
                for i in range(car["length"]):
                    if quizz[car['start_y']+1+length][car['start_x']+1-i] != 0:
                        return False
                return True

    def convert_to_key(self, state):
        key = ''.join([str(i) for list in state for i in list])
        key = key.replace('-1','')
        return key
    def create_neighbors(self, parent, cars):  
        neighbors = []
        print("parent: ",self.convert_to_key(parent))
        for index in range(len(cars)):
            if cars[index]["lines"] == 'h':
                if self.can_move(parent, cars[index], 'l'):
                    cost = 1
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    self.update_car(new_car[index])
                    new_car[index]
                    new_car[index]["start_x"] -= 1
                    new_car[index]["end_x"] -=1
                    new_state[new_car[index]["start_y"]+1][new_car[index]["start_x"]] = new_car[index]["cate"]
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'l', cost))
                if self.can_move(parent, cars[index], 'r'):
                    cost = 1
                    length = cars[index]['length']
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_car[index]["start_x"] += 1 
                    self.update_car(new_car[index])
                    new_state[new_car[index]["start_y"]+1][new_car[index]["start_x"] + 2] = new_car[index]["cate"] 
                    new_state[new_car[index]["start_y"]+1][new_car[index]["start_x"]] = 0
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'r', cost))
                if self.can_move(parent, cars[index], 'ru'):
                    cost = 2
                    print("-------ru--------")
                    length = cars[index]['length']
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_car[index]["start_x"] += length
                    new_car[index]["start_y"] -= (length - 1)
                    new_car[index]['lines'] = 'v'
                    self.update_car(new_car[index])
                    print(new_car[index]['end_x'], new_car[index]["end_y"])
                    #Luc xe nam ngang
                    for i in range(length):
                        if (cars[index]["start_x"]+1+i < self.settings.map_width and cars[index]["start_y"]+1 < self.settings.map_height):
                            new_state[cars[index]["start_y"]+1][cars[index]["start_x"]+1+i] = 0
                    #Luc xe nam doc sau khi turn
                    for i in range(length):
                        if (new_car[index]["start_y"]+1+i < self.settings.map_height and new_car[index]["start_x"]+1 < self.settings.map_width):

                            new_state[new_car[index]["start_y"]+1+i][new_car[index]["start_x"]+1] = cars[index]['cate']
                    
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'ru', cost))
                if self.can_move(parent, cars[index], 'lu'):
                    cost = 2

                    length = cars[index]['length']
                    print("-------lu--------")
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_car[index]["start_x"] -= 1
                    new_car[index]["start_y"] -= length-1
                    new_car[index]['lines'] = 'v'
                    self.update_car(new_car[index])
                    #Luc xe nam ngang
                    for i in range(length):
                        if (cars[index]["start_x"]+1+i < self.settings.map_width and cars[index]["start_y"]+1 < self.settings.map_height):
                            new_state[cars[index]["start_y"]+1][cars[index]["start_x"]+1+i] = 0
                    #Luc xe nam doc sau khi turn
                    for i in range(length):
                        if (new_car[index]["start_y"]+1+i < self.settings.map_height and new_car[index]["start_x"]+1 < self.settings.map_width):

                            new_state[new_car[index]["start_y"]+1+i][new_car[index]["start_x"]+1] = cars[index]['cate']
                    
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'lu', cost))
                if self.can_move(parent, cars[index], 'rd'):
                    cost = 2
                    length = cars[index]['length']
                    print("-------rd--------")
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_car[index]["start_x"] += length
                    new_car[index]["start_y"] = cars[index]["start_y"]
                    new_car[index]['lines'] = 'v'
                    self.update_car(new_car[index])
                    #Luc xe nam ngang
                    for i in range(length):
                        if (cars[index]["start_x"]+1+i < self.settings.map_width and cars[index]["start_y"]+1 < self.settings.map_height):
                            new_state[cars[index]["start_y"]+1][cars[index]["start_x"]+1+i] = 0
                    #Luc xe nam doc sau khi turn
                    for i in range(length):
                        if (new_car[index]["start_y"]+1+i < self.settings.map_height and new_car[index]["start_x"]+1 < self.settings.map_width):
                            new_state[new_car[index]["start_y"]+1+i][new_car[index]["start_x"]+1] = cars[index]['cate']
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'rd', cost))
                if self.can_move(parent, cars[index], 'ld'):
                    cost = 2
                    length = cars[index]['length']
                    print("-------ld--------")
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_car[index]["start_x"] -= 1
                    new_car[index]['lines'] = 'v'
                    self.update_car(new_car[index])
                    #Luc xe nam ngang
                    for i in range(length):
                        if (cars[index]["start_x"]+1+i < self.settings.map_width and cars[index]["start_y"]+1 < self.settings.map_height):

                            new_state[cars[index]["start_y"]+1][cars[index]["start_x"]+1+i] = 0
                    #Luc xe nam doc sau khi turn
                    for i in range(length):
                        if (new_car[index]["start_y"]+1+i < self.settings.map_height and new_car[index]["start_x"]+1 < self.settings.map_width):

                            new_state[new_car[index]["start_y"]+1+i][new_car[index]["start_x"]+1] = cars[index]['cate']
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'ld', cost))
            if cars[index]["lines"] == 'v':
                if self.can_move(parent, cars[index], 'u'):
                    cost = 1
                    length = cars[index]['length']
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_state[new_car[index]["start_y"]][new_car[index]["start_x"]+1] = new_car[index]["cate"]
                    new_car[index]["start_y"] -= 1
                    new_car[index]["end_y"] -=1
                    new_state[new_car[index]["start_y"]+1][new_car[index]["start_x"]+1] = 0
                    for i in range(length):
                        if (cars[index]["start_x"]+1< self.settings.map_width and cars[index]["start_y"]+1 + i < self.settings.map_height):

                            new_state[cars[index]["start_y"]+1+i][cars[index]["start_x"]+1] = new_car[index]["cate"]
                    
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'u', cost))
                if self.can_move(parent, cars[index], 'd'):
                    cost = 1
                    length = cars[index]['length']
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_car[index]["start_y"] += 1 
                    self.update_car(new_car[index])
                    new_state[new_car[index]["start_y"]+2][new_car[index]["start_x"] + 1] = new_car[index]["cate"] 
                    new_state[new_car[index]["start_y"]][new_car[index]["start_x"] + 1] = 0
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'd', cost))
                
                if self.can_move(parent, cars[index], 'ur'):
                    cost = 2
                    print("------ur-------")
                    length = cars[index]['length']
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_car[index]["start_y"] -= 1
                    new_car[index]['lines'] = 'h'
                    self.update_car(new_car[index])
                    print(new_car[index]['end_x'], new_car[index]["end_y"])
                    #Luc xe nam doc
                    for i in range(length):
                        if (cars[index]["start_x"]+1 < self.settings.map_width and cars[index]["start_y"]+1+i < self.settings.map_height):
                            new_state[cars[index]["start_y"]+1+i][cars[index]["start_x"]+1] = 0
                    #Luc xe nam doc sau khi turn
                    for i in range(length):
                        if (new_car[index]["start_y"]+1 < self.settings.map_height and new_car[index]["start_x"]+1+i < self.settings.map_width):

                            new_state[new_car[index]["start_y"]+1][new_car[index]["start_x"]+1+i] = cars[index]['cate']
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'ur', cost))
                if self.can_move(parent, cars[index], 'ul'):
                    cost = 2
                    print("------ul-------")
                    length = cars[index]['length']
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_car[index]['start_x'] -= length-1
                    new_car[index]["start_y"] -= 1
                    new_car[index]['lines'] = 'h'
                    self.update_car(new_car[index])
                    print(new_car[index]['end_x'], new_car[index]["end_y"])
                    #Luc xe nam doc
                    for i in range(length):
                        if (cars[index]["start_x"]+1 < self.settings.map_width and cars[index]["start_y"]+1+i < self.settings.map_height):
                            new_state[cars[index]["start_y"]+1+i][cars[index]["start_x"]+1] = 0
                    #Luc xe nam doc sau khi turn
                    for i in range(length):
                        if (new_car[index]["start_y"]+1 < self.settings.map_height and new_car[index]["start_x"]+1+i < self.settings.map_width):

                            new_state[new_car[index]["start_y"]+1][new_car[index]["start_x"]+1+i] = cars[index]['cate']
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'ul', cost))
                if self.can_move(parent, cars[index], 'dr'):
                    cost = 2
                    print("------dr-------")
                    length = cars[index]['length']
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    
                    new_car[index]["start_y"] += length
                    new_car[index]['lines'] = 'h'
                    self.update_car(new_car[index])
                    print(new_car[index]['end_x'], new_car[index]["end_y"])
                    #Luc xe nam doc

                    for i in range(length):
                        if (cars[index]["start_x"]+1 < self.settings.map_width and cars[index]["start_y"]+1+i < self.settings.map_height):
                        
                            new_state[cars[index]["start_y"]+1+i][cars[index]["start_x"]+1] = 0
                    #Luc xe nam doc sau khi turn
                    for i in range(length):
                        if (new_car[index]["start_y"]+1 < self.settings.map_height and new_car[index]["start_x"]+1+i < self.settings.map_width):
                            new_state[new_car[index]["start_y"]+1][new_car[index]["start_x"]+1+i] = cars[index]['cate']
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'dr', cost))
                if self.can_move(parent, cars[index], 'dl'):
                    cost = 2
                    print("------dl-------")
                    length = cars[index]['length']
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_car[index]['start_x'] -= length-1
                    new_car[index]["start_y"] += length-1
                    new_car[index]['lines'] = 'h'
                    self.update_car(new_car[index])
                    print(new_car[index]['end_x'], new_car[index]["end_y"])
                    #Luc xe nam doc
                    for i in range(length):
                        if (cars[index]["start_x"]+1 < self.settings.map_width and cars[index]["start_y"]+1+i < self.settings.map_height):

                            new_state[cars[index]["start_y"]+1+i][cars[index]["start_x"]+1] = 0
                    #Luc xe nam doc sau khi turn
                    for i in range(length):
                        if (new_car[index]["start_y"]+1 < self.settings.map_height and new_car[index]["start_x"]+1+i < self.settings.map_width):
                            new_state[new_car[index]["start_y"]+1][new_car[index]["start_x"]+1+i] = cars[index]['cate']
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'dl', cost))
        return neighbors

    def update_car(self, car):
        if car['lines'] == 'v':
            car['end_x'] = car['start_x'] + car['length']-1
            car['end_y'] = car['start_y']
        else:
            car['end_x'] = car['start_x']
            car['end_y'] = car['start_y'] + car['length']-1
            
    

    def heuristic(self, current_state):
        x_car_position = None
        for row_idx, row in enumerate(current_state):
            for col_idx, value in enumerate(row):
                if value == self.index_car:
                    x_car_position = (row_idx, col_idx)
                    break
            if x_car_position:
                break

        if x_car_position is None:
            return 0
        goal_position = (self.goal[0] - 1, self.goal[1] - 1)
        distance = abs(x_car_position[0] - goal_position[0]) + abs(x_car_position[1] - goal_position[1])

        return distance
    def heuristic_obstacle(self, node):
        total_obstacle_distance = 0
        if hasattr(self, 'game') and hasattr(self.game, 'obstacles') and self.game.obstacles:
            for obstacle in self.game.obstacles:
                for car in node.all_cars:
                    if car['cate'] != 'x' and obstacle["type"] == 'x':
                        distance = abs(car["start_x"] - obstacle["x"]) + abs(car["start_y"] - obstacle["y"])
                        total_obstacle_distance += distance
        return total_obstacle_distance
    def solve(self, index):
        self.init_cars()
        visited = set()
        start_node = Node(self.quizz, None, self.cars, None, None, 0)
        self.index_car = index
        priority_queue = queue.PriorityQueue()
        priority_queue.put(QueueElement(start_node, 0, self.heuristic(start_node.state), 0))

        while not priority_queue.empty():
            current_element = priority_queue.get()
            current_node = current_element.value

            key = self.convert_to_key(current_node.state)
            if key in visited:
                continue
            visited.add(key)
            self.visited_states_count += 1

            # Check if the current node is a goal state
            for car in current_node.all_cars:
                if car['cate'] == self.index_car and car["start_y"] + 1 == self.goal[0] and car["start_x"] + 1 == self.goal[1] and car['lines'] == 'h':
                    # Reconstruct the path
                    path = [current_node]
                    while current_node.parent is not None:
                        path.insert(0, current_node.parent)
                        current_node = current_node.parent
                    return path

            for neighbor_state in self.create_neighbors(current_node.state, current_node.all_cars):
                neighbor_node = Node(neighbor_state[0], current_node, neighbor_state[1], neighbor_state[2], neighbor_state[3], current_node.cost + 1)
                key = self.convert_to_key(neighbor_node.state)
                if key not in visited:
                    heuristic_value = self.heuristic(neighbor_node.state) + self.heuristic_obstacle(neighbor_node)
                    priority_queue.put(QueueElement(neighbor_node, current_element.priority1 + 1, heuristic_value, 0))

        return None

    def test(self):
        self.init_cars()
        list = self.solve()
        for i in list:
            for a in range(self.settings.map_height):
                for b in range(self.settings.map_width):
                    print(i.state[a][b], end= ' ')
                print()
            print(i.all_cars, end= ' ')
            # print(i.parent.parent.parent.all_cars, end= ' ')
            # print(i.parent.parent.all_cars, end= ' ')
            # print(i.parent.all_cars, end= ' ')
                # print()
    