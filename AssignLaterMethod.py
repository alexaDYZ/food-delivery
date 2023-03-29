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
        self.FPT_knowledge =  None
        self.threshold = None

    def addOrder(self, newOrder):
        return super().addOrder(newOrder)

    def addCurrTime(self, currTime):
        return super().addCurrTime(currTime)
    def addRiderList(self, rider_list):
        return super().addRiderList(rider_list)
    # def addThreshold(self, x):
    #     args["threshold_assignment_time"] = x*60 # x is in min
    #     self.threshold = x

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
            '''get the time when this rider reaches the restaurant'''
            R2R = math.dist(rider.lastStop if rider.lastStop else rider.loc, rest_loc) / args["riderSpeed"]
            t_start = max(currTime, rider.nextAvailableTime_actual)
            return round(t_start + R2R,3)


        for r in self.rider_list:
            arrival_time = getTimeReachedRestaurant(r, currTime)
            if arrival_time in RiderArriveTime:
                RiderArriveTime[arrival_time].append(r)
            else:
                RiderArriveTime[arrival_time] = [r]
        
        

        return RiderArriveTime

    # driver function, called in Event.py
    def find_best_rider(self):

        

        # 1. set predicted FPT given knowledge:
        if self.FPT_knowledge == 1:
            self.order.FPT_predicted = self.order.rest.order_FPT_dict[self.order.index]
        elif self.FPT_knowledge == 0.5:
            self.order.FPT_predicted = 30*60
        elif self.FPT_knowledge == 0:
            self.order.FPT_predicted = 10*60
        elif self.FPT_knowledge == 2:
            self.order.FPT_predicted = 50*60

        # Case 1. check if the order belongs to delayed assignment -> need to assign now
        if self.order.index in self.to_be_assigned:
            self.to_be_assigned.remove(self.order.index)
            best_rider = self.assignNow()
            print(" ===== Reassign:", self.order.index, "to rider", best_rider.index, "at time", self.currTime, )
            return best_rider


        # Case 2. otherwise, it is a new order
        else:
            # 1. check if FPT > threshold
            diff = self.find_pred_FPT_minus_threshold()
            # 2.1 if FPT <= threshold, assign now, using AnticipationMethodd <=> pick first rider who arrives at the restaurant
            if diff <= 0:
                "FPT is short, assign now."
                print("FPT is short, assign now.: FPT pred is ", self.order.FPT_predicted, "threshold is ", self.threshold, "actual FPT is ", self.order.rest.order_FPT_dict[self.order.index])
                best_rider = self.assignNow()
                if best_rider == None:
                    print("No rider found for order", self.order.index, "at time", self.currTime)
                print("Assign:", self.order.index, "to rider", best_rider.index, "at time", self.currTime,)
            # 2.2 FPT is large, assign later
            else: 
                self.to_be_assigned.append(self.order.index)
                self.order.reassign_time = self.currTime + diff
                self.order.status  = 5 #  order is waiting for reassignment
                self.order.ifReassigned = True
        

            



    def assignNow(self):
        " same as findBestRider() in AnticipationMethod.py"

        self.R2RforAll = self.findR2RforAll() # key: time arrived at the restaurant, value: list of riders who arrive at that time

        t_arrive_restaurant_pred = self.find_ealiest_arrival() # find min in self.R2RforAll

        bestRiders = self.R2RforAll[t_arrive_restaurant_pred] # find best rider using the min
        bestRider = random.choice(bestRiders) # randomly choose one from the best riders

        t_start_actual = bestRider.nextAvailableTime_actual # time when he finish the last order, before start this order
        t_start_actual = bestRider.nextAvailableTime_actual

        if self.FPT_knowledge == 1: t_arrive_restaurant_actual = t_arrive_restaurant_pred
        else: t_arrive_restaurant_actual = t_start_actual + (t_arrive_restaurant_pred - bestRider.nextAvailableTime_predicted)

        # update order status
        self.order.foundRider(bestRider)
        self.order.addRiderReachReatsurantTime(t_arrive_restaurant_actual)
        self.order.addRiderReachReatsurantTime_pred( t_arrive_restaurant_pred)
        self.order.addDeliveredTime() # order.t_delivered

        # update rider status
        bestRider.deliver(self.order, t_start_actual)

        self.bestRider = bestRider

        return bestRider

    def find_pred_FPT_minus_threshold(self):
        # output = FPT - threshold
        # output > 0 means FPT is later than the threshold, hence assign later
        # output <= 0 means FPT is fast enough to be assigned now
        
        FPT_pred = self.order.FPT_predicted
        self.threshold = args["threshold_assignment_time"]
        res = round(FPT_pred - self.threshold, 3)
        return res

    def find_ealiest_arrival(self):
        '''same as findEarliestArrival() in AnticipationMethod.py'''
        # print("calling ==== find_ealiest_arrival") if args["printAssignmentProcess"] else None

        return min(self.R2RforAll.keys())   
     
class AssignLaterMethod_UsefulWork(AssignLaterMethod):
    def __init__(self):
        super().__init__()
   
    def addOrder(self, newOrder):
        return super().addOrder(newOrder)
        
    def addCurrTime(self, currTime):
        return super().addCurrTime(currTime)
    def addRiderList(self, rider_list):
        return super().addRiderList(rider_list)
    def findR2RforAll(self):
        return super().findR2RforAll()
    def addThreshold(self, x):
        super().addThreshold(x)

    def find_best_rider(self):
        best_rider = None
        # Case 1. check if the order belongs to delayed assignment -> need to assign now
        if self.order.index in self.to_be_assigned:
            self.to_be_assigned.remove(self.order.index)
            best_rider = self.assignNow()
            # print(" ===== Reassigned:", self.order.index, "to rider", best_rider.index, "at time", self.currTime, )
            return best_rider


        # Case 2. otherwise, it is a new order
        else:
            # 1. check if FPT > threshold
            diff = self.find_pred_FPT_minus_threshold()
            # 2.1 if FPT <= threshold, assign now, using AnticipationMethodd <=> pick first rider who arrives at the restaurant
            if diff <= 0:
                "FPT is short, assign now."
                best_rider = self.assignNow()
                # print("Assign:", self.order.index, "to rider", best_rider.index, "at time", self.currTime,)
            # 2.2 FPT is large, assign later
            else: 
                self.to_be_assigned.append(self.order.index)
                self.order.reassign_time = self.currTime + diff
                self.order.status  = 5 #  order is waiting for reassignment
                self.order.ifReassigned = True
                # print("Assign later:", self.order.index, "at time", self.order.reassign_time,)

            return best_rider


    # overwrite the assignNow() function in AssignLaterMethod class
    def assignNow(self):
        RiderArriveTime_dict = self.findR2RforAll() # key: time arrived at the restaurant, value: list of riders who arrive at that time
        RiderArriveTime_beforeFRT = self.find_time_before_FRT( RiderArriveTime_dict ) # list
        
        bestRider = None
        restaurant_arrival_time = -10000
        if len(RiderArriveTime_beforeFRT) > 0: # if there are riders who can reach before FRT
            # print(len(RiderArriveTime_beforeFRT),"riders can reach before FRT")

            # 1.1 get those riders
            filtered_riders = []
            # debug
            
            for t in RiderArriveTime_beforeFRT:
                riders = RiderArriveTime_dict[t]
                filtered_riders.extend(riders)
        

            # 2. among these riders, find who is the last one to be available <=> most useful work done during the FPT
            random.shuffle(filtered_riders)

            bestRider_id = -1
            for r in filtered_riders:
                max_next_available_time = 0
                if r.nextAvailableTime_actual >= max_next_available_time:
                    max_next_available_time = r.nextAvailableTime
                    bestRider_id = r.index
            bestRider = self.rider_list[bestRider_id]
            t_start = max_next_available_time
            R2R = math.dist(bestRider.lastStop if bestRider.lastStop else bestRider.loc, self.order.rest.loc)
            restaurant_arrival_time = t_start + R2R

        else: # no one can reach before FRT
            # greedy: find the earliest arrival time
            # print(" NO riders can reach before FRT for Order", self.order.index)
            arrival_time_ls = list(RiderArriveTime_dict.keys())
            earliest_arrival_time = min(arrival_time_ls)
            bestRiders = RiderArriveTime_dict[earliest_arrival_time] # list
            bestRider = random.choice(bestRiders)
            restaurant_arrival_time = earliest_arrival_time
        
        riderAvailableTime = bestRider.nextAvailableTime # time when he finish the last order, before start this order
        
        # update order status
        self.order.foundRider(bestRider)
        self.order.addRiderReachReatsurantTime(restaurant_arrival_time)
        self.order.addDeliveredTime() # order.t_delivered
        # update rider status
        bestRider.deliver(self.order, riderAvailableTime)
        
        self.bestRider = bestRider
        return bestRider
        
    # from UsefulWorkMethod class
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
    # from AssignLaterMethoe class
    
    def find_pred_FPT_minus_threshold(self):
        return super().find_pred_FPT_minus_threshold()
    



# # debug
# u1 = AssignLaterMethod_UsefulWork()
# u2 = AssignLaterMethod()
# sim_1 = runEpisode_single_medthod(u1)
# sim_2 = runEpisode_single_medthod(u2)

# def get_order_df_from_sim_res(sim):
#     orders = sim.order_list
    
#     df_2dlist = []
#     for o in orders:
#         row = []
#         # 1. Order Index
#         row.append(o.index)
#         # 2. "Order-in Time"
#         row.append(o.t)
#         # 3. Rider Index
#         row.append(o.rider.index)
#         # 4. "Rider Arrives at Restaurant"
#         row.append(o.t_riderReachedRestaurant)
#         # 5. "Order Delivered Time"
#         row.append(o.t_delivered)
#         # 6. "Waiting Time"
#         row.append(o.wt)
        

#         # 7. "DT"
#         if args["FPT_avg"] > args["gridSize"]:
#             # when FPT is extremely largs, WT = max(FPT, R2R) + DT = FPT + DT
#             row.append(o.t_delivered - o.t  - args["FPT_avg"])
#         elif args["FPT_avg"] == 0:
#             # when FPT is negligible, WT = R2R + DT
#             row.append(o.t_delivered - o.t_riderReachedRestaurant) 
#         else:
#             row.append(None)
#         # 8. "Time taken before delivery"
#         row.append(o.wt - row[6] if row[6] else None)
#         # 9. "Theoretical Best WT"
#         optimal_wt = o.rest.order_FPT_dict[o.index] + math.dist(o.rest.loc, o.cust.loc)
#         row.append(optimal_wt)
#         # 10. "WT regret"
#         regret_wt = o.wt - optimal_wt
#         row.append(regret_wt)
#         # 11. "FPT"
#         row.append(o.rest.order_FPT_dict[o.index])

#         df_2dlist.append(row)
#     df = pd.DataFrame(df_2dlist, columns=["Order Index", "Order-in Time", 
#                                         "Rider Index", "Rider Arrives at Restaurant",
#                                         "Order Delivered Time", "Waiting Time", 
#                                         "DT", "Time taken before delivery", "Theoretical Best WT", "WT regret", "FPT"])
#     df.to_csv("results/"+ sim.method.name+ ".csv")
#     return df           

# get_order_df_from_sim_res(sim_1)
# get_order_df_from_sim_res(sim_2)
