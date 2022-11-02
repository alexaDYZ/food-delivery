
'''
To visualize what happeend in the simulation, I have developed this class
'''
# from ... import Simulation
from re import S
from turtle import width
import numpy as np
import matplotlib.pyplot as plt

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

    def setGridSize(self, size):
        self.grid_size = size

    def setInput(self, ls):
        '''
        This function takes the input in the form of the following:
        input = [(a, b), (c, d), (e, f), ...]
        where a, b, c, d, e, f are locations,
        with the first one in the tuple being the restaurant, and the second one being the customer
        '''
        self.input = ls

    def visualize(self):
        '''
        This function generates the visualization of route
        '''
        print("Visualizing the route...")
        self.defaultSettings()

        prev_location = None # first node of pair is connected to the second node of the previous pair

        for i in range(len(self.input)):
            # get the current pair
            pair = self.input[i]
            # plot the two nodes
            a = pair[0]
            b = pair[1]
            plt.scatter(a[0], a[1],color=self.marker_colors[0],zorder=1) # restaurant
            plt.scatter(b[0], b[1] ,color=self.marker_colors[1],zorder=1) # customer
            plt.annotate("O"+str(i), xy=(a[0], a[1]), xytext=(a[0], a[1]-0.05), size = 10, zorder=2)
            plt.annotate("O"+str(i), xy=(b[0], b[1]), xytext=(b[0], b[1]-0.05), size = 10, zorder=2)
            
            # connect the two nodes
            x = [a[0], b[0]]
            y = [a[1], b[1]]
            

            plt.plot(x, y, color = self.line_color,
                           alpha = self.line_alpha, 
                           linewidth = self.line_width,
                           zorder=3)

            # plot the arrow
            mid_x = (a[0] + b[0]) / 2
            mid_y = (a[1] + b[1]) / 2
            dx, dy = self.get_dx_dy(a, b)
            print("dx, dy are ", dx, dy)
            
            plt.arrow(mid_x, mid_y, dx, dy, head_width = self.line_width*5, 
                                            head_length = self.line_width*5,
                                            
                                            
                                            zorder=4)

            if prev_location:
                # connect the current node to the previous node
                x = [prev_location[0], a[0]]
                y = [prev_location[1], a[1]]
                plt.plot(x, y, color = "grey", linewidth = self.line_width,
                                    alpha = self.line_alpha, zorder=3)
                print("lines ploted are ", x, y)


            
            prev_location = b

        

        plt.title("Route Visualization")
        # plt.legend()
        plt.show()






        pass
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


# ls = [((1,2),(2,2))]
# ls.append(((3,2), (4,2)))
# ls.append(((4,4), (6,4)))
# # ls.append(((4,2), (0,2)))
# # ls.append(((2,4), (4,4)) )
# # ls.append(((1,1),(2,2)))
# v = RouteVisualization()
# v.setInput(ls)
# v.visualize()