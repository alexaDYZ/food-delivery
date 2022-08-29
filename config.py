
from utils import dotdict
''' Program Settings'''

# set key args
args = dotdict({
    "numEpisode":100, # for averaging 
    
    "gridSize": 10,
    "numOrders":150, # same as num customers
    "numCustomers": 150,
    "numRiders": 3,
    "numRestaurants": 5,
    "avgOrderTime": 300, # order appear time # originally 60
    "FPT_avg": 15, 
    "FPT_sd":5,
    "riderSpeed":1,

    "riderSelectionThreshold": 100000,
    "forwardLookingTime": 5,
})