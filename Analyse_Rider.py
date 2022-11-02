
from ast import arg
from audioop import avg
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
from visualization.Visualization import RouteVisualization
from visualization.Visualization import visualize_multiple, visualizeMaxMin

class Analyse_Rider():

    def __init__(self) -> None:
        self.baselineMethod = DefaultMethod_1a()
        self.anticipativeMethod = AnticipationMethod()
        self.default = None
        self.anti = None
        self.stats_d = [] # consisting of many lists. Each is [fr_a, fr_d] for 1 simulation
        self.stats_a = []
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

    def get_num_delivered_per_rider(self):
        '''
        This function returns the number of orders delivered by each rider
        '''
        
        # baseline method
        ls_d = [self.default.rider_list[i].totalOrderDelivered for i in range(args["numRiders"])]
        stats_d = [np.mean(ls_d), np.std(ls_d), np.max(ls_d), np.min(ls_d)]
        self.stats_d.append(stats_d)
        # anticipative method
        ls_a = [self.anti.rider_list[i].totalOrderDelivered for i in range(args["numRiders"])]
        stats_a = [np.mean(ls_a), np.std(ls_a), np.max(ls_a), np.min(ls_a)]
        self.stats_a.append(stats_a)
        
        visualizeMaxMin(self.anti.rider_list)

        
        

    def multipleExperiments(self, n): # n sets of experiment 
        '''
        This fucntion will the generate n sets of data with same config to compute the 
        percentage of dropped-out rate for both orders
        '''
        for i in range(n):
            print("#############Experiment ", i, "#############")
            self.simulateOnce()
            self.get_num_delivered_per_rider()
            
        df_a = pd.DataFrame(self.stats_a, columns = ["mean", "std", "max", "min"])
        df_d = pd.DataFrame(self.stats_d, columns = ["mean", "std", "max", "min"])


        df_a.to_csv(args["path"] + "Anti_numDelivered_" + str(args["numOrders"])+ "orders" + 
                "_numRider"+str(args['numRiders'])+
                "_gridSize" + str(args['gridSize']) +
                "_FPT" + str(args["FPT_avg"])+
                ".csv",index=False)
        df_d.to_csv(args["path"] + "Default_numDelivered_" + str(args["numOrders"])+ "orders" + 
                "_numRider"+str(args['numRiders'])+
                "_gridSize" + str(args['gridSize']) +
                "_FPT" + str(args["FPT_avg"])+
                ".csv",index=False)

    def run(self):
        self.multipleExperiments(args["numExperiments"])
    # def AnalyseRider():
        
    #     start_time = time.time()

    #     dataGeneration()
    #     simulation_default,simulation_anti = runEpisode() # 2 dictionaries
    #     res_default,res_anti = simulation_default.rider_status_check_dict, simulation_anti.rider_status_check_dict
    #     # averaging: omitted
            
    #     '''
    #     generate big dict:
    #         key -> time interval
    #         value -> [ratio_default, ratio_anti]
    #     '''

    #     ''' individual plot  '''
    #     x_axis_d = list(res_default.keys())
    #     x_axis_a = list(res_anti.keys())
    #     y_d = list(res_default.values())
    #     y_a =list(res_anti.values())

    #     plt.plot(x_axis_d,y_d, '--', label = "Default")
    #     plt.plot(x_axis_a, y_a,':',label = "Anticipation")
        
    #     # plt.axhline(y=np.nanmean(y_1), color='C0', label = "mean="+str(round(np.nanmean(y_1),3)))
    #     # plt.axhline(y=np.nanmean(y_2), color= 'C1', label = "mean="+str(round(np.nanmean(y_2),3)))
        
    #     plt.legend()
    #     title = "Percentage of Riders Occupied\nlambda :" + str(args["orderLambda"])+"\n#Orders per period:"+ str(args["numOrders"]) +"\n NUmber of Riders:" + str(args["numRiders"])
    #     subtitle = 'Difference in mean='+str(round(abs(np.nanmean(y_d)-np.nanmean(y_a)),3))
    #     plt.title(title+"\n"+subtitle)
        
        
    #     markPoint = False
    #     # if markPoint:
            
    #     #     for x,y in zip(x_axis,y_1):

    #     #         label = "{:.2f}".format(y)

    #     #         plt.annotate(label, # this is the text
    #     #                     (x,y), # these are the coordinates to position the label
    #     #                     textcoords="offset points", # how to position the text
    #     #                     xytext=(0,10), # distance from text to points (x,y)
    #     #                     ha='center')
            
    #     #     for x,y in zip(x_axis,y_2):

    #     #         label = "{:.2f}".format(y)

    #     #         plt.annotate(label, # this is the text
    #     #                     (x,y), # these are the coordinates to position the label
    #     #                     textcoords="offset points", # how to position the text
    #     #                     xytext=(0,10), # distance from text to points (x,y)
    #     #                     ha='center')
    
        
        
    #     plt.savefig(args["path"]+str(datetime.datetime.now())+ "_RiderOccupancyRate"+
    #             "_numOrders" + str(args["numOrders"]) + 
    #             "_lambda" + str(args["orderLambda"]) +
    #             "_numRider"+str(args['numRiders'])+
    #             "_gridSize" + str(args['gridSize']) + 
    #             ".svg", format='svg', dpi=2000)


    #     '''average percentage plot '''
        
    #     # numOrders =  [10,20,30,40,50,60,70,80] # x-axis
    #     # diff_list = [] # y-axis
        
    #     # for num in numOrders:
    #     #     args["numOrders"] = num
    #     #     args["numCustomers"] = num
            
    #     #     repeat = 30
    #     #     ls = []
    #     #     for i in range(repeat):
    #     #         dataGeneration()
                
    #     #         res_default,res_anti = runEpisode() # 2 dictionaries
    #     #         default = list(res_default.values())
    #     #         anti = list(res_anti.values())
    #     #         diff = np.nanmean(default) - np.nanmean(anti)
    #     #         ls.append(diff)
    #     #     avg_diff = sum(ls)/len(ls)
    #     #     diff_list.append(avg_diff)
    #     # print(diff_list)
    #     # plt.plot(numOrders,diff_list, '--', label = "Difference in mean")
    #     # plt.xlabel("number of orders / period ")
    #     # plt.ylabel("difference in mean ratio: default - anticipation ")
    #     # plt.axhline(y=0, color='black')
    #     # plt.show()
        
        
        
    #     print("total time taken:", time.time() - start_time)
        

