'''
This file will take in the data from the simulation and generate a graph
'''


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from config import args

def importData(filename):
    df = pd.read_csv(args["path"]+filename+".csv")
    for col_name in df.columns: 
        df[col_name].astype(float)
    return df

def plot_dropped_rate(filename_in, plotname_out):
    df = importData(filename_in)
    x = df["numRiders"]
    plt.plot(x, 100*df["median"], label = "median", marker = 'o')
    plt.plot(x, 100*df["mean"], label = "mean", marker = '.')
    plt.fill_between(x, 100*df["upper_quantile"], 100*df["lower_quantile"], label = "IQR", alpha = 0.5)
    plt.xticks([i for i in range(20,46,2)])
    plt.ylim(0,50)
    plt.title("Percentage of Orders Dropped within 1 Simulation using Default_1a \n (100 simulations)")
    plt.xlabel("Number of Riders")
    plt.ylabel("Percentage")
    plt.legend()
    # plt.show()
    plt.savefig(args["path"] + plotname_out + ".png",format="png", dpi=1200)
    plt.clf()

plot_dropped_rate("summary_DR_2000orders_numRider44_gridSize1000_FPT30", "drop_rate_plot")

def plot_no_drop(filename_in, plotname_out):
    df = importData(filename_in)
    x = df["numRiders"]
    plt.plot(x, 100*df["percentage simulations with no drop-out"], label = "Simulations with all orders delivered(%)")
    plt.xticks([i for i in range(20,46,2)])
    plt.title("Simulations with all orders delivered(%) by Default_1a \n (100 simulations)")
    plt.xlabel("Number of Riders")
    plt.ylabel("Percentage")
    # plt.show()
    plt.savefig(args["path"] + plotname_out + ".png",format="png", dpi=1200)
    plt.clf()
    
plot_no_drop("summary_DR_2000orders_numRider44_gridSize1000_FPT30", "percentage_all_done_plot")






   