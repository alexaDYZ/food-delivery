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
        2: 'WALKING',
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
        self.walking_path = None # t_start, t_end, loc_start, loc_dest

    
    def __lt__(self, other):
        return self.index < other.index


    def distance_to(self, another_loc): # place is a list of two elements, [x, y]
        # not in walking mode
        return math.dist(self.loc, another_loc)
    
    def getStatus(self):
        return Rider.status[self.status]

    def deliver(self, order:Order, time_start_deliver:float):
        if self.status == 2: # if rider is walking, stop walking and start deliver
            print("Rider "+ str(self.index)+" status change: walking -> deliver")
            self.status = 1
            self.loc = self.getLocation(time_start_deliver) # halfway of walking
            self.nextAvailableTime = time_start_deliver # now
            self.walking_path = None # clear the walking path
            order.assigned_to_walking_rider = True

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

    # walking mode only
    def find_walking_dest(self, rest_list, walking_rule):
        """
        input: a list of restaurant objects
        output: location of the destination
        """
        if walking_rule == 1: # nearest restaurant
            nearest_rest_index = -1
            nearest_rest_dist = float('inf')
            for rest in rest_list:
                d = self.distance_to(rest.loc)
                if d < nearest_rest_dist:
                    nearest_rest_dist = d
                    nearest_rest_index = rest.index
            return rest_list[nearest_rest_index].loc
                
        elif walking_rule == 2: # probablistic
            pass
    
    # walking mode only
    def moveTo(self, currTime, loc_dest):
        loc_start = self.loc
        t_start = currTime
        t_end = t_start + self.distance_to(loc_dest)/args["riderSpeed"]
        self.walking_path = t_start, t_end, loc_start, loc_dest
        return self.walking_path


    def getLocation(self, currTime):
        if self.status == 2: # rider is walking
            t_start, t_end, loc_start, loc_dest = self.walking_path
            if t_start <= currTime <= t_end:
                return loc_start + (loc_dest - loc_start) * (currTime - t_start)/(t_end - t_start)
            elif currTime > t_end:
                print("Error: Rider should have finished walking, but status is not updated")
            else:
                print("Error: see getLocation() in Rider.py")
        else:
            print("Error: Rider is not in walking mode")
            pass



            



    

    
