from Order import Order
from Customer import Customer
from Restaurant import Restaurant
from config import args
from Rider import Rider
import numpy as np
import matplotlib.pyplot as plt


# def main():
#     data = [np.random.random((2, 3)) for _ in range(5)]
#     fig, ax = plt.subplots()
#     polygons = plot_polygons(data, alpha=0.5, ax=ax, color='gray')
#     verts = plot_verts(data, marker='s', color='red', ax=ax, s=200)

#     def on_click(event):
#         visible = polygons[0][0].get_visible()
#         plt.setp(polygons, visible=not visible)
#         plt.setp(verts, color=np.random.random(3))
#         plt.draw()
#     fig.canvas.mpl_connect('button_press_event', on_click)

#     ax.set(title='Click on plot to change')
#     plt.show()


# def plot_polygons(data, ax=None, **kwargs):
#     if ax is None:
#         ax = plt.gca()

#     artists = [ax.fill(x, y, **kwargs) for x, y in data]
#     return artists

# def plot_verts(data, ax=None, **kwargs):
#     if ax is None:
#         ax = plt.gca()

#     artists = [ax.scatter(x, y, **kwargs) for x, y in data]
#     return artists
l =[i for i in range(10)]
print(l)
def getAverage(ls):
    avgLs = []
    for i in range(len(ls)):
        curr_avg = sum(ls[:i+1]) / (i+1) # convert to minutes
        avgLs.append(curr_avg)
    return avgLs
def main():
    print(getAverage(l))
print(sum(l)/len(l))
main()


# rider_loc = np.random.randint(0,args["gridSize"], 
#                                     size=(args["numRiders"],2))
# rider_list = [Rider(i, rider_loc[i],args) 
#                 for i in range(args["numRiders"])]
# rider_list.sort()
# print([r.index for r in rider_list])
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
