
from AssignmentMethod import AssignmentMethod
from itertools import count
import logging
from tabnanny import check
import time
import random
from typing import Counter, Dict
import numpy as np
from utils import dotdict
from datetime import datetime, timedelta
import threading
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
from DefaultMethod import DefaultMethod

class Simulation():
    def __init__(self, method: AssignmentMethod,restaurant_list, rider_list, order_list, customer_list, order_time) -> None:
        self.restaurant_list = restaurant_list
        self.rider_list = rider_list
        self.order_list = order_list
        self.customer_list = customer_list
        self.order_time = order_time
        self.method = method
        self.numDelivered = 0

    def simulate(self):
        self.method.addRiderList(self.rider_list)
        # create event checkpoints
        checkpoint = EventQueue()      
        order_time_dict = {}
        self.order_list.sort()
        for o in self.order_list:
            order_time_dict[o.t] = o
            e = Event(o.t, 1, o)
            checkpoint.put(e)
    

        #initialize status for all
        # updateAllStatus(0)
        counter = 0
        #simulation starts
        while not checkpoint.empty():
            # see event type, update status
            currEvent = checkpoint.get()

            # currEvent.print()
            currTime = currEvent.time
            # print("\n 💥 checkpoint", counter, " time ", round(currTime,2), "Event cat:", currEvent.getCategory() ,"\n")

            # check Event category, if it's a new order, tell it how to assign rider
            if currEvent.getCategory() == 'New Order':
                currEvent.addAssignmentMethod(self.method)

            if currEvent.getCategory() == 'Order Delivered':
                self.numDelivered += 1

            # execute current event:
            triggedEvent = currEvent.executeEvent(currTime)
            # if there is/are new events triggered, add to checkpoint
            if triggedEvent: 
                for e in triggedEvent:
                    checkpoint.put(e)
                    
            
            
            # # Situation 1: new order comes in
            # if currEvent.getCategory() ==  'New Order':
            #     curr_order = order_time_dict[currTime]
            #     self.method.addOrder(curr_order)
            #     self.method.addCurrTime(currTime)
            #     bestRider = self.method.assign()
                
            #     # if best rider can be found:
            #     if bestRider:
            #         # create "arrive at restaturant" event
            #         rest_arrival_time = bestRider.getRestArrivalTime(curr_order.index)
            #         e_arrival = Event(rest_arrival_time, 3, curr_order)
            #         checkpoint.put(e_arrival)
            #         # create "order delivered" event
            #         finishTime = bestRider.getOrderCompleteTime(curr_order.index)
            #         e_finish = Event(finishTime, 2, curr_order)
            #         checkpoint.put(e_finish)
            
            # Situation 2 and 3: order is delivered
            
            counter += 1
        # self.printResult()
        return self.numDelivered

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
        # print_all_order_status(self.order_list)
        # print_all_rider_waiting_time(self.rider_list)