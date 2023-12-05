import queue
class QueueElement:
    def __init__(self, value, priority1, priority2, priority3):
        self.value = value
        self.priority1 = priority1
        self.priority2 = priority2
        self.priority3 = priority3

    def __lt__(self, other):
        # So sánh theo tiêu chí 1
        if self.priority1 != other.priority1:
            return self.priority1 < other.priority1
        elif self.priority2 != other.priority2:
            return self.priority2 < other.priority2
        return self.priority3 < other.priority3
#Cách dùng  
#priority_queue = queue.PriorityQueue()

# Thêm các phần tử vào hàng đợi
#priority_queue.put(QueueElement("A", 3, 7))
#priority_queue.put(QueueElement("B", 1, 5))
#priority_queue.put(QueueElement("C", 2, 6))

# Lấy các phần tử từ hàng đợi theo thứ tự ưu tiên
#while not priority_queue.empty():
    #element = priority_queue.get()
    #print(element.value)