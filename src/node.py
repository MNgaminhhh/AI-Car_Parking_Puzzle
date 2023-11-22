class Node:
    def __init__(self, state, parent, all_cars, car_choose, action, cost):
        self.state = state
        self.parent = parent
        self.all_cars = all_cars
        self.car_choose = car_choose
        self.action = action
        self.cost = cost


    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)

#so sánh chi phí
    def __lt__(self, other):
        if self.cost == other.cost:
            return str(self.state) < str(other.state)
        return self.cost < other.cost
