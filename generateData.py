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
    
        ''' resturant list: restaurant = (location, food prep time) for reach restaurant '''
    
    def generateRestaurantList(numRestaurants, gridSize):
        # uniform distribution in 2d space
        loc_ls = np.random.randint(0, gridSize, size=(numRestaurants,2))
        restaurant_list = [Restaurant(i, loc_ls[i], None, args) 
                        for i in range(args["numRestaurants"])]
        return restaurant_list
    
    def generateFPT():
        # Food Preparation Time(FPT): 
        # A list of length numOrders, each element is the food preparation time for the corresponding order
        
        if args["if_truncated_normal"]:
            fpt_sd = args["FPT_sd"]
            fpt_mean = args["FPT_avg"]
            print("Using truncated normal distribution for food preparation time")
            food_prep_time = stats.truncnorm((args["FPT_lower"] - fpt_mean) / fpt_sd,
                                            (args["FPT_upper"] - fpt_mean) / fpt_sd, 
                                            loc=fpt_mean, scale=fpt_sd).rvs(args['numOrders']).tolist()
            #### debug #######
            showFPTplot = 0# for 1 simulation only
            if showFPTplot:
                fpt_in_minute = [round(i/60, 3) for i in food_prep_time]
                plt.hist(fpt_in_minute, bins=15, alpha=0.5)
                plt.title('FPT Distribution (Truncated Normal)\n ('+ str(len(fpt_in_minute))+' orders)')
                plt.xlabel("FPT (min)")
                plt.ylabel("Frequency")
                plt.xticks(np.arange(0, 21, 5))

                params = ("_lambda" + str(args["orderArrivalRate"]) 
                        + "_numRider"+str(args['numRiders'])
                        + "_numRest"+str(args['numRestaurants'])
                        + "_bacthSize" + str(args['SMA_batchsize'])
                        + "_gridSize" + str(args['gridSize'])
                        + "_FPT" + str(args["FPT_avg"])
                        )

                plt.savefig(args["path"] + "FPT_distribution" + params + ".png", dpi=300)
            #### debug #######
        elif args['if_TNM']:
            # suppose we have 4 clusters, all are modeled as truncated normal distribution
            total_num = args['numOrders']
            weights = args["TNM_weights"]
            means = [i*60 for i in [10, 30, 40, 60]]
            stds = [i*60 for i in [2, 5, 5, 10]]
            upper = [i*60 for i in [20, 40, 60, 100]]
            lower = [i*60 for i in [5, 10, 20, 40]]
            groups = []
            group_names = ['fast', 'normal', 'slow', 'very_slow']
            food_prep_time = []
            
            for i in range(len(group_names)):
                if i == len(group_names) - 1:  num_orders = int(total_num - len(food_prep_time)) # to avoid rounding error
                else: num_orders = int(total_num*weights[i])
                group = stats.truncnorm((lower[i] - means[i]) / stds[i],
                                            (upper[i] - means[i]) / stds[i], 
                                            loc=means[i], scale=stds[i]).rvs(num_orders).tolist()
                group = [round(x,2) for x in group]
                groups.append(group) # debug
                food_prep_time.extend(group) 
            print("TNM - mean FPT = ", str(round(np.mean(food_prep_time)/60,2)))

            
            #### debug #######
            showFPTplot = False # for 1 simulation only
            if showFPTplot:
                for i in range(len(group_names)):
                    # plot in minutes
                    data = [x/60 for x in groups[i]]
                    plt.hist(data, bins=int(max(data)-min(data)), alpha=0.5, label=group_names[i])
                
                plt.legend(loc='upper right')
                plt.xlim(0, 100)
                plt.xticks(np.arange(0, 105, 5))
                plt.xlabel('FPT (min)')
                # plt.yticks(np.arange(0, 500, 100))
                plt.ylabel('Frequency')
                plt.title('FPT Distribution (Mixture of Truncated Normal)\n ('+ str(total_num)+' orders)')

                params = ("_lambda" + str(args["orderArrivalRate"]) 
                        + "_numRider"+str(args['numRiders'])
                        + "_numRest"+str(args['numRestaurants'])
                        + "_bacthSize" + str(args['SMA_batchsize'])
                        + "_gridSize" + str(args['gridSize'])
                        + "_FPT" + str(args["FPT_avg"])
                        + "_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

                plt.savefig(args["path"] + "FPT_TNM" + params + ".png")
                plt.close()
        elif args['weibull']:
            print("Using Weibull distribution for food preparation time")
            k = 2
            # l = 21.807
            l = 22.5
            samples = np.random.weibull(k, args['numOrders']) * l
            fpt = [round(x+10, 2) for x in samples]
            print("weibull - mean FPT = ", str(np.mean(fpt)))


            # for debugging
            args["mean_estimator"]  = np.mean(fpt) # to tell the algorithm, what is the mean FPT

            plot = False
            if plot:
                plt.hist(fpt, bins = 100,alpha=0.5, color='blue')
                plt.title('FPT Distribution (Weibull)\n ('+ str(len(fpt))+' orders)')
                plt.xlabel("FPT (min)")
                plt.ylabel("Frequency")
                plt.savefig(args["path"] + "FPT_weibull" + ".png")
                plt.close()
                
            fpt_in_seconds = [i*60 for i in fpt]
            food_prep_time = np.array(fpt_in_seconds)
        else:
            fpt_mean = args["FPT_avg"]
            food_prep_time = np.random.normal(fpt_mean, 0, args['numOrders']).tolist()
        return food_prep_time
    
         
    def generateOrderList(restaurant_list, order_time, customer_list):
        order_list = [] # store all the orders generated
        order_time.sort() # small to large
        customer_list_copy = copy.deepcopy(customer_list)
        order_time_copy = copy.deepcopy(order_time)
        order_time_copy.sort(reverse=True)
        FPT_list = generateFPT()
        random.shuffle(FPT_list)
        # if args['if_TNM']:
        #     '''each restaurant has a range of FPT'''
        #     FPT_list.sort()


        # else:
        for i in range(len(order_time)):
            c = customer_list_copy.pop()
            r_index = random.randint(0,args["numRestaurants"]-1)
            r = restaurant_list[r_index]
            t = order_time_copy.pop()
            o = Order(i, t, c, r)
            order_list.append(o)
            r.addOrder_FPT(i, FPT_list[i])
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
        restaurant_list = generateRestaurantList(args["numRestaurants"], args["gridSize"]) # locaion only
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


dataGeneration()