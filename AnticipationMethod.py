
from ast import arg
from AssignmentMethod import AssignmentMethod
from Rider import Rider
from Restaurant import Restaurant
from Order import Order
from Customer import Customer
from config import args
import math
import random  


class AnticipationMethod(AssignmentMethod):
    def __init__(self):
        super().__init__()
        self.R2RforAll = None # a list of R2R time for the current order for all riders. will update every time a new order comes in
        self.bestRider = None # for the current order
        self.pred_FPT = -1 # the predicted FPT for the current order
        self.FPT_knowledge = None
        self.pred_bias = None
    
    def setFPT_pred_accuracy(self, level):
        # level can be "full", "partial", "poor"
        if level in AssignmentMethod.accuracy_of_prediction.keys():
            self.FPT_knowledge = AssignmentMethod.accuracy_of_prediction[level]
        else:
            raise Exception("Invalid FPT knowledge level")
        
    def setFPT_pred_bias(self, percentage):
        # the predicted FPT is biased by a percentage
        'eg. percentage = 10%. predicted FPT = actual * random.uniform(1-10%, 1+10%)'
        # e.g. if the 
        self.pred_bias = percentage
        

    def addOrder(self, newOrder):
        return super().addOrder(newOrder)
    
    def addCurrTime(self, currTime):
        return super().addCurrTime(currTime)
    def addRiderList(self, rider_list):
        return super().addRiderList(rider_list)
    
    # This part is different from the baseline method 
    def findR2RforAll(self):
        
        '''
        This function returns a dictionary, 
        key = Time of arrival at the restaurant for Rider r;
        value = Rider r, object.

        R2R in this case is the time when the rider reaches the restaurant.
        '''

        self.R2RforAll = {}
       
        rest_loc = self.order.rest.loc
        currTime = self.currTime

        def getTimeReachedRestaurant(rider:Rider, currTime): 
            
            # print("** For Order " + str(self.order.index)) if args["printAssignmentProcess"] else None
            
            '''get the time when this rider reaches the restaurant'''

            # Case 1: rider is idle/free now, and stays at a fixed place
            if rider.status == 0:
                # ######################### debug #########################
                # print("Rider " + str(rider.index) + "is idle at t = " + str(currTime) ) if args["printAssignmentProcess"] else None
                # print("Rider " + str(rider.index) +  " will reach at " +  
                #         str(rider.distance_to(rest_loc) / args["riderSpeed"] + currTime) ) if args["printAssignmentProcess"] else None
                # ######################### debug #########################
                
                R2R = rider.distance_to(rest_loc) / args["riderSpeed"]
                
                return currTime + R2R
            
            # Case 2: rider is walking
            elif rider.status == 2:
                # print(" - Rider " + str(rider.index) + "is walking at t = " + str(currTime) ) 
                curr_loc = rider.getLocation(currTime)
                R2R = math.dist(curr_loc, rest_loc) / args["riderSpeed"]
                return currTime + R2R

            # Case 3: rider is busy now
            else:
                # Assuming there's no maximum num of orders one can take
                
                # ######################### debug #########################
                # orderIndex = list(rider.orderDict.keys()) 
                # orderIndex.sort()
                # print("Rider " + str(rider.index) +  "have the fllowing orders in process: " + 
                #          str(orderIndex))if args["printAssignmentProcess"] else None
                # ######################### debug #########################


                nextAvilableTime = rider.nextAvailableTime_actual if self.FPT_knowledge == 1 else rider.nextAvailableTime_predicted

                
                lastStop = rider.lastStop # after finish the last order in the bag, rider stays there
                
                R2R = math.dist(lastStop, rest_loc) / args["riderSpeed"]

                # print("Rider "  +  str(rider.index)  + "'s nextAvilableTime: "  + str(nextAvilableTime) + 
                #         "\n R2R = " + str(R2R) + 
                #         "\n Hence will reach the restaurant at " + str(nextAvilableTime + R2R)) if args["printAssignmentProcess"] else None
                
                return nextAvilableTime + R2R
        
        for r in self.rider_list:
            arrival_time = getTimeReachedRestaurant(r, currTime)
            if arrival_time in self.R2RforAll:
                self.R2RforAll[arrival_time].append(r)
            else:
                self.R2RforAll[arrival_time] = [r]



    def find_ealiest_arrival(self):
        # print("calling ==== find_ealiest_arrival") if args["printAssignmentProcess"] else None
        # print the dict
        # print("🔮 Order " + str(self.order.index))
        # for k, v in self.R2RforAll.items():
        #     print("t = " + str(k) + " : \n" )
        #     for r in v:
        #         print(r.index) 
        # earliest = min(self.R2RforAll.keys())
        # print("shortedt is " + str(earliest) + "which are riders:")
        # for r in self.R2RforAll[earliest]:
        #     print(r.index)
             
        return min(self.R2RforAll.keys())

    # driver function, called in Event.py
    def find_best_rider(self):
        # print("🔮 Order" + str(self.order.index) + " 🔮")

        # 1. set predicted FPT given knowledge:
        if self.FPT_knowledge == 1:
            self.order.FPT_predicted = self.order.rest.order_FPT_dict[self.order.index]
        elif self.FPT_knowledge == 0.5:
            self.order.FPT_predicted = 30*60
        elif self.FPT_knowledge == 0:
            self.order.FPT_predicted = 10*60
        elif self.FPT_knowledge == 2:
            self.order.FPT_predicted = 50*60

        if self.pred_bias is not None:
            self.order.FPT_predicted = self.order.rest.order_FPT_dict[self.order.index] * random.uniform(1-self.pred_bias/100,1+self.pred_bias/100)

        # self.order.rest.order_FPT_dict[self.order.index] * random.uniform(0.8,1.2)
        
        # 2. find the predicted arribal time for all riders

        
        self.findR2RforAll() # compute self.R2RforAll

        t_arrive_restaurant_pred = self.find_ealiest_arrival() # find min in self.R2RforAll
        
        
        bestRiders = self.R2RforAll[t_arrive_restaurant_pred] # find best rider using the min
        bestRider = random.choice(bestRiders) # randomly choose one from the best riders

        # 3. update rider status
        t_arrive_restaurant_actual = -1 


        if bestRider.status == 2: # if rider is walking
            t_start_actual = self.currTime # let him start right away, more update when r.deliver() is called
        else:
            '''Using the ACTUAL FPT, update rider status'''
            t_start_actual = bestRider.nextAvailableTime_actual
            # best_rider_R2R = math.dist(bestRider.lastStop.loc if bestRider.lastStop.loc else bestRider.loc, self.order.rest.loc) / args["riderSpeed"]
            # t_arrive_restaurant_actual = t_start_actual + best_rider_R2R
            if self.FPT_knowledge == 1: t_arrive_restaurant_actual = t_arrive_restaurant_pred
            else: t_arrive_restaurant_actual = t_start_actual + (t_arrive_restaurant_pred - bestRider.nextAvailableTime_predicted)
        
            # print("Order " + str(self.order.index) + " is assigned to rider " + str(bestRider.index) + " at time " + str(self.currTime/60) + 
            #         " with predicted arrival time " + str(t_arrive_restaurant_pred/60) + " and actual arrival time " + str(t_arrive_restaurant_actual/60) ) 
        
        # update order status
        self.order.foundRider(bestRider)
        self.order.addRiderReachReatsurantTime( t_arrive_restaurant_actual)
        self.order.addRiderReachReatsurantTime_pred( t_arrive_restaurant_pred)
        # if self.FPT_knowledge != 1: self.order.addRiderReachReatsurantTime_pred( t_arrive_restaurant_pred ) 
        self.order.addDeliveredTime() # order.t_delivered

        # update rider status
        bestRider.deliver(self.order, t_start_actual)
        
        self.bestRider = bestRider
        
        return bestRider
        
    
    


    
