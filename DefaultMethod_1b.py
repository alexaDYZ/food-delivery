
from operator import index
from AssignmentMethod import AssignmentMethod
from Rider import Rider
from Restaurant import Restaurant
from Order import Order
from Customer import Customer
from config import args
from Event import Event
import math

class DefaultMethod_1b(AssignmentMethod):
    '''
    If no idel rider at the moment, order is put in a queue. 
    Whoever finishes his/her order first will pick up the order
    '''
    def __init__(self) -> None:
        super().__init__()
        self.idle_candidates = None
        self.bestRider = None
        self.earliestRestaurantArrival = None

    
    def addOrder(self, newOrder):
        return super().addOrder(newOrder)
    def addCurrTime(self, currTime):
        return super().addCurrTime(currTime)
    def addRiderList(self, rider_list):
        return super().addRiderList(rider_list)
   
    def find_idle_candidates(self):
        # print("finding eligibles" )if args["printAssignmentProcess"] else None
        # Eligible: status is free, aka idle; within a threshold of distance
        rest_loc = self.order.rest.loc
        # eligible_candidates = [r for r in self.rider_list  if r.distance_to(rest_loc) < args["riderSelectionThreshold"] and r.getStatus() == "FREE"]
        eligible_candidates = []
        for r in self.rider_list:
            if r.status != 1:
                eligible_candidates.append(r)
        self.idle_candidates = eligible_candidates
        # print("!!!! eligible riders are:") if args["printAssignmentProcess"] else None
        # print([r.index for r in self.idle_candidates]) if args["printAssignmentProcess"] else None
        

   
    def find_best_rider(self):
        # print("=================  Default Method  ================= ") if args["printAssignmentProcess"] else None
        self.find_idle_candidates()
        
        # if there are free rider(s), pick the one with shortest R2R
        if self.idle_candidates:
            
            # self.eligible_candidates.sort(key=lambda x: math.dist(x.lastStop if x.lastStop else x.loc, self.order.rest.loc), reverse=False) # sort all riders by distance to resturant
            def getR2R(rider:Rider, order:Order, ):
                # calculate the R2R time for each rider for the order
                R2R = math.dist(rider.lastStop if rider.lastStop else rider.loc, order.rest.loc)/ args["riderSpeed"]
                return R2R

            R2RForAllEligible_dict = {} # key: R2R of rider r; value: rider index

            for r in self.idle_candidates:
                R2RForAllEligible_dict[getR2R(r, self.order)] = r.index

            # print(R2RForAllEligible_dict) if args["printAssignmentProcess"] else None
            bestRiderR2R = min(R2RForAllEligible_dict.keys())
            self.rider_list.sort()
            bestRider = self.rider_list[R2RForAllEligible_dict[bestRiderR2R]]
            
            self.earliestRestaurantArrival = self.currTime + bestRiderR2R


            self.order.foundRider(bestRider)
            # update rider status
            bestRider.deliver(self.order, self.currTime) # update the rider's lastStop loc, nextAvaiTime

            self.bestRider = bestRider
            
            return bestRider
        
        # if everyone is busy, pick the one who can finish his/her order the ealiest
        else:
            nextAvailTimeForAll_dict = {} # key: nextAvailTime; value: rider index
            for r in self.rider_list:
                nextAvailTimeForAll_dict[r.nextAvailableTime] = r
            
            earliestStartingTime = min(nextAvailTimeForAll_dict.keys()) 
            bestRider = nextAvailTimeForAll_dict[earliestStartingTime]

            # find time arrival at the restaurant
            R2R = math.dist(bestRider.lastStop, self.order.rest.loc) / args["riderSpeed"]
            self.earliestRestaurantArrival = earliestStartingTime + R2R

            # update relevant information 
            # update order status
            self.order.foundRider(bestRider)

            self.order.t_riderReachedRestaurant = self.earliestRestaurantArrival

            # update rider status
            bestRider.deliver(self.order, earliestStartingTime)

            self.bestRider = bestRider


            return bestRider
        


    # def find_ealiest_arrival(self):
    #     return self.earliestRestaurantArrival

    def find_order_delivered_time(self):
        return self.bestRider.nextAvailableTime
        


