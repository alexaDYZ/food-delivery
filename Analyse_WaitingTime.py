
from cProfile import label
import copy
from ctypes.wintypes import PINT
from glob import escape
from tkinter.tix import COLUMN
from turtle import color
from typing import Tuple
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


class AnalyseWaitingTime():
    def __init__(self) -> None:
        self.default = None
        self.anti = None
    
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
    
    def basicAnalysis(self):
        ''' printing result for analysis'''
        # get avg waiting time per order
        def compute_avg(ls):
            if ls:
                return sum(ls)/len(ls)
            else:
                print("empty list")
        
        avg_wt_default = compute_avg(self.default.wt_ls)
        avg_wt_anti = compute_avg(self.anti.wt_ls)

        print("Default Method: #order finished", len(self.default.wt_ls))
        print("Anticipation Method: #order finished", len(self.anti.wt_ls))
        print("Average Waiting Time: \n",avg_wt_default, avg_wt_anti)
        diff = avg_wt_default-avg_wt_anti
        print(diff)

        return [args["numOrders"], args["orderLambda"], avg_wt_default, avg_wt_anti, diff]   

    def multipleAnalysis(self):
        '''Experiment with different num orders and lambda'''
        numOrders = [ 10*i for i in range(30, 50)]
        lams = [1]
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

    def movingAverageAnalysis(self):
        '''This function compute and plot the moving average of the waiting time'''
        # get waiting time
        order_in_time_d = [o.t for o in self.default.order_list]
        order_in_time_a = [o.t for o in self.anti.order_list]
        wt_d = [o.wt for o in self.default.order_list]
        wt_a = [o.wt for o in self.anti.order_list]

        df = pd.DataFrame(zip(order_in_time_d, wt_d, order_in_time_a, wt_a), 
            columns = [ "time ",'WT_default', 'time', 'WT_anticipation'])
        '''Moving Average Plot'''

        # get moving average for every 'MA_batchsize' number of orders
        d_avg  = df["WT_default"].rolling(window=args['MA_batchsize']).mean()
        a_avg  = df["WT_anticipation"].rolling(window=args['MA_batchsize']).mean()

        # plot
        fig, axs = plt.subplots(2, figsize=(15, 7.5))
        fig.suptitle('Waiting Time')
        axs[0].plot(df["WT_default"], 'k-', label='Original')
        axs[0].plot(d_avg, 'r-', label='Running average')
        axs[0].grid(linestyle=':')
        # plt.fill_between(t_average.index, 0, t_average, color='r', alpha=0.1)
        axs[0].set_title('Default')
        axs[0].legend(loc='upper left')

        axs[1].plot(df["WT_anticipation"], 'k-', label='Original')
        axs[1].plot(a_avg, 'r-', label='Running average')

        axs[1].grid(linestyle=':')
        # plt.fill_between(t_average.index, 0, t_average, color='r', alpha=0.1)
        axs[1].legend(loc='upper left')

        for ax in axs.flat:
            ax.set(xlabel='Number of Orders', ylabel='Waiting Time')
            
        # plt.savefig("./week6/"+
        #             "_time" + str(args["totalTime"]) +
        #             "_numRider"+str(args['numRiders'])+
        #             "_grid"+ str(args['gridSize'])+
        #             "WaitingTime" + 
        #             ".svg", format='svg', dpi=2000)
        plt.savefig("./week6/"+
            "time" + str(args["totalTime"]) + 
            "_lambda" + str(args["orderLambda"]) +
            "_numRider"+str(args['numRiders'])+
            "WaitingTime" + 
            ".svg", format='svg', dpi=2000)
        plt.show()




    def showEventPlot(self):
        
        delivered_time_d = [(o.t, o.t_delivered) for o in self.default.order_list]
        delivered_time_a = [(o.t, o.t_delivered) for o in self.anti.order_list]
        # plt.eventplot(events_d,linelengths = 1, 
        #                 colors=['C{}'.format(i) for i in range(len(events_d))],
        #                 )
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
        #             "delivered_time" + 
        #             ".svg", format='svg', dpi=2000)
        plt.savefig("./week6/"+
            "time" + str(args["totalTime"]) + 
            "_lambda" + str(args["orderLambda"]) +
            "_numRider"+str(args['numRiders'])+
            "delivered_time" + 
            ".svg", format='svg', dpi=2000)
        plt.show()
        



analysis = AnalyseWaitingTime()

if args["showWTplot"]: 
    analysis.multipleAnalysis()
else:
    analysis.analyseOnce()
    analysis.basicAnalysis()

    if args["showEventPlot"]:
        # analysis.showEventPlot()
        analysis.plotBFL()

    if args["movingAvegrageAnalysis"]: 
        analysis.movingAverageAnalysis()

    
    
