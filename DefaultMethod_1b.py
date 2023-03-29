
from operator import index
from AssignmentMethod import AssignmentMethod
from Rider import Rider
from Restaurant import Restaurant
from Order import Order
from Customer import Customer
from config import args
from Event import Event
import math
import random

class DefaultMethod_1b(AssignmentMethod):
    '''
    If no idel rider at the moment, order is put in a queue. 
    Whoever finishes his/her order first will pick up the order
    '''
    def __init__(self) -> None:
        super().__init__()
        self.candidates = None
        self.bestRider = None
        self.earliestRestaurantArrival = None

    
    def addOrder(self, newOrder):
        return super().addOrder(newOrder)
    def addCurrTime(self, currTime):
        return super().addCurrTime(currTime)
    def addRiderList(self, rider_list):
        return super().addRiderList(rider_list)
   
    def find_candidates(self):# idle and walking
        # Eligible: status is free, aka idle or walking; within a threshold of distance
        rest_loc = self.order.rest.loc
        eligible_candidates = []
        for r in self.rider_list:
            if r.status != 1: # idle and walking
                eligible_candidates.append(r)
        self.candidates = eligible_candidates
   
    def find_best_rider(self):
        # print("=================  Default Method  ================= ") if args["printAssignmentProcess"] else None
        self.find_candidates()
        bestRider = None
        earliestStartingTime = -100000
        R2R = -100000
        
        '''
        Find 
        1) best rider 
        2) earliest time for him/her to start working on this order
        3)R2R
        '''
        # if there are free rider(s), pick the one with shortest R2R
        if self.candidates: # idle and walking riders
            
            def getR2R(rider:Rider, order:Order):
                R2R = -1
                # calculate the R2R time for each rider for the order
                if rider.status == 2: # Case: rider is walking
                    curr_loc = rider.getLocation(self.currTime)
                    R2R = math.dist(curr_loc, order.rest.loc) / args["riderSpeed"]
                else: R2R = math.dist(rider.lastStop if rider.lastStop else rider.loc, order.rest.loc)/ args["riderSpeed"]
                return round(R2R,3)

            R2RForAllEligible_dict = {} # key: R2R of rider r; value: rider index

            for r in self.candidates:
                R2R = getR2R(r, self.order)
                if R2R in R2RForAllEligible_dict.keys():
                    R2RForAllEligible_dict[R2R].append(r.index)
                else:
                    R2RForAllEligible_dict[R2R] = [r.index]

            R2R = min(R2RForAllEligible_dict.keys())
            
            
            bestRiders = R2RForAllEligible_dict[R2R]
            self.rider_list.sort()
            bestRider = self.rider_list[random.choice(bestRiders)]
            
            earliestStartingTime = self.currTime

        
        # if everyone is busy, pick the one who can finish his/her order the ealiest
        else: # busy riders
            nextAvailTimeForAll_dict = {} # key: nextAvailTime; value: rider index
            for r in self.rider_list:
                if r.nextAvailableTime_actual in nextAvailTimeForAll_dict.keys():
                    nextAvailTimeForAll_dict[r.nextAvailableTime_actual].append(r.index)
                else:
                    nextAvailTimeForAll_dict[r.nextAvailableTime_actual] = [r.index]
            
            earliestStartingTime = min(nextAvailTimeForAll_dict.keys()) 
            
            bestRiders = nextAvailTimeForAll_dict[earliestStartingTime]
            self.rider_list.sort()
            bestRider = self.rider_list[random.choice(bestRiders)]
            # find time arrival at the restaurant
            R2R = math.dist(bestRider.lastStop, self.order.rest.loc) / args["riderSpeed"]
            


        self.earliestRestaurantArrival = earliestStartingTime + R2R
        # update relevant information 
        # update order status
        self.order.foundRider(bestRider)
        self.order.addRiderReachReatsurantTime(self.earliestRestaurantArrival)
        self.order.addDeliveredTime() # order.t_delivered

        # update rider status
        bestRider.deliver(self.order, earliestStartingTime)

        self.bestRider = bestRider
        return bestRider



    # def find_ealiest_arrival(self):
    #     return self.earliestRestaurantArrival

    def find_order_delivered_time(self):
        return self.bestRider.nextAvailableTime
        


