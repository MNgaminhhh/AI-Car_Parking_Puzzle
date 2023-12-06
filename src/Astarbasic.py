from src.node import Node
from src.priority_queue import QueueElement
import copy
import queue
class ASTAR:
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
            if (quizz[car["start_y"]+1][car["start_x"]] == 0 and car["start_x"] > 0):
                return True
        if dir == 'r':
            if (car["end_x"] + 1 < self.game.settings.map_width - 1):
                if (quizz[car["end_y"]+1][car["end_x"]+2] == 0 ):
                    return True
        if dir == 'u':
            if (quizz[car["start_y"]][car["start_x"]+1] == 0):
                return True
        if dir =='d':
            if (quizz[car["end_y"]+2][car["end_x"]+1] == 0):
                return True
        return False
    
    def heuristic(self, current_state):
        x_car_position = None
        for row_idx, row in enumerate(current_state):
            for col_idx, value in enumerate(row):
                if value == 'x':
                    x_car_position = (row_idx, col_idx)
                    break
            if x_car_position:
                break

        if x_car_position is None:
            return 0
        goal_position = (self.goal[0] - 1, self.goal[1] - 1)
        distance = abs(x_car_position[0] - goal_position[0]) + abs(x_car_position[1] - goal_position[1])

        return distance

    def convert_to_key(self, state):
        key = ''.join([str(i) for row in state for i in row])
        key = key.replace('-1', '')
        return key
    
    def create_neighbors(self, parent, cars):
        neighbors = []
        print("parent: ", self.convert_to_key(parent))
        for index in range(len(cars)):
            if cars[index]["lines"] == 'h':
                if self.can_move(parent, cars[index], 'l'):
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_state[new_car[index]["start_y"]+1][new_car[index]["start_x"]] = new_car[index]["cate"]
                    new_state[new_car[index]["end_y"]+1][new_car[index]["end_x"]+1] = 0
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
    
    def solve(self):
        self.init_cars()
        visited = set()
        start_node = Node(self.quizz, None, self.cars, None, None, None)

        priority_queue = queue.PriorityQueue()
        priority_queue.put(QueueElement(start_node, 0, self.heuristic(start_node.state)))

        while not priority_queue.empty():
            current_element = priority_queue.get()
            current_node = current_element.value

            key = self.convert_to_key(current_node.state)
            if key in visited:
                continue

            visited.add(key)
            self.visited_states_count += 1
            for neighbor_state in self.create_neighbors(current_node.state, current_node.all_cars):
                neighbor_node = Node(neighbor_state[0], current_node, neighbor_state[1], neighbor_state[2], neighbor_state[3], None)

                key = self.convert_to_key(neighbor_node.state)
                if key not in visited:
                    if self.is_goal_state(neighbor_node):
                        # Found the goal state
                        path = [neighbor_node]
                        while neighbor_node.parent is not None:
                            path.insert(0, neighbor_node.parent)
                            neighbor_node = neighbor_node.parent
                        return path
                    priority_queue.put(QueueElement(neighbor_node, current_element.priority1 + 1, current_element.priority2))

        return None

    def is_goal_state(self, node):
        for car in node.all_cars:
            if car['cate'] == 'x' and car["start_y"] + 1 == self.goal[0] and car["start_x"] + 1 == self.goal[1] :
                return True
        return False
