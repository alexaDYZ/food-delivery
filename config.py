
from utils import dotdict
''' Program Settings'''

# set key args
args = dotdict({
    "numSimulations":100, # for averaging, 100
    
    "gridSize": 1000, # unit: m, default is 1000

    "useMcData": 1, # if we use the data from the McDelivery dataset
    
    # for each time window
    # "totalTime": 1000,
    # "numOrders": 2000, # same as num customers, initiliazed with -1. Assigned in generateData.py
    # "numCustomers": 2000, 
    'numOrders': None, # to be assigned in generateData.py
    'numCustomers': None,   # to be assigned in generateData.py
    'simulationTime': 60*60*12, # unit: s, 24 hours

    "orderArrivalRate": round(1/30,3), # unit: number per second. default is 1/30, meaning 2 per minute

    "numRiders": 30,
    "numRestaurants": 20, # originally 20
    
    # For food preparation time
    "if_truncated_normal": 0, # if we use truncated normal distribution for food preparation time
    "FPT_avg": 600, # unit: s # second # average food preparation time. default is 300
    "FPT_sd":100,
    "FPT_lower": 100, # lower bound of truncated normal distribution
    "FPT_upper": 500, # upper bound of truncated normal distribution

    "riderSpeed":1, # unit m/s

    # "riderSelectionThreshold": 100000,
    # "forwardLookingTime": 3000, # unit: s 300
    # "reassignTime": 60,  # unit: s
    
    "statusCheckInterval":5, # interval for regularly checking rider status

    "SMA_batchsize": 20, # moving average batch size
    "IA_interval": 60*30, # unit: s # simple moving average interval
    
    # boolean variables:
    "printAssignmentProcess": 0,
    "saveAssignmentHistory":1,
    "showOrderTimeDist": 0,
    "printCheckPt": 0,
    'regularcheck':0,
    
    "showWTplot": 0, # waiting time, see Analyse_WaitingTime.py
    "showEventPlot": 0, #  waiting time, see Simulation.py
    
    "showCMA_wait_time": 0, # cumulative moving average of waiting time
    "doMultipleExperiments":0, # generate a csv for numEpisode number of experiments
    "findCompetitiveRatio":1, # find the competitive ratio for the given numRiders
    "saveCRhistory": 0, # save the CR history for each numRiders
    "showRoute": 0, # plot rider's route
    
    # list of colors for plot
    "colorls": ['lightcoral', 'gold', 'forestgreen', 'royalblue',
                'indigo', 'black', 'darkgrey', 'orange', 'cyan',
                'red', 'olive'],

    "path": "./sem2_w3/McData/",
    
})