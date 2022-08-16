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
        self.nextFreeTime = 0 # time when he will finish deliver all orders
        self.orderCompleteTimeList = [] # This keeps track of the completion time of all orders this rider is delivering
        self.orderDict= {} # order dictionary. key: order index, value: order object
        self.totalWaitingTime = 0
        self.totalOrderDelivered = 0
        self.totalCurrOrder= 0 # total number of orders assigned, and delivering
    
    def distance_to(self, another_loc): # place is a list of two elements, [x, y]
        return math.dist(self.loc, another_loc)
    
    def getStatus(self):
        
        return Rider.status[self.status]

    def deliver(self, order:Order, currTime:float):
        self.totalCurrOrder += 1
        self.status = 1
        self.orderDict[order.index] = order
        # calculate delivery time
        rest_loc = order.rest.loc
        cust_loc = order.cust.loc
        rest_prep_time = order.rest.prepTime
        fmtime = self.distance_to(rest_loc)/args["riderSpeed"]
        lmtime = math.dist(rest_loc, cust_loc)/args["riderSpeed"]
        self.nextFreeTime = currTime+ lmtime + max(rest_prep_time, fmtime) 
        self.orderCompleteTimeList.append(self.nextFreeTime)
        # calculate waiting time
        waiting_time = fmtime - rest_prep_time if rest_prep_time<fmtime else 0
        # print("------ Order #" , order.index, " waiting time is" ,waiting_time, "\n Finish Time: ", self.nextFreeTime)
        self.totalWaitingTime+= waiting_time

    # def updateStatus(self, currTime:float):
    #     # finish all current orders
    #     if currTime > self.nextFreeTime or currTime == self.nextFreeTime:  
    #         self.status = 0 
    #         if self.orderList:
    #             self.orderList.delivered()
    #             self.loc = self.orderList.rest.loc
    #             self.orderList = None
    #             self.totalCurrOrder -= 1 
    #         self.nextFreeTime = currTime
    #     # # finish one of the current orders
    #     # elif currTime in self.orderCompleteTimeList:
            

    def predictStatus(self, currTime, predTime): # output is string
        #Predict rider status after 'predTime' minute
        predStatus = -1 # initialize
        if self.status == 1: # if busy
            predStatus = 0 if self.nextFreeTime < currTime+predTime else 1
        elif self.status == 0:
            predStatus = self.status
        else:
            print("Error: Rider status error.")
        return Rider.status[predStatus]

    def getFoodReadyTime(self, orderIndex): # given an order, returns when the food is ready on the timeline
        order = self.orderDict[orderIndex]
        # check if order is taken???
        orderInTime = order.t
        foodPrepTime = order.rest.prepTime
        return foodPrepTime + orderInTime

    def getRestArrivalTime(self, orderIndex): # given an order, returns when therider will arrive at the restaurant of the order
        order = self.orderDict[orderIndex]
        orderInTime = order.t
        fmtime = self.distance_to(order.rest.loc)/args["riderSpeed"]
        arrival_time = orderInTime + fmtime
        return arrival_time
    
    def getOrderCompleteTime(self, orderIndex):# given an order, returns when the rider will complete the delivery for the order
        order = self.orderDict[orderIndex]
        arrival_time = self.getRestArrivalTime(orderIndex) # specific time
        foodReadyTime = self.getFoodReadyTime(orderIndex) # specific time
        lmtime = math.dist(order.rest.loc, order.cust.loc)/args["riderSpeed"] # length of time 
        return max(arrival_time, foodReadyTime) + lmtime



            



    

    
