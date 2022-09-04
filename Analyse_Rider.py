
from ast import arg
import copy
from mailbox import MaildirMessage
from turtle import color
from typing import Counter, Dict
from unittest import result
import numpy as np
from ProposedMethod import ProposedMethod
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
    sim1 = Simulation(greedy,restaurant_list, rider_list, order_list, customer_list, order_time)
    simulation_default = sim1.simulate()

    # Method 2: proposed method, expectation + greedy
    expectation = ProposedMethod()
    sim2 = Simulation(expectation,restaurant_list, rider_list_copy, order_list_copy, customer_list_copy, order_time_copy)
    simulation_anti = sim2.simulate()

    return simulation_default,simulation_anti


def AnalyseRider():
    
    start_time = time.time()

    dataGeneration()
    simulation_default,simulation_anti = runEpisode() # 2 dictionaries
    res_default,res_anti = simulation_default.rider_status_check_dict, simulation_anti.rider_status_check_dict
    # averaging: omitted
        
    '''
    generate big dict:
        key -> time interval
        value -> [ratio_default, ratio_anti]
    '''
    res = {}
    for t in res_default.keys():
        res[t] = []
        res[t].append(res_default[t])
        res[t].append(res_anti[t])
            
    

    
    # df = pd.DataFrame.from_dict(res, orient='index',
    #                         columns=['ratio_default', 'ratio_anticipation'])
    # # print(df)


    ''' individual plot  '''
    x_axis = res_default.keys()
    y_1 = [i[0] for i in res.values()]
    y_2 = [i[1] for i in res.values()]
    plt.plot(x_axis,y_1, '--', label = "Default")
    plt.plot(x_axis, y_2,'-+',label = "Anticipation")
    
    plt.axhline(y=np.nanmean(y_1), color='C0', label = "mean="+str(round(np.nanmean(y_1),3)))
    plt.axhline(y=np.nanmean(y_2), color= 'C1', label = "mean="+str(round(np.nanmean(y_2),3)))
    
    plt.legend()
    title = "Percentage of Riders Occupied\nlambda :" + str(args["avgOrderTime"])+"\n#Orders per period:"+ str(args["numOrders"]) +"\n NUmber of Riders:" + str(args["numRiders"])
    subtitle = 'Difference in mean='+str(round(abs(np.nanmean(y_1)-np.nanmean(y_2)),3))
    plt.title(title+"\n"+subtitle)
    
    
    markPoint = False
    if markPoint:
        
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


    '''average percentage plot '''
    
    # numOrders =  [10,20,30,40,50,60,70,80] # x-axis
    # diff_list = [] # y-axis
    
    # for num in numOrders:
    #     args["numOrders"] = num
    #     args["numCustomers"] = num
        
    #     repeat = 30
    #     ls = []
    #     for i in range(repeat):
    #         dataGeneration()
            
    #         res_default,res_anti = runEpisode() # 2 dictionaries
    #         default = list(res_default.values())
    #         anti = list(res_anti.values())
    #         diff = np.nanmean(default) - np.nanmean(anti)
    #         ls.append(diff)
    #     avg_diff = sum(ls)/len(ls)
    #     diff_list.append(avg_diff)
    # print(diff_list)
    # plt.plot(numOrders,diff_list, '--', label = "Difference in mean")
    # plt.xlabel("number of orders / period ")
    # plt.ylabel("difference in mean ratio: default - anticipation ")
    # plt.axhline(y=0, color='black')
    # plt.show()
    
    
    
    print("total time taken:", time.time() - start_time)
    

