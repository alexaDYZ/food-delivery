


from tkinter.messagebox import NO
from AssignmentMethod import AssignmentMethod
from Order import Order
from Rider import Rider
from Restaurant import Restaurant
from Customer import Customer
from config import args


class Event():
    category = {
        1: 'New Order',
        2: 'Order Delivered',
        3: 'Rider Arrived at Restaurant',
        4: 'Regular Check', # for rider saturation rate
    }
    def __init__(self, time, cat:int, order:Order):
        self.time = time # time when the event is executed
        self.cat = cat
        self.order = order
        self.rider_list = None # this is for event 4 to check status for all riders; and event 2 to reassign
        self.method = None
        self.status_check_dict = None
        self.programEndTime = -1
        self.qsize = -1 # for 'Regular Check event'. to know if this is the end
        self.record = [] # columns: [order.index, t, r2r, restArrival, delivered]
    
    def getCategory(self) : #returns a string
        return Event.category[self.cat]
    
    def print(self):
        print("time", self.time, ":", self.getCategory())
    
    def __lt__(self, other):
        return self.time < other.time
    
    def executeEvent(self, currTime):
        triggeredEvent = []
        # case 1: new order comes in 
        if self.getCategory() ==  'New Order':
            # print("******* Order " +  str(self.order.index) + " comes in at t = " + 
            #         str(currTime) + "*******" if args["printAssignmentProcess"] else '')
            curr_order = self.order
            curr_order.cust.order(currTime) # customer makes order at time currTime
            assignment_method = self.method
            assignment_method.addOrder(curr_order)
            assignment_method.addCurrTime(currTime)
            
            # find best rider
            bestRider = assignment_method.find_best_rider()
            
            # add estimated delivered time for the order, for anticipative method
            
            # if best rider can be found:
            if bestRider:
                # print("******* Order "+ str(self.order.index)+ " is assigned to Rider "+
                #          str(bestRider.index) + "******" if args["printAssignmentProcess"] else '')
                
                # create "arrive at restaturant" event
                
                # print("************ Rider " + str(bestRider.index) + 
                #          " will arrive at Restaurant at t = "+str(self.order.t_riderReachedRestaurant)+ 
                #          "************" if args["printAssignmentProcess"] else '')

                e_arrival = Event(self.order.t_riderReachedRestaurant, 3, curr_order)
                triggeredEvent.append(e_arrival)
                
                # create "order delivered" event
                t = self.order.t_delivered
                e_finish = Event(t, 2, curr_order)
                triggeredEvent.append(e_finish)
                # curr_order.t_est_delivered = t
                # curr_order.t_delivered = t

            else:
                # print("******* Order " + str(self.order.index) + " is dropped ******" if args["printAssignmentProcess"] else '')
                self.order.status = 4 # dropped
            
        # case 2: an order is delivered

        elif self.cat == 2:
            
            # print("******* Order " + str(self.order.index) +  " is delivered by Rider " + 
            #         str(self.order.rider.index) + " at t = " + str(currTime)+ 
            #         "******" if args["printAssignmentProcess"] else '')
            
            # update status for rider and order
            self.order.delivered(currTime)
            

        
        # case 3: rider arrives at restaurant
        elif self.cat == 3:
            #update rider location
            rest_loc = self.order.rest.loc
            rider = self.order.rider
            if rider:
                rider.loc = rest_loc
            elif rider is None: print("Error: Rider arrives at resturant but cannot find its rider")
        
        # case 4: check % riders occupied, at regular time interval
        elif self.cat == 4:
            # check if thats the 'end' of the program
            # if currTime >= self.programEndTime+args["statusCheckInterval"]:
            #     return []
            if self.qsize <= 1:
                return []
            
            else:
                # compute %
                numOccupiedRiders = 0
                for r in self.rider_list:
                    if r.getStatus() == "BUSY":
                        numOccupiedRiders += 1
                ratio = round(numOccupiedRiders / args["numRiders"],2)
                # record
                self.status_check_dict[currTime] = ratio
                
                # trigger next regular check event
                next_check = Event(currTime+args["statusCheckInterval"], 4, None)
                triggeredEvent.append(next_check)
       
        return triggeredEvent # a list of events to be added to the checkpoints EventQueue

    def addAssignmentMethod(self, method: AssignmentMethod):
        self.method = method      
    def addRiderList(self, ls):
        self.rider_list = ls
    def addStatusCheckDict(self, dict):
        self.status_check_dict = dict
    def addProgramEndTime(self, t):
        self.programEndTime = t
    def passCurrQSize(self, qsize):
        # for 'Regular Check Event'
        if self.cat == 4:
            self.qsize = qsize
        else:
            print("Error: Event.py, wrong event type")

r = Rider(1, [0,0], args)
rest = Restaurant(1, [5,0], 10,args)
cust = Customer([10,0],args )
o = Order(1, 100, cust, rest)
e_1 = Event(100, 1, o)
e_2 = Event(110, 3, o)
e_3 = Event(125, 2, o)

# e_1.executeEvent()
# e_2.executeEvent()
# e_3.executeEvent()
        

