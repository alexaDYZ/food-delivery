

from ast import arg
import copy
from re import L
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
from DefaultMethod_1b import DefaultMethod_1b
from Simulation import Simulation
from tabulate import tabulate
from generateData import dataGeneration
import matplotlib.pyplot as plt
import time
from RunSimulation import runEpisode
from Analyse_Orders import AnalyseOrders
import datetime
import math
from visualization.Visualization import RouteVisualization, visualize_one, visualize_multiple


class AnalyseWaitingTime():
    def __init__(self) -> None:
        self.baselineMethod = DefaultMethod_1b()
        self.anticipativeMethod = AnticipationMethod()
        self.default = None
        self.anti = None
        self.avg_d = -1 # average waiting time for default method, unit = s
        self.avg_a = -1 # average waiting time for anticipation method, unit = s
        self.wt_df = None # waiting time data frame. ["wt_defauly", "wt_anticipation"], values for all orders in 1 simulation
        self.summary = []
        

    
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
        default, anti = runEpisode(self.baselineMethod, self.anticipativeMethod) # 2 simulation results
        self.default = default
        self.anti = anti
        df = pd.DataFrame(zip( self.default.wt_ls, self.anti.wt_ls), 
            columns = ['WT_default',  'WT_anticipation'])
        self.wt_df = df

        # 10.31
        # summary stats for 1 simulations -> 1 row of self.wt_df_summary
        mean_d = self.wt_df["WT_default"].mean()
        mean_a = self.wt_df["WT_anticipation"].mean()
        std_d = self.wt_df["WT_default"].std()
        std_a = self.wt_df["WT_anticipation"].std()
        max_d = self.wt_df["WT_default"].max()
        max_a = self.wt_df["WT_anticipation"].max()
        min_d = self.wt_df["WT_default"].min()
        min_a = self.wt_df["WT_anticipation"].min()
        ifbeter = 1 if mean_a < mean_d else 0
        row = [mean_a, mean_d, std_a,std_d, max_a,max_d,min_a,min_d, ifbeter]
        row = [round(i/60) for i in row]
        
        return row
        

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
                self.simulateOnce()
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

    # def multipleExperiments(self, n): # n sets of experiment 
    #     '''
    #     This fucntion will the multiple sets of data with same config to compute the 
    #     Average waiting time for each experiment
    #     '''
    #     avg_wt_d = []
    #     avg_wt_a = []
    #     diff = []
    #     for i in range(n):
    #         self.simulateOnce()
    #         avg_wt_d.append(self.wt_df["WT_default"].mean())
    #         avg_wt_a.append(self.wt_df["WT_anticipation"].mean())
    #         diff.append(self.wt_df["WT_default"].mean() - self.wt_df["WT_anticipation"].mean())
    #     ifbetter = [1 if diff[i]> 0 else 0 for i in range(len(diff)) ]
    #     df = pd.DataFrame(zip(avg_wt_d, avg_wt_a, diff, ifbetter), 
    #         columns = ['Average Waiting Time_Default(s)',  
    #                     'Average Waiting Time_Anticipation(s)',
    #                     'Difference(s)', 
    #                     'if Anticipation is better'])
    #     df.loc[-1] = [sum(df['Average Waiting Time_Default(s)'])/n, 
    #                 sum(df['Average Waiting Time_Anticipation(s)'])/n,
    #                 sum(df['Difference(s)'])/n,
    #                 round(sum(df['if Anticipation is better'])/n,2)
    #                 ]

       
    #     df.to_csv(args["path"] + "_AverageWaitingTime_" + str(args["numOrders"])+ "orders" + 
    #             "_numRider"+str(args['numRiders'])+
    #             "_gridSize" + str(args['gridSize']) +
    #             "_FPT" + str(args["FPT_avg"])+
    #             ".csv",index=False)

    def multipleSims(self, n): # n sets of simulations 
        '''
        Multiple(n) simulations conducted for the same set of parameters
        '''
        exp_stats=[]
        
        for i in range(n):
            print("numRiders: ", args["numRiders"], "----Simulation", i)
            
            sim_result = self.simulateOnce()
            self.cumulative_moving_average_analysis()
            exp_stats.append(sim_result)
            
        
        df = pd.DataFrame(exp_stats, columns = ['mean_a', 'mean_d', 'std_a','std_d', 'max_a','max_d','min_a','min_d', 'ifbetter'])
        
        exp_summary = [args["numRiders"], 
                    df["mean_a"].mean(), df["mean_d"].mean(),
                    df["std_a"].mean(), df["std_d"].mean(),
                    df["max_a"].mean(), df["max_d"].mean(),
                    df["min_a"].mean(), df["min_d"].mean(),
                    round(df["ifbetter"].sum()/len(df["ifbetter"]),3)
                    ]

        self.summary.append(exp_summary)


    # input: simulation result dataframe with columns: "WT_default", "WT_anticipation"
    # output: plot of cumulative moving average of waiting time
    def cumulative_moving_average_analysis(self, wt_df):

        '''This function compute and plot the moving average of the waiting time'''
        
        if args["showCMA_wait_time"]:
            df = wt_df

            # get cumulative average till t for every 'MA_batchsize = 10' number of orders
            
            # helper function
            def getAverage(waitingTimeLs):
                avgLs = []
                for i in range(len(waitingTimeLs)):
                    curr_avg = sum(waitingTimeLs[:i+1]) / (i+1) / 60 # convert to minutes
                    avgLs.append(curr_avg)
                return avgLs
            
            d_avg = getAverage(list(df["WT_default"]))
            a_avg = getAverage(list(df["WT_anticipation"]))

            # plot
            # plt.plot(df["WT_default"], '-', color = 'blue', label='Waiting Time (Default)', linewidth = 0.2)
            # plt.plot(df["WT_anticipation"], '-', color = 'orange', label='Waiting Time (Anticipation)', linewidth = 0.2)
            plt.plot(d_avg, ':', color = 'blue', label='Average (Default)', linewidth = 2)
            plt.plot(a_avg, ':', color = 'orange',label='Average (Anticipation)', linewidth = 2)
            plt.ylim(0, 100)
            plt.title('Waiting Time Plot\n avg_d = '+ 
                        str(d_avg[-1])+" \n avg_a = "+ 
                        str(a_avg[-1]) + "diff = " + str(d_avg[-1] - a_avg[-1])
                        )
            plt.xlabel('Number of Orders')
            plt.ylabel('Waiting Time/s')
            plt.legend()
            

            plt.savefig(args["path"] + str(datetime.datetime.now())+ "_WaitingTimePlot"+
                "_numOrders" + str(args["numOrders"]) + 
                "_lambda" + str(args["orderLambda"]) +
                "_numRider"+str(args['numRiders'])+
                "_gridSize" + str(args['gridSize']) + 
                "_FPT" + str(args["FPT_avg"])+".svg", format='svg', dpi=2000)
            plt.clf()
            # plt.show()
        else: pass

    
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
                    + "_FPT" + str(args["FPT_avg"])+
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
        
        plt.savefig(args["path"]+ 
            "delivered_time" + 
            "_numOrders" + str(args["numOrders"]) + 
            "_lambda" + str(args["orderLambda"]) +
            "_numRider"+str(args['numRiders'])+
            "_gridSize" + str(args['gridSize']) + 
            "_FPT" + str(args["FPT_avg"])+
            ".svg", format='svg', dpi=2000)
        plt.show()
        
    def printOrderHistory(self):
        a = AnalyseOrders(self.default, self.anti) # pass in the result for 1 simulation object each
        a.printHistory()

    def findOptimalAverageWaitingTime(self,order_list):
        '''
        This function finds the LOWER BOUND of the optimal average waiting time for the default and anticipation
        '''
        minWaitingTimeLs = [] # min waiting time = distance(customer, restaurant)/speed
        for o in order_list:
            minWaitingTime = math.dist(o.cust.loc, o.rest.loc)/args["riderSpeed"]
            minWaitingTimeLs.append(minWaitingTime)
        return sum(minWaitingTimeLs)/len(minWaitingTimeLs)
    
    def multipleExperimentOnCompetitiveRatio(self):
        '''
        This function runs multiple experiments to find the competitive ratio of the anticipation algorithm
        '''
        numExperiment = args["numExperiments"]
        df_ls = []
        for i in range(numExperiment):
            print("Experiment", i)
            self.simulateOnce() # run the simulation once
            minAverageWaitingTime = self.findOptimalAverageWaitingTime(self.anti.order_list)
            competitiveRatio_anti = round(self.wt_df['WT_anticipation'].mean() / minAverageWaitingTime , 3)
            competitiveRatio_default = round(self.wt_df['WT_default'].mean() / minAverageWaitingTime , 3)

            # maxCR_anti = round(self.wt_df['WT_anticipation'].max() / minAverageWaitingTime , 3)
            # maxCR_default= round(self.wt_df['WT_default'].max() / minAverageWaitingTime , 3)

            row = [minAverageWaitingTime, 
                    self.wt_df['WT_anticipation'].mean(), self.wt_df['WT_default'].mean(), 
                    competitiveRatio_anti, competitiveRatio_default]
            df_ls.append(row)
        df = pd.DataFrame(df_ls, columns = ['WT_minimum', 
                                            'AverageWT_anticipation', 'AverageWT_default',
                                            'Ratio_anti', 'Ratio_default'])
        if args['saveCRhistory']:
            df.to_csv(args["path"] + "CR" + str(datetime.datetime.now())+
                    "Riders" + str(args["numRiders"]) +
                    "FPT" + str(args["FPT_avg"]) + ".csv")
        # return round(df['Ratio_anti'].mean(),5), round(df['Ratio_default'].mean(),5)
        return competitiveRatio_anti, competitiveRatio_default
    
    def varyNumRiders(self):
        '''
        This function runs multiple experiments to find the competitive ratio of the anticipation algorithm
        '''
        numExperiment = args["numExperiments"]
        numRiders = range(20,62, 2)
        # numRiders = range(50,51)
        
        for n in numRiders:
            print("numRiders", n)
            args["numRiders"] = n
            self.wt_df = []
            self.multipleSims(numExperiment)
        
        df = pd.DataFrame(self.summary, columns =  ['numRiders', 'mean_a', 'mean_d', 'std_a', 'std_d', 'max_a', 'max_d', 'min_a', 'min_d', 'percentage better'] )
        
       
        df.to_csv(args["path"] + "summary_WT_" + str(args["numOrders"])+ "orders" + 
                "_numRider"+str(args['numRiders'])+
                "_gridSize" + str(args['gridSize']) +
                "_FPT" + str(args["FPT_avg"])+
                str(datetime.datetime.now())+
                ".csv",index=False)

    def run(self):
        self.varyNumRiders()
        # if args["showWTplot"]: 
        #     self.multipleAnalysis()
        # if args["doMultipleExperiments"]:
        #     self.multipleExperiments(args["numRepeat"])
        # if args["findCompetitiveRatio"]:
        #     ratio_anti_ls = []
        #     ratio_default_ls = []
        #     for i in range(20, 80, 5): 
        #         args["numRiders"] = i
        #         ratio_anti, ratio_default = self.multipleExperimentOnCompetitiveRatio()
        #         ratio_anti_ls.append(ratio_anti)
        #         ratio_default_ls.append(ratio_default)
        #     x = [i for i in range(20, 80, 5)]
        #     y1 = ratio_default_ls
        #     y2 = ratio_anti_ls
        #     plt.plot(x, y1)
        #     plt.plot(x, y2)
        #     plt.legend(["default", "anticipation"])
        #     plt.title("Competitive Ratio vs Number of Riders")
        #     plt.savefig(args["path"] + "CRvsRiders" + "FPT"+ str(args["FPT_avg"])+ "_2.svg", format='svg', dpi=2000)


        # self.simulateOnce()
        # self.basicAnalysis()

        # if args["showEventPlot"]:
        #     # analysis.showEventPlot()
        #     self.plotBFL()
        # if args["showCMA_wait_time"]: 
        #     self.AverageAnalysis()

        # if args["saveAssignmentHistory"]:
        #     self.printOrderHistorr()



# For visualization of routes

    def visualizeRoute(self):
        self.simulateOnce()
        for r in self.anti.rider_list:
            if r.orderDict:
                visualize_one(r, title="Route of Rider " + str(r.index) + " with "+ str(len(r.orderDict))+ " orders")


    def visualizeMaxMin(self):
        '''
        This function visualize specifically, the route of 2 riders:
        rider who delivered the most orders, and who delivered the least.
        '''
        self.simulateOnce()
        # get location list
        
        max = 0
        max_r = None
        min = np.Infinity
        min_r = None
        for r in self.anti.rider_list:
            if r.orderDict:
                if len(r.orderDict) > max:
                    max_r = r
                    max = len(r.orderDict)
                    print("max", max_r.index)

                if len(r.orderDict) < min:
                    min_r = r
                    min = len(r.orderDict)
                    print("min", min_r.index)
        print("max", max_r)
        print("min", min_r)
       
        fig = visualize_multiple([max_r, min_r])

        


             






    
    
