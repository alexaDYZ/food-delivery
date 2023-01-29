
from typing import Counter, Dict
from unittest import result
import numpy as np
from AnticipationMethod import AnticipationMethod
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
from Simulation import Simulation
from generateData import dataGeneration
import matplotlib.pyplot as plt
import time
import datetime
import copy



# this function does 1 iteration of data-generation and simulation
# input is two Method object
def runEpisode(baselineMethod, anticipationMethod):
    ''' 
    Import Data 
    '''
    # from Data import restaurant_list, customer_list, order_list, order_time,rider_list
    
    with open('data.dict', "rb") as f:
        dict = pickle.load(f)
        restaurant_list = dict["restaurant list"]
        rider_list = dict["rider list"]
        order_list = dict["order list"]
        customer_list = dict["customer list"]
        order_time = dict["order time"]

        restaurant_list_copy = copy.deepcopy(restaurant_list)
        rider_list_copy = copy.deepcopy(rider_list)
        order_list_copy = copy.deepcopy(order_list)
        customer_list_copy = copy.deepcopy(customer_list )
        order_time_copy = copy.deepcopy(order_time)
        
        
    def getOrderDist(orderls):
        timels = [o.t for o in orderls]
        plt.hist(timels, bins=[i for i in range(min(timels), max(timels)+1)])
        plt.show()
        pass
    
    if args["showOrderTimeDist"]:
        getOrderDist(order_list)


    '''
    Start Simulation
    '''
    # start timer:
    # start_time = time.time()



    # Method 1: default method
    # greedy = DefaultMethod()
    # baselineMethod
    sim1 = Simulation(baselineMethod,restaurant_list, rider_list, order_list, customer_list, order_time, args)
    default = sim1.simulate()

    # Method 2: anticipative method
    # expectation = AnticipationMethod()
    sim2 = Simulation(anticipationMethod,restaurant_list_copy, rider_list_copy, order_list_copy, customer_list_copy, order_time_copy, args)
    anti = sim2.simulate()

    return default, anti
