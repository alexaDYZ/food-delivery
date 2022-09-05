from config import args
from utils import dotdict
import random
import numpy as np

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
    # resturants  
    # location and food prep time
    restaurant_loc = np.random.randint(0, args["gridSize"], 
                                        size=(args["numRestaurants"],2))
    # food preptime: normal distribution
    fpt_mean = args["FPT_avg"]
    fpt_sd = args["FPT_sd"]
    food_prep_time = np.random.normal(fpt_mean, fpt_sd, args["numRestaurants"]).tolist()

    # uniform distribution in 2d space
    restaurant_list = [Restaurant(i, restaurant_loc[i], food_prep_time[i], args) 
                       for i in range(args["numRestaurants"])]
        
    # riders
    # location
    rider_loc = np.random.randint(0,args["gridSize"], 
                                    size=(args["numRiders"],2))
    rider_list = [Rider(i, rider_loc[i],args) 
                    for i in range(args["numRiders"])]

    
    customer_loc, customer_list, order_time=[],[],[]
    
    # for peiord in range(1, args["numRepeatedWindow"]+1):
    #     loc = np.random.randint(0, args["gridSize"], size=(args["numCustomers"],2)).tolist()
    #     customer_list += [Customer(loc[i],args) 
    #                       for i in range(args["numCustomers"])]
    #     customer_loc += loc

    #     # generate list of orders, with index, time, customer, restaurant
        
    #     time = np.random.poisson(lam = args["orderLambda"], size = args["numOrders"]).tolist()
    #     order_time += [t + peiord*2*args["orderLambda"] for t in time]
    
    loc = np.random.randint(0, args["gridSize"], size=(args["numCustomers"],2)).tolist()
    customer_list += [Customer(loc[i],args) 
                        for i in range(args["numCustomers"])]
    customer_loc += loc

    # generate list of orders, with index, time, customer, restaurant
    
    order_time = np.random.poisson(lam = args["orderLambda"], size = args["numOrders"]).tolist()
        
    order_time.sort() # small to large
    # print("number of orders:" ,len(order_time))
    # print(order_time)


    order_list = [] # store all the orders generated

    def generateOrders():
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

    generateOrders() # update 'orders' list


    # save data
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


