# from Analyse_NumOrders import AnalyseNumOrders
# from Analyse_Rider import Analyse_Rider
# from Analyse_DroppedOrders import Analyse_DroppedOrders
# from make_waiting_time_plot_ClosestToFPT import WaitingTimePLot
# from make_waiting_time_plot_bulk import WaitingTimePLot
from make_waiting_time_plot_all import WaitingTimePLot
import datetime
from Analyse_Orders import Simple
from AnticipationMethod import AnticipationMethod
from DefaultMethod_1b import DefaultMethod_1b
import sys
from Experiment_FPT import experiment1, experiment2, experiment3




def main():
   

   
   
   startTime = datetime.datetime.now()
   # experiment1()
   experiment2()
   # experiment3()
   # AnalyseNumOrders()
   # AnalyseRider()
   # a = Analyse_DroppedOrders() # Default_1a
   # a = AnalyseWaitingTime() # Default_1b
   # a = Analyse_Rider() # analyse equality in job allocation
   # a.visualizeMaxMin()
   # a.visualizeRoute()

   # a = WaitingTimePLot()
   # a.add_method("AnticipationMethod") 
   # a.add_method("DefaultMethod_1b")
   # a.plot()
   # a.test_assign_later()
   # a.run()
   # a = WaitingTimePLot()
   # a.add_method("AssignLaterMethod_UsefulWork")
   # a.add_method("AssignLaterMethod")
   # a.add_method("UsefulWorkMethod")
   # a.add_all_methods()
   def compare_anticipation_w_waiting():
      a.add_method("AnticipationMethod") 
      anti_waiting = AnticipationMethod()
      # anti_waiting.setWalkingRule("Nearest Restaurant")
      anti_waiting.setWalkingRule("Probabilistic")
      # a.add_additional_method(anti_waiting, color_ls  = ["yellow", "yellow", "lightyellow", "lightyellow", "lightyellow"])
      a.add_additional_method(anti_waiting, color_ls  = ["green", "green", "lightgreen", "lightgreen", "lightgreen"])

      
      # a.add_method("DefaultMethod_1b") 
      # default_waiting = DefaultMethod_1b()
      # # default_waiting.setWalkingRule("Nearest Restaurant")
      # default_waiting.setWaitingRule("Probabilistic")
      # a.add_additional_method(default_waiting, color_ls  = ["green", "green", "lightgreen", "lightgreen", "lightgreen"])
      # # a.add_additional_method(default_waiting, color_ls  = ["yellow", "yellow", "lightyellow", "lightyellow", "lightyellow"])
      
      a.plot()
   # compare_anticipation_w_waiting()

   # a = Simple()
   # a.add_method("DefaultMethod_1b")
   # # default_waiting = DefaultMethod_1b()
   # # default_waiting.setWalkingRule("Nearest Restaurant")
   # # a.add_additional_method(default_waiting)
   # a.add_method("AnticipationMethod")
   # # anti_waiting = AnticipationMethod()
   # # anti_waiting.setWalkingRule("Probabilistic")
   # # a.add_additional_method(anti_waiting)
   # a.run()
   # run this in terminal: python3 main.py &> out.txt
   

   endTime = datetime.datetime.now()
   print("Time taken: ", endTime - startTime)



if __name__ == "__main__":
   main()
