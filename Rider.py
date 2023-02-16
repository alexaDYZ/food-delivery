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
        self.init_loc = loc
        self.loc = loc
        self.status = 0
        self.nextAvailableTime = 0 # time when he will finish deliver all orders
        self.lastStop = None # last order's customer loc
        self.orderCompleteTimeList = [] # This keeps track of the completion time of all orders this rider is delivering
        self.orderDict= {} # order dictionary. key: order index, value: order object. of All orders the rider has served/is serving
        self.activeOrderDict = {} # order dictionary. key: order index, value: order object. of All orders the rider has served/is serving
        self.totalWaitingTime = 0
        self.totalOrderDelivered = 0
        self.totalCurrOrder= 0 # total number of orders assigned, and delivering
    
    def __lt__(self, other):
        return self.index < other.index


    def distance_to(self, another_loc): # place is a list of two elements, [x, y]
        return math.dist(self.loc, another_loc)
    
    def getStatus(self):
        return Rider.status[self.status]

    def deliver(self, order:Order, time_start_deliver:float):

        self.totalCurrOrder += 1
        self.status = 1
        self.orderDict[order.index] = order
        self.activeOrderDict[order.index] = order

        # rider
        self.nextAvailableTime = order.t_delivered
        self.lastStop = order.cust.loc
        self.orderCompleteTimeList.append(self.nextAvailableTime)

        # Calculate Rider Wait Time
        
        FPT = order.rest.order_FPT_dict[order.index]
        FRT = FPT + order.t  # Food Ready Time
        
        R2R = math.dist(order.rest.loc, self.lastStop if self.lastStop else self.loc)/args["riderSpeed"]
        t_reached  = time_start_deliver + R2R # Time Rider reach the restaurant 
        
        riderWT = max(0, FRT - t_reached)
        self.totalWaitingTime += riderWT



    def getFoodReadyTime(self, orderIndex): # given an order, returns when the food is ready on the timeline
        order = self.orderDict[orderIndex]
        orderInTime = order.t
        foodPrepTime = order.rest.order_FPT_dict[orderIndex]
        return foodPrepTime + orderInTime



            



    

    
