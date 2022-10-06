from Order import Order
from Customer import Customer
from Restaurant import Restaurant
from config import args
from Rider import Rider
import numpy as np
import matplotlib.pyplot as plt



rider_loc = np.random.randint(0,args["gridSize"], 
                                    size=(args["numRiders"],2))
rider_list = [Rider(i, rider_loc[i],args) 
                for i in range(args["numRiders"])]
rider_list.sort()
print([r.index for r in rider_list])
# # c = Customer((10,1), args)
# # r = Restaurant(1, (10,10), 10, args)
# id = [1,2,3,4,5]
# t = [10,20,30,40,50]
# # t.sort(reverse=True)
# # ls = []
# # for i,time in zip(id, t):
# #     o = Order(i, time, c, r)
# #     ls.append(o)

# # ls.sort()
# # for o in ls:
# #     o.print()

# for i in range(len(id) - 3 + 1):
#     print(id[i:i+3])
