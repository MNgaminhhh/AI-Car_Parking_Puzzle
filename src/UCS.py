from src.node import Node
from collections import deque
from src.priority_queue import QueueElement
import copy
import queue

class UCS:
    def __init__(self, game):
        self.quizz = game.map
        self.goal = game.goal
        self.game = game
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
            self.cars.append({"cate": cate, "lines": lines, "start_x": start_x, "start_y": start_y, "end_x": end_x, "end_y": end_y})

    def can_move(self, quizz, car, dir):
        if dir == 'l':
            if (quizz[car["start_y"] + 1][car["start_x"]] == 0 and car["start_x"] > 0):
                return True
        if dir == 'r':
            if (car["end_x"] + 1 < self.game.settings.map_width - 1):
                if (quizz[car["end_y"] + 1][car["end_x"] + 2] == 0):
                    return True
        if dir == 'u':
            if (quizz[car["start_y"]][car["start_x"] + 1] == 0):
                return True
        if dir == 'd':
            if (quizz[car["end_y"] + 2][car["end_x"] + 1] == 0):
                return True
        return False

    def convert_to_key(self, state):
        key = ''.join([str(i) for list in state for i in list])
        key = key.replace('-1', '')
        return key

    def create_neighbors(self, parent, cars, cost):
        neighbors = []
        print("parent: ", self.convert_to_key(parent))
        #cost=parent.cost
        for index in range(len(cars)):
            if cars[index]["lines"] == 'h':
                if self.can_move(parent, cars[index], 'l'):
                    new_cost = cost
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_state[new_car[index]["start_y"] + 1][new_car[index]["start_x"]] = new_car[index]["cate"]
                    new_state[new_car[index]["end_y"] + 1][new_car[index]["end_x"] + 1] = 0
                    new_car[index]["start_x"] -= 1 
                    new_car[index]["end_x"] -= 1
                    new_cost = new_cost + 1
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'l', new_cost))
                if self.can_move(parent, cars[index], 'r'):
                    new_cost = cost
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_state[new_car[index]["end_y"] + 1][new_car[index]["end_x"] + 2] = new_car[index]["cate"]
                    new_state[new_car[index]["start_y"] + 1][new_car[index]["start_x"] + 1] = 0
                    new_car[index]["start_x"] += 1
                    new_car[index]["end_x"] += 1
                    new_cost = new_cost + 1
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'r', new_cost))
            if cars[index]["lines"] == 'v':
                if self.can_move(parent, cars[index], 'u'):
                    new_cost = cost
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_state[new_car[index]["start_y"]][new_car[index]["start_x"] + 1] = new_car[index]["cate"]
                    new_state[new_car[index]["end_y"] + 1][new_car[index]["end_x"] + 1] = 0
                    new_car[index]["start_y"] -= 1
                    new_car[index]["end_y"] -= 1
                    new_cost = new_cost + 1
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'u', new_cost))
                if self.can_move(parent, cars[index], 'd'):
                    new_cost = cost
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_state[new_car[index]["end_y"] + 2][new_car[index]["end_x"] + 1] = new_car[index]["cate"]
                    new_state[new_car[index]["start_y"] + 1][new_car[index]["start_x"] + 1] = 0
                    new_car[index]["start_y"] += 1
                    new_car[index]["end_y"] += 1
                    new_cost = new_cost + 1
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'd', new_cost))
        return neighbors


    def solve(self):
        self.init_cars()
        visited = []
        start_node = Node(self.quizz, None, self.cars, None, None, 0)

        priority_queue = queue.PriorityQueue()
        priority_queue.put(QueueElement(start_node, 0, start_node.cost))

        #duyệt hàng đợi
        while not priority_queue.empty():
            current_element = priority_queue.get()
            current_node = current_element.value            
            key = self.convert_to_key(current_node.state)
            visited.append(key)
            for neighbor_state in self.create_neighbors(current_node.state, current_node.all_cars, current_node.cost):
                neighbor_node = Node(neighbor_state[0], current_node, neighbor_state[1], neighbor_state[2], neighbor_state[3], neighbor_state[4]) 
            #chuyển trạng thái thành khóa
                key = self.convert_to_key(neighbor_node.state)
                #kiểm tra đã được thăm chưa
                if key not in visited:
                    for car in neighbor_node.all_cars:
                        if car["cate"] == 'x':
                            #nếu 1 trong các xe là đích thì ktra đã đến đích chưa
                            if car["start_y"]+1 == self.goal[0] and car["start_x"]+1 == self.goal[1]: #
                                #nếu đến đích trả về danh sách đường đi
                                path = [neighbor_node]
                                while neighbor_node.parent is not None:
                                    path.insert(0, neighbor_node.parent)
                                    neighbor_node = neighbor_node.parent
                                return path
                    #không phải đích thì thêm vào hàng đợi ưu tiên    
                    priority_queue.put(QueueElement(neighbor_node, current_node.cost, neighbor_node.cost))        
        return None
       
    def test(self):
        path = self.solve()
        if path:
            for i, node in enumerate(path):
                print(f"Step {i}:")
                print(node.car_choose, node.action)
        else:
            print("No solution found.")
