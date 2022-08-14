
from ast import Or
from distutils.sysconfig import customize_compiler
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


''' Import Data '''
# from Data import restaurant_list, customer_list, order_list, order_time,rider_list
with open('data.dict', "rb") as f:
    dict = pickle.load(f)
    restaurant_list = dict["restaurant list"]
    rider_list = dict["rider list"]
    order_list = dict["order list"]
    customer_list = dict["customer list"]
    order_time = dict["order time"]

def main():

    '''
    Start Simulation
    '''

    # start timer:
    start_time = time.time()
    log = logging.getLogger(__name__)



    # Dynamic ------ schedule order appearing time:
    # threading.Timer(t, assiagn).start()

    # Static ------- only update when order comes out
    # checkpoint = order_time.copy()

    checkpoint = EventQueue() 
    for t in order_time:
        e = Event(t, 1)
        checkpoint.put(e)
    
    order_time_dict = {}
    for t,o in zip(order_time, order_list):
        order_time_dict[t] = o
  
    def updateAllStatus(currTime):
        for r in rider_list:
            r.updateStatus(currTime)
   
    #initialize status for all
    updateAllStatus(0)
    counter = 0
    # *****Events start here ****** #
    while not checkpoint.empty():
        print("💥 checkpoint", counter)
        currEvent = checkpoint.get()
        if counter ==17: print(currEvent)
        currEvent.print()
        currTime = currEvent.time
        updateAllStatus(currTime)

        if currEvent.getCategory() ==  'New Order':
            curr_order = order_time_dict[currTime]
            bestRider = assign_order_to_rider(curr_order, rider_list, currTime) # find best rider, using greedy
            # if best rider can be found, get order finish time
            if bestRider:
                finishTime = bestRider.nextFreeTime
                e = Event(finishTime, 2)
                checkpoint.put(e)
        counter+=1

    
    # counter=0
    # # for p in checkpoint:
    # #     currTime = p

    # #     updateAllStatus(currTime)
    # #     curr_order = order_list[counter]
    # #     bestRiderIndex = assign_order_to_rider(curr_order, rider_list, currTime) # find best rider, using greedy
    # #     counter+=1
        
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

    print_all_order_status(order_list)

    def print_all_rider_waiting_time(rider_list):
        dict = {}
        for r in rider_list:
            dict[r.index] = []
            dict[r.index].append(r.totalOrderDelivered)
            dict[r.index].append(round(r.totalWaitingTime,2))
            dict[r.index].append(round(r.totalWaitingTime/r.totalOrderDelivered,2))
            
        # print 
        df = pd.DataFrame.from_dict(dict, orient='index',
                        columns=[ '# orders delivered', 'total waiting time', 'waiting time per order'])
        print(df)
    print_all_rider_waiting_time(rider_list)


if __name__ == "__main__":
   main()