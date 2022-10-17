
from utils import dotdict
''' Program Settings'''

# set key args
args = dotdict({
    "numRepeat":100, # for averaging 
    
    "gridSize": 1000, # unit: m
    
    # for each time window
    # "totalTime": 1000,
    "numOrders":2000, # same as num customers, initiliazed with -1. Assigned in generateData.py
    "numCustomers": 2000, 

    "orderLambda": 30, # unit: s # second # miu of the poisson process, mean of time interval between 2 orders

    "numRiders": 30,
    "numRestaurants": 20,
    
    
    "FPT_avg": 0, 
    "FPT_sd":0,
    "riderSpeed":1, # unit m/s

    "riderSelectionThreshold": 100000,
    # "forwardLookingTime": 3000, # unit: s 300
    # "reassignTime": 60,  # unit: s
    
    "statusCheckInterval":5, # interval for regularly checking rider status

    "MA_batchsize": 10, # moving average batch size
    
    # boolean variables:
    "printAssignmentProcess": 0,
    "saveAssignmentHistory":1,
    "showOrderTimeDist": 0,
    "printCheckPt": 0,
    'regularcheck':0,
    
    "showWTplot": 0, # waiting time, see Analyse_WaitingTime.py
    "showEventPlot": 0, #  waiting time, see Simulation.py
    
    "showAvgWT": 1,
    "doMultipleExperiments":0, # generate a csv for numEpisode number of experiments
    "findCompetitiveRatio":1, # find the competitive ratio for the given numRiders
    "saveCRhistory": 0, # save the CR history for each numRiders
    
    # list of colors for plot
    "colorls": ['lightcoral', 'gold', 'forestgreen', 'royalblue',
                'indigo', 'black', 'darkgrey', 'orange', 'cyan',
                'red', 'olive'],

    "path": "./week9/",
    
    
})