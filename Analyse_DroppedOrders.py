

from ast import arg
import copy
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
from RunSimulation import runEpisode
from Analyse_Orders import AnalyseOrders
from DefaultMethod_1a import DefaultMethod_1a
import datetime
import math


class Analyse_DroppedOrders():
    def __init__(self) -> None:
        self.baselineMethod = DefaultMethod_1a()
        self.anticipativeMethod = AnticipationMethod()
        self.default = None
        self.anti = None
        self.dr_a = -1 # Dropped-out Rate, fraction of orders that are better off with anticipation method
        self.dr_d = -1 # Dropped-out Rate, fraction of orders that are better off with default method
        self.dr = [] # consisting of many lists. Each is [fr_a, fr_d] for 1 simulation
        self.summary_stats_d = []
    def simulateOnce(self):
        '''
        This function performs 1 analysis using the given set of parameters.
        Output: [number of Orders, 
                rate of orders appearing, 
                average waiting time per order for Default Method,
                average waiting time per order for Anticipation Method,
                difference between the waiting time per order,
                ]
        '''
        dataGeneration()

        default,anti = runEpisode(self.baselineMethod, self.anticipativeMethod) # 2 simulation results
        self.default = default
        self.anti = anti


    def findDR(self):
        '''
        This function will find the fraction of orders dropped by both methods
        '''
        # baseline method
        ls_d = [1 if self.default.order_list[i].status == 4 else 0 for i in range(len(self.default.order_list))]
        self.dr_d = sum(ls_d)/len(ls_d)
        # anticipative method
        ls_a = [1 if self.anti.order_list[i].status == 4 else 0 for i in range(len(self.anti.order_list))]
        self.dr_a = sum(ls_a)/len(ls_a)

        self.dr.append([self.dr_a, self.dr_d])
        


    # def basicAnalysis(self):
    #     ''' printing result for analysis'''
    #     print(self.wt_df.mean())
    #     # print(self.wt_df.std())
        

    #     # print("Default Method: #order finished", len(self.default.wt_ls))
    #     # print("Anticipation Method: #order finished", len(self.anti.wt_ls))
    #     # print("Average Waiting Time: \n",avg_wt_default, avg_wt_anti)
        
    #     diff = self.wt_df['WT_default'].mean()-self.wt_df['WT_anticipation'].mean() # wt_default - wt_anti
    #     print("Difference in Average WT = ", diff)

    #     return [args["numOrders"], args["orderLambda"], self.wt_df['WT_default'].mean(), self.wt_df['WT_anticipation'].mean(), diff]   


    # def multipleAnalysis(self):
    #     '''Experiment with different num orders and lambda'''
    #     '''week 5 plot'''
    #     numOrders = [ 100*i for i in range(1, 11)]
    #     lams = [30]
    #     # lams = [ 10*i for i in range(1, 6)]
        
    #     dfls = []
        
    #     colorcounter = 0
    #     for l in lams:
    #         c = args["colorls"][colorcounter]
        
    #         y_d = [] # avg waiting time for default method
    #         y_a = [] # anticipation 
            
    #         for j in numOrders:
    #             args["numOrders"] = j
    #             args["numCustomers"] = j
    #             args["orderLambda"] = l
    #             self.simulateOnce()
    #             res = self.basicAnalysis()
    #             dfls.append(res)
    #             y_d.append(res[2])
    #             y_a.append(res[3])
                
    #         if args["showWTplot"]:
    #             plt.plot(numOrders, y_d, label = "Default,lambda =" + str(l), 
    #                      linestyle = 'dashed', color = c, marker = 'o')
    #             plt.plot(numOrders, y_a, label = "Anticipation, lambda =" + str(l), 
    #                      linestyle = 'solid', color = c, marker = 'o')
            
    #         colorcounter+=1
    
        
        
    #     df = pd.DataFrame(dfls, columns = ['# orders', 'lambda', 
    #                                             'avg Waiting t. - Default', 
    #                                             'avg Waiting t. - Anticipation', 
    #                                             'difference'])
    #     print(df)
        
    #     plt.title("Average Waiting Time \n number of riders = "+ str(args["numRiders"])+
    #               "\n gridsize:" + str(args["gridSize"]))
        
    #     plt.xlabel("Number of Orders")
    #     plt.ylabel("Average Waiting Time")
    #     plt.legend()
    #     plt.show()

    def multipleExperiments(self, n): # n sets of experiment 
        '''
        This fucntion will the generate n sets of data with same config to compute the 
        percentage of dropped-out rate for both orders
        '''
        for i in range(n):
            print("#############Experiment ", i, "#############")
            self.simulateOnce()
            self.findDR()
            
        df = pd.DataFrame(self.dr, columns = ["DR_anticipation", "DR_default"])
        mean = df.mean()
        std = df.std()
        max = df.max()
        min = df.min()
        df.loc['mean'] = mean
        df.loc['std'] = std
        df.loc['max'] = max
        df.loc['min'] = min
        count = (df['DR_default'] == 0).sum()
        percentage = count/len(df)

        # df.to_csv(args["path"] + "_DR_" + str(args["numOrders"])+ "orders" + 
        #         "_numRider"+str(args['numRiders'])+
        #         "_gridSize" + str(args['gridSize']) +
        #         "_FPT" + str(args["FPT_avg"])+
        #         ".csv",index=False)
        
        self.summary_stats_d.append([args["numRiders"],mean[1], std[1], max[1], min[1], percentage])
        self.dr = []
        
    
    def varyNumRiders(self):
        '''
        This function will vary the number of riders and find the average waiting time for each case
        '''
        numRiders = range(20,52,2)
        for num in numRiders:
            args["numRiders"] = num
            self.multipleExperiments(args["numExperiments"])
        
        summary_df = pd.DataFrame(self.summary_stats_d, columns = ["numRiders", "mean", "std", "max", "min", "percentage of no drop-out"])
        summary_df.to_csv(args["path"] + "summary_DR_" + str(args["numOrders"])+ "orders" + 
                "_numRider"+str(args['numRiders'])+
                "_gridSize" + str(args['gridSize']) +
                "_FPT" + str(args["FPT_avg"])+
                ".csv",index=False)

        
    def run(self):
        # self.multipleExperiments(args["numExperiments"])
        self.varyNumRiders()
        
