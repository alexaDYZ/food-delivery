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
import scipy.stats as stats


# def getLocation(self, currTime):
#     if self.status == 2: # rider is walking
#         t_start, t_end, loc_start, loc_dest = self.walking_path
#         if t_start <= currTime <= t_end:
#             return loc_start + (loc_dest - loc_start) * (currTime - t_start)/(t_end - t_start)
#         elif currTime > t_end:
#             print("Error: Rider should have finished walking, but status is not updated")
#         else:
#             print("Error: see getLocation() in Rider.py")
#     else:
#         print("Error: Rider is not in walking mode")
#         pass

t_s = 0
loc_s = np.array([0,0])
loc_end = np.array([10,0])
t_e = math.dist(loc_s, loc_end)/args["riderSpeed"]

t_inquiry = 5
# curr_loc_x = loc_s + (loc_end[0] - loc_s[0]) * (t_inquiry - t_s)/(t_e - t_s)
# curr_loc_y = loc_s + (loc_end[1] - loc_s[1]) * (t_inquiry - t_s)/(t_e - t_s)
# curr_loc = (curr_loc_x, curr_loc_y)
curr_loc = loc_s + (loc_end - loc_s) * (t_inquiry - t_s)/(t_e - t_s)
print(curr_loc)
print(type(curr_loc))



# def generate_a_FPT():
#     '''Generate a FPT for the restaurant'''
#     means = [i*60 for i in [10, 20, 40, 60]]
#     stds = [i*60 for i in [2, 5, 5, 10]]
#     upper = [i*60 for i in [20, 40, 60, 100]]
#     lower = [i*60 for i in [5, 10, 20, 40]]

#     i = 3
#     FPT = stats.truncnorm((lower[i] - means[i]) / stds[i],
#                                         (upper[i] - means[i]) / stds[i], 
#                                         loc=means[i], scale=stds[i]).rvs(1).tolist()[0]
#     FPT = round(FPT, 2)
#     return FPT

# print(generate_a_FPT())




# # total_num = 10000
# # weights = [0.2, 0.5, 0.25, 0.05]
# # # check if weights sum to 1
# # print(sum(weights))

# # fast = np.random.normal(10, 2, int(total_num*weights[0]))
# # normal = np.random.normal(20, 5, int(total_num*weights[1]))
# # slow = np.random.normal(40, 5, int(total_num*weights[2]))
# # very_slow = np.random.normal(60, 10, int(total_num*weights[3]))
# # # all = np.concatenate((fast, normal, slow, very_slow))
# # fast = stats.truncnorm.rvs((5 - 10) / 2, (20 - 10) / 2, loc=10, scale=2, size=int(total_num*weights[0])) # range : 5-20
# # normal = stats.truncnorm.rvs((10 - 20) / 5, (40 - 20) / 5, loc=20, scale=5, size=int(total_num*weights[1])) # range : 10-40
# # slow = stats.truncnorm.rvs((20 - 40) / 5, (60 - 40) / 5, loc=40, scale=5, size=int(total_num*weights[2])) # range : 20-60
# # very_slow = stats.truncnorm.rvs((40 - 60) / 10, (100 - 60) / 10, loc=60, scale=10, size=int(total_num*weights[3])) # range : 40-100
# # all = np.concatenate((fast, normal, slow, very_slow))

# # # 1 bin for 1 unit

# # plt.hist(all, bins=95, alpha=0.5, label='all')
# plt.hist(fast, bins=15, alpha=0.5, label='fast')
# plt.hist(normal, bins=30, alpha=0.5, label='normal')
# plt.hist(slow, bins=40, alpha=0.5, label='slow')
# plt.hist(very_slow, bins=60, alpha=0.5, label='very_slow')

# plt.legend(loc='upper right')
# plt.xlim(0, 100)
# plt.xticks(np.arange(0, 100, 5))
# plt.xlabel('FPT (min)')
# plt.yticks(np.arange(0, 500, 100))
# plt.ylabel('Frequency')
# plt.title('FPT Distribution\n (total number = 10000)')

# plt.show()