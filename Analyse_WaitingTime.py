
import copy
from ctypes.wintypes import PINT
from glob import escape
import numpy as np
from ProposedMethod import ProposedMethod
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

    print(len(default.wt_ls))
    print(len(anti.wt_ls))
    print(sum(default.wt_ls), sum (anti.wt_ls))
    
    # for i, j in zip(default.wt_ls,  anti.wt_ls):
    #     print(i == j) 

    print(avg_wt_default-avg_wt_anti )

    # print(simulation_default.wt_ls)
    # print(avg_wt_default)
    # print(simulation_anti.wt_ls)
    # print(avg_wt_anti)

    # plt.plot(simulation_default.wt_ls,simulation_default.wt_ls, '--', label = "Default")
    # plt.axhline(y=avg_wt_default, color='black')
    # # plt.plot(x_axis, y_2,'-+',label = "Anticipation")
    # plt.show()
    # print("total time taken:", time.time() - start_time)
