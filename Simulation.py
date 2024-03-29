
from tkinter import font
from AssignmentMethod import AssignmentMethod
from PatientAnticipativeMethod_Bulk import PatientAnticipativeMethod_Bulk
from PatientAnticipativeMethod_Soft import PatientAnticipativeMethod_Soft
from itertools import count
from tabnanny import check
import time
import random
from typing import Counter, Dict
import numpy as np
from utils import dotdict
from datetime import datetime, timedelta
from Order import Order
from Restaurant import Restaurant
from Customer import Customer
from Rider import Rider
from  OriginalAssignment import assign_order_to_rider
from config import args
import pickle
import pandas as pd
from EventQueue import EventQueue
from Event import Event
from DefaultMethod_1b import DefaultMethod_1b
import matplotlib.pyplot as plt

class Simulation():
    def __init__(self, method: AssignmentMethod,restaurant_list, rider_list, order_list, customer_list, order_time, args) -> None:
        self.args = args
        self.restaurant_list = restaurant_list
        self.rider_list = rider_list
        self.order_list = order_list
        self.customer_list = customer_list
        self.order_time = order_time
        self.method = method
        # Analysis: orders
        self.numDelivered = 0 # total number of orders delivered within this simulation
        # Analysis: ridrs
        self.rider_status_check_dict = {} # %of busy riders, checked at regular intervals
        # Analysis: waiting time
        self.wt_ls = [] # a list of waiting time, each element is the waiting time of an order
        
        # end of simulation
        self.t_termination = -1

        
    def simulate(self):

        '''
        This funtion performs 1 simulation, using 1 set of data
        consisting of rider list, restaurant list, customer list 
        and order list.
        '''
        # Patient Anticipative Methods(Stalling Time involved)
        if self.method.__class__.__name__ == PatientAnticipativeMethod_Bulk.__name__:
            self.method.addRiderList(self.rider_list)
            '''Initialize regular check point'''
            checkpoint = EventQueue()   
            initial_check = Event(0, 4, None)
            checkpoint.put(initial_check)
            
            '''Put in new orders event'''
            order_time_dict = {}
            self.order_list.sort()
            for o in self.order_list:
                order_time_dict[o.t] = o
                e = Event(o.t, 1, o)
                checkpoint.put(e)
            
            
            counter = 0
            
            stallingTime = args["stallingTime"] # the first cutoff time for orders to be assigned
            # assign_pending_orders = Event(cutoff_time, 5, None)
            # checkpoint.put(assign_pending_orders)

            '''Start the Simulation'''
            while not checkpoint.empty():
                # see event type, update status
                currEvent = checkpoint.get()
                currEvent.addAssignmentMethod(self.method)

                # currEvent.print()
                currTime = currEvent.time
                
                if self.args["printCheckPt"] and currEvent.cat != 4: pass
                    # print("\n 💥 checkpoint", counter, " time ", round(currTime,2), "Event cat:", currEvent.getCategory() ,"\n")

                # check Event category, if it's a new order, tell it how to assign rider
                if currEvent.getCategory() == 'New Order':
                    '''Start the stalling time window when a new order comes in '''
                    
                    if len(self.method.pending_order_dict) == 0:
                        cutoff_time = currEvent.order.t + stallingTime

                        assign_pending_orders = Event(cutoff_time, 5, None)
                        checkpoint.put(assign_pending_orders)

                    self.method.addPendingOrder(currEvent.order)
                    #### debug
                    # print("New order added, pending orders:", len(self.method.pending_order_dict), "at time", currTime)

                elif currEvent.getCategory() == 'Match Pending Orders':
                    # print("Match Pending Orders at time ", currTime)
                    
                    self.method.addCurrTime(currTime)
                    # matching
                    matched_res_dict = self.method.matchPendingOrders() # key: order, value: best rider
                    #### debug
                    # print("matched_res_dict:")
                    # for o, r in matched_res_dict.items():
                    #     print(o.index, r.index)

                    # assign
                    self.method.assignPendingOrders(matched_res_dict) # update status for rider and order
                    # create new events for rider arrival and order delivered
                    currEvent.addMatchedOrderRiderDict(matched_res_dict) # when exicute, update status for rider and order
                    # clear pending orders
                    self.method.clearPendingOrders()

                    
                elif currEvent.getCategory() == 'Regular Check':
                    currEvent.addRiderList(self.rider_list) 
                    currEvent.addStatusCheckDict(self.rider_status_check_dict)
                    currEvent.passCurrQSize(checkpoint.qsize())
                    currEvent.addProgramEndTime(self.t_termination)
                    # print("Status check at", currTime, ":", self.status_check_dict.keys())
                
                elif currEvent.getCategory() == 'Order Delivered':
                    
                    self.numDelivered += 1
                    # get total waiting time
                    currOrder = currEvent.order
                    wt = currOrder.wt
                    self.wt_ls.append(wt)

                # execute current event:
                triggedEvent = currEvent.executeEvent(currTime)

                # if there is/are new events triggered, add to checkpoint
                if triggedEvent: 
                    for e in triggedEvent:
                        checkpoint.put(e)

                counter += 1

        # # 
        # elif self.method.__class__.__name__ == PatientAnticipativeMethod_Soft.__name__:
        #     self.method.addRiderList(self.rider_list)
        #     '''Initialize regular check point'''
        #     checkpoint = EventQueue()   
        #     initial_check = Event(0, 4, None)
        #     checkpoint.put(initial_check)

        #     '''Put in new orders event'''
        #     order_time_dict = {}
        #     self.order_list.sort()
        #     for o in self.order_list:
        #         order_time_dict[o.t] = o
        #         e = Event(o.t, 1, o)
        #         checkpoint.put(e)

        #     stallingTime = args["stallingTime"] # the first cutoff time for orders to be assigned


        #     '''Start the Simulation'''
        #     while not checkpoint.empty():
        #         # see event type, update status
        #         currEvent = checkpoint.get()
        #         currEvent.addAssignmentMethod(self.method)

        #         # currEvent.print()
        #         currTime = currEvent.time
                
        #         if self.args["printCheckPt"] and currEvent.cat != 4: pass
        #             # print("\n 💥 checkpoint", counter, " time ", round(currTime,2), "Event cat:", currEvent.getCategory() ,"\n")

        #         # check Event category, if it's a new order, tell it how to assign rider
        #         if currEvent.getCategory() == 'New Order':
        #             '''each order is assigned after the stalling time window'''
                    
        #             # for every new order, add a checkpoint event in the future
        #             cutoff_time = currEvent.order.t + stallingTime

        #             assign_pending_orders = Event(cutoff_time, 5, None)
        #             checkpoint.put(assign_pending_orders)
                        

        #             self.method.addPendingOrder(currEvent.order)
        #             #### debug
        #             # print("New order added, pending orders:", len(self.method.pending_order_dict), "at time", currTime)

        #         elif currEvent.getCategory() == 'Match Pending Orders':
        #             # print("Match Pending Orders at time ", currTime)
                    
        #             self.method.addCurrTime(currTime)
        #             # matching
        #             matched_res_dict = self.method.matchPendingOrders() # key: order, value: best rider
        #             #### debug
        #             # print("matched_res_dict:")
        #             # for o, r in matched_res_dict.items():
        #             #     print(o.index, r.index)

        #             # assign
        #             self.method.assignPendingOrders(matched_res_dict) # update status for rider and order
        #             # create new events for rider arrival and order delivered
        #             currEvent.addMatchedOrderRiderDict(matched_res_dict) # when exicute, update status for rider and order
        #             # clear pending orders
        #             self.method.clearPendingOrders()

                    
        #         elif currEvent.getCategory() == 'Regular Check':
        #             currEvent.addRiderList(self.rider_list) 
        #             currEvent.addStatusCheckDict(self.rider_status_check_dict)
        #             currEvent.passCurrQSize(checkpoint.qsize())
        #             currEvent.addProgramEndTime(self.t_termination)
        #             # print("Status check at", currTime, ":", self.status_check_dict.keys())
                
        #         elif currEvent.getCategory() == 'Order Delivered':
                    
        #             self.numDelivered += 1
        #             # get total waiting time
        #             currOrder = currEvent.order
        #             wt = currOrder.wt
        #             self.wt_ls.append(wt)

        #         # execute current event:
        #         triggedEvent = currEvent.executeEvent(currTime)

        #         # if there is/are new events triggered, add to checkpoint
        #         if triggedEvent: 
        #             for e in triggedEvent:
        #                 checkpoint.put(e)

        #         counter += 1

        
        # Immediate Assignment Methods
        else:

            self.method.addRiderList(self.rider_list)
            self.method.addRestList(self.restaurant_list)
            
            # create event checkpoints
            checkpoint = EventQueue()   
            
            '''Initialize regular check point'''
            initial_check = Event(0, 4, None)
            checkpoint.put(initial_check)
            
            '''Put in new orders event'''
            order_time_dict = {}
            self.order_list.sort()
            for o in self.order_list:
                order_time_dict[o.t] = o
                e = Event(o.t, 1, o)
                checkpoint.put(e)
                # get program end time. 
                # Note: self.end < actual ending time of the program, 
                # since it ends at "order appear time" of the last order, instaed
                # of "delivered time" of the last order. 
                # but it desent matter if we wish to know % riders occupied
            
            # self.end = max(order_time_dict.keys())
            
    

            #initialize status for all
            
            counter = 0
            
            #simulation starts
            while not checkpoint.empty():
                # see event type, update status
                currEvent = checkpoint.get()

                # currEvent.print()
                currTime = currEvent.time
                
                if self.args["printCheckPt"] and currEvent.cat != 4: pass
                    # print("\n 💥 checkpoint", counter, " time ", round(currTime,2), "Event cat:", currEvent.getCategory() ,"\n")

                # check Event category, if it's a new order, tell it how to assign rider
                if currEvent.getCategory() == 'New Order':
                    # print("New order === Order Index ", currEvent.order.index, " at ",currTime)
                    currEvent.addAssignmentMethod(self.method)
                    
                elif currEvent.getCategory() == 'Regular Check':
                    currEvent.addRiderList(self.rider_list) 
                    currEvent.addStatusCheckDict(self.rider_status_check_dict)
                    currEvent.passCurrQSize(checkpoint.qsize())
                    currEvent.addProgramEndTime(self.t_termination)
                    # print("Status check at", currTime, ":", self.status_check_dict.keys())

                elif currEvent.getCategory() == 'Order Delivered':
                    currEvent.addAssignmentMethod(self.method) # to provide self.walking_rule
                    self.numDelivered += 1
                    # get total waiting time
                    currOrder = currEvent.order
                    wt = currOrder.wt
                    self.wt_ls.append(wt)

                elif currEvent.getCategory() == "Re-Assignment": 
                    # print("Reassigning Order " + str(currEvent.order.index) + " at t = " + str(currTime))
                    currEvent.addAssignmentMethod(self.method)
                
                # execute current event:
                triggedEvent = currEvent.executeEvent(currTime)

                # if there is/are new events triggered, add to checkpoint
                if triggedEvent: 
                    for e in triggedEvent:
                        checkpoint.put(e)

                counter += 1
            
            if self.args["showEventPlot"]:
                self.plotTimeHorizon()
            
            # # reset all order status
            # for o in self.order_list:
            #     o.reset()

        return self




# debug functions for visulization
    def printResult(self):
        
        print("\n ****************** \n ", self.method.__class__.__name__, "\n ****************** \n ")
        def print_all_order_status(orders):
            dict = {}
            for o in orders:
                dict[o.index] = []
                dict[o.index].append("Delivered" if o.getOrderStatus() == "DELIVERED" else "NOT Delivered")
                dict[o.index].append( "Rider #"+str(o.rider.index) if o.rider is not None else "NA")
            # print 
            df = pd.DataFrame.from_dict(dict, orient='index',
                            columns=[ 'Status', 'Delivered by'])
            print(df)

        def print_all_rider_waiting_time(rider_list):
            dict = {}
            for r in rider_list:
                dict[r.index] = []
                dict[r.index].append(r.totalOrderDelivered)
                dict[r.index].append(round(r.totalWaitingTime,2))
                dict[r.index].append(0 if r.totalOrderDelivered ==0 else round(r.totalWaitingTime/r.totalOrderDelivered,2))
                
            # print 
            df = pd.DataFrame.from_dict(dict, orient='index',
                            columns=[ '# orders delivered', 'total waiting time', 'waiting time per order'])
            print(df)
        print_all_order_status(self.order_list)
        print_all_rider_waiting_time(self.rider_list)
    
    def plotTimeHorizon(self):
        plot = False
        if plot:
            events = [(o.t, o.t_delivered) for o in self.order_list]
            plt.eventplot(events,linelengths = 1, 
                        colors=['C{}'.format(i) for i in range(len(events))],
                        )
            plt.ylabel("OrderNumber")
            plt.xlabel("Time")
            plt.title("Events acorss time \n Method:" + self.method.name +
                    "\n #Orders" + str(args["numOrders"]) +
                    "  #Riders:" + str(args["numRiders"]) +
                    "  Gridsize:" + str(args["gridSize"]) +
                    "  lambda:" + str(args["orderArrivalRate"]), fontsize = 10)
            
            plt.show()
        