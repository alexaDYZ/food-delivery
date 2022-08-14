


class Event():
    category = {
        1: 'New Order',
        2: 'Order Delivered',
    }
    def __init__(self, time, cat:int) -> None:
        self.time = time
        self.cat = cat
    
    def getCategory(self) : #returns a string
        return Event.category[self.cat]
    
    def print(self):
        print("time", self.time, ":", self.getCategory())
    
    def __lt__(self, other):
        return self.time < other.time