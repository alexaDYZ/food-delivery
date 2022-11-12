from Analyse_NumOrders import AnalyseNumOrders
from Analyse_Rider import Analyse_Rider
from Analyse_WaitingTime import AnalyseWaitingTime
from Analyse_DroppedOrders import Analyse_DroppedOrders


def main():
   # AnalyseNumOrders()
   # AnalyseRider()
   a = Analyse_DroppedOrders() # Default_1a
   # a = AnalyseWaitingTime() # Default_1b
   # a = Analyse_Rider()
   # a.visualizeMaxMin()
   # a.visualizeRoute()
   a.run()
   pass


if __name__ == "__main__":
   main()