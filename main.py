
import copy
from distutils.sysconfig import customize_compiler
from itertools import count
import logging
from tabnanny import check
import time
import random
from typing import Counter, Dict
import numpy as np
from ProposedMethod import ProposedMethod
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
from Simulation import Simulation




def main():
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

        
        rider_list_copy = copy.deepcopy(rider_list)
        order_list_copy = copy.deepcopy(order_list)
        customer_list_copy = copy.deepcopy(customer_list )
        order_time_copy = copy.deepcopy(order_time)

    '''
    Start Simulation
    '''
    # start timer:
    # start_time = time.time()
    # log = logging.getLogger(__name__)
    # Method 1: default method, greedy
    greedy = DefaultMethod()
    sim1 = Simulation(greedy,restaurant_list, rider_list, order_list, customer_list, order_time)
    sim1.simulate()

    # Method 2: proposed method, expectation + greedy
    expectation = ProposedMethod()
    sim2 = Simulation(expectation,restaurant_list, rider_list_copy, order_list_copy, customer_list_copy, order_time_copy)
    sim2.simulate()


    




if __name__ == "__main__":
   main()