
import copy
from mailbox import MaildirMessage
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
from DefaultMethod import DefaultMethod
from Simulation import Simulation
from tabulate import tabulate
from generateData import dataGeneration
import matplotlib.pyplot as plt
import time

'''
Variable/x-axis: number of variables
What's kept constant: time window
'''


# this function does 1 iteration of data-generation and simulation

def runEpisode():
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

    # Method 1: default method, greedy
    greedy = DefaultMethod()
    sim1 = Simulation(greedy,restaurant_list, rider_list, order_list, customer_list, order_time, args)
    res_default=sim1.simulate()

    # Method 2: proposed method, expectation + greedy
    expectation = AnticipationMethod()
    sim2 = Simulation(expectation,restaurant_list, rider_list_copy, order_list_copy, customer_list_copy, order_time_copy, args)
    res_anti = sim2.simulate()

    return res_default,res_anti


def AnalyseNumOrders():
    
    start_time = time.time()
    
    # x-axis: number of orders
    numOrder = [50, 100, 150, 200]
    
    
    avg = {} # record avg % of ordered delivered for each iteration
    # higher = {} # record % of better performance 

    numEpisode = args["numEpisode"]

    for num in numOrder:
        args["numOrders"] = num
        args["numCustomers"] = num
        

        # keep track of #orders delivered for each episode for the two method
        num_delivered_list_default = []
        num_delivered_list_anticipation = []

        for i in range(numEpisode):
            dataGeneration()
            res_default,res_anti = runEpisode()
            numDeliveredDefault,numDeliveredExpectation = res_default.numDelivered,res_anti.numDelivered
            num_delivered_list_default.append(numDeliveredDefault)
            num_delivered_list_anticipation.append(numDeliveredExpectation)
        
        # averaging
        avg_default = round(sum(num_delivered_list_default)/num/numEpisode,3)
        avg_anticipation = round(sum(num_delivered_list_anticipation)/num/numEpisode,3)

        if num not in avg.keys():
            avg[num] = []
        
        avg[num].append(avg_default)
        avg[num].append(avg_anticipation)


    '''
    plot  
    '''    
    
    df = pd.DataFrame.from_dict(avg, orient='index',
                            columns=['avg_default', 'avg_anticipation'])
    print(df)


    
    x_axis = numOrder
    y_1 = [i[0] for i in avg.values()]
    y_2 = [i[1] for i in avg.values()]
    plt.plot(x_axis,y_1, label = "Default")
    plt.plot(x_axis, y_2, label = "Anticipation")
    
    plt.legend()
    title = "Average percentage of orders delivered \n #Simulation = " + str(numEpisode)
    plt.title(title)

    for x,y in zip(x_axis,y_1):

        label = "{:.2f}".format(y)

        plt.annotate(label, # this is the text
                    (x,y), # these are the coordinates to position the label
                    textcoords="offset points", # how to position the text
                    xytext=(0,10), # distance from text to points (x,y)
                    ha='center')
    
    for x,y in zip(x_axis,y_2):

        label = "{:.2f}".format(y)

        plt.annotate(label, # this is the text
                    (x,y), # these are the coordinates to position the label
                    textcoords="offset points", # how to position the text
                    xytext=(0,10), # distance from text to points (x,y)
                    ha='center')

    plt.show()
    


    

    print("total time taken:", time.time() - start_time)
    


    
    




