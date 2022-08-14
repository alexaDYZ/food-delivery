from config import args
from utils import dotdict
import random
import numpy as np

from Order import Order
from Restaurant import Restaurant
from Customer import Customer
from Rider import Rider

'''
This file generate data needed for the simulation. Data generated is saved to perform simulations of different 
allocation algorithm. Data generated includes:
1) restaurant_list
2) rider_list
3) customer_list
4) order_time
5) order_list
'''

# generate locations for restaurants, customers and riders
restaurant_loc = np.random.randint(0, args["gridSize"], size=(args["numRestaurants"],2))
food_prep_time = [random.expovariate(1/args["avgFoodPrepTime"]) for i in range(args["numRestaurants"])]
restaurant_list = [Restaurant(i, restaurant_loc[i], food_prep_time[i], args) for i in range(args["numRestaurants"])]

rider_loc = np.random.randint(0,args["gridSize"], size=(args["numRiders"],2))
rider_list = [Rider(i, rider_loc[i],args) for i in range(args["numRiders"])]

customer_loc = np.random.randint(0,args["gridSize"], size=(args["numCustomers"],2))
customer_list = [Customer(customer_loc[i],args) for i in range(args["numCustomers"])]

# generate list of orders, with index, time, customer, restaurant
order_time = [random.expovariate(1/args["avgOrderTime"]) for i in range(args["numOrders"])]
order_time.sort()




order_list = [] # store all the orders generated

def generateOrders():
    customer_list_copy = customer_list.copy()
    order_time_copy = order_time.copy()
    for i in range(args["numOrders"]):
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