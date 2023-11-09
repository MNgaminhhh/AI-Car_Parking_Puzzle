class Node:
    def __init__(self, state, parent, car_choose, action):
        self.state = state
        self.parent = parent
        self.car_choose = car_choose
        self.action = action

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self.state))