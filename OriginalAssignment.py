from Rider import Rider
from Restaurant import Restaurant
from Order import Order
from Customer import Customer
from config import args

def assign_order_to_rider(order: Order, rider_list, currTime:float) -> Rider: # returns the index of the best rider
    rest_loc = order.rest.loc
    eligible_candidates = [r for r in rider_list  if r.distance_to(rest_loc) < args["riderSelectionThreshold"] and r.getStatus() == "FREE"]
    
    # check if there is eligible rider:
    if len(eligible_candidates) == 0:
        print("Error: Order #", order.index, "is unable to be delivered,all available riders are too far away")
   
    # select the nearest rider(to restaurant)
    else:
        eligible_candidates.sort(key=lambda x: x.distance_to(rest_loc), reverse=False) # sort all riders by distance to resturant
        bestRider = eligible_candidates[0]
        bestRiderId = bestRider.index # nearest rider is the best rider
        # print("best rider is ", bestRiderId)
        # update rider status
        bestRider.deliver(order, currTime)
        # update order status
        order.rider = bestRider
        order.foundRider()
        return bestRider

        
        





    