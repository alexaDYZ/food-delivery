import math
from config import args
from Order import Order

class Rider():
    status = {
        0: 'FREE',
        1: 'BUSY',
    }
    def __init__(self, id, loc, args) :
        self.args = args
        self.id = id
        self.loc = loc
        self.x = loc[0]
        self.y = loc[1] 
        self.status = 0
        self.nextFreeTime = 0 # time when he will finish the next delivery
        self.order = None # orders that this rider is currently delivering
    
    def distance_to(self, another_loc): # place is a list of two elements, [x, y]
        return math.dist(self.loc, another_loc)
    
    def getStatus(self):
        return Rider.status[self.status]

    def deliver(self, order:Order, currTime:float):
        self.status = 1
        # calculate delivery time
        rest_loc = order.rest.loc
        deliveryTime = self.distance_to(rest_loc)/args["riderSpeed"]
        self.nextFreeTime = currTime+ deliveryTime
        self.order = order

    def updateStatus(self, currTime:float):
        if currTime > self.nextFreeTime:
            self.status = 0 
            if self.order:
                self.order.delivered()
                self.order = None
            self.nextFreeTime = currTime


            



    

    
