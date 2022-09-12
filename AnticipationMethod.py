
from ast import arg
from AssignmentMethod import AssignmentMethod
from Rider import Rider
from Restaurant import Restaurant
from Order import Order
from Customer import Customer
from config import args
import math

class AnticipationMethod(AssignmentMethod):
    def __init__(self):
        super().__init__()

    def addOrder(self, newOrder):
        return super().addOrder(newOrder)
    def addCurrTime(self, currTime):
        return super().addCurrTime(currTime)
    def addRiderList(self, rider_list):
        return super().addRiderList(rider_list)

    def find_eligible_candidates(self):
        # Eligible: x minute later, rider is free; within a threshold of distance
        rest_loc = self.order.rest.loc

        def getExpectedStatus(rider:Rider):
            return rider.predictStatus(self.currTime, args["forwardLookingTime"])
        def getExpectedDistance(rider:Rider): # riders who are free after x min
            # Case 1: rider is currently free
            if len(rider.orderDict) == 0:
                dist = rider.distance_to(rest_loc)
            # Case 2: rider is currently delivering 
            else:
                orderIndex = list(rider.orderDict.keys())
                orderIndex.sort()
                currOrderIndex = orderIndex[0]
                currOrder = rider.orderDict[currOrderIndex]
                rider_loc = currOrder.cust.loc # after finish this order, rider stays there
                dist = math.dist(rider_loc, rest_loc)
            return dist
        
        free_candidates = [r for r in self.rider_list if getExpectedStatus(r) == "FREE"]
        eligible_candidates = [r for r in free_candidates  if getExpectedDistance(r) < args["riderSelectionThreshold"] ]
        return eligible_candidates

    def find_best_rider(self,eligible_candidates):
        # greedy
        eligible_candidates.sort(key=lambda x: x.distance_to(self.order.rest.loc), reverse=False) # sort all riders by distance to resturant
        bestRider = eligible_candidates[0]
        # update rider status
        bestRider.deliver(self.order, self.currTime)
        # update order status
        self.order.rider = bestRider
        self.order.foundRider()
        # print("best rider found")
        return bestRider


    def assign(self):
        eligible_candidates = self.find_eligible_candidates()
    
        # check if there is eligible rider:
        if len(eligible_candidates) == 0:
            pass
            # print("Order #", self.order.index, ": unable to find a rider")
    
        # select the nearest rider(to restaurant)
        else:
            bestRider = self.find_best_rider(eligible_candidates)
            # print("order assigned")
            return bestRider