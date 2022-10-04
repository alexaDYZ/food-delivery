# from Order import Order
# from Customer import Customer
# from Restaurant import Restaurant
# from config import args




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
import numpy as np

import matplotlib.pyplot as plt

ls = []
for i in range(10):
    interval = np.random.poisson(30)
    ls.append(interval)
    # if len(ls) != 0:
    #     next_t = ls[-1] + interval
    # else:
    #     next_t = 0 + interval
    # ls.append(next_t)
print(ls)

# plt.plot(ls, np.zeros_like(ls), "-o")
# for i in ls:
#     plt.annotate(str(i), (i, 0))
# plt.show()