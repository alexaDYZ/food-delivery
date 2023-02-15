
from ast import arg
from AssignmentMethod import AssignmentMethod_Batching
from Rider import Rider
from Restaurant import Restaurant
from Order import Order
from Customer import Customer
from config import args
import math
import random  
from min_cost_max_flow import min_cost_max_flow

class PatientAnticipativeMethod_Bulk(AssignmentMethod_Batching):
    '''
    Patient Anticipative Method:
    For every x minutes, the system will assign all orders arrived during this period to riders.
    It's a minimum matching problem:
    1. For each rider, find it's arrival time to all the restaurants for all the orders.
    2. Assign weight to the edges (rider, restaurant) = (arrival time)
    3. Find the minimum matching.
    4. Assign the orders to the riders.
    
    '''
    def __init__(self):
        super().__init__() # self.order_ls, self.pending_order_ls, self.currTime, self.name, self.rider_list
        self.R2RforAll = {} # a dictionary of R2R time for the current order for all riders. key: time arrived at the restaurant, value: a list of rider objects
        self.bestRider = None # for the current order
        
    def addOrder(self, newOrder):
        return super().addOrder(newOrder)
    def addPendingOrder(self, newOrder):
        return super().addPendingOrder(newOrder)
    def addCurrTime(self, currTime):
        return super().addCurrTime(currTime)
    def addRiderList(self, rider_list):
        return super().addRiderList(rider_list)

    # This part is different from the lookAhead method 
    def findR2R(self, order, rider):
        
        '''
        given an order and rider, find the time when the rider arrives at the restaurant
        
        '''
       
        rest_loc = order.rest.loc
        currTime = self.currTime

        def getTimeReachedRestaurant(rider:Rider, currTime): 
            
            # print("** For Order " + str(self.order.index)) if args["printAssignmentProcess"] else None
            
            '''get the time when this rider reaches the restaurant'''

            # Case 1: rider is idle/free now
            if rider.status != 1:
                # ######################### debug #########################
                # print("Rider " + str(rider.index) + "is idle at t = " + str(currTime) ) if args["printAssignmentProcess"] else None
                # print("Rider " + str(rider.index) +  " will reach at " +  
                #         str(rider.distance_to(rest_loc) / args["riderSpeed"] + currTime) ) if args["printAssignmentProcess"] else None
                # ######################### debug #########################
                
                R2R = rider.distance_to(rest_loc) / args["riderSpeed"]

                timeArrival = round(R2R + currTime, 3)
                
            # Case 2: rider is busy now
            else:
                # Assuming there's no maximum num of orders one can take
                
                # ######################### debug #########################
                # orderIndex = list(rider.orderDict.keys()) 
                # orderIndex.sort()
                # print("Rider " + str(rider.index) +  "have the fllowing orders in process: " + 
                #          str(orderIndex))if args["printAssignmentProcess"] else None
                # ######################### debug #########################


                nextAvilableTime = rider.nextAvailableTime
                lastStop = rider.lastStop # after finish the last order in the bag, rider stays there
                
                R2R = math.dist(lastStop, rest_loc) / args["riderSpeed"]

                # print("Rider "  +  str(rider.index)  + "'s nextAvilableTime: "  + str(nextAvilableTime) + 
                #         "\n R2R = " + str(R2R) + 
                #         "\n Hence will reach the restaurant at " + str(nextAvilableTime + R2R)) if args["printAssignmentProcess"] else None
                timeArrival = round(nextAvilableTime + R2R, 3)
            return timeArrival
        
        timeArrival = getTimeReachedRestaurant(rider, currTime)
        return timeArrival

    def matchPendingOrders(self):
        # debug
        log = False


        matched_res_dict = {} # key: order, value: matched rider

        # input is  
        # #vertices, #edges, source node index, sink node index
        numPendingOrders = len(self.pending_order_dict)
        numRiders = args["numRiders"]

        V = numRiders + numPendingOrders + 2
        E = numRiders + numPendingOrders + numPendingOrders * numRiders
        source = 0

        mf = min_cost_max_flow(V) # Create a min_cost_max_flow object

        # Create the Edge list
        edge_list = []

        rider_index_in_map = [r.index + 1 for r in self.rider_list] # source is 0, so rider index starts from 1
        
        order_index_in_map_dict = {} # key: index in map, value: real index
        pending_order_index = list(self.pending_order_dict.keys())
        
        for i in range(numPendingOrders):
            map_index = i + max(rider_index_in_map) + 1
            order_index_in_map_dict[map_index] = pending_order_index[i]
    
        
        self.rider_list.sort(key=lambda x: x.index)
        sink = max(order_index_in_map_dict.keys()) + 1




        # add edges
        # 1. source to all riders
        for r in rider_index_in_map:
            edge_list.append((source, r, 1, 0))
        if log: print("after adding riders, num edges = ",len(edge_list))

        # 2. all riders to all orders
        for r in rider_index_in_map:
            for o in order_index_in_map_dict.keys():
                
                o_real_index = order_index_in_map_dict[o]
                r_real_index = r - 1
                

                order = self.pending_order_dict[o_real_index] # recover the real index
                rider = self.rider_list[r_real_index] # recover the real index
                timeArrival = self.findR2R(order, rider) # recover the real index

                edge_list.append((r, o, 1, timeArrival))
        if log: print("after adding rider-order pair, num edges = ",len(edge_list))

        # 3. all orders to sink
        for o in order_index_in_map_dict.keys():
            edge_list.append((o, sink, 1, 0))
        if log: print("after adding orders , num edges = ",len(edge_list))


        #########  debug
        # print("check if the number is edges is correct: " + str(len(edge_list)) + " == " + str(E))
        # print("input for mf: ", V, E, source, sink)
        # print("egdes are ")
        # for e in edge_list:
        #     print(e)
        for edge in edge_list: 
            u, v, w, c = edge # u, v, capacity, cost
            mf.add_edge(u, v, w, int(c)) # Add edge from u to v with capacity w and cost c
        
        
        # record the optimal edges
        optimal_edges = mf.mcmf(source, sink)
        
        o = None
        r = None
        for e in optimal_edges:
            if e[1] == sink and e[0] in order_index_in_map_dict.keys(): # the last node
                o_real_index = order_index_in_map_dict[e[0]]
                o = self.pending_order_dict[o_real_index]

            elif e[0] == source and e[1] in rider_index_in_map: # the first node
                r = self.rider_list[e[1] - 1]

            if o is not None and r is not None:
                matched_res_dict[o] = r
                o = None
                r = None

        return matched_res_dict

    def assignPendingOrders(self, matched_res_dict):
        for o, r in matched_res_dict.items():
            if r:
                r_startTimeForCurrOrder = r.nextAvailableTime
                o.foundRider(r)
                r.deliver(o, r_startTimeForCurrOrder)
                ### debug:
                # print("Order " + str(o.index) + " is assigned to Rider " + str(r.index) ) 
            else:
                print("Cannot match a Rider for Order " + str(o.index))
    
    def clearPendingOrders(self):
        return super().clearPendingOrders()