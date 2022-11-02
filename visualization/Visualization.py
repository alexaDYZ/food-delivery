
'''
To visualize what happeend in the simulation, I have developed this class
'''
# from ... import Simulation
import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('..')
from Order import Order
from Rider import Rider
from Restaurant import Restaurant
from Customer import Customer
from config import args


class RouteVisualization():
    def __init__(self) -> None:
        self.input = None
        # styles
        self.line_color = None
        self.line_width = None
        self.marker_colors = None
        self.marker_styles = None
        self.marker_size = None
        self.grid_size = None
        self.text_size = None
        self.text_color = None
        self.start = None
        self.start_color = None
        self.timeStamp = None

    def setGridSize(self, size):
        self.grid_size = size
    def setStartingPoint(self, pt):
        '''This function adds a starting point for the route'''
        self.start = pt
    def loadData(self, ls):
        '''
        This function takes the input in the form of the following:
        input = [(a, b), (c, d), (e, f), ...]
        where a, b, c, d, e, f are locations,
        with the first one in the tuple being the restaurant, and the second one being the customer
        '''
        self.input = ls
    def loadTimeStamp(self, timeStamp):
        self.timeStamp = timeStamp
    def visualize(self, plot=plt):
        '''
        This function generates the visualization of route
        '''
        print("Visualizing the route...")
        self.defaultSettings()

        prev_location = None # first node of pair is connected to the second node of the previous pair
        # plot.xlim([0, 1000])
        # plot.ylim([0, 1000])
        plot.set_xlim([0, self.grid_size])
        plot.set_ylim([0, self.grid_size])
        plot.scatter(self.start[0], self.start[1],
                    color = self.start_color,
                    zorder=1) # restaurant
        prev_location = self.start

        
        if self.input:
            for i in range(len(self.input)):
                # get the current pair
                pair = self.input[i]
                # plot the two nodes
                a = pair[0]
                b = pair[1]
                plot.scatter(a[0], a[1],color=self.marker_colors[0],zorder=1) # restaurant
                plot.scatter(b[0], b[1] ,color=self.marker_colors[1],zorder=1) # customer
                plot.annotate("O"+str(self.timeStamp[i]), xy=(a[0], a[1]), xytext=(a[0], a[1]-0.05), size = 10, zorder=2)
                plot.annotate("O"+str(self.timeStamp[i]), xy=(b[0], b[1]), xytext=(b[0], b[1]-0.05), size = 10, zorder=2)
                
                # connect the two nodes
                x = [a[0], b[0]]
                y = [a[1], b[1]]
                

                plot.plot(x, y, color = self.line_color,
                            alpha = self.line_alpha, 
                            linewidth = self.line_width,
                            zorder=3)

                # plot the arrow
                mid_x = (a[0] + b[0]) / 2
                mid_y = (a[1] + b[1]) / 2
                dx, dy = self.get_dx_dy(a, b)
                
                plot.arrow(mid_x, mid_y, dx, dy, head_width = self.line_width*5, 
                                                head_length = self.line_width*5,
                                                
                                                
                                                zorder=4)

                
                # connect the current node to the previous node
                x = [prev_location[0], a[0]]
                y = [prev_location[1], a[1]]
                plot.plot(x, y, color = "grey", linewidth = self.line_width,
                                    alpha = self.line_alpha, zorder=3)


                
                prev_location = b

        else:
            print("No other places visited:(")

        # plt.title("Route Visualization")
        # plt.legend()
        # plt.show()


    # anesthetics 
    def defaultSettings(self):
        '''
        This function sets the default settings for the visualization
        '''
        # color of the lines
        self.line_color = "darkblue"
        # width of the lines
        self.line_width = 1
        # transparency of the lines
        self.line_alpha = 0.2

        # size of the markers
        self.marker_size = 10
        # color of the markers
        self.marker_colors = ("green", "blue")
        self.start_color = "red"
        # marker style
        self.marker_styles = ("o", "s")

        self.text_size = 10
        self.text_color = "black"

    
    # customized style 
    def setLineColor(self, color):
        self.line_color = color
    def setLineWidth(self, width):
        self.line_width = width
    def setMarkerSize(self, size):
        self.marker_size = size
    def setMarkerColor(self, color):
        self.marker_colors = color
    def setMarkerStyle(self, style):
        self.marker_styles = style
    # helper function for arrow
    def get_dx_dy(self,p1,p2):
        # p1 and p2 are 2 coordinates in the form of tuple, (x, y)
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        slope = dy/dx
        return 1/1000, slope/1000

def visualize_one(rider:Rider, title:str):
    '''
    The function takes in a Rider object, and visualize the route he/she has gone through'''
    v = RouteVisualization()
    v.setStartingPoint(rider.init_loc)
    
    # to input the route data
    loc_ls = None
    order_dict = rider.orderDict
    if not order_dict:
        print("No orders have been made yet!")
    else:
        order_index = list(order_dict.keys())
        order_index.sort()
        loc_ls = []
        for i in order_index:
            o = order_dict[i]
            pair = (o.rest.loc, o.cust.loc)
            loc_ls.append(pair)

    
    v.loadData(loc_ls)
    v.setGridSize(args["gridSize"])
    v.visualize()
    plt.title(title)
    plt.show()

def visualize_multiple(riders, title = "Route Visualization of two riders"):
    '''
    The function takes in a list of Rider objects, and visualize the route they have gone through
    '''
    
    fig, (ax1, ax2) = plt.subplots(1, 2)
    x = np.linspace(0, 2 * np.pi, 400)
    y = np.sin(x ** 2)
    # axs[0, 0].plot(x, y)
    # axs[0, 0].set_title('Axis [0, 0]')
    # axs[0, 1].plot(x, y, 'tab:orange')
    # axs[0, 1].set_title('Axis [0, 1]')
    
    # print("Visualizing the route...")
    # print("Number of riders: ", len(riders))
    
    for i in range(len(riders)):
        rider = riders[i]
        v = RouteVisualization()
        v.setStartingPoint(rider.init_loc)
        # to input the route data
        loc_ls = None
        order_dict = rider.orderDict
        if not order_dict:
            print("No orders have been made yet!")
        else:
            order_index = list(order_dict.keys())
            order_index.sort()
            loc_ls = []
            for j in order_index:
                o = order_dict[j]
                pair = (o.rest.loc, o.cust.loc)
                loc_ls.append(pair)
        
        plt_at = ax1 if i == 0 else ax2
        v.loadTimeStamp(order_index)
        v.loadData(loc_ls)
        v.setGridSize(args["gridSize"])
        v.visualize(plt_at)
        plt_at.set_title("Rider "+str(rider.index) + " with " + str(len(order_dict)) + " orders")
    
    plt.show()
        

def visualizeMaxMin(riders, title = "Route Visualization of two riders"):
    '''
    This function visualize specifically, the route of 2 riders:
    rider who delivered the most orders, and who delivered the least.
    '''        
    max = 0
    max_r = None
    min = np.Infinity
    min_r = None
    for r in riders:
        if r.orderDict:
            if len(r.orderDict) > max:
                max_r = r
                max = len(r.orderDict)
                print("max", max_r.index)

            if len(r.orderDict) < min:
                min_r = r
                min = len(r.orderDict)
                print("min", min_r.index)
    print("max", max_r)
    print("min", min_r)
    
    visualize_multiple([max_r, min_r])

    



# ls = [((1,2),(2,2))]
# ls.append(((3,2), (4,2)))
# ls.append(((4,4), (6,4)))
# # ls.append(((4,2), (0,2)))
# # ls.append(((2,4), (4,4)) )
# # ls.append(((1,1),(2,2)))
# v = RouteVisualization()
# v.setInput(ls)
# v.visualize()