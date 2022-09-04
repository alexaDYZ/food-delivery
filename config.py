
from utils import dotdict
''' Program Settings'''

# set key args
args = dotdict({
    "numEpisode":100, # for averaging 
    
    "gridSize": 100, # 10
    
    # for each time window
    "numOrders": 8, # same as num customers
    "numCustomers": 8,
    
    "avgOrderTime": 5, # 10
    "numRepeatedWindow":1, 

    "numRiders": 2,
    "numRestaurants": 5,
    
    
    "FPT_avg": 15, 
    "FPT_sd":5,
    "riderSpeed":1,

    "riderSelectionThreshold": 100000,
    "forwardLookingTime": 5,
    "reassignTime": 1, 
    
    "statusCheckInterval":10, # interval for regularly checking rider status
    
    # boolean variables:

    
})