from src.node import Node
from collections import deque 
import copy
class BFS:
    def __init__(self, game):
        self.quizz = game.map
        self.goal = game.goal
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
            if (quizz[car["start_y"]+1][car["start_x"]] != 0):
                return False
        if dir == 'r':
            if (quizz[car["end_y"]+1][car["end_x"]+2] != 0):
                return False
        if dir == 'u':
            if (quizz[car["start_y"]][car["start_x"]+1] != 0):
                return False
        if dir =='d':
            if (quizz[car["end_y"]+2][car["end_x"]+1] != 0):
                return False
        return True

    
    def create_neighbors(self, parent, cars):
        neighbors = []
        for index in range(len(cars)):
            if cars[index]["lines"] == 'h':
                if self.can_move(parent, cars[index], 'l'):
                    print(cars[index])
                    print("--------------")
                    new_state = copy.deepcopy(parent)
                    new_state[cars[index]["start_y"]+1][cars[index]["start_x"]] = cars[index]["cate"]
                    new_state[cars[index]["end_y"]+1][cars[index]["end_x"]+1] = 0
                    cars[index]
                    cars[index]["start_x"] -= 1
                    cars[index]["end_x"] -=1
                    neighbors.append((new_state, cars))
                elif self.can_move(parent, cars[index], 'r'):
                    print(cars[index])
                    print("--------------")
                    new_state = copy.deepcopy(parent)
                    new_state[cars[index]["end_y"]+1][cars[index]["end_x"]+2] = cars[index]["cate"]
                    new_state[cars[index]["start_y"]+1][cars[index]["start_x"]+1] = 0
                    cars[index]["start_x"] += 1
                    cars[index]["end_x"] +=1
                    neighbors.append((new_state, cars))
            elif cars[index]["lines"] == 'v':
                if self.can_move(parent, cars[index], 'u'):
                    print(cars[index])
                    print("--------------")
                    new_state = copy.deepcopy(parent)
                    new_state[cars[index]["start_y"]][cars[index]["start_x"]+1] = cars[index]["cate"]
                    new_state[cars[index]["end_y"]+1][cars[index]["end_x"]+1] = 0
                    cars[index]["start_y"] -= 1
                    cars[index]["end_y"] -=1
                    neighbors.append((new_state, cars))
                elif self.can_move(parent, cars[index], 'd'):
                    print(cars[index])
                    print("--------------")
                    new_state = copy.deepcopy(parent)
                    new_state[cars[index]["end_y"]+2][cars[index]["end_x"]+1] = cars[index]["cate"]
                    new_state[cars[index]["start_y"]+1][cars[index]["start_x"]+1] = 0
                    cars[index]["start_y"] += 1
                    cars[index]["end_y"] +=1
                    neighbors.append((new_state, cars))
        return neighbors
    
    def solve(self):
        self.init_cars()
        visited = set()
        print(self.goal)
        start_node = Node(self.quizz, None, self.cars, None, None)
        print(start_node.state)

        queue = deque()
        queue.append(start_node)
        print(len(queue))

        while queue:
            visited = set()
            current_node = queue.popleft()
            visited.add(current_node)

            for neighbor_state in self.create_neighbors(current_node.state, current_node.all_cars):
                neighbor_node = Node(neighbor_state[0], current_node, neighbor_state[1], None, None)
                print(neighbor_node.state, neighbor_node.all_cars)

                if neighbor_node not in visited:
                    for car in neighbor_node.all_cars:
                        if car["cate"] == 'x':
                            if car["start_y"]+1 == self.goal[0] and car["start_x"]+1 == self.goal[1]:
                                path = [neighbor_node]
                                while neighbor_node.parent is not None:
                                    path.insert(0, neighbor_node.parent)
                                    neighbor_node = neighbor_node.parent
                                return path
                            queue.append(neighbor_node)
        return None
    def test(self):
        path = self.solve()
        if path:
            for i, node in enumerate(path):
                print(f"Step {i}:")
                for row in node.state:
                    print(row)
                print()
        else:
            print("No solution found.")