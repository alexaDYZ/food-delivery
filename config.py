
from utils import dotdict
''' Program Settings'''

# set key args
args = dotdict({
    "numEpisode":100, # for averaging 
    
    "gridSize": 50, # 10
    
    # for each time window
    "numOrders": 10, # same as num customers
    "numCustomers": 10,
    
    "orderLambda": 10, # 10
    "numRepeatedWindow":1, 

    "numRiders": 2,
    "numRestaurants": 5,
    
    
    "FPT_avg": 15, 
    "FPT_sd":5,
    "riderSpeed":1,

    "riderSelectionThreshold": 100000,
    "forwardLookingTime": 5,
    "reassignTime": 2, 
    
    "statusCheckInterval":5, # interval for regularly checking rider status
    
    # boolean variables:
    "showOrderTimeDist": 0,
    "printCheckPt": 0,
    'regularcheck':0,
    
    "showWTplot": 0, # waiting time
    "showEventPlot": 1, #  waiting time
    
    
    # list of colors for plot
    "colorls": ['lightcoral', 'gold', 'forestgreen', 'royalblue',
                'indigo', 'black', 'darkgrey', 'orange', 'cyan',
                'red', 'olive']
    
    
})