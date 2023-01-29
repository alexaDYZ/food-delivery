from AssignmentMethod import AssignmentMethod
from Rider import Rider
from Restaurant import Restaurant
from Order import Order
from Customer import Customer
from config import args
import math

class ClosestToFPTMethod(AssignmentMethod):
    def __init__(self):
        super().__init__()
        self.R2RforAll = None # a list of R2R time for the current order for all riders. will update every time a new order comes in
        self.bestRider = None # for the current order
        self.order = None
        self.currTime = None
        self.rider_list = None

    def addOrder(self, newOrder):
        return super().addOrder(newOrder)
    def addCurrTime(self, currTime):
        return super().addCurrTime(currTime)
    def addRiderList(self, rider_list):
        return super().addRiderList(rider_list)

    def findR2RforAll(self):
        
        '''
        This function returns a dictionary, 
        key = Time when Rider r reaches the restaurant;
        value = Rider r, object.

        R2R in this case is the time when the rider reaches the restaurant.
        '''
        RiderArriveTime = {}
       
        rest_loc = self.order.rest.loc
        currTime = self.currTime

        def getTimeReachedRestaurant(rider:Rider, currTime): 
            
            # print("** For Order " + str(self.order.index)) if args["printAssignmentProcess"] else None
            
            '''get the time when this rider reaches the restaurant'''

            # Case 1: rider is idle/free now
            if rider.status != 1:
                # ######################### debug #########################
                # print("Rider " + str(rider.index) + "is idle at t = " + str(currTime) ) if args["printAssignmentProcess"] else None
                # print("Rider " + str(rider.index) +  " will reach at " +  
                #         str(rider.distance_to(rest_loc) / args["riderSpeed"] + currTime) ) if args["printAssignmentProcess"] else None
                # ######################### debug #########################
                
                R2R = rider.distance_to(rest_loc) / args["riderSpeed"]

                riderArriveTime = currTime + R2R
                
                return riderArriveTime

            # Case 2: rider is busy now
            else:
                # Assuming there's no maximum num of orders one can take
                
                # ######################### debug #########################
                # orderIndex = list(rider.orderDict.keys()) 
                # orderIndex.sort()
                # print("Rider " + str(rider.index) +  "have the fllowing orders in process: " + 
                #          str(orderIndex))if args["printAssignmentProcess"] else None
                # ######################### debug #########################


                nextAvilableTime = rider.nextAvailableTime
                lastStop = rider.lastStop # after finish the last order in the bag, rider stays there
                
                R2R = math.dist(lastStop, rest_loc) / args["riderSpeed"]

                # print("Rider "  +  str(rider.index)  + "'s nextAvilableTime: "  + str(nextAvilableTime) + 
                #         "\n R2R = " + str(R2R) + 
                #         "\n Hence will reach the restaurant at " + str(nextAvilableTime + R2R)) if args["printAssignmentProcess"] else None
                
                riderArriveTime = nextAvilableTime + R2R
                return riderArriveTime
        
        
        for r in self.rider_list:
            RiderArriveTime[getTimeReachedRestaurant(r, currTime)] = r
        
        return RiderArriveTime


    # driver function, called in Event.py
    def find_best_rider(self):

        # print("🔮🔮🔮🔮🔮🔮🔮🔮🔮 Anticipative Method 🔮🔮🔮🔮🔮🔮🔮🔮🔮" )if args["printAssignmentProcess"] else None
        # print("calling ==== find_best_rider") if args["printAssignmentProcess"] else None

        RiderArriveTime = self.findR2RforAll() 

        closestTime = self.find_closest_time() # find min in self.R2RforAll
        
        bestRider = RiderArriveTime[earliestRestaurantArrivalTime] # find best rider using the min

        # print("---------Order " + str(self.order.index) + " is assigned to Rider" + str(bestRider.index)+"-----------") if args["printAssignmentProcess"] else None
        
        riderAvailableTime = bestRider.nextAvailableTime # time when he finish the last order, before start this order
        
        # update rider status
        self.order.foundRider(bestRider)
        bestRider.deliver(self.order, riderAvailableTime)
        
        self.bestRider = bestRider
        
        return bestRider
    
    def find_order_delivered_time(self):
        return self.bestRider.nextAvailableTime

    def find_closest_time(self, RiderArriveTime, ):
        # print("calling ==== find_ealiest_arrival") if args["printAssignmentProcess"] else None
        '''
        Find the rider arrival time that is nearest to the Food Ready Time(FRT) of the order.
        FRT = FPT + current time
        Note: only consider who can reach the restaurant before FRT
        '''
        rest_loc = self.order.rest.loc
        time = list(RiderArriveTime.keys())
        

        return earliestRestaurantArrivalTime

   