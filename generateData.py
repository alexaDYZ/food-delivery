from config import args
from utils import dotdict
import random
import numpy as np
import pandas as pd
from scipy.stats import poisson
import scipy.stats as stats
from matplotlib import pyplot as plt
import datetime



from Order import Order
from Restaurant import Restaurant
from Customer import Customer
from Rider import Rider
import copy

'''
This file generate data needed for the simulation. Data generated is saved to perform simulations of different 
allocation algorithm. Data generated includes:
1) restaurant_list
2) rider_list
3) customer_list
4) order_time
5) order_list
'''

def dataGeneration():

    '''
    This fucntion generates locations for restaurants, customers and riders
    '''
    
    
    ''' resturant list: restaurant = (location, food prep time) for reach restaurant '''
    def generateRestaurantLocation(numRestaurants, gridSize):
        # uniform distribution in 2d space
        res = np.random.randint(0, gridSize, size=(numRestaurants,2))
        return res
    
    def generateFPT():
        # food preptime: normal distribution
        
        
        if args["if_truncated_normal"]:
            fpt_sd = args["FPT_sd"]
            print("Using truncated normal distribution for food preparation time")
            food_prep_time = stats.truncnorm((args["FPT_lower"] - fpt_mean) / fpt_sd,
                                            (args["FPT_upper"] - fpt_mean) / fpt_sd, 
                                            loc=fpt_mean, scale=fpt_sd).rvs(args["numRestaurants"]).tolist()
            #### debug #######
            showFPTplot = 0 # for 1 simulation only
            if showFPTplot:
                plt.hist(food_prep_time)
                plt.suptitle("Food preparation time distribution of the Simulations")
                plt.title("(" + str(args['numRestaurants']) + " Restaurants)")
                plt.xlabel("Food preparation time (s)")
                plt.ylabel("Frequency")

                params = ("_lambda" + str(args["orderArrivalRate"]) 
                        + "_numRider"+str(args['numRiders'])
                        + "_numRest"+str(args['numRestaurants'])
                        + "_bacthSize" + str(args['SMA_batchsize'])
                        + "_gridSize" + str(args['gridSize'])
                        + "_FPT" + str(args["FPT_avg"])
                        + "_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

                plt.savefig(args["path"] + "FPT_distribution" + params + ".png", dpi=300)
            #### debug #######
        else:
            fpt_mean = args["FPT_avg"]
            food_prep_time = np.random.normal(fpt_mean, 0, args["numRestaurants"]).tolist()
        return food_prep_time
    
    def generateRestaurantList(numRestaurants, gridSize):
        restaurant_loc = generateRestaurantLocation(numRestaurants, gridSize)
        food_prep_time = generateFPT()
        # combine location an corresponding food prep time
        restaurant_list = [Restaurant(i, restaurant_loc[i], food_prep_time[i], args) 
                        for i in range(args["numRestaurants"])]
        return restaurant_list
            
    ''' rider list: rider = (initial location) for reach restaurant '''
    def generateRiderList(num, gridSize):
        rider_loc = np.random.randint(0, gridSize, size=(num,2))
        rider_list = [Rider(i, rider_loc[i],args) for i in range(num)]
        return rider_list


    '''Initialize Orders and customers'''

    # Synthetic data
    def generateSyntheticOrderTime():
        order_time = []
        rate = args["orderArrivalRate"]
        
            # Order arrivals follows a Posisson process, with mean rate lambda = args["orderRate"]
            # Interarrival time follows an exponential distribution with mean 1/lambda
            # random.expovariate(arrival_rate) -> interarrival time

        t = 0
        while True:
            t += random.expovariate(rate)
            if t < args["simulationTime"]:
                order_time.append(t)
            else:
                break
        order_time = [round(t,2) for t in order_time]
        # old version: order_time = np.random.poisson(lam = args["orderArrivalRate"], size = args["numOrders"]).tolist()
        args['numOrders'] = len(order_time)
        return order_time
    
    # # McDonald data
    # def getMcOrderTime(mcdf):
    #     order_time = []
    #     for i in range(len(mcdf["phTimeStart_s"])):
    #         order_time.append(mcdf.iloc[i]['phTimeStart_s'])
    #     args['numOrders'] = len(order_time)
    #     return order_time

    def generateCutomerList():
        # Customer:
        customer_list = []
        args['numCustomers'] = args['numOrders']
        loc = np.random.randint(0, args["gridSize"], size=(args["numCustomers"],2)).tolist()
        customer_list += [Customer(loc[i],args) for i in range(args["numCustomers"])]
        return customer_list
    
        
    
    def generateOrderList(restaurant_list, order_time, customer_list):
        order_list = [] # store all the orders generated
        order_time.sort() # small to large
        customer_list_copy = copy.deepcopy(customer_list)
        order_time_copy = copy.deepcopy(order_time)
        order_time_copy.sort(reverse=True)
        for i in range(len(order_time)):
            c = customer_list_copy.pop()
            r_index = random.randint(0,args["numRestaurants"]-1)
            r = restaurant_list[r_index]
            t = order_time_copy.pop()
            o = Order(i, t,c,r)
            order_list.append(o)
        return order_list

    # The main function

    ## generate data
    useMcData = args["useMcData"]
    if useMcData:
        import pickle
        with open('data_mc_orders.ls', 'rb') as data_file:
            order_time = pickle.load(data_file)
        args['simulationTime'] = max(order_time)
        args['numOrders'] = len(order_time)
        args['numRestaurants'] = 20 # from dataset 
    
        restaurant_list = generateRestaurantList(args["numRestaurants"], args["gridSize"])
        rider_list = generateRiderList(args["numRiders"], args["gridSize"])
        customer_list = generateCutomerList()
        
    else:
        restaurant_list = generateRestaurantList(args["numRestaurants"], args["gridSize"])
        rider_list = generateRiderList(args["numRiders"], args["gridSize"])
        order_time = generateSyntheticOrderTime()
        customer_list = generateCutomerList()
    
    order_list = generateOrderList(restaurant_list, order_time, customer_list)


    ## save data
    import pickle
    data = dotdict({
        'restaurant list': restaurant_list, 
        "rider list":rider_list, 
        "order list":order_list, 
        "customer list": customer_list,
        "order time" : order_time,
    })
    # data_dictionary = {'restaurant list': restaurant_list, "rider list":rider_list, "order list":order_list, "customer list": customer_list}
    with open('data.dict', 'wb') as data_file:
        pickle.dump(data, data_file)


