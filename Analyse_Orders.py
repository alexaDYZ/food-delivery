
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
from generateData import dataGeneration
import matplotlib.pyplot as plt
import math 
import datetime
import os
from RunSimulation import runEpisode, runEpisode_single_medthod
from ClosestToFPTMethod import ClosestToFPTMethod
from DefaultMethod_1b import DefaultMethod_1b
from PatientAnticipativeMethod_Bulk import PatientAnticipativeMethod_Bulk
from  AnticipationMethod import AnticipationMethod
from UsefulWorkMethod import UsefulWorkMethod
from AssignLaterMethod import AssignLaterMethod, AssignLaterMethod_UsefulWork  

class AnalyseOrders():
    # first, run the simulation
    # then:
    # input: 2 simulation class object, that has the result of 2 simulations
    # output: 1 csv file with the delivery/assignment history for all orders, for each method
    def __init__(self, res_default, res_anti) -> None:
        self.default = res_default
        self.anti = res_anti
        self.path = args["path"]

    def printHistory(self):
        '''
        This fucntion output one csv file with the delivery/assignment history for all orders,
        for each method
        '''
        def printIndividual(res:Simulation, csvName):
            '''
            Save the delivery/assignment history to csv
            Columns are ["Order Index", "Order-in Time", "Rider Index", 
                        "Rider Arrives at Restaurant","Order Delivered Time", "Waiting Time"]
            '''

            orders = res.order_list
            df_2dlist = []
            for o in orders:
                row = []
                row.append(o.index)
                row.append(o.t)
                row.append(o.rider.index)
                row.append(o.t_riderReachedRestaurant)
                row.append(o.t_delivered)
                row.append(o.wt) # WT + lagtime, where WT = max(FPT, R2R) + DT 

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
            df.to_csv(self.path + str(datetime.datetime.now()) + csvName + 
                        "_numOrders" + str(args["numOrders"]) + 
                        "_lambda" + str(args["orderArrivalRate"]) +
                        "_numRider"+str(args['numRiders'])+
                        "_gridSize" + str(args['gridSize']) + 
                        "_FPT"+str(args['FPT_avg'])+".csv", index=False)

        printIndividual(self.default, "DeliveryHistory_Default")
        printIndividual(self.anti, "DeliveryHistory_Anticipative" )                   

class Simple():
    methods = {
        "DefaultMethod_1b": DefaultMethod_1b(),
        "AnticipationMethod": AnticipationMethod(),
        "ClosestToFPTMethod": ClosestToFPTMethod(),
        "PatientAnticipativeMethod_Bulk": PatientAnticipativeMethod_Bulk(),
        "UsefulWorkMethod": UsefulWorkMethod(),
        "AssignLaterMethod": AssignLaterMethod(),
        "AssignLaterMethod_UsefulWork": AssignLaterMethod_UsefulWork(),
    }
    def __init__(self) -> None:
        self.methods = []

    # to add all methods
    def add_all_methods(self):
        self.methods = list(Simple.methods.values())
    
    # to add a single method
    def add_method(self, method_name):
        m = Simple.methods[method_name]
        self.methods.append(m)
    
  

    def get_order_df_from_sim_res(self,sim):
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
            # 5. FRT
            row.append(o.t + o.rest.order_FPT_dict[o.index] )
            # 6. "Order Delivered Time"
            row.append(o.t_delivered)
            # 7. "Waiting Time"
            row.append(o.wt)
        
            # 8. "Theoretical Best WT"
            optimal_wt = o.rest.order_FPT_dict[o.index] + math.dist(o.rest.loc, o.cust.loc)
            row.append(optimal_wt)
            # 9. "WT regret"
            regret_wt = o.wt - optimal_wt
            row.append(regret_wt)
            # 10. "FPT"
            row.append(o.rest.order_FPT_dict[o.index])
            # 11. rider_reached_before_FRT
            x = 1 if o.t_riderReachedRestaurant<o.rest.order_FPT_dict[o.index]+o.t else 0
            row.append(x)

            row = [round(x, 2) if x else None for x in row]
            df_2dlist.append(row)
        df = pd.DataFrame(df_2dlist, columns=["Order Index", "Order-in Time", 
                                            "Rider Index", "Rider Arrives at Restaurant", "FRT",
                                            "Order Delivered Time", "Waiting Time", 
                                             "Theoretical Best WT", "WT regret", "FPT", "rider_reached_before_FRT"])
        df.to_csv("results/df_"+ sim.method.name+ ".csv")
        return df           


    def run(self):
        for m in self.methods:
            sim = runEpisode_single_medthod(m)
            self.get_order_df_from_sim_res(sim)
            print(m.name, "done")
