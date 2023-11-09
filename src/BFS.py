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
            new_car = copy.deepcopy(cars)
            if cars[index]["lines"] == 'h':
                if self.can_move(parent, new_car[index], 'l'):
                    new_state = copy.deepcopy(parent)
                    new_state[new_car[index]["start_y"]+1][new_car[index]["start_x"]] = new_car[index]["cate"]
                    new_state[new_car[index]["end_y"]+1][new_car[index]["end_x"]+1] = 0
                    new_car[index]
                    new_car[index]["start_x"] -= 1
                    new_car[index]["end_x"] -=1
                    neighbors.append((new_state, new_car))
                elif self.can_move(parent, new_car[index], 'r'):
                    new_state = copy.deepcopy(parent)
                    new_state[new_car[index]["end_y"]+1][new_car[index]["end_x"]+2] = new_car[index]["cate"]
                    new_state[new_car[index]["start_y"]+1][new_car[index]["start_x"]+1] = 0
                    new_car[index]["start_x"] += 1
                    new_car[index]["end_x"] +=1
                    neighbors.append((new_state, new_car))
            elif new_car[index]["lines"] == 'v':
                if self.can_move(parent, new_car[index], 'u'):
                    new_state = copy.deepcopy(parent)
                    new_state[new_car[index]["start_y"]][new_car[index]["start_x"]+1] = new_car[index]["cate"]
                    new_state[new_car[index]["end_y"]+1][new_car[index]["end_x"]+1] = 0
                    new_car[index]["start_y"] -= 1
                    new_car[index]["end_y"] -=1
                    neighbors.append((new_state, new_car))
                elif self.can_move(parent, new_car[index], 'd'):
                    new_state = copy.deepcopy(parent)
                    new_state[new_car[index]["end_y"]+2][new_car[index]["end_x"]+1] = new_car[index]["cate"]
                    new_state[new_car[index]["start_y"]+1][new_car[index]["start_x"]+1] = 0
                    new_car[index]["start_y"] += 1
                    new_car[index]["end_y"] +=1
                    neighbors.append((new_state, new_car))
        return neighbors
    
    def solve(self):
        self.init_cars()
        visited = set()
        print(self.goal)
        start_node = Node(self.quizz, None, self.cars, None, None)
        print(start_node.state)

        queue = deque()
        queue.append(start_node)

        for i in range(20):
            print("Gen" ,i)
            current_node = queue.popleft()
            visited.add(current_node)
            for neighbor_state in self.create_neighbors(current_node.state, current_node.all_cars):
                neighbor_node = Node(neighbor_state[0], current_node, neighbor_state[1], None, None)

                if neighbor_node not in visited:
                    print("##################")
                    for car in neighbor_node.all_cars:
                        print(car)
                        if car["cate"] == 'x':
                            if car["start_y"]+1 == self.goal[0]-1 and car["start_x"]+1 == self.goal[1]-1:
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

       