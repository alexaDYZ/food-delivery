import numpy as np
from AnticipationMethod import AnticipationMethod
from DefaultMethod_1b import DefaultMethod_1b
from Order import Order
from Restaurant import Restaurant
from Customer import Customer
from Rider import Rider
from config import args
import pickle
import pandas as pd
import math


from Simulation import Simulation
from generateData import dataGeneration
import matplotlib.pyplot as plt
import time
import datetime
from RunSimulation import runEpisode, runEpisode_single_medthod
from ClosestToFPTMethod import ClosestToFPTMethod
from DefaultMethod_1b import DefaultMethod_1b
from PatientAnticipativeMethod_Bulk import PatientAnticipativeMethod_Bulk
from  AnticipationMethod import AnticipationMethod
from UsefulWorkMethod import UsefulWorkMethod
from AssignLaterMethod import AssignLaterMethod, AssignLaterMethod_UsefulWork  



class WaitingTimePLot():
    methods = {
        "DefaultMethod_1b": DefaultMethod_1b(),
        "AnticipationMethod": AnticipationMethod(),
        "ClosestToFPTMethod": ClosestToFPTMethod(),
        "PatientAnticipativeMethod_Bulk": PatientAnticipativeMethod_Bulk(),
        "UsefulWorkMethod": UsefulWorkMethod(),
        "AssignLaterMethod": AssignLaterMethod(),
        "AssignLaterMethod_UsefulWork": AssignLaterMethod_UsefulWork(),
    }
    method_colors = {
        "DefaultMethod_1b":  ["red", "lightcoral", "pink", "pink", "pink"],
        "AnticipationMethod": ["cornflowerblue", "royalblue", "lightblue", "lightblue", "lightblue"],
        "ClosestToFPTMethod": ["green", "mediumseagreen", "lightgreen", "lightgreen", "lightgreen"],
        "PatientAnticipativeMethod_Bulk": ["sandybrown", "orange", "bisque", "bisque", "bisque"],
        "UsefulWorkMethod": ["yellow", "gold",  "lightyellow", "lightyellow", "lightyellow"],
        "AssignLaterMethod": ["purple", "mediumpurple", "thistle", "thistle", "thistle"],
        "Optimal": ["black", "grey", "grey", "grey", "grey"],
        "AssignLaterMethod_UsefulWork":["pink", "hotpink", "lightpink", "lightpink", "lightpink"],
    }
    
    def __init__(self) -> None:
        self.methods = []

    # to add all methods
    def add_all_methods(self):
        self.methods = list(WaitingTimePLot.methods.values())
    
    # to add a single method
    def add_method(self, method_name):
        m = WaitingTimePLot.methods[method_name]
        self.methods.append(m)
    
    def simulateOnce_all_methods(self):
        '''
        This function performs 1 simulation using each method in self.methods.
        Same set of synthetic data is used for all methods.
        
        Output: 'simulation' class objects, with simulation results. 
                refer to Simulation.py for more details
        '''
        dataGeneration() # generate initial data
        sim_res_dict = {}
        for m in self.methods:
            sim = runEpisode_single_medthod(m)
            sim_res_dict[m.name] = sim
        return sim_res_dict

    def get_ia_df(self):
        '''
        input
        =====
        sim_res_dict: dict, key = method name, value = simulation object
        m_name: str, method name
        
        output:
        =======
        df: get data ready to plot interval average distribution by time
        Note: intervals are non-overlapping, with a time window of "IA_interval"
        '''
        def get_theoretical_best_wt_per_order(o:Order):
            # get theoretical best waiting time for each order
            # best_wt = FPT + DT
            
            FPT = o.rest.order_FPT_dict[o.index]
            fastest_DT = math.dist(o.cust.loc, o.rest.loc)/args["riderSpeed"]

            best_wt = FPT + fastest_DT
            return round(best_wt, 2)

        def get_order_df_from_sim_res(sim:Simulation):
            orders = sim.order_list
            df_2dlist = []
            for o in orders:
                row = []
                # 1. Order Index
                row.append(o.index)
                # 2. "Order-in Time"
                row.append(o.t)
                # 3. Rider Index
                row.append(o.rider.index)
                # 4. "Rider Arrives at Restaurant"
                row.append(o.t_riderReachedRestaurant)
                # 5. "Order Delivered Time"
                row.append(o.t_delivered)
                # 6. "Waiting Time"
                row.append(o.wt)
                

                # 7. "DT"
                if args["FPT_avg"] > args["gridSize"]:
                    # when FPT is extremely largs, WT = max(FPT, R2R) + DT = FPT + DT
                    row.append(o.t_delivered - o.t  - args["FPT_avg"])
                elif args["FPT_avg"] == 0:
                    # when FPT is negligible, WT = R2R + DT
                    row.append(o.t_delivered - o.t_riderReachedRestaurant) 
                else:
                    row.append(None)
                # 8. "Time taken before delivery"
                row.append(o.wt - row[6] if row[6] else None)
                # 9. "Theoretical Best WT"
                optimal_wt = get_theoretical_best_wt_per_order(o)
                row.append(optimal_wt)
                # 10. "WT regret"
                regret_wt = o.wt - optimal_wt
                row.append(regret_wt)

                df_2dlist.append(row)
            df = pd.DataFrame(df_2dlist, columns=["Order Index", "Order-in Time", 
                                                "Rider Index", "Rider Arrives at Restaurant",
                                                "Order Delivered Time", "Waiting Time", 
                                                "DT", "Time taken before delivery", "Theoretical Best WT", "WT regret"])
            # df.to_csv("df_"+ sim.method.name+".csv")
            return df           

        def compute_ia_from_df(df):
            # arrange all orders by "Order-in Time"
            df = df.sort_values(by = "Order-in Time")
            # get time of the last delivered order
            t_end = args["simulationTime"]
            # assign each order to an interval number
            interval = args["IA_interval"]
            df['interval_number'] = df["Order-in Time"] // interval + 1
            N = int(t_end // args["IA_interval"] + 1) # number of intervals
            print("N = ", N)
            
            # compute average waiting time for each interval to 2 decimal places
            wt_ia = list( df.groupby("interval_number")["Waiting Time"].mean())
            wt_ia = [round(i, 2) for i in wt_ia]
            # wt_ia.pop()# last interval is not complete, so remove it

            optimal_ia = list( df.groupby("interval_number")["Theoretical Best WT"].mean())
            optimal_ia = [round(i, 2) for i in optimal_ia]
            # optimal_ia.pop()# last interval is not complete, so remove it

            regret_ia = list( df.groupby("interval_number")["WT regret"].mean())
            regret_ia = [round(i, 2) for i in regret_ia]
            # regret_ia.pop()# last interval is not complete, so remove it
            return wt_ia, optimal_ia, regret_ia


        
        # initiate a dict to store results
        m_names = [m.name for m in self.methods]
        
        wt_ia_dict = {} # ket = method name, value = list of df, each df is from 1 simulation 
        regret_ia_dict = {}
        for m_name in m_names:
            wt_ia_dict[m_name] = []
            regret_ia_dict[m_name] = []
        if self.add_optimal_wt: wt_ia_dict["Optimal"] = []


        # ==  start multiple simulations ==
        for i in range(args["numSimulations"]):
            # === for each simulation, get the results for all method === 
            print("Simulation ", i, )
            sim_res_dict = self.simulateOnce_all_methods()
            
            # for each methods, get the interval average
            for m_name, sim_res in sim_res_dict.items():
                df = get_order_df_from_sim_res(sim_res)
                wt_ia, optimal_ia, regret_ia = compute_ia_from_df(df)

                wt_ia_dict[m_name].append(wt_ia)
                if self.plot_regret:
                    regret_ia_dict[m_name].append(regret_ia)
                print("✅ Method ", m_name, " done")
            
            # add theoretical optimal 
            if self.add_optimal_wt:
                wt_ia_dict["Optimal"].append(optimal_ia)
                

            
            # == end of 1 simulation ==

        # == end of multiple simulations ==

        wt_ia_dict_res = {}
        for m_name, ia_ls in wt_ia_dict.items(): 
            max_num_intervals = max([len(i) for i in ia_ls]) # find the max number of intervals in all simulations
            col_names = [str(i*args["IA_interval"]) for i in range(1, max_num_intervals+1)] # column names are order index
            df = pd.DataFrame(ia_ls, columns = col_names)
            wt_ia_dict_res[m_name] = df
        
        regret_ia_dict_res = {}
        for m_name, ia_ls in regret_ia_dict.items():
            max_num_intervals = max([len(i) for i in ia_ls]) # find the max number of intervals in all simulations
            col_names = [str(i*args["IA_interval"]) for i in range(1, max_num_intervals+1)] # column names are order index
            df = pd.DataFrame(ia_ls, columns = col_names)
            regret_ia_dict_res[m_name] = df
        
        
        return wt_ia_dict_res, regret_ia_dict_res

    def plot_wt_ia(self,ia_dict):
        '''
        Plot interval average distribution by time
        Note: intervals are non-overlapping, with a time window of "IA_interval"
        '''

        def compute_stats(df):
            mean, median, uq, lq = [],[],[],[]
            for col in df:                
                mean.append(df[col].mean(skipna=True))
                median.append(df[col].median(skipna=True))
                uq.append(df[col].quantile(0.75))
                lq.append(df[col].quantile(0.25))
            for stat in [mean, median, uq, lq]:
                stat = [round(i/60, 2) for i in stat] # convert to minutes, to 2 decimal places
            return mean, median, uq, lq

        def plot(df, method_name):
            method_color = WaitingTimePLot.method_colors[method_name]
            median_color, mean_color, uq_color, lq_color, shade_color = method_color[0], method_color[1], method_color[2], method_color[3], method_color[4]
            # get data in seconds
            mean, median, uq, lq = compute_stats(df)
            # convert to minutes
            mean = [round(i/60, 2) for i in mean]
            median = [round(i/60, 2) for i in median]
            uq = [round(i/60, 2) for i in uq]
            lq = [round(i/60, 2) for i in lq]
            # get x-axis labels
            valid_col_names = [round(int(col)/60,2) for col in df.columns.tolist()]
            

            # plot
            # plt.plot(valid_col_names, median, color = median_color, linewidth = 1, alpha = 0.5)
            if method_name == "AssignLaterMethod": method_name = "AssignLaterMethod(thereshold:" + str(int(args["threshold_assignment_time"]/60)) +"min)"

            plt.plot(valid_col_names, uq, color = uq_color, linewidth = 0.5, alpha = 0.5)
            plt.plot(valid_col_names, lq, color = lq_color, linewidth = 0.5, alpha = 0.5)
            plt.plot(valid_col_names, mean, color = mean_color, label = method_name + "(Mean WT = " +  str(round(sum(mean)/len(mean),2))+")" , linewidth = 1, alpha = 0.8)
            # fill between uq and lq
            plt.fill_between(valid_col_names, uq, lq, color = shade_color, alpha = 0.5)

        

        
        ######## Plot a combined plot ########
        params = ("_numSim"+str(args["numSimulations"])
                + "_numRider"+str(args['numRiders'])
                + "_numRest"+str(args['numRestaurants'])
                + "_orderMiu" + str(round(args['orderArrivalRate'],3))
                + "_interval" + str(args['IA_interval'])
                + "_gridSize" + str(args['gridSize'])
                + "_FPT" + str(args["FPT_avg"])
                + "window" + str(args["stallingTime"]/60) + "min_"
                + "_ts"+ str(int(args["threshold_assignment_time"]/60)))
        if args["useMcData"]: params += "_Mc"

        figname = args["path"] + "IA_distribution"+ params
        
        if args["numRiders"] < 40:
            # set background color
            plt.figure(figsize=(10,5))
            if args["if_truncated_normal"]:
                    figname+='_tnormal'
                    #  change the background color
                    ax = plt.axes()
                    ax.set_facecolor("seashell")
            elif args["if_TNM"]:
                    figname+='_TNM'
                    #  change the background color
                    ax = plt.axes()
                    ax.set_facecolor("aliceblue")

            # plot for each method
            for m_name, df in ia_dict.items(): # keys are all method + "Optimal"
                plot(df, m_name)

            plt.axhline(y = 45, color = 'r', linestyle = 'dashed', label = "Acceptable Waiting Time (45 min)") 
            plt.ylim(0,100)
            plt.xlabel("Time Horizon (Hours)")
            plt.ylabel("Waiting Time (Minutes)")
            plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), fontsize = 8, borderaxespad=0.)
            x_lables = [int(i/60) for i in np.arange(0, int(args["simulationTime"]/60 + 60), step = 60)]
            plt.xticks(np.arange(0, int(args["simulationTime"]/60 + 60), step = 60), x_lables)    
            title = "Customer's Wait Time (Interval Average)"

            if args["if_truncated_normal"]:
                plt.title(title + "\nTruncated Normal Distribution for FPT, " + str(args["numRiders"]) + " Riders")
            elif args["if_TNM"]:
                plt.title(title + "\n TNM for FPT, " + str(args["numRiders"]) + " Riders")
            else:
                plt.title(title + "\n Deterministic FPT, " + str(args["numRiders"]) + " Riders")
            
            plt.tight_layout()
            plt.savefig(figname+".png", dpi=200)

            plt.close()

        # plot another one on for numRiders = 40
        if args["numRiders"] >= 40:
            plt.figure(figsize=(10,5))
            params = ("_numSim"+str(args["numSimulations"])
                    + "_numRider"+str(args['numRiders'])
                    + "_numRest"+str(args['numRestaurants'])
                    + "_orderMiu" + str(round(args['orderArrivalRate'],3))
                    + "_interval" + str(args['IA_interval'])
                    + "_gridSize" + str(args['gridSize'])
                    + "_FPT" + str(args["FPT_avg"])
                    + "_window" + str(round(args["stallingTime"]/60,1))+"min_"
                    + "all_methods")
            if args["useMcData"]: params += "_Mc"
            figname = args["path"] + "IA_distribution"+ params+ "_enlarged"
            if args["if_truncated_normal"]:
                figname+='_tnormal'
                #  change the background color
                ax = plt.axes()
                ax.set_facecolor("seashell")
            elif args["if_TNM"]:
                figname+='_TNM'
                #  change the background color
                ax = plt.axes()
                ax.set_facecolor("aliceblue")

            for m_name, df in ia_dict.items():
                plot(df, m_name)
            
            
            plt.axhline(y = 45, color = 'r', linestyle = 'dashed', label = "Acceptable Waiting Time (45 min)")
            plt.ylim(0, 100) # uniform the scale and range for different parameters
            plt.xlabel("Time Horizon (hours)")
            plt.ylabel("Waiting Time (minutes)")
            plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), fontsize = 8, borderaxespad=0.)
            x_lables = [int(i/60) for i in np.arange(0, int(args["simulationTime"]/60 + 60), step = 60)]
            plt.xticks(np.arange(0, int(args["simulationTime"]/60 + 60), step = 60), x_lables)    
            title = "Customer's Wait Time (Interval Average)"

            if args["if_truncated_normal"]:
                plt.title(title + "\nTruncated Normal Distribution for FPT, " + str(args["numRiders"]) + " Riders")
            elif args["if_TNM"]:
                plt.title(title + "\n TNM for FPT, " + str(args["numRiders"]) + " Riders")
            else:
                plt.title(title + "\n Deterministic FPT, " + str(args["numRiders"]) + " Riders")
            plt.tight_layout()
            plt.savefig(figname+".png", dpi=200)
            # plt.show()
            plt.close()

    def plot_regreat_ia(self, regret_ia_dict):
        def compute_stats(df):
            mean, median, uq, lq = [],[],[],[]
            for col in df:                
                mean.append(df[col].mean(skipna=True))
                median.append(df[col].median(skipna=True))
                uq.append(df[col].quantile(0.75))
                lq.append(df[col].quantile(0.25))
            for stat in [mean, median, uq, lq]:
                stat = [round(i/60, 2) for i in stat] # convert to minutes, to 2 decimal places
            return mean, median, uq, lq

        def plot(df, method_name):
            method_color = WaitingTimePLot.method_colors[method_name]
            median_color, mean_color, uq_color, lq_color, shade_color = method_color[0], method_color[1], method_color[2], method_color[3], method_color[4]
            # get data in seconds
            mean, median, uq, lq = compute_stats(df)
            # convert to minutes
            mean = [round(i/60, 2) for i in mean]
            median = [round(i/60, 2) for i in median]
            uq = [round(i/60, 2) for i in uq]
            lq = [round(i/60, 2) for i in lq]
            # get x-axis labels
            valid_col_names = [round(int(col)/60,2) for col in df.columns.tolist()]
            

            # plot
            if method_name == "AssignLaterMethod": method_name = "AssignLaterMethod(thereshold:" + str(int(args["threshold_assignment_time"]/60)) +"min)"
            # plt.plot(valid_col_names, median, color = median_color,  linewidth = 1, alpha = 0.5)
            plt.plot(valid_col_names, uq, color = uq_color,  linewidth = 0.5, alpha = 0.5)
            plt.plot(valid_col_names, lq, color = lq_color, linewidth = 0.5, alpha = 0.5)
            plt.plot(valid_col_names, mean, color = mean_color, label = method_name + "(Avg Regret = " +  str(round(sum(mean)/len(mean),2))+")", linewidth = 1, alpha = 0.8)
            # fill between uq and lq
            plt.fill_between(valid_col_names, uq, lq, color = shade_color, alpha = 0.5)

        
        ######## Plot a combined plot ########
        params = ("_numSim"+str(args["numSimulations"])
                + "_numRider"+str(args['numRiders'])
                + "_numRest"+str(args['numRestaurants'])
                + "_orderMiu" + str(round(args['orderArrivalRate'],3))
                + "_interval" + str(args['IA_interval'])
                + "_gridSize" + str(args['gridSize'])
                + "_FPT" + str(args["FPT_avg"])
                + "_window" + str(round(args["stallingTime"]/60,1))+"min_"
                + "_ts"+ str(int(args["threshold_assignment_time"]/60)))
        figname = args["path"] + "Regret"+ params

        # plot another one on for numRiders = 40
        plt.figure(figsize=(10,5))

        # FPT distribution - background color
        if args["if_truncated_normal"]:
            figname+='_tnormal'
            ax = plt.axes()
            ax.set_facecolor("seashell")
        elif args["if_TNM"]:
            figname+='_TNM'
            ax = plt.axes()
            ax.set_facecolor("aliceblue")

        for m_name, df in regret_ia_dict.items():
            plot(df, m_name)
        
        # plt.axhline(y = 45, color = 'r', linestyle = 'dashed', label = "Acceptable Waiting Time (45 min)")
        plt.ylim(0, 20) # uniform the scale and range for different parameters
        plt.xlabel("Time Horizon (hours)")
        plt.ylabel("Regret (minutes)")
        plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), fontsize = 8, borderaxespad=0.)
        x_lables = [int(i/60) for i in np.arange(0, int(args["simulationTime"]/60 + 60), step = 60)]
        plt.xticks(np.arange(0, int(args["simulationTime"]/60 + 60), step = 60), x_lables)    
        title = "Regret of Customer's Wait Time (Interval Average)"

        if args["if_truncated_normal"]:
            plt.title(title + "\nTruncated Normal Distribution for FPT, " + str(args["numRiders"]) + " Riders")
        elif args["if_TNM"]:
            plt.title(title + "\n TNM for FPT, " + str(args["numRiders"]) + " Riders")
        else:
            plt.title(title + "\n Deterministic FPT, " + str(args["numRiders"]) + " Riders")
        plt.tight_layout()
        plt.savefig(figname+".png", dpi=200)
        # plt.show()
        plt.close()


    # main function
    def plot(self):
        self.add_optimal_wt = True
        self.plot_wt = True
        self.plot_regret = True
        
        # for i in [i*5 for i in range(4,7)]: # TNM, synthetic data
        for i in [i*100 for i in range(5,12)]:
        # for i in [40]:
        # for i in [i*5 for i in range(7, 10)]: # deterministic FPT, synthetic data
        # for j in [i*60*5 for i in range(5, 15)]: # TNM, real data
            args["numRiders"] = i
            args["if_TNM"] = 1
            # args["threshold_assignment_time"] = j
            # print("threshold_assignment_time: ", str(int(j/60))+"min")
            
            wt_ia_dict_res, regret_ia_dict_res = self.get_ia_df()
            if self.plot_wt: self.plot_wt_ia(wt_ia_dict_res)
            if self.plot_regret: self.plot_regreat_ia(regret_ia_dict_res)
