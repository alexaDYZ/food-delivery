
from tkinter import font
from AssignmentMethod import AssignmentMethod
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
from DefaultMethod import DefaultMethod
import matplotlib.pyplot as plt

class Simulation():
    def __init__(self, method: AssignmentMethod,restaurant_list, rider_list, order_list, customer_list, order_time) -> None:
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
        self.end = -1

        
    def simulate(self):

        '''
        This funtion performs 1 simulation, using 1 set of data
        consisting of rider list, restaurant list, customer list 
        and order list.
        '''

        self.method.addRiderList(self.rider_list)
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
            
            if args["printCheckPt"] and currEvent.cat != 4:
                print("\n 💥 checkpoint", counter, " time ", round(currTime,2), "Event cat:", currEvent.getCategory() ,"\n")

            # check Event category, if it's a new order, tell it how to assign rider
            if currEvent.getCategory() == 'New Order':
                currEvent.addAssignmentMethod(self.method)
                
            elif currEvent.getCategory() == 'Regular Check':
                currEvent.addRiderList(self.rider_list) 
                currEvent.addStatusCheckDict(self.rider_status_check_dict)
                currEvent.passCurrQSize(checkpoint.qsize())
                currEvent.addProgramEndTime(self.end)
                # print("Status check at", currTime, ":", self.status_check_dict.keys())

            # execute current event:
            triggedEvent = currEvent.executeEvent(currTime)


            if currEvent.getCategory() == 'Order Delivered':
                
                self.numDelivered += 1
                # get total waiting time
                currOrder = currEvent.order
                wt = currOrder.wt
                self.wt_ls.append(wt)


            # if there is/are new events triggered, add to checkpoint
            if triggedEvent: 
                for e in triggedEvent:
                    checkpoint.put(e)

            counter += 1
        
        if args["showEventPlot"]:
            self.plotTimeHorizon()
        
        # # reset all order status
        # for o in self.order_list:
        #     o.reset()

        return self

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
    
    def plotTimeHorizon(self):
        pass
        # events = [(o.t, o.t_delivered) for o in self.order_list]
        # plt.eventplot(events,linelengths = 1, 
        #               colors=['C{}'.format(i) for i in range(len(events))],
        #              )
        # plt.ylabel("OrderNumber")
        # plt.xlabel("Time")
        # plt.title("Events acorss time \n Method:" + self.method.name +
        #           "\n #Orders" + str(args["numOrders"]) +
        #           "  #Riders:" + str(args["numRiders"]) +
        #           "  Gridsize:" + str(args["gridSize"]) +
        #           "  lambda:" + str(args["orderLambda"]), fontsize = 10)
        
        # plt.show()