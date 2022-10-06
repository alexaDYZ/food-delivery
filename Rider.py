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

    def deliver(self, order:Order, riderFreeTime:float):

        self.totalCurrOrder += 1
        self.status = 1
        self.orderDict[order.index] = order
        self.activeOrderDict[order.index] = order

        # calculate delivery time
        rest_loc = order.rest.loc
        cust_loc = order.cust.loc
        FPT = order.rest.prepTime

        R2R = math.dist(rest_loc, self.lastStop if self.lastStop else self.loc)/args["riderSpeed"]
        DT = math.dist(rest_loc, cust_loc)/args["riderSpeed"]
        WT = max(FPT, R2R) + DT

        # order 
        order.rider = self
        order.t_riderReachedRestaurant = max(riderFreeTime, order.t) + R2R
        order.t_delivered = max(riderFreeTime, order.t) + WT
        print("Order ", order.index, ": rider_start_t, order.t, R2R, DT, WT, reach_rest, delivered :\n",
                     [riderFreeTime, order.t, R2R, DT, WT, order.t_riderReachedRestaurant, order.t_delivered])
        order.wt = order.t_delivered - order.t # the actual waiting time: WT + lagtime, where WT = max(FPT, R2R) + DT 
        # order.wt = WT + max((riderFreeTime - order.t),0) # when the assigned rider is busy, the waiting time also includes 
        

        # rider
        self.nextAvailableTime = riderFreeTime + WT # the same as the order delivered time. 
        self.lastStop = order.cust.loc
        self.orderCompleteTimeList.append(self.nextAvailableTime)
        

        
        

        
        
        
        
        

       
        
        # calculate waiting time for rider
        riderWT = R2R - FPT if FPT<R2R else 0
        # print("------ Order #" , order.index, " waiting time is" ,waiting_time, "\n Finish Time: ", self.nextFreeTime)
        self.totalWaitingTime+= riderWT

            

    # def predictStatus(self, currTime, predTime): # output is string
    #     #Predict rider status after 'predTime' minute
    #     predStatus = -1 # initialize
    #     if self.status == 1: # if busy
    #         predStatus = 0 if self.nextAvailableTime < currTime+predTime else 1
    #     elif self.status == 0:
    #         predStatus = self.status
    #     else:
    #         print("Error: Rider status error.")
    #     return Rider.status[predStatus]

    def getFoodReadyTime(self, orderIndex): # given an order, returns when the food is ready on the timeline
        order = self.orderDict[orderIndex]
        orderInTime = order.t
        foodPrepTime = order.rest.prepTime
        return foodPrepTime + orderInTime

    
    # def getOrderDeliveredTime(self):# given an order, returns when the rider will complete the delivery for the order
    #     return self.nextAvailableTime



            



    

    
