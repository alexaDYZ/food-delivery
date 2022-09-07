
from cProfile import label
import copy
from ctypes.wintypes import PINT
from glob import escape
from tkinter.tix import COLUMN
from turtle import color
import numpy as np
from AnticipationMethod import AnticipationMethod
from utils import dotdict
from Order import Order
from Restaurant import Restaurant
from Customer import Customer
from Rider import Rider
from OriginalAssignment import assign_order_to_rider
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
from Analyse_Rider import runEpisode




def AnalyseWaitingTime():
    
    def analyseOnce():
        '''
        This function performs 1 analysis using the given set of parameters.
        Output: [number of Orders, 
                rate of orders appearing, 
                average waiting time per order for Default Method,
                average waiting time per order for Anticipation Method,
                difference between the waiting time per order,
                ]
        '''
        start_time = time.time()

        dataGeneration()
        default,anti = runEpisode() # 2 simulation results

        # get avg waiting time per order
        def compute_avg(ls):
            if ls:
                return sum(ls)/len(ls)
            else:
                print("empty list")
        
        avg_wt_default = compute_avg(default.wt_ls)
        avg_wt_anti = compute_avg(anti.wt_ls)

        print("Default Method:num order finished", len(default.wt_ls))
        print("Anticipation Method: num order finished", len(anti.wt_ls))
        print(avg_wt_default, avg_wt_anti)
        diff = avg_wt_default-avg_wt_anti
        print(diff)
       
        
        return [args["numOrders"], args["orderLambda"], avg_wt_default, avg_wt_anti, diff]
    
    
    
    
    def multipleAnalysis():
        '''Experiment with different num orders and lambda'''
        numOrders = [ 50*i for i in range(8, 14)]
        lams = [ 10*i for i in range(1, 6)]
        dfls = []
        
        colorcounter = 0
        for l in lams:
            c = args["colorls"][colorcounter]
        
            y_d = [] # avg waiting time for default method
            y_a = [] # anticipation 
            
            for j in numOrders:
                args["numOrders"] = j
                args["numCustomers"] = j
                args["orderLambda"] = l
                res = analyseOnce()
                dfls.append(res)
                y_d.append(res[2])
                y_a.append(res[3])
                
            if args["showWTplot"]:
                plt.plot(numOrders, y_d, label = "Default,lambda =" + str(l), 
                         linestyle = 'dashed', color = c, marker = 'o')
                plt.plot(numOrders, y_a, label = "Anticipation, lambda =" + str(l), 
                         linestyle = 'solid', color = c, marker = 'o')
            
            colorcounter+=1
    
        
        
        df = pd.DataFrame(dfls, columns = ['# orders', 'lambda', 
                                                'avg Waiting t. - Default', 
                                                'avg Waiting t. - Anticipation', 
                                                'difference'])
        print(df)
        
        plt.title("Average Waiting Time \n number of riders = "+ str(args["numRiders"])+
                  "\n gridsize:" + str(args["gridSize"]))
        
        plt.xlabel("Number of Orders")
        plt.ylabel("Average Waiting Time")
        plt.legend()
        plt.show()
        
    if args["showWTplot"]: multipleAnalysis()

    if args["showEventPlot"]:analyseOnce()
    # print(simulation_default.wt_ls)
    # print(avg_wt_default)
    # print(simulation_anti.wt_ls)
    # print(avg_wt_anti)

    # plt.plot(simulation_default.wt_ls,simulation_default.wt_ls, '--', label = "Default")
    # plt.axhline(y=avg_wt_default, color='black')
    # # plt.plot(x_axis, y_2,'-+',label = "Anticipation")
    # plt.show()
    # print("total time taken:", time.time() - start_time)
    
    
    
