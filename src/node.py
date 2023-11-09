class Node:
    def __init__(self, state, parent, all_cars, car_choose, action):
        self.state = state
        self.parent = parent
        self.all_cars = all_cars
        self.car_choose = car_choose
        self.action = action

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)