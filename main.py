from Analyse_NumOrders import AnalyseNumOrders
from Analyse_Rider import Analyse_Rider
from Analyse_DroppedOrders import Analyse_DroppedOrders
from make_waiting_time_plot import WaitingTimePLot
# from make_waiting_time_plot_ClosestToFPT import WaitingTimePLot
# from make_waiting_time_plot_bulk import WaitingTimePLot
from make_waiting_time_plot_all import WaitingTimePLot
import datetime
from Analyse_Orders import Simple


def main():
   # AnalyseNumOrders()
   # AnalyseRider()
   # a = Analyse_DroppedOrders() # Default_1a
   # a = AnalyseWaitingTime() # Default_1b
   # a = Analyse_Rider() # analyse equality in job allocation
   # a.visualizeMaxMin()
   # a.visualizeRoute()
   startTime = datetime.datetime.now()
   a = WaitingTimePLot()
   # a.run()
   # a = WaitingTimePLot()
   # a.add_method("AssignLaterMethod_UsefulWork")
   # a.add_method("AssignLaterMethod")
   # a.add_method("UsefulWorkMethod")
   a.add_all_methods()
   a.plot()

   # a = Simple()
   # a.add_all_methods()
   # a.run()

   endTime = datetime.datetime.now()
   print("Time taken: ", endTime - startTime)


if __name__ == "__main__":
   main()
