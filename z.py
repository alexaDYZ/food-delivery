from Order import Order
from Customer import Customer
from Restaurant import Restaurant
from config import args
from Rider import Rider
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd
import pickle
import math

from PatientAnticipativeMethod_Bulk import PatientAnticipativeMethod_Bulk

a = PatientAnticipativeMethod_Bulk()
print(PatientAnticipativeMethod_Bulk.__name__)
# df = pd.read_csv('./McDonald_data/mc_data_processed.csv')
# print(df.columns)
# print(df["phpsStoreID"].nunique())
# print(max(df["phTimeStart_s"]))

# with open('data_mc_orders.ls', 'rb') as data_file:
#     order_time = pickle.load(data_file)
# print(order_time[:10])


# # def main():
# #     data = [np.random.random((2, 3)) for _ in range(5)]
# #     fig, ax = plt.subplots()
# #     polygons = plot_polygons(data, alpha=0.5, ax=ax, color='gray')
# #     verts = plot_verts(data, marker='s', color='red', ax=ax, s=200)

# #     def on_click(event):
# #         visible = polygons[0][0].get_visible()
# #         plt.setp(polygons, visible=not visible)
# #         plt.setp(verts, color=np.random.random(3))
# #         plt.draw()
# #     fig.canvas.mpl_connect('button_press_event', on_click)

# #     ax.set(title='Click on plot to change')
# #     plt.show()


# # def plot_polygons(data, ax=None, **kwargs):
# #     if ax is None:
# #         ax = plt.gca()

# #     artists = [ax.fill(x, y, **kwargs) for x, y in data]
# #     return artists

# # def plot_verts(data, ax=None, **kwargs):
# #     if ax is None:
# #         ax = plt.gca()

# #     artists = [ax.scatter(x, y, **kwargs) for x, y in data]
# #     return artists
# # l =[i for i in range(10)]
# # print(l)
# # def getAverage(ls):
# #     avgLs = []
# #     for i in range(len(ls)):
# #         curr_avg = sum(ls[:i+1]) / (i+1) # convert to minutes
# #         avgLs.append(curr_avg)
# #     return avgLs
# # def main():
# #     print(getAverage(l))
# # print(sum(l)/len(l))
# # main()


# # rider_loc = np.random.randint(0,args["gridSize"], 
# #                                     size=(args["numRiders"],2))
# # rider_list = [Rider(i, rider_loc[i],args) 
# #                 for i in range(args["numRiders"])]
# # rider_list.sort()
# # print([r.index for r in rider_list])
# # # c = Customer((10,1), args)
# # # r = Restaurant(1, (10,10), 10, args)
# # id = [1,2,3,4,5]
# # t = [10,20,30,40,50]
# # # t.sort(reverse=True)
# # # ls = []
# # # for i,time in zip(id, t):
# # #     o = Order(i, time, c, r)
# # #     ls.append(o)

# # # ls.sort()
# # # for o in ls:
# # #     o.print()

# # for i in range(len(id) - 3 + 1):
# #     print(id[i:i+3])
# def round_up(ls,digit):
#     return [round(i,digit) for i in ls]

# ls = []
# t = 0
# while True:
#     t += random.expovariate(1/30)
#     if t < 60*60*1 :
#         ls.append(t)
#     else: break
# ls= round_up(ls,1)


# # ls_2 = []
# # t2 = 0
# # while len(ls_2)<120:
# #     t2 += (np.random.poisson(30) / 60)
# #     ls_2.append(t2)
# # ls_2 = round_up(ls_2,2)



# print(ls)
# print("empirical rate:", max(ls)/len(ls))
# print("# orders:", len(ls))
# # print(ls_2)

# plt.hist(ls, bins=200, alpha=0.5, label='expovariate')
# # plt.hist(ls_2, bins=20, alpha=0.5, label='poisson')
# # plt.legend()
# plt.show()


#### find probability of number of arrivals within x min > numriders

# def find_prob(arrival_rate, stalling_time, numRiders):
#     # pmf of poisson distribution
#     # P(N(x) = k) = [e^(-lambda * x) * (lambda * x)^k]/k!
#     def find_pmf(k, arrival_rate, stalling_time):
#         return math.exp(-arrival_rate * stalling_time) * (arrival_rate * stalling_time)**k / math.factorial(k)
#     # find probability of number of arrivals within x min > numriders
#     prob = 0
#     cmf_ls = []
#     for i in range(numRiders, 100):
#         prob += find_pmf(i, arrival_rate, stalling_time)
#         cmf_ls.append(prob)
#     print("probability of number of arrivals within {} min > {}: {}".format(stalling_time, numRiders, prob))
#     x = [i for i in range(numRiders, 100)]
#     plt.plot(x, cmf_ls)
#     plt.title("CMF of number of arrivals within {} min > {}".format(stalling_time, numRiders))
#     plt.show()
    

# arrival_rate = 2 # orders per min
# stalling_time = 3 # min
# numRiders = 20
# find_prob(arrival_rate, stalling_time, numRiders)
