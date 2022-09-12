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

s = np.random.poisson(lam=2, size=100)
import matplotlib.pyplot as plt
count, bins, ignored = plt.hist(s, 10, density=True)
print(s)
plt.show()