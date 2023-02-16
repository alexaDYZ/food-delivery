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

class UsefulWorkMethod(AssignmentMethod):
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
        self.freqRidersArriveBeforeFRT = 0
        
        # self.numOrdersProcessed = 0

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

    def find_time_before_FRT(self, RiderArriveTime):
        '''
        Find the rider arrival time that is nearest to the Food Ready Time(FRT) of the order.
        FRT = FPT + current time
        Note: first consider who can reach the restaurant before FRT; if no riders can do that, find the earliest arrival time
        '''
        order_index = self.order.index
        FPT = self.order.rest.order_FPT_dict[order_index]
        FRT = self.order.t + FPT

        arrival_time_ls = list(RiderArriveTime.keys()) # time arrived at the restaurant
        arrival_time_ls.sort()
        time_before_FRT = [t for t in arrival_time_ls if t<=FRT]
       
        return time_before_FRT



    # driver function, called in Event.py
    def find_best_rider(self):

        # 1. find all riders who can reach before FRT

        RiderArriveTime_dict = self.findR2RforAll() # dict

        RiderArriveTime_beforeFRT = self.find_time_before_FRT( RiderArriveTime_dict ) # list

        bestRider = None
        t_reach_rest = -100000 # time of the best rider reaches the restaurant

        if len(RiderArriveTime_beforeFRT) > 0: # if there are riders who can reach before FRT

            # 1.1 get those riders
            filtered_riders = []
            for t in RiderArriveTime_beforeFRT:
                riders = RiderArriveTime_dict[t]
                filtered_riders.extend(riders)
            
            # # debug
            # d = {}
            # for r in filtered_riders:
            #     d[r.index] = r.nextAvailableTime
            # print("filtered_riders: ")
            # for k,v in d.items():
            #     print(k,v)

            # 2. among these riders, find who is the last one to be available <=> most useful work done during the FPT
            random.shuffle(filtered_riders)

            bestRider_id = -1
            for r in filtered_riders:
                max_next_available_time = 0
                if r.nextAvailableTime >= max_next_available_time:
                    max_next_available_time = r.nextAvailableTime
                    bestRider_id = r.index
            bestRider = self.rider_list[bestRider_id]
            # get time it reaches the restaurnat
            R2R = math.dist(r.lastStop if r.lastStop else r.loc, self.order.rest.loc) / args["riderSpeed"]
            t_reach_rest = r.nextAvailableTime + R2R

            # bookkeeping
            self.freqRidersArriveBeforeFRT += 1
                   
        else: # no one can reach before FRT
            # greedy: find the earliest arrival time
            # print(" NO riders can reach before FRT")
            arrival_time_ls = list(RiderArriveTime_dict.keys())
            
            t_reach_rest = min(arrival_time_ls)
            bestRiders = RiderArriveTime_dict[t_reach_rest] # list
            bestRider = random.choice(bestRiders)
        
        
        # 3. found the best rider, update status
        t_start = bestRider.nextAvailableTime
        # update order status
        self.order.foundRider(bestRider)
        self.order.addRiderReachReatsurantTime(t_reach_rest)
        self.order.addDeliveredTime() # order.t_delivered
        # update rider status
        bestRider.deliver(self.order, t_start)
        self.bestRider = bestRider

        # bookkeeping
        # self.numOrdersProcessed += 1
        total_num_orders = args["numOrders"]
        if self.order.index == total_num_orders - 1:
            p = round(self.freqRidersArriveBeforeFRT/total_num_orders, 3)*100 
            print(str(p) +"% of orders are assigned to riders who arrive before FRT - ", str(args["numRiders"]) + " riders")
            self.freqRidersArriveBeforeFRT = 0
        return bestRider
    
    def find_order_delivered_time(self):
        return self.bestRider.nextAvailableTime


