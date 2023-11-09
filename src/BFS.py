from src.node import Node
from collections import deque 
import copy
class BFS:
    def __init__(self, game):
        self.quizz = game.map
        self.goal = game.goal
        self.cars = game.cars
    
    def test(self):
        for car in self.cars:
            print(car.start_x, car.start_y)

    def can_move(self, quizz, car, dir):
        if dir == 'l':
            if (quizz[car.start_y+1][car.start_x] != 0):
                return False
        if dir == 'r':
            if (quizz[car.end_y+1][car.end_x+2] != 0):
                return False
        if dir == 'u':
            if (quizz[car.start_y][car.start_x+1] != 0):
                return False
        if dir =='d':
            if (quizz[car.end_y+2][car.end_x+1] != 0):
                return False
        return True

    
    def create_neighbors(self, parent):
        neighbors = []
        for car in self.cars:
            if car.lines == 'h':
                if self.can_move(parent, car, 'l'):
                    new_state = copy.deepcopy(parent)
                    new_state[car.start_y+1][car.start_x] = car.cate
                    new_state[car.end_y+1][car.end_x+1] = 0
                    neighbors.append(new_state)
                if self.can_move(parent, car, 'r'):
                    new_state = copy.deepcopy(parent)
                    new_state[car.end_y+1][car.end_x+2] = car.cate
                    new_state[car.start_y+1][car.start_x+1] = 0
                    neighbors.append(new_state)
            if car.lines == 'v':
                if self.can_move(parent, car, 'u'):
                    new_state = copy.deepcopy(parent)
                    new_state[car.start_y][car.start_x+1] = car.cate
                    new_state[car.end_y+1][car.end_x+1] = 0
                    neighbors.append(new_state)
                if self.can_move(parent, car, 'd'):
                    new_state = copy.deepcopy(parent)
                    new_state[car.end_y+2][car.end_x+1] = car.cate
                    new_state[car.start_y+1][car.start_x+1] = 0
                    neighbors.append(new_state)
        return neighbors
    
    def solve(self):
        visited = set()
        start_node = Node(self.quizz, None, None)
        goal_node = Node(self.goal, None, None)

        if start_node == goal_node:
            return [start_node]

        queue = deque()
        queue.append(start_node)

        while queue:
            current_node = queue.popleft()
            visited.add(current_node)

            for neighbor_state in self.get_neigbors(current_node.state):
                neighbor_node = Node(neighbor_state, current_node, None)

                if neighbor_node not in visited:
                    if neighbor_node == goal_node:
                        path = [neighbor_node]
                        while neighbor_node.parent is not None:
                            path.insert(0, neighbor_node.parent)
                            neighbor_node = neighbor_node.parent
                        return path
                    queue.append(neighbor_node)

        return None