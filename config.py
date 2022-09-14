
from utils import dotdict
''' Program Settings'''

# set key args
args = dotdict({
    "numEpisode":100, # for averaging 
    
    "gridSize": 50, # 10
    
    # for each time window
    "totalTime": 1000,
    "numOrders": -1, # same as num customers, initiliazed with -1. Assigned in generateData.py
    "numCustomers": -1,
 
    "orderLambda": 4, # expected number of orders per minute
    # "numRepeatedWindow":1, 

    "numRiders": 100,
    "numRestaurants": 5,
    
    
    "FPT_avg": 15, 
    "FPT_sd":0,
    "riderSpeed":1,

    "riderSelectionThreshold": 100000,
    "forwardLookingTime": 15,
    "reassignTime": 2, 
    
    "statusCheckInterval":5, # interval for regularly checking rider status

    "MA_batchsize": 10, # moving average batch size
    
    # boolean variables:
    "showOrderTimeDist": 0,
    "printCheckPt": 0,
    'regularcheck':0,
    
    "showWTplot": 0, # waiting time, see Analyse_WaitingTime.py
    "showEventPlot": 1, #  waiting time, see Simulation.py
    "movingAvegrageAnalysis": 1,
    
    
    # list of colors for plot
    "colorls": ['lightcoral', 'gold', 'forestgreen', 'royalblue',
                'indigo', 'black', 'darkgrey', 'orange', 'cyan',
                'red', 'olive']
    
    
})