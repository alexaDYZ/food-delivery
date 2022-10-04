
from audioop import avg
from cProfile import label
import copy
from ctypes.wintypes import PINT
from glob import escape
from tkinter.tix import COLUMN
from turtle import color
from typing import Tuple
import numpy as np
from torch import lt
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
import datetime
import os


class AnalyseWaitingTime():
    def __init__(self) -> None:
        self.default = None
        self.anti = None
        self.avg_d = -1 # average waiting time for default method, unit = s
        self.avg_a = -1 # average waiting time for anticipation method, unit = s
        self.wt_df = None # waiting time data frame. ["wt_defauly", "wt_anticipation"]

    
    def analyseOnce(self):
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
        self.default = default
        self.anti = anti
        df = pd.DataFrame(zip( self.default.wt_ls, self.anti.wt_ls), 
            columns = ['WT_default',  'WT_anticipation'])
        self.wt_df = df


    
    def basicAnalysis(self):
        ''' printing result for analysis'''
        print(self.wt_df.mean())
        print(self.wt_df.std())
        

        # print("Default Method: #order finished", len(self.default.wt_ls))
        # print("Anticipation Method: #order finished", len(self.anti.wt_ls))
        # print("Average Waiting Time: \n",avg_wt_default, avg_wt_anti)
        
        diff = self.wt_df['WT_default'].mean()-self.wt_df['WT_anticipation'].mean() # wt_default - wt_anti
        print(diff)

        return [args["numOrders"], args["orderLambda"], self.wt_df['WT_default'].mean(), self.wt_df['WT_anticipation'].mean(), diff]   


    def multipleAnalysis(self):
        '''Experiment with different num orders and lambda'''
        '''week 5 plot'''
        numOrders = [ 100*i for i in range(1, 11)]
        lams = [30]
        # lams = [ 10*i for i in range(1, 6)]
        
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
                self.analyseOnce()
                res = self.basicAnalysis()
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

    def multipleExperiments(self, n): # n sets of experiment 
        '''
        This fucntion will the multiple sets of data with same config to compute the 
        Average waiting time for each experiment
        '''
        avg_wt_d = []
        avg_wt_a = []
        diff = []
        for i in range(n):
            self.analyseOnce()
            avg_wt_d.append(self.wt_df["WT_default"].mean())
            avg_wt_a.append(self.wt_df["WT_anticipation"].mean())
            diff.append(self.wt_df["WT_default"].mean() - self.wt_df["WT_anticipation"].mean())
        ifbetter = [1 if diff[i]> 0 else 0 for i in range(len(diff)) ]
        df = pd.DataFrame(zip(avg_wt_d, avg_wt_a, diff, ifbetter), 
            columns = ['Average Waiting Time_Default(s)',  
                        'Average Waiting Time_Anticipation(s)',
                        'Difference(s)', 
                        'if Anticipation is better'])
        df.loc[-1] = [sum(df['Average Waiting Time_Default(s)'])/n, 
                    sum(df['Average Waiting Time_Anticipation(s)'])/n,
                    sum(df['Difference(s)'])/n,
                    round(sum(df['if Anticipation is better'])/n,2)
                    ]

        path = os.path.join("./week8/", str(datetime.datetime.now())) 
        os.mkdir(path)
        df.to_csv(path + "_AverageWaitingTime_" + str(args["numOrders"])+ "orders" + 
                "_numRider"+str(args['numRiders'])+
                "_gridSize" + str(args['gridSize']) +
                ".csv",index=False)
        


    def AverageAnalysis(self):
        '''This function compute and plot the moving average of the waiting time'''

        df = self.wt_df
        
        '''Average Plot'''

        # get average till t for every 'MA_batchsize' number of orders
        
        # helper function
        def getAverage(waitingTimeLs):
            avgLs = []
            for i in range(len(waitingTimeLs)):
                curr_avg = sum(waitingTimeLs[:i+1]) / (i+1)
                avgLs.append(curr_avg)
            return avgLs
        
        d_avg = getAverage(list(df["WT_default"]))
        a_avg = getAverage(list(df["WT_anticipation"]))

        # plot
        # plt.plot(df["WT_default"], '-', color = 'blue', label='Waiting Time (Default)', linewidth = 0.2)
        # plt.plot(df["WT_anticipation"], '-', color = 'orange', label='Waiting Time (Anticipation)', linewidth = 0.2)
        plt.plot(d_avg, ':', color = 'blue', label='Average (Default)', linewidth = 2)
        plt.plot(a_avg, ':', color = 'orange',label='Average (Anticipation)', linewidth = 2)
        plt.title('Waiting Time Plot\n avg_d = '+ 
                    str(d_avg[-1])+" \n avg_a = "+ 
                    str(a_avg[-1]) +"diff = " + str(d_avg[-1] - a_avg[-1]))
        plt.xlabel('Number of Orders')
        plt.ylabel('Waiting Time/s')
        plt.legend()
        

        plt.savefig("./post_intro_talk/"+str(datetime.datetime.now())+ "_WaitingTimePlot"+
            "_numOrders" + str(args["numOrders"]) + 
            "_lambda" + str(args["orderLambda"]) +
            "_numRider"+str(args['numRiders'])+
            "_gridSize" + str(args['gridSize']) + 
            ".svg", format='svg', dpi=2000)
        plt.show()


    def showEventPlot(self):
        
        delivered_time_d = [(o.t, o.t_delivered) for o in self.default.order_list]
        delivered_time_a = [(o.t, o.t_delivered) for o in self.anti.order_list]
        plt.eventplot(delivered_time_d,linelengths = 1, 
                        colors=['C{}'.format(1) for i in range(len(delivered_time_d))],
                        label='Default',
                        )   
        plt.eventplot(delivered_time_a,linelengths = 1, 
                        colors=['C{}'.format(2) for i in range(len(delivered_time_a))],
                        label='Anticipation',
                        ) 
        plt.legend()           
        plt.ylabel("OrderNumber")
        plt.xlabel("Time")
        plt.title("Events acorss time \n #Orders" + str(args["numOrders"]) +
                    "  #Riders:" + str(args["numRiders"]) +
                    "  Gridsize:" + str(args["gridSize"]) +
                    "  lambda:" + str(args["orderLambda"]), fontsize = 10)
        plt.savefig("./week6/EventPlot"+"numRider"+str(args['numRiders'])
                    +"grid"+ str(args['gridSize'])
                    +"lambda" + str(args['orderLambda'])
                    +".svg", format='svg', dpi=2000)
        plt.show()

    def plotBFL(self): 
        
        '''
        This function plots a graph to analyse order delivered time
        x-axis: order comes in time
        y-axis: order delivered time
        '''
        
        scatter = False
        #find line of best fit
        o_index = np.array([o.index for o in self.default.order_list])
        t_in = np.array([o.t for o in self.default.order_list])
        t_d = np.array([o.t_delivered for o in self.default.order_list])
        t_a = np.array([o.t_delivered for o in self.anti.order_list])
        
        

        
        # if scatter: 
        #     plt.plot(t_in, t_d, label = "default", linestyle="-.")
        #     plt.plot(t_in, t_a, label = "anticipation", linestyle=":")

        plt.plot(o_index, t_in, label = "Time In", color='limegreen', linestyle='solid', linewidth=1)
        plt.plot(o_index, t_d, label =  "Time Delivered - Default" , color='royalblue', linestyle='dashed', linewidth=1)
        plt.plot(o_index, t_a, label = "Time Delivered - Anticipation", color='orange', linestyle='dotted', linewidth=1)

        a1, b1 = np.polyfit(o_index, t_d, 1)
        a2, b2 = np.polyfit(o_index, t_a, 1)
        plt.plot(o_index, a1 * o_index + b1, color='midnightblue', linestyle='dashed', linewidth=0.5, label = "best fit line for default")
        plt.plot(o_index, a2 * o_index + b2, color='red', linestyle='dotted', linewidth=0.5, label = "best fit line for anticipation")
        plt.xlabel("Order Index")
        plt.ylabel("Order Delivered Time")
        plt.legend()
        plt.title("numRider"+str(args['numRiders'])+"\n grid"+ str(args['gridSize']))
        # plt.savefig("./week6/"+
        #             "_time" + str(args["totalTime"]) +
        #             "_numRider"+str(args['numRiders'])+
        #             "_grid"+ str(args['gridSize'])+
        #             "delivered_time" +      ".svg", format='svg', dpi=2000)
        
        plt.savefig("./week8/"+ 
            "delivered_time" + 
            "_numOrders" + str(args["numOrders"]) + 
            "_lambda" + str(args["orderLambda"]) +
            "_numRider"+str(args['numRiders'])+
            "_gridSize" + str(args['gridSize']) + 
            ".svg", format='svg', dpi=2000)
        plt.show()
        



analysis = AnalyseWaitingTime()

if args["showWTplot"]: 
    analysis.multipleAnalysis()
elif args["doMultipleExperiments"]:
    analysis.multipleExperiments(args["numEpisode"])
else:
    analysis.analyseOnce()
    analysis.basicAnalysis()

    if args["showEventPlot"]:
        # analysis.showEventPlot()
        analysis.plotBFL()
    if args["showAvgWT"]: 
        analysis.AverageAnalysis()


    
    
