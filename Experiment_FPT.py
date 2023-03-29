
from make_waiting_time_plot_all import WaitingTimePLot
import datetime
from Analyse_Orders import Simple
from AnticipationMethod import AnticipationMethod
from AssignLaterMethod import AssignLaterMethod
from DefaultMethod_1b import DefaultMethod_1b
import sys
from config import args
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd




def experiment1():
   'full knowledge of FPT'
   a = WaitingTimePLot()
   a.add_method("AnticipationMethod") 
   a.add_method("DefaultMethod_1b")
   a.add_method("AssignLaterMethod")
   a.plot()

def experiment2():
   a = WaitingTimePLot()
   a.add_method("AnticipationMethod") 
   a.add_method("AnticipationMethod_ImperfectKnowldge")
   a.plot()
   # a = Simple()
   # a.add_method("AnticipationMethod_ImperfectKnowldge")
   # a.add_method("AnticipationMethod")
   # a.run()
   # run this in terminal: python3 main.py &> out.txt

def experiment3():
   a = WaitingTimePLot()
   a.add_method("AssignLaterMethod") 
   a.add_method("AssignLaterMethod_ImperfectKnowldge")
   a.plot()
   # a = Simple()
   # a.add_method("AssignLaterMethod")
   # a.add_method("AssignLaterMethod_ImperfectKnowledge")
   # a.run()
   
# section 4.6.1 
def vanilla_w_diff_FPT():
   '''This experiment is corresponding to the following setup:
   1. FPT is fixed at 10 min
   2. FPT follows Weibull Distribution
   3. FPT follows a mixture of truncated normal Distribution

   Algorithm used: Anticipative_greedy

   FPT knowledge: Full knowledge
   '''
   a = WaitingTimePLot()
   a.add_method("AnticipationMethod") 
   a.plot()

   a = WaitingTimePLot()
   args["weibull"] = 1
   a.add_method("AnticipationMethod") 
   a.plot()

   a = WaitingTimePLot()
   args["weibull"] = 0
   args["if_TNM"] = 1
   a.add_method("AnticipationMethod") 
   a.plot()

# section 4.6.2
def later_w_diff_FPT():
   '''This experiment is corresponding to the following setup:
   1. FPT is fixed at 10 min
   2. FPT follows Weibull Distribution
   3. FPT follows a mixture of truncated normal Distribution

   Algorithm used: Anticipative_later

   FPT knowledge: Full knowledge
   '''
   a = WaitingTimePLot()
   a.add_method("AssignLaterMethod") 
   a.plot()

   a = WaitingTimePLot()
   args["weibull"] = 1
   a.add_method("AssignLaterMethod") 
   a.plot()

   a = WaitingTimePLot()
   args["weibull"] = 0
   args["if_TNM"] = 1
   a.add_method("AssignLaterMethod") 
   a.plot()

# section 4.6.3 
def vanilla_w_diff_knowledge_diff_FPT():

   def vanilla_w_diff_knowledge():
      # perfect knowledge
      a = WaitingTimePLot()

      vanilla1 = AnticipationMethod()
      vanilla1.setFPT_pred_accuracy("full")
      vanilla1.name = "Perfect Knowledge"
      col_1 = ["blue", "blue", "lightblue", "lightblue", "lightblue"]

      vanilla2 = AnticipationMethod()
      vanilla2.setFPT_pred_accuracy("partial")
      vanilla2.name = "Partial Knowledge"
      col_2 = ["indigo", "indigo", "thistle", "thistle", "thistle"]

      vanilla3 = AnticipationMethod()
      vanilla3.setFPT_pred_accuracy("poor_short")
      vanilla3.name = "Poor Knowledge - Underestimate"
      col_3 = ["red", "red", "lightcoral", "lightcoral", "lightcoral"]

      vanilla4 = AnticipationMethod()
      vanilla4.setFPT_pred_accuracy("poor_long")
      vanilla4.name = "Poor Knowledge - Overestimate"
      col_4 = ["orange", "orange", "bisque", "bisque", "bisque"]

      a.add_additional_method(vanilla1, col_1)
      a.add_additional_method(vanilla2, col_2)
      a.add_additional_method(vanilla3, col_3)
      a.add_additional_method(vanilla4, col_4)

      a.plot()
   
   vanilla_w_diff_knowledge()

   # weibull
   args["weibull"] = 1
   vanilla_w_diff_knowledge()

   # TNM
   args["weibull"] = 0
   args["if_TNM"] = 1
   vanilla_w_diff_knowledge()

# still buggy
def later_w_diff_knowledge():
   # perfect knowledge
   a = WaitingTimePLot()

   # later1 = AssignLaterMethod()
   # later1.setFPT_pred_accuracy("full")
   # later1.name = "Perfect Knowledge"
   # col_1 = ["blue", "blue", "lightblue", "lightblue", "lightblue"]

   # # later2 = AssignLaterMethod()
   # # later2.setFPT_pred_accuracy("partial")
   # # later2.name = "Partial Knowledge"
   # # col_2 = ["indigo", "indigo", "thistle", "thistle", "thistle"]

   later3 = AssignLaterMethod()
   later3.setFPT_pred_accuracy("poor_short")
   later3.name = "Poor Knowledge - Underestimate"
   col_3 = ["red", "red", "lightcoral", "lightcoral", "lightcoral"]

   # later4 = AssignLaterMethod()
   # later4.setFPT_pred_accuracy("poor_long")
   # later4.name = "Poor Knowledge - Overestimate"
   # col_4 = ["orange", "orange", "bisque", "bisque", "bisque"]

   # a.add_additional_method(later1, col_1)
   # a.add_additional_method(later2, col_2)
   a.add_additional_method(later3, col_3)
   # a.add_additional_method(later4, col_4)

   a.plot()


# section 4.6.3 - 2 precision
def vanilla_w_diff_bias_diff_FPT():
   'Simulation takes some time'

   def vanilla_w_diff_bias():
      # perfect knowledge
      a = WaitingTimePLot()
      bias = [i for i in range(0,10)]
      bias.extend([i for i in range(10, 100, 10)])
      for b in bias:
         m = AnticipationMethod()
         m.setFPT_pred_bias(b)
         m.name = str(b) + "% Bias"
         a.add_additional_method(m)

      a.compute_avg_wt()
   
   
   # weibull
   args["weibull"] = 1
   print("---- Weibull ----")
   vanilla_w_diff_bias()

   # TNM
   args["weibull"] = 0
   args["if_TNM"] = 1
   print("---- TNM ----")
   vanilla_w_diff_bias()
   
# section 4.6.3 - 2 precision
def read_results_and_plot():
   'Produce results immediately'

   # read results and plot Precision-Percentage increase curve
   # read csv into df
   filenames = ["MeanWT_25riders_weibull", "MeanWT_25riders_TNM",  "MeanWT_30riders_weibull","MeanWT_30riders_TNM",]
   bigdf = pd.DataFrame()
   bigdf["Precision of FPT Prediction"] = [100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
   for f in filenames:
      
      df = pd.read_csv("results/"+f+".csv")
      df["Percentage Increase in WT"] = round((df["Avg Wait Time (min)"] - df["Avg Wait Time (min)"][0])/df["Avg Wait Time (min)"][0] * 100,2)
      df = df[:-1]
      bigdf[f] = df["Percentage Increase in WT"]
      
      
   # plot line graph 
   plt.plot(bigdf["Precision of FPT Prediction"], bigdf[filenames], marker='o', markersize=5)
   plt.legend(filenames)
   plt.grid()
   plt.xlabel("Precision of FPT Prediction (%)")
   plt.ylabel("Percentage Increase in WT \n (as compared to perfect prediction)")
   plt.xticks(np.arange(0, 110, 10))
   plt.yticks(np.arange(0, 14, 1))
   plt.xlim(0,100)
   plt.ylim(0,13)
   plt.title("Percentage Increase in WT VS Precision of FPT Prediction\n")
   plt.savefig("results/Precision_and_MeanWT.png")
   plt.close( )






# vanilla_w_diff_bias_diff_FPT()
read_results_and_plot()

   


  


