
from utils import dotdict
''' Program Settings'''

# set key args
args = dotdict({
    "numEpisode":1000,

    "gridSize": 10,
    "numOrders":30, # same as num customers
    "numCustomers": 30,
    "numRiders": 3,
    "numRestaurants": 5,
    "avgOrderTime": 60, # order appear time
    "avgFoodPrepTime": 7, 
    "riderSpeed":1,

    "riderSelectionThreshold": 100000,
    "forwardLookingTime": 5,
})