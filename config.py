
from utils import dotdict
''' Program Settings'''

# set key args
args = dotdict({
    "numEpisode":100, # for averaging 
    
    "gridSize": 10,
    
    # per time window
    "numOrders":20, # same as num customers
    "numCustomers": 40,
    
    
    "numRiders": 10,
    "numRestaurants": 5,
    
    "avgOrderTime": 50, # order appear time # originally 60
    "numRepeatedWindow":10, # n umber of repeated window across the same tiemline
    
    
    "FPT_avg": 15, 
    "FPT_sd":5,
    "riderSpeed":1,

    "riderSelectionThreshold": 100000,
    "forwardLookingTime": 5,
    
    "statusCheckInterval":10, # interval for regularly checking rider status
})