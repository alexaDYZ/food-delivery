from Rider import Rider
from Restaurant import Restaurant
from Order import Order
from Customer import Customer
from config import args

def find_eligible_candidates(order: Order, rider_list, currTime:float):
    rest_loc = order.rest.loc
    eligible_candidates = [r for r in rider_list  if r.distance_to(rest_loc) < args["riderSelectionThreshold"] and r.getStatus() == "FREE"]
    return eligible_candidates

def greedyAllocation(order, rider_list, currTime:float, eligible_candidates) -> Rider:
    rest_loc = order.rest.loc
    eligible_candidates.sort(key=lambda x: x.distance_to(rest_loc), reverse=False) # sort all riders by distance to resturant
    bestRider = eligible_candidates[0]
    # update rider status
    bestRider.deliver(order, currTime)
    # update order status
    order.rider = bestRider
    order.foundRider()
    return bestRider
    


def assign_order_to_rider(order: Order, rider_list, currTime:float) -> Rider: # returns the index of the best rider
    
    eligible_candidates = find_eligible_candidates(order, rider_list, currTime)
    
    # check if there is eligible rider:
    if len(eligible_candidates) == 0:
            print("Order #", self.order.index, ": unable to find a rider")
   
    # select the nearest rider(to restaurant)
    else:

        bestRider = greedyAllocation(order, rider_list, currTime, eligible_candidates)
        
        return bestRider

        
        





    