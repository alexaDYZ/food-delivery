
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
from generateData import dataGeneration
import matplotlib.pyplot as plt
import time
from Analyse_Rider import runEpisode
import datetime
import os

class AnalyseOrders():
    # This object takes in result of 2 simulations using their corresponding methods, and conduct analysis
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
                        "_lambda" + str(args["orderLambda"]) +
                        "_numRider"+str(args['numRiders'])+
                        "_gridSize" + str(args['gridSize']) + 
                        "_FPT"+str(args['FPT_avg'])+".csv", index=False)

        printIndividual(self.default, "DeliveryHistory_Default")
        printIndividual(self.anti, "DeliveryHistory_Anticipative" )                   


