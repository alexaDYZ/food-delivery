
from utils import dotdict
''' Program Settings'''

# set key args
args = dotdict({
    "numEpisode":100, # for averaging 
    
    "gridSize": 10,
    "numOrders":30, # same as num customers
    "numCustomers": 30,
    "numRiders": 3,
    "numRestaurants": 5,
    "avgOrderTime": 60, # order appear time
    "FPT_avg": 15, 
    "FPT_sd":5,
    "riderSpeed":1,

    "riderSelectionThreshold": 100000,
    "forwardLookingTime": 5,
})