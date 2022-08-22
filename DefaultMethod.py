
from AssignmentMethod import AssignmentMethod
from Rider import Rider
from Restaurant import Restaurant
from Order import Order
from Customer import Customer
from config import args
from Event import Event

class DefaultMethod(AssignmentMethod):
    def __init__(self) -> None:
        super().__init__()
    
    def addOrder(self, newOrder):
        return super().addOrder(newOrder)
    def addCurrTime(self, currTime):
        return super().addCurrTime(currTime)
    def addRiderList(self, rider_list):
        return super().addRiderList(rider_list)
   
    def find_eligible_candidates(self):
        # Eligible: status is free, aka idle; within a threshold of distance
        rest_loc = self.order.rest.loc
        eligible_candidates = [r for r in self.rider_list  if r.distance_to(rest_loc) < args["riderSelectionThreshold"] and r.getStatus() == "FREE"]
        return eligible_candidates
   
    def find_best_rider(self, eligible_candidates):
        # greedy
        eligible_candidates.sort(key=lambda x: x.distance_to(self.order.rest.loc), reverse=False) # sort all riders by distance to resturant
        bestRider = eligible_candidates[0]
        # update rider status
        bestRider.deliver(self.order, self.currTime)
        # update order status
        self.order.rider = bestRider
        self.order.foundRider()
        return bestRider

    # main function:
    def assign(self): 
        eligible_candidates = self.find_eligible_candidates()
    
        # check if there is eligible rider:
        if len(eligible_candidates) == 0:
            pass
            # print("Order #", self.order.index, ": unable to find a rider")
    
        # select the nearest rider(to restaurant)
        else:
            bestRider = self.find_best_rider(eligible_candidates)
            return bestRider