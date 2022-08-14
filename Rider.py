import math
from config import args
from Order import Order

# terms:
# fmdistance: first mile distance, from rider location to the restaurant
# lmdistance: last mile distance, from the restaurant to customer

class Rider():
    status = {
        0: 'FREE',
        1: 'BUSY',
    }
    def __init__(self, index, loc, args) :
        self.args = args
        self.index = index
        self.loc = loc
        self.x = loc[0]
        self.y = loc[1] 
        self.status = 0
        self.nextFreeTime = 0 # time when he will finish the next delivery
        self.order = None # orders that this rider is currently delivering
        self.totalWaitingTime = 0
        self.totalOrderDelivered = 0
    
    def distance_to(self, another_loc): # place is a list of two elements, [x, y]
        return math.dist(self.loc, another_loc)
    
    def getStatus(self):
        return Rider.status[self.status]

    def deliver(self, order:Order, currTime:float):
        self.status = 1
        # calculate delivery time
        rest_loc = order.rest.loc
        cust_loc = order.cust.loc
        rest_prep_time = order.rest.prepTime
        fmtime = self.distance_to(rest_loc)/args["riderSpeed"]
        lmtime = math.dist(rest_loc, cust_loc)/args["riderSpeed"]
        self.nextFreeTime = currTime+ lmtime + max(rest_prep_time, fmtime) # change here
        self.order = order
        # calculate waiting time
        waiting_time = fmtime - rest_prep_time if rest_prep_time<fmtime else 0
        print("------ Order #" , order.index, " waiting time is" ,waiting_time, "\n Finish Time: ", self.nextFreeTime)
        self.totalWaitingTime+= waiting_time
        

    def updateStatus(self, currTime:float):
        if currTime > self.nextFreeTime or currTime == self.nextFreeTime:
            self.status = 0 
            if self.order:
                self.order.delivered()
                self.loc = self.order.rest.loc
                self.order = None
            self.nextFreeTime = currTime


            



    

    
