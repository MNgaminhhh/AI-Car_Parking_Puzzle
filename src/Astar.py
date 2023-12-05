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
        width = self.settings.map_width;
        height = self.settings.map_height;
        if car["lines"] == 'h':
            if dir == 'l':
                if (car["start_x"] < width and car["start_y"]+1< height):
                    if (quizz[car["start_y"]+1][car["start_x"]] == 0):
                        return True
            if dir == 'r':
                if (car["end_x"]+2 < width and car["end_y"]+1 < height):
                    if (quizz[car["end_y"]+1][car["end_x"]+2] == 0 ):
                        return True
            if dir == 'ru':
                bool = True
                for i in range(car['length']):
                    if (car["end_x"]+2 < width and car["end_y"]+1-i < height):
                        if quizz[car["end_y"]+1-i][car["end_x"]+2] != 0:
                            bool = False
                            break
                return bool
            if dir == 'lu':
                bool = True
                for i in range(car['length']):
                    if (car['start_x'] < width and car['start_y']+1-i < height):
                        if quizz[car['start_y']+1-i][car['start_x']] != 0:
                            bool = False
                            break
                return bool
            if dir == 'rd':
                bool = True
                for i in range(car['length']):
                    if (car['start_x']+car["length"] < self.settings.map_width and car['start_y']+1+i < height):
                        if quizz[car['start_y']+1+i][car['start_x']+car["length"]] != 0:
                            bool = False
                            break
                return bool
            if dir == 'ld':
                print('ld can move')
                print(car['length'])
                bool = True
                for i in range(car['length']):
                    if (car["start_x"] < width and car["start_y"]+1+i < height):
                        if quizz[car["start_y"]+1+i][car["start_x"]] != 0:
                            bool = False
                            break
                return bool
        #Vertical
        else:
            if dir == 'u':
                if(car["start_y"] < height and car["start_x"]+1 < width):
                    if (quizz[car["start_y"]][car["start_x"]+1] == 0):
                        return True
                    return False
            if dir =='d':
                if(car["end_y"]+2 < height and car["end_x"]+1 < width):
                    if (quizz[car["end_y"]+2][car["end_x"]+1] == 0):
                        return True
                    return False
            if dir == 'ul':
                print('ul')
                bool = True
                for i in range(car['length']):
                    if(car["start_y"] < height and car["start_x"]+1-i < width):
                        if quizz[car["start_y"]][car["start_x"]+1-i] != 0:
                            bool = False
                            break
                return bool    
            if dir == 'ur':
                print('ur')
                bool = True
                for i in range(car['length']):
                    if(car["start_y"] < height and car["start_x"]+1+i < width):
                        if quizz[car["start_y"]][car["start_x"]+1+i] != 0:
                            bool = False
                            break
                return bool   
                
            if dir == 'dr':
                bool = True
                for i in range(car["length"]):
                    if (car['end_y']+2 < height and car['end_x']+1+i < width):
                        if quizz[car['end_y']+2][car['end_x']+1+i] != 0:
                            bool = False
                            break
                return bool  
            if dir == 'dl':
                print('dl')
                bool = True
                for i in range(car["length"]):
                    if(car['end_y']+2 < height and car['end_x']+1-i < width):
                        if quizz[car['end_y']+2][car['end_x']+1-i] != 0:
                            return False
                            break
                return bool

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
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_state[new_car[index]["end_y"]+1][new_car[index]["end_x"]+2] = new_car[index]["cate"]
                    new_state[new_car[index]["start_y"]+1][new_car[index]["start_x"]+1] = 0
                    new_car[index]["start_x"] += 1
                    new_car[index]["end_x"] +=1
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
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_state[new_car[index]["end_y"]+2][new_car[index]["end_x"]+1] = new_car[index]["cate"]
                    new_state[new_car[index]["start_y"]+1][new_car[index]["start_x"]+1] = 0
                    new_car[index]["start_y"] += 1
                    new_car[index]["end_y"] +=1
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
    # def solve(self):
    #     self.init_cars()
    #     print(self.goal)
    #     visited = set()
    #     start_node = Node(self.quizz, None, self.cars, None, None, 0)

    #     priority_queue = queue.PriorityQueue()
    #     priority_queue.put(QueueElement(start_node, 0, self.heuristic(start_node), 0))

    #     while not priority_queue.empty():
    #         current_element = priority_queue.get()
    #         current_node = current_element.value

    #         key = self.convert_to_key(current_node.state)
    #         if key in visited:
    #             continue
            
    #         visited.add(key)
    #         self.visited_states_count += 1
    #         for neighbor_state in self.create_neighbors(current_node.state, current_node.all_cars):
    #             cost = neighbor_state[4]
    #             neighbor_node = Node(neighbor_state[0], current_node, neighbor_state[1], neighbor_state[2], neighbor_state[3],neighbor_state[4])
    #             n_distance = self.heuristic(neighbor_node) 
    #             key = self.convert_to_key(neighbor_node.state)
    #             if key not in visited:
    #                 for car in neighbor_node.all_cars:
    #                     if car['cate'] == 'x' and car["start_y"]+1 == self.goal[0] and car["start_x"]+1 == self.goal[1] and car['lines'] == 'h':
    #                         # Found the goal state
    #                         print(car["end_x"])
    #                         # for i in range(car["end_x"] + 2, self.settings.map_width):
    #                         #     if(neighbor_node.state[car["start_y"] +1][i] != 0 ):
    #                         #         return False
    #                         path = [neighbor_node]
    #                         while neighbor_node.parent is not None:
    #                             path.insert(0, neighbor_node.parent)
    #                             neighbor_node = neighbor_node.parent
    #                         return path
    #                 priority_queue.put(QueueElement(neighbor_node, cost, n_distance, 0))

    #     return None
    # def solve(self, index):
    #     self.init_cars()
    #     visited = set()
    #     start_node = Node(self.quizz, None, self.cars, None, None, 0)

    #     priority_queue = queue.PriorityQueue()
    #     priority_queue.put(QueueElement(start_node, 0, self.heuristic(start_node.state),0))

    #     while not priority_queue.empty():
    #         current_element = priority_queue.get()
    #         current_node = current_element.value

    #         key = self.convert_to_key(current_node.state)
    #         if key in visited:
    #             continue
    #         visited.add(key)
    #         self.visited_states_count += 1
    #         for neighbor_state in self.create_neighbors(current_node.state, current_node.all_cars):
    #             neighbor_node = Node(neighbor_state[0], current_node, neighbor_state[1], neighbor_state[2], neighbor_state[3], current_node.cost + 1)
    #             key = self.convert_to_key(neighbor_node.state)
    #             if key not in visited:
    #                 if self.is_goal_state(neighbor_node):
    #                     path = [neighbor_node]
    #                     while neighbor_node.parent is not None:
    #                         path.insert(0, neighbor_node.parent)
    #                         neighbor_node = neighbor_node.parent
    #                     return path
    #                 priority_queue.put(QueueElement(neighbor_node, current_element.priority1 + 1, current_element.priority2 + 1,0))

    #     return None
    # def is_goal_state(self, node):
    #     for car in node.all_cars:
    #         if car['cate'] == 'x' and car["start_y"]+1 == self.goal[0] and car["start_x"]+1 == self.goal[1] and car['lines'] == 'h':
    #             return True
    #     return False
    def solve(self, index):
        self.init_cars()
        visited = set()
        start_node = Node(self.quizz, None, self.cars, None, None, 0)
        self.index_car = index
        print(self.index_car)
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
                    priority_queue.put(QueueElement(neighbor_node, current_element.priority1 + 1, current_element.priority2 + 1, 0))

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
    