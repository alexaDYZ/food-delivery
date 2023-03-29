
from utils import dotdict
''' Program Settings'''

# set key args
args = dotdict({
    "numSimulations":100, # for averaging, 100
    
    "gridSize": 1000, # unit: m, default is 1000

    "useMcData": 0, # if we use the data from the McDelivery dataset

    'numOrders': None, # to be assigned in generateData.py
    'numCustomers': None,   # to be assigned in generateData.py
    'simulationTime': 60*60*12, # unit: s, 60*60*12 # 12 hours
    'stallingTime': 60*3,   # unit: s, 3 min. For PatientAnticipativeMethods


    "orderArrivalRate": round(1/30,3), # unit: number per second. default is 1/30, meaning 2 per minute

    "numRiders": 30, # default: 30
    "numRestaurants": 20, # default: 20
    
    # FPT distribution
    # "FPT_pred": 50*60,
    "if_truncated_normal": 0, # if we use truncated normal distribution for food preparation time
    "if_TNM": 0, # if we use TNM to model FPT
    "weibull": 0, # if we use weibull distribution for food preparation time
    "mean_estimator": 0, # the actual mean of the distribution, set in "generateData.py"
    "TNM_weights": [0.2, 0.5, 0.25, 0.05],
    "FPT_avg": 60*30, # unit: s # second # average food preparation time. default is 600
    "FPT_sd":200,
    "FPT_lower": 300, # lower bound of truncated normal distribution
    "FPT_upper": 1200, # upper bound of truncated normal distribution


    "riderSpeed":1, # unit m/s

    "threshold_assignment_time": 10*60 , # unit: s, 35 min. For AssignLaterMethod

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

    "path": "./results/",

})
