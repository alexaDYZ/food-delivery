
from os import WTERMSIG
import math
from config import args



class Order():
    """
    This class is about the order generated by customers.
    """
    status = {
        1: 'ORDERED',
        2: 'ASSIGNED',
        3: 'DELIVERED',
        4: 'DROPPED',
        5: 'WAITINGforREASSIGNMENT',
    }

    def __init__(self, index, t_in, customer, restaurant):
        self.index = index
        self.t = t_in # order in time
        self.cust = customer
        self.rest= restaurant
        self.rider = None
        self.status = 1
        self.t_riderReachedRestaurant = -1
        self.t_delivered = -1
        # self.t_est_delivered = -1 # once we have a rider, we can find the estimated delivered time
        self.wt = -1
        self.reassign_time = -1 # for AssignLaterMethod. When FPT is too long and order needs to be reassigned
        self.ifReassigned = False # for AssignLaterMethod. debug
        self.assigned_to_walking_rider = False # debug
        self.FPT_predicted = None
        self.t_riderReachedRestaurant_pred = -1
        self.t_delivered_pred = -1
        self.FRT_pred = -1

    def getOrderStatus(self):
        return Order.status[self.status]

    def foundRider(self, rider):
        self.rider = rider
        self.status = 2
        # print("------ Order #" , self.index, "is assigned to Rider #", self.rider.index , "order is ", self.getOrderStatus() )
    
    def addRiderReachReatsurantTime(self, t:float):
        # time that the assigned rider reaches the restaurant
        # called in find_best_rider() in AssignMethod child classes
        self.t_riderReachedRestaurant = t
        
    def addRiderReachReatsurantTime_pred(self, t_pred):
        self.t_riderReachedRestaurant_pred = t_pred
    
    def addDeliveredTime(self):
        # called after addRiderReachReatsurantTime()
        '''Actual'''
        t_rest = self.t_riderReachedRestaurant
        rest2cust = math.dist(self.rest.loc, self.cust.loc)/args["riderSpeed"]
        FPT_real = self.rest.order_FPT_dict[self.index]
        FRT = FPT_real + self.t
        self.t_delivered = max(t_rest, FRT) + rest2cust
        self.wt = self.t_delivered - self.t
        self.rider.nextAvailableTime_actual = self.t_delivered

        '''Predicted'''
        # update the predicted rider's next_available_time
        
        self.FRT_pred  = self.FPT_predicted + self.t
        self.t_delivered_pred = max(self.t_riderReachedRestaurant_pred, self.FRT_pred ) + rest2cust
        self.rider.nextAvailableTime_predicted = self.t_delivered_pred
            
            
        

    def delivered(self, t_delivered):
        # order:
        self.status = 3
        if self.wt != self.t_delivered - self.t:
            print("Error in compute WT: self.wt = ", self.wt, " while calculated value is ", self.t_delivered - self.t)
            print("self.t_delivered = ", self.t_delivered, " and self.t = ",  self.t)
    
        # rider:
        self.rider.totalOrderDelivered += 1
        del self.rider.activeOrderDict[self.index]
        self.rider.status = 0 if len(self.rider.activeOrderDict) == 0 else 1
        self.rider.loc = self.cust.loc
        self.rider.totalCurrOrder -= 1 

        # customer
        self.cust.receivesOrder(self.t_delivered) # update user: received order
        # print("------ Order #" , self.index, "is", self.getOrderStatus(), "by Rider #", self.rider.index)
    
    def print(self):
        print("------ Order #" , self.index, "comes in at ", self.t, " and delivered at", self.t_delivered)
        # print("------ Order #" , self.index, "is ", self.getOrderStatus(), "\n Customer:", self.customer.loc, "Restaurant:", self.restaurant.loc)

    def __lt__(self, other):
        return self.t < other.t

    def reset(self):
        self.rider = None
        self.status = 1
        self.t_delivered = -1
        self.wt = -1


