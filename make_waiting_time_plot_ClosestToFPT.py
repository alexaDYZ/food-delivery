


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

from DefaultMethod_1b import DefaultMethod_1b
from Simulation import Simulation
from generateData import dataGeneration
import matplotlib.pyplot as plt
import time
import datetime
from RunSimulation import runEpisode
from ClosestToFPTMethod import ClosestToFPTMethod



class WaitingTimePLot():
    def __init__(self) -> None:
        self.baselineMethod = DefaultMethod_1b()
        self.anticipativeMethod = AnticipationMethod()
        self.closestToFPTMethod = ClosestToFPTMethod()
    
##################### To generage simulation data for analysis #####################

    def simulateOnce(self):
        '''
        This function performs 1 simulation using the given set of parameters.
        Output: 2 'simulation' class objects, with simulation results. 
                refer to Simulation.py for more details
        '''
        dataGeneration() # generate initial data
        default, useFPT = runEpisode(self.baselineMethod, self.closestToFPTMethod) # 2 simulation results
        return default, useFPT

    # input: 1 simulation class object, for each method
    # output: 1 dataframes, with the delivery/assignment history for all orders, for each method
    #        order data columns are ["Order Index", "Order-in Time", "Rider Index", "Rider Index", 
    #                               "Rider Arrives at Restaurant","Order Delivered Time", "Waiting Time", 
    #                               "DT", "Time taken before delivery"
    def get_order_data_from_one_simulation(self,sim_default, sim_useFPT):        
        def helper(sim:Simulation):
            orders = sim.order_list
            df_2dlist = []
            for o in orders:
                row = []
                row.append(o.index)
                row.append(o.t)
                row.append(o.rider.index)
                row.append(o.t_riderReachedRestaurant)
                row.append(o.t_delivered)
                row.append(o.wt)

                # Then append DT 
                if args["FPT_avg"] > args["gridSize"]:
                    # when FPT is extremely largs, WT = max(FPT, R2R) + DT = FPT + DT
                    row.append(o.t_delivered - o.t  - args["FPT_avg"])
                elif args["FPT_avg"] == 0:
                    # when FPT is negligible, WT = R2R + DT
                    row.append(o.t_delivered - o.t_riderReachedRestaurant) 
                else:
                    row.append(None)
                
                row.append(o.wt - row[-1] if row[-1] else None)

                df_2dlist.append(row)
            df = pd.DataFrame(df_2dlist, columns=["Order Index", "Order-in Time", 
                                                "Rider Index", "Rider Arrives at Restaurant",
                                                "Order Delivered Time", "Waiting Time", 
                                                "DT", "Time taken before delivery"])
            # df.to_pickle(args["path"] +"df_{sim.method}_{sim.numOrders}.pkl")
            # save to csv
            # df.to_csv(args["path"] + "df_si{sim.method}_{sim.numOrders}.csv") 
            return df           
        
        df_order_data_default = helper(sim_default)
        df_order_data_useFPT = helper(sim_useFPT)
        
        return df_order_data_default, df_order_data_useFPT
    
##################### 1. Plot for 1 simulation #####################

    def compute_sma_by_numOrders(self, df_order_data_default, df_order_data_FPT):
        # compute the average waiting time for previous n orders, n = SMA_batchsize
        # input: 2 dataframes
        # output: a list of SMA for all orders, for each method
        def compute(df):
            # output: a list of SMA for all orders. len = numOrders. for orders w/o enough previous orders, SMA = None
            
            # arrange all orders by order index
            df = df.sort_values(by="Order Index")
            
            # find average waiting time for previous n orders
            wt = df["Waiting Time"]
            wt_average = wt.rolling(window=args["SMA_batchsize"]).mean()
            return list(wt_average)

        MA_ls_default = compute(df_order_data_default)
        MA_ls_anticipation = compute(df_order_data_FPT)
        
        return MA_ls_default, MA_ls_anticipation


    def plot_sma_by_numOrders(self, df_order_data_default, df_order_data_FPT):
        # input: 2 dataframes
        # output: plot: x0 = numOrders, y0 = SMA for default method
        def plot(df, method_name, original_color, MA_color):
            # sort by order index
            df = df.sort_values(by="Order Index")
            wt = df["Waiting Time"]
            wt_average = wt.rolling(window=args["SMA_batchsize"]).mean()
            plt.figure(figsize=(10, 5))
            plt.plot(wt, color = original_color,label='Original', linewidth=0.5)
            plt.plot(wt_average, color = MA_color, label='Moving Average', linewidth = 1)
            plt.legend(loc='best')
            plt.title('Waiting Time Plot ('+ method_name + ')')
            plt.ylabel('Waiting Time(s)')
            plt.xlabel('Order Index')
            params = ("_lambda" + str(args["orderArrivalRate"]) 
                + "_numRider"+str(args['numRiders'])
                + "_numRest"+str(args['numRestaurants'])
                + "_bacthSize" + str(args['SMA_batchsize'])
                + "_gridSize" + str(args['gridSize'])
                + "_FPT" + str(args["FPT_avg"]))
            
            plt.savefig(args["path"] + "SMA_order_" + method_name + params + ".png", dpi=500)
            plt.show()
            
        
        plot(df_order_data_default, "Default_1b", "orange", "red")
        plot(df_order_data_FPT, "Anticipation","lightgreen", "darkgreen" )


    def compute_interval_avg_by_time(self, df_order_data_default, df_order_data_FPT):
        # compute the average waiting time orders delivered in consecutive non-overlapping intervals
        # input: 2 dataframes 
        # outout: a list of interval average waiting time for all intervals, for each method
        def compute(df):
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
            result = list( df.groupby("interval_number")["Waiting Time"].mean())
            result = [round(i, 2) for i in result]
            # print("result = ", result)
            result.pop()# last interval is not complete, so remove it
            return result
            
        interval_avg_default = compute(df_order_data_default)
        interval_avg_useFPT = compute(df_order_data_FPT)
        return interval_avg_default, interval_avg_useFPT


    def plot_interval_avg_by_time(self, df_order_data_default, df_order_data_FPT):
        # input: 2 dataframes
        # output: plot: x0 = time, y0 = SMA for default method

        plt.figure(figsize=(10, 5))
        # use the interval average to plot
        avg_default, avg_anti = self.compute_interval_avg_by_time(df_order_data_default, df_order_data_FPT)
        def plot_avg(avg_ls, method_name, line_color):
            time_ls = [round(i*args["IA_interval"]/60,2) for i in range(1, len(avg_ls)+1)] # end of each interval, in minutes
            avg_ls = [round(j/60, 2) for j in avg_ls] # convert to minutes
            plt.plot(time_ls, avg_ls, color = line_color, label = "Average - "+ method_name, linewidth = 1)
            # annotate data points
            # for i in range(len(avg_ls)):
            #     plt.annotate(str(avg_ls[i]), (time_ls[i], avg_ls[i]))


        # use the original waiting time to plot
        def plot_original(df, method_name, line_color):
            df = df.sort_values(by="Order Delivered Time")
            wt_ls = [round(i/60, 2) for i in list(df["Waiting Time"])]
            x_ls = [round(j/60, 2) for j in list(df["Order Delivered Time"])]
            plt.plot(x_ls, wt_ls, color = line_color, label = "Original - "+ method_name, linewidth = 0.5)

        
        def plot():
            plot_original(df_order_data_default, "Default_1b", "orange")
            plot_original(df_order_data_FPT, "ClosestToFPT", "lightgreen")

            plot_avg(avg_default, "Default_1b", "darkred")
            plot_avg(avg_anti, "ClosestToFPT", "darkgreen")

            
        plot()
        plt.suptitle('Average Waiting Time Plot (1 simulation)')
        plt.title('Interval = ' + str(int(args["IA_interval"]//60)) + ' min')
        plt.ylabel('Average Waiting Time(min)')
        plt.xlabel('Time(min)')

        params = ("_lambda" + str(args["orderArrivalRate"])
            + "_numRider"+str(args['numRiders'])
            + "_numRest"+str(args['numRestaurants'])
            + "_interval" + str(args['IA_interval'])
            + "_gridSize" + str(args['gridSize'])
            + "_FPT" + str(args["FPT_avg"])
            + "usingFPT")

        plt.legend(loc='best')
        plt.savefig(args["path"] + "IA_time_min" + params + ".png", dpi=500)
        plt.show()

        pass

    
##################### 2. Run multiple simulation #####################
    def plot_sma_distribution_by_numOrders(self):
        # 2 list to store the SMA list for each simulation
        d = []
        a = []
        # start multiple simulations:
        for i in range(args["numSimulations"]):
            print("Simulation ", i)
            sim_default, sim_anti = self.simulateOnce()
            df_default, df_anti = self.get_order_data_from_one_simulation(sim_default, sim_anti)
            sma_default, sma_anti = self.compute_sma_by_numOrders(df_default, df_anti)
            d.append(sma_default)
            a.append(sma_anti)
        col_names = [str(i) for i in range(1, args["numOrders"]+1)] # column names are order index
        # 1 row: wt of each order in 1 simulation
        # 1 column: wt of order of the same index in all simulations. note: same index does not mean same order
        df_d = pd.DataFrame(d, columns = col_names)
        df_a = pd.DataFrame(a, columns = col_names)
        # ### debug ####
        # # save to csv
        # df_d.to_csv(args["path"] + "df_sma_default.csv")
        # df_a.to_csv(args["path"] + "df_sma_anti.csv")
        # ##############

        def compute_stats(df):
            mean, median, uq, lq = [],[],[],[]
            for col in col_names:
                # only compute stats for columns that are not empty
                if int(col) >= args["SMA_batchsize"]:
                    mean.append(df[col].mean())
                    median.append(df[col].median())
                    uq.append(df[col].quantile(0.75))
                    lq.append(df[col].quantile(0.25))
            for stat in [mean, median, uq, lq]:
                stat = [round(i/60, 2) for i in stat] # convert to minutes, to 2 decimal places
            return mean, median, uq, lq
        
        def plot(df, method_name, mean_color, median_color, uq_color, lq_color, shade_color):
            # get data in seconds
            mean, median, uq, lq = compute_stats(df)
            valid_col_names = col_names[args["SMA_batchsize"]-1:] # only plot columns that are not empty
            # convert to minutes
            mean = [round(i/60, 2) for i in mean]
            median = [round(i/60, 2) for i in median]
            uq = [round(i/60, 2) for i in uq]
            lq = [round(i/60, 2) for i in lq]
            # ### debug ####
            # # save to csv
            # df_stat = pd.DataFrame([mean, median, uq, lq], columns = valid_col_names)
            # df_stat.to_csv(args["path"] + "df_sma_" + method_name + "_stat.csv")
            # ##############

            # plot
            plt.plot(valid_col_names, mean, color = mean_color, label = "Mean - "+ method_name, linewidth = 1)
            plt.plot(valid_col_names, median, color = median_color, label = "Median - "+ method_name, linewidth = 1)
            plt.plot(valid_col_names, uq, color = uq_color, label = "Upper Quartile - "+ method_name, linewidth = 0.5)
            plt.plot(valid_col_names, lq, color = lq_color, label = "Lower Quartile - "+ method_name, linewidth = 0.5)
            # fill between uq and lq
            plt.fill_between(valid_col_names, uq, lq, color = shade_color, alpha = 0.2)

        plot_combined_graph = True
        plot_anticipation = False
        
        ######## Plot a combined graph for both methods ########
        if plot_combined_graph:
            plt.figure(figsize=(10, 5))
            plot(df_d, "Default_1b", "darkred", "red", "pink", "pink","lightpink")
            plot(df_a, "Anticipation", "darkgreen", "green", "lightgreen", "lightgreen", "lightgreen")

            
            plt.xticks(np.arange(0, args["numOrders"]+ 400, step = 200))  # Set label locations.

            plt.suptitle('SMA Distribution Plot ('+ str(args["numSimulations"])+' simulations, Default_1b vs Anticipation)')
            plt.title('Window = ' + str(int(args["SMA_batchsize"])) + " orders")
            plt.ylabel('Waiting Time(min)')
            plt.xlabel('Order Index')
            plt.legend(loc='best')

            params = ("_lambda" + str(args["orderArrivalRate"])
                + "_numRider"+str(args['numRiders'])
                + "_numRest"+str(args['numRestaurants'])
                + "_window" + str(args['SMA_batchsize'])
                + "_gridSize" + str(args['gridSize'])
                + "_FPT" + str(args["FPT_avg"]))
            
            plt.savefig(args["path"] + "SMA_distribution" + params + ".png", dpi=200)
            plt.show()
        
        ######## Plot one for anticipation methods, as the scales of the two doesnt match ########
        if plot_anticipation:
            plt.figure(figsize=(10, 5))
            # df to csv
            df_a.to_csv(args["path"] + "df_sma_anti.csv")
            plot(df_a, "Anticipation", "darkgreen", "green", "lightgreen", "lightgreen", "lightgreen")

            plt.xticks(np.arange(0, args["numOrders"]+200, step = 200))  # Set label locations.

            plt.suptitle('SMA Distribution Plot ('+ str(args["numSimulations"])+' simulations, Anticipation Method only)')
            plt.title('Window = ' + str(int(args["SMA_batchsize"])) + " orders")
            plt.ylabel('Waiting Time(min)')
            plt.xlabel('Order Index')
            plt.legend(loc='best')

            params = ("_lambda" + str(args["orderArrivalRate"])
                + "_numRider"+str(args['numRiders'])
                + "_numRest"+str(args['numRestaurants'])
                + "_window" + str(args['SMA_batchsize'])
                + "_gridSize" + str(args['gridSize'])
                + "_FPT" + str(args["FPT_avg"]))
            
            plt.savefig(args["path"] + "SMA_distribution_anti" + params + ".png", dpi=500)
            plt.show()


    def plot_ia_distribution_by_time(self):
        '''
        Plot interval average distribution by time
        Note: intervals are non-overlapping, with a time window of "IA_interval"
        '''
        # 2 list to store the SMA list for each simulation
        d = []
        a = []
        # start multiple simulations:
        for i in range(args["numSimulations"]):
            print("Simulation ", i)
            sim_default, sim_anti = self.simulateOnce()
            # break # debug
            df_default, df_anti = self.get_order_data_from_one_simulation(sim_default, sim_anti)
            ia_d, ia_a = self.compute_interval_avg_by_time(df_default, df_anti)
            d.append(ia_d)
            a.append(ia_a)
        
        # exit() # debug

        max_num_intervals_d = max([len(i) for i in d]) # find the max number of intervals in all simulations
        max_num_intervals_a = max([len(i) for i in a])

        col_names_d = [str(i*args["IA_interval"]) for i in range(1, max_num_intervals_d+1)] # column names are order index
        col_names_a = [str(i*args["IA_interval"]) for i in range(1, max_num_intervals_a+1)] # column names are order index
        
        # 1 row: wt of each order in 1 simulation
        # 1 column: wt of order of the same index in all simulations. note: same index does not mean same order
        df_d = pd.DataFrame(d, columns = col_names_d)
        df_a = pd.DataFrame(a, columns = col_names_a)

        # ############### debug ###############
        # # df to csv
        # df_d.to_csv(args["path"] + "df_ia_default.csv")
        # df_a.to_csv(args["path"] + "df_ia_anti.csv")
        # ############### debug ###############

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

        def plot(df, method_name, mean_color, median_color, uq_color, lq_color, shade_color):
            # get data in seconds
            mean, median, uq, lq = compute_stats(df)
            # convert to minutes
            mean = [round(i/60, 2) for i in mean]
            median = [round(i/60, 2) for i in median]
            uq = [round(i/60, 2) for i in uq]
            lq = [round(i/60, 2) for i in lq]
            # get x-axis labels
            valid_col_names = [round(int(col)/60,2) for col in df.columns.tolist()]
            
            # ### debug ####
            # # save to csv
            # df_stat = pd.DataFrame([mean, median, uq, lq], columns = valid_col_names)
            # df_stat.to_csv(args["path"] + "df_ia_" + method_name + "_stat.csv")
            # ##############

            # plot
            plt.plot(valid_col_names, mean, color = mean_color, label = "Mean - "+ method_name, linewidth = 1)
            plt.plot(valid_col_names, median, color = median_color, label = "Median - "+ method_name, linewidth = 1)
            plt.plot(valid_col_names, uq, color = uq_color, label = "Upper Quartile - "+ method_name, linewidth = 0.5)
            plt.plot(valid_col_names, lq, color = lq_color, label = "Lower Quartile - "+ method_name, linewidth = 0.5)
            # fill between uq and lq
            plt.fill_between(valid_col_names, uq, lq, color = shade_color, alpha = 0.2)


        plot_combined = True
        plot_anticipation = False
        
        ######## Plot a combined plot ########
        if plot_combined:
            params = ("_numSim"+str(args["numSimulations"])
                    + "_numRider"+str(args['numRiders'])
                    + "_numRest"+str(args['numRestaurants'])
                    + "_orderMiu" + str(round(args['orderArrivalRate'],3))
                    + "_interval" + str(args['IA_interval'])
                    + "_gridSize" + str(args['gridSize'])
                    + "_FPT" + str(args["FPT_avg"])
                    + "useFPT")

            figname = args["path"] + "IA_distribution"+ params
            
            # plot
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
            plot(df_d, "Default", "darkred", "red", "pink", "pink", "pink")
            plot(df_a, "ClosestToFPT", "darkgreen", "green", "lightgreen", "lightgreen", "lightgreen")
            plt.axhline(y = 45, color = 'r', linestyle = 'dashed', label = "Acceptable Waiting Time (45 min)") 
            # plt.ylim(0, 550) # uniform the scale and range for different parameters
            plt.ylim(0,600)
            plt.xlabel("Time Horizon (Hours)")
            plt.ylabel("Waiting Time (minutes)")
            plt.legend()
            x_lables = [int(i/60) for i in np.arange(0, int(max_num_intervals_d*args["IA_interval"]/60 + 120), step = 60)]
            plt.xticks(np.arange(0, int(max_num_intervals_d*args["IA_interval"]/60 + 120), step = 60), x_lables)
               
            plt.suptitle("Interval Average of Waiting Time using Default_1b and ClosestToFPT")
            if args["if_truncated_normal"]:
                plt.title("Truncated Normal Distribution for FPT, " + str(args["numRiders"]) + " Riders")
            elif args["if_TNM"]:
                    plt.title("TNM for FPT, " + str(args["numRiders"]) + " Riders")
            else:
            # plt.title( "mean time between order arrivals = "+ str(args["orderArrivalRate"]) + "s")
                plt.title(str(args["numRiders"]) + " Riders")

            plt.savefig(figname+".png", dpi=200)

            # plt.show()
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
                        + "useFPT")
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

                plot(df_d, "Default", "darkred", "red", "pink", "pink", "pink")
                plot(df_a, "Anticipation", "darkgreen", "green", "lightgreen", "lightgreen", "lightgreen")
                plt.axhline(y = 45, color = 'r', linestyle = 'dashed', label = "Acceptable Waiting Time (45 min)")
                plt.ylim(0, 45) # uniform the scale and range for different parameters
                plt.xlabel("Time (minutes)")
                plt.ylabel("Waiting Time (minutes)")
                plt.legend()
                x_lables = [int(i/60) for i in np.arange(0, int(max_num_intervals_d*args["IA_interval"]/60 + 120), step = 60)]
                plt.xticks(np.arange(0, int(max_num_intervals_d*args["IA_interval"]/60 + 120), step = 60), x_lables)    
                plt.suptitle("Interval Average of Waiting Time using Default_1b and ClosestToFPT")
                if args["if_truncated_normal"]:
                    plt.title("Truncated Normal Distribution for FPT, " + str(args["numRiders"]) + " Riders")
                elif args["if_TNM"]:
                    plt.title("TNM for FPT, " + str(args["numRiders"]) + " Riders")
                else:
                # plt.title( "mean time between order arrivals = "+ str(args["orderArrivalRate"]) + "s")
                    plt.title(str(args["numRiders"]) + " Riders")
               
                plt.savefig(figname+".png", dpi=200)
                # plt.show()
                plt.close()



        ######## Plot one for anticipation methods, as the scales of the two doesnt match ########
        if plot_anticipation:
            # plot
            plt.figure(figsize=(10,5))
            plot(df_a, "Anticipation", "darkgreen", "green", "lightgreen", "lightgreen", "lightgreen")
            plt.axhline(y = 45, color = 'r', linestyle = 'dashed', label = "Acceptable Waiting Time (45 min)")    
            plt.xlabel("Time (minutes)")
            plt.ylabel("Waiting Time (minutes)")
            plt.legend()
            x_lables = [int(i/60) for i in np.arange(0, int(max_num_intervals_d*args["IA_interval"]/60 + 120), step = 60)]
            plt.xticks(np.arange(0, int(max_num_intervals_d*args["IA_interval"]/60 + 120), step = 60), x_lables)
            plt.suptitle('Interval Average Distribution Plot ('+ str(args["numSimulations"])+' simulations, Anticipation Method only)')
            # plt.title( "mean time between order arrival = "+ str(args["orderArrivalRate"]) + "s")
            plt.title( str(args["numRiders"]) + " Riders")
            params = ("_numSim"+str(args["numSimulations"])
                    + "_numRider"+str(args['numRiders'])
                    + "_numRest"+str(args['numRestaurants'])
                    + "_orderMiu" + str(round(args['orderArrivalRate'],3))
                    + "_interval" + str(args['IA_interval'])
                    + "_gridSize" + str(args['gridSize'])
                    + "_FPT" + str(args["FPT_avg"])
                    + "useFPT")
            plt.savefig(args["path"] + "IA_distribution_anti" + params + ".png", dpi=500)
            # plt.show()
            plt.close()


            
             
    

##################### Main function #####################


    def main(self):
        # sim_default, sim_anti = self.simulateOnce()
        # df_default, df_anti = self.get_order_data_from_one_simulation(sim_default, sim_anti)

        ### Single simulation ###
        # sma_default, sma_anti = self.compute_sma_by_numOrders(df_default, df_anti)
        # self.plot_sma_by_numOrders(df_default, df_anti)
        # self.compute_interval_avg_by_time(df_default, df_anti)
        # self.plot_interval_avg_by_time(df_default, df_anti)

        ### Multiple simulations ###
        
        # Variations of numRiders
        # self.plot_sma_distribution_by_numOrders()
        for i in [i*10 for i in range(3,9)]:
        # for i in [250, 300, 350, 400, 450, 500]:
        # for i in [600, 700, 800, 1000, 1100]:
            args["numRiders"] = i
            self.plot_ia_distribution_by_time()
        
        # # vary the order arrival rate
        # for j in [25]:
        #     args["orderArrivalRate"] = j
        #     self.plot_ia_distribution_by_time()






    def run(self):
        print("Start running")

        self.main()
