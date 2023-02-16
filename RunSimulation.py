
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

def get_data_for_simulation():
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

        
        
    # debug
    def getOrderDist(orderls):
        timels = [o.t for o in orderls]
        plt.hist(timels, bins=[i for i in range(min(timels), max(timels)+1)])
        plt.show()
        pass
    # debug
    if args["showOrderTimeDist"]:
        getOrderDist(order_list)
    
    return restaurant_list, rider_list, order_list, customer_list, order_time,
    
    


def runEpisode(baselineMethod, alternativeMethod):
    
    # get data
    restaurant_list, rider_list, order_list, customer_list, order_time = get_data_for_simulation()

    restaurant_list_copy = copy.deepcopy(restaurant_list)
    rider_list_copy = copy.deepcopy(rider_list)
    order_list_copy = copy.deepcopy(order_list)
    customer_list_copy = copy.deepcopy(customer_list )
    order_time_copy = copy.deepcopy(order_time)
    
    '''
    Start Simulation
    '''

    # Method 1: default method
    # baselineMethod
    sim1 = Simulation(baselineMethod,restaurant_list, rider_list, order_list, customer_list, order_time, args)
    default = sim1.simulate()

    # Method 2: alternative method
    sim2 = Simulation(alternativeMethod,restaurant_list_copy, rider_list_copy, order_list_copy, customer_list_copy, order_time_copy, args)
    alt = sim2.simulate()

    return default, alt

def runEpisode_single_medthod(method):
    # get data
    restaurant_list, rider_list, order_list, customer_list, order_time = get_data_for_simulation()
    args["numOrders"] = len(order_list)
    '''
    Start Simulation
    '''
    sim = Simulation(method, restaurant_list, rider_list, order_list, customer_list, order_time, args)
    sim_res = sim.simulate()

    if method.name == "AssignLaterMethod":
        count = 0
        for o in sim.order_list:
            if o.ifReassigned:
                count += 1
        
        print("Reassigned orders: ", round(count/len(sim.order_list), 2)*100, "%")
    
    return sim_res
