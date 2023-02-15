from AssignmentMethod import AssignmentMethod
from Rider import Rider
from Restaurant import Restaurant
from Order import Order
from Customer import Customer
from config import args
import math
import random
import pandas as pd
import os
from RunSimulation import runEpisode_single_medthod

class AssignLaterMethod(AssignmentMethod):
    def __init__(self):
        super().__init__()
        self.R2RforAll = None # a list of R2R time for the current order for all riders. will update every time a new order comes in
        self.bestRider = None # for the current order
        self.order = None
        self.currTime = None
        self.rider_list = None
        self.FPT = None
        self.FRT = None
        # self.timeArrivalDict_rider_time = {} # for analysis
        self.to_be_assigned = [] # list of order index, to be asssigned later, due to large FPT

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
                
                return round(riderArriveTime,3)

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
                return round(riderArriveTime,3)
        
        
        for r in self.rider_list:
            arrival_time = getTimeReachedRestaurant(r, currTime)
            if arrival_time in RiderArriveTime:
                RiderArriveTime[arrival_time].append(r)
            else:
                RiderArriveTime[arrival_time] = [r]

        return RiderArriveTime

    def find_time_before_FRT(self, RiderArriveTime):
        '''
        Find the rider arrival time that is nearest to the Food Ready Time(FRT) of the order.
        FRT = FPT + current time
        Note: first consider who can reach the restaurant before FRT; if no riders can do that, find the earliest arrival time
        '''
        order_index = self.order.index
        FPT = self.order.rest.order_FPT_dict[order_index]
        FRT = self.currTime + FPT

        arrival_time_ls = list(RiderArriveTime.keys()) # time arrived at the restaurant
        arrival_time_ls.sort()
        time_before_FRT = [t for t in arrival_time_ls if t<=FRT]
       
        return time_before_FRT



    # driver function, called in Event.py
    def find_best_rider(self):

        best_rider = None

        # Case 1. check if the order belongs to delayed assignment -> need to assign now
        if self.order.index in self.to_be_assigned:
            self.to_be_assigned.remove(self.order.index)
            best_rider = self.assignNow()
            return best_rider
            
 
        # Case 2. otherwise, it is a new order
        else:
            # 1. check if FPT > threshold
            diff = self.find_FPT_minus_threshold()
            # 2.1 if FPT <= threshold, assign now, using AnticipationMethodd <=> pick first rider who arrives at the restaurant
            if diff <= 0:
                "FPT is short, assign now."
                best_rider = self.assignNow()
            # 2.2 FPT is large, assign later
            else: 
                self.to_be_assigned.append(self.order.index)
                self.order.reassign_time = self.currTime + diff
                self.order.status  = 5 #  order is waiting for reassignment
                self.order.ifReassigned = True
                
            return best_rider

        
    
    def assignNow(self):
        " same as findBestRider() in AnticipationMethod.py"
        
        self.R2RforAll = self.findR2RforAll() # key: time arrived at the restaurant, value: list of riders who arrive at that time

        earliestRestaurantArrivalTime = self.find_ealiest_arrival() # find min in self.R2RforAll
        
        bestRiders = self.R2RforAll[earliestRestaurantArrivalTime] # find best rider using the min
        bestRider = random.choice(bestRiders) # randomly choose one from the best riders
        
        riderAvailableTime = bestRider.nextAvailableTime # time when he finish the last order, before start this order
        
        # update rider status
        self.order.foundRider(bestRider)
        bestRider.deliver(self.order, riderAvailableTime)
        
        self.bestRider = bestRider

        return bestRider


    def find_FPT_minus_threshold(self):
        # output = FPT - threshold
        # output > 0 means FPT is later than the threshold, hence assign later
        # output <= 0 means FPT is fast enough to be assigned now
        order_index = self.order.index
        FPT = self.order.rest.order_FPT_dict[order_index]
        threshold = args["threshold_assignment_time"]
        res = round(FPT - threshold, 3)
        return res

    def find_ealiest_arrival(self):
        '''same as findEarliestArrival() in AnticipationMethod.py'''
        # print("calling ==== find_ealiest_arrival") if args["printAssignmentProcess"] else None

        return min(self.R2RforAll.keys())

# # debug
# u = AssignLaterMethod()
# sim = runEpisode_single_medthod(u)

# def get_order_df_from_sim_res(sim):
#             orders = sim.order_list
#             df_2dlist = []
#             for o in orders:
#                 row = []
#                 # 1. Order Index
#                 row.append(o.index)
#                 # 2. "Order-in Time"
#                 row.append(o.t)
#                 # 3. Rider Index
#                 row.append(o.rider.index)
#                 # 4. "Rider Arrives at Restaurant"
#                 row.append(o.t_riderReachedRestaurant)
#                 # 5. "Order Delivered Time"
#                 row.append(o.t_delivered)
#                 # 6. "Waiting Time"
#                 row.append(o.wt)
                

#                 # 7. "DT"
#                 if args["FPT_avg"] > args["gridSize"]:
#                     # when FPT is extremely largs, WT = max(FPT, R2R) + DT = FPT + DT
#                     row.append(o.t_delivered - o.t  - args["FPT_avg"])
#                 elif args["FPT_avg"] == 0:
#                     # when FPT is negligible, WT = R2R + DT
#                     row.append(o.t_delivered - o.t_riderReachedRestaurant) 
#                 else:
#                     row.append(None)
#                 # 8. "Time taken before delivery"
#                 row.append(o.wt - row[6] if row[6] else None)
#                 # 9. "Theoretical Best WT"
#                 optimal_wt = 10
#                 row.append(optimal_wt)
#                 # 10. "WT regret"
#                 regret_wt = o.wt - optimal_wt
#                 row.append(regret_wt)

#                 df_2dlist.append(row)
#             df = pd.DataFrame(df_2dlist, columns=["Order Index", "Order-in Time", 
#                                                 "Rider Index", "Rider Arrives at Restaurant",
#                                                 "Order Delivered Time", "Waiting Time", 
#                                                 "DT", "Time taken before delivery", "Theoretical Best WT", "WT regret"])
#             df.to_csv("results/df_assignLater.csv")
#             return df           

# get_order_df_from_sim_res(sim)