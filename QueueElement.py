import queue

class QueueElement:
    def __init__(self, value, priority1, priority2):
        self.value = value
        self.priority1 = priority1
        self.priority2 = priority2

    def __lt__(self, other):
        if self.priority1 != other.priority1:
            return self.priority1 < other.priority1
        return self.priority2 < other.priority2