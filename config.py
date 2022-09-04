
from utils import dotdict
''' Program Settings'''

# set key args
args = dotdict({
    "numEpisode":100, # for averaging 
    
    "gridSize": 10,
    
    # for each time window
    "numOrders": 40, # same as num customers
    "numCustomers": 40,
    
    "avgOrderTime": 10, # 
    "numRepeatedWindow":10, # 100 min
    
    "numRiders": 50,
    "numRestaurants": 5,
    
    
    "FPT_avg": 15, 
    "FPT_sd":5,
    "riderSpeed":1,

    "riderSelectionThreshold": 100000,
    "forwardLookingTime": 5,
    
    "statusCheckInterval":10, # interval for regularly checking rider status
    
    
})