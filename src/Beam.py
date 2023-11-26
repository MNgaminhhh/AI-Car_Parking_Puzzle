from src.node import Node
import copy
import queue

class BEAM:
    def __init__(self, game, beam_width):
        self.quizz = game.map
        self.goal = game.goal
        self.game = game
        self.beam_width = beam_width

    def init_cars(self):
        self.cars = []
        for car in self.game.cars:
            cate = car.cate
            lines = car.lines
            start_x = car.start_x
            start_y = car.start_y
            end_x = car.end_x
            end_y = car.end_y
            self.cars.append({"cate": cate, "lines": lines, "start_x": start_x, "start_y": start_y, "end_x": end_x,
                              "end_y": end_y})

    def can_move(self, quizz, car, dir):
        if dir == 'l':
            if quizz[car["start_y"] + 1][car["start_x"]] == 0 and car["start_x"] > 0:
                return True
        if dir == 'r':
            if car["end_x"] + 1 < self.game.settings.map_width - 1 and quizz[car["end_y"] + 1][car["end_x"] + 2] == 0:
                return True
        if dir == 'u':
            if quizz[car["start_y"]][car["start_x"] + 1] == 0:
                return True
        if dir == 'd':
            if quizz[car["end_y"] + 2][car["end_x"] + 1] == 0:
                return True
        return False

    def convert_to_key(self, state):
        key = ''.join([str(i) for row in state for i in row])
        key = key.replace('-1', '')
        return key

    def create_neighbors(self, parent, cars):
        neighbors = []
        for index in range(len(cars)):
            if cars[index]["lines"] == 'h':
                if self.can_move(parent, cars[index], 'l'):
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_state[new_car[index]["start_y"] + 1][new_car[index]["start_x"]] = new_car[index]["cate"]
                    new_state[new_car[index]["end_y"] + 1][new_car[index]["end_x"] + 1] = 0
                    new_car[index]["start_x"] -= 1
                    new_car[index]["end_x"] -= 1
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'l'))
                if self.can_move(parent, cars[index], 'r'):
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_state[new_car[index]["end_y"] + 1][new_car[index]["end_x"] + 2] = new_car[index]["cate"]
                    new_state[new_car[index]["start_y"] + 1][new_car[index]["start_x"] + 1] = 0
                    new_car[index]["start_x"] += 1
                    new_car[index]["end_x"] += 1
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'r'))
            if cars[index]["lines"] == 'v':
                if self.can_move(parent, cars[index], 'u'):
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_state[new_car[index]["start_y"]][new_car[index]["start_x"] + 1] = new_car[index]["cate"]
                    new_state[new_car[index]["end_y"] + 1][new_car[index]["end_x"] + 1] = 0
                    new_car[index]["start_y"] -= 1
                    new_car[index]["end_y"] -= 1
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'u'))
                if self.can_move(parent, cars[index], 'd'):
                    new_state = copy.deepcopy(parent)
                    new_car = copy.deepcopy(cars)
                    new_state[new_car[index]["end_y"] + 2][new_car[index]["end_x"] + 1] = new_car[index]["cate"]
                    new_state[new_car[index]["start_y"] + 1][new_car[index]["start_x"] + 1] = 0
                    new_car[index]["start_y"] += 1
                    new_car[index]["end_y"] += 1
                    neighbors.append((new_state, new_car, new_car[index]["cate"], 'd'))
        return neighbors

    def solve(self):
        self.init_cars()
        visited = set()
        start_node = Node(self.quizz, None, self.cars, None, None, None)
        beam = [start_node]
        while beam:
            next_beam = []
            for current_node in beam:
                key = self.convert_to_key(current_node.state)
                if key in visited:
                    continue
                visited.add(key)
                for neighbor_state in self.create_neighbors(current_node.state, current_node.all_cars):
                    neighbor_node = Node(neighbor_state[0], current_node, neighbor_state[1], neighbor_state[2],
                                         neighbor_state[3], None)
                    key = self.convert_to_key(neighbor_node.state)
                    if key not in visited:
                        if self.is_goal_state(neighbor_node):
                            path = [neighbor_node]
                            while neighbor_node.parent is not None:
                                path.insert(0, neighbor_node.parent)
                                neighbor_node = neighbor_node.parent
                            return path
                        next_beam.append(neighbor_node)
            beam = next_beam[:self.beam_width]

        return None

    def is_goal_state(self, node):
        for car in node.all_cars:
            if car['cate'] == 'x' and car["start_y"] + 1 == self.goal[0] and car["start_x"] + 1 == self.goal[1]:
                return True
        return False
