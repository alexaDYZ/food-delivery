
from ast import Or
from distutils.sysconfig import customize_compiler
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
    checkpoint = order_time.copy()

    def updateAllStatus(currTime):
        for r in rider_list:
            r.updateStatus(currTime)

    updateAllStatus(0)
    counter=0
    for p in checkpoint:
        currTime = p
        updateAllStatus(currTime)
        curr_order = order_list[counter]
        bestRiderIndex = assign_order_to_rider(curr_order, rider_list, currTime) # find best rider, using greedy
        counter+=1
        
    def print_all_order_status(orders):
        dict = {}
        for o in orders:
            dict[o.index] = []
            dict[o.index].append("Delivered" if o.getOrderStatus() == "DELIVERED" else "NOT Delivered")
            dict[o.index].append( "Rider #"+str(o.rider) if o.rider is not None else "NA")
        # print 
        df = pd.DataFrame.from_dict(dict, orient='index',
                        columns=[ 'Status', 'Delivered by'])
        print(df)

    print_all_order_status(order_list)


if __name__ == "__main__":
   main()