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

class ClosestToFPTMethod(AssignmentMethod):
    def __init__(self):
        super().__init__()
        self.R2RforAll = None # a list of R2R time for the current order for all riders. will update every time a new order comes in
        self.bestRider = None # for the current order
        self.order = None
        self.currTime = None
        self.rider_list = None
        self.FPT = None
        self.FRT = None
        self.timeArrivalDict_rider_time = {} # for analysis

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
            # # debug:
            # self.timeArrivalDict_rider_time[r.index] = arrival_time
            # # debug ends
            if arrival_time in RiderArriveTime:
                RiderArriveTime[arrival_time].append(r)
            else:
                RiderArriveTime[arrival_time] = [r]

        
        
        return RiderArriveTime



    # driver function, called in Event.py
    def find_best_rider(self):

        # print("🔮🔮🔮🔮🔮🔮🔮🔮🔮 Anticipative Method 🔮🔮🔮🔮🔮🔮🔮🔮🔮" )if args["printAssignmentProcess"] else None
        # print("calling ==== find_best_rider") if args["printAssignmentProcess"] else None

        RiderArriveTime = self.findR2RforAll() 

        closestTime = self.find_closest_time(RiderArriveTime) 
        
        
        bestRiders = RiderArriveTime[closestTime] # find those who can reach the restaurant at the same time
        bestRider = random.choice(bestRiders) # randomly choose one of them
        # # debug:
        # for k,v in RiderArriveTime.items():
        #     print("TimeArrival: " + str(k))
        #     print("Riders:")
        #     for r in v:
        #         print(r.index)
        # print("---------Order " + str(self.order.index) + " is assigned to Rider" + str(bestRider.index)+"-----------")
        
        t_start = bestRider.nextAvailableTime 
        # update order status
        self.order.foundRider(bestRider)
        self.order.addRiderReachReatsurantTime(closestTime)
        self.order.addDeliveredTime() # order.t_delivered

        # update rider status
        bestRider.deliver(self.order, t_start)
        
        self.bestRider = bestRider

        # Debug: check assignment
        checkAssignment = False
        if checkAssignment:
            self.checkAssignment(self.FRT, closestTime, bestRider.index)
        
        return bestRider
    
    def find_order_delivered_time(self):
        return self.bestRider.nextAvailableTime

    def find_closest_time(self, RiderArriveTime):
        # print("calling ==== find_ealiest_arrival") if args["printAssignmentProcess"] else None
        '''
        Find t of (rider reaches restaurant) that is nearest to the Food Ready Time(FRT) of the order.
        FRT = FPT + current time
        Note: first consider who can reach the restaurant before FRT; if no riders can do that, find the earliest arrival time
        '''
        order_index = self.order.index
        FPT = self.order.rest.order_FPT_dict[order_index]
        self.FPT = FPT
        currTime = self.currTime
        FRT = FPT + currTime
        self.FRT = FRT

        arrival_time_ls = list(RiderArriveTime.keys())
        time_diff_ls = [round(FRT - t,3) for t in arrival_time_ls] # if time_diff > 0, rider arrives before FRT
        time_diff_ls = [t for t in time_diff_ls if t >= 0] # only consider riders who arrive before FRT


        if len(time_diff_ls) == 0: # no one can arrive before FRT
            # print("No rider can arrive before FRT")
            closestRestaurantArrivalTime = round(min(arrival_time_ls),3)
        else: # when there are riders can arrive before FRT
            closestRestaurantArrivalTime = round(FRT - min(time_diff_ls),3)
        return round(closestRestaurantArrivalTime,3)


    def checkAssignment(self, FRT, closestTime, bestRiderIndex):
        '''
        Check if the assignment method picked the correct rider
        Generate a dataframe with the following columns:
            - rider index
            - rider status
            - rider R2R
            - rider time arrival at restaurant
            - FRT
            - chosen rider
        '''
        TimeArrivalDict = self.timeArrivalDict_rider_time
        riderIndexls = list(TimeArrivalDict.keys())
        riderIndexls.sort()
        df = pd.DataFrame(columns = ["rider index", "Time Arrival", "FRT", "closestArrivalFound","if chosen"])
        for r in riderIndexls:
            newrow = pd.DataFrame({"rider index": r, "Time Arrival": TimeArrivalDict[r], "FRT": FRT, "closestArrivalFound":closestTime, "if chosen": r == bestRiderIndex}, index = [0])
            df = pd.concat([newrow,df.loc[:]]).reset_index(drop=True)

        # save to csv
        if not os.path.exists("assignment_check"):
            os.makedirs("assignment_check")
        df.to_csv("assignment_check/assignment_check_order" + str(self.order.index) + ".csv", index=False)
