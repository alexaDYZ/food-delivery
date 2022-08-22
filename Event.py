


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
    }
    def __init__(self, time, cat:int, order:Order):
        self.time = time # time when the order comes in
        self.cat = cat
        self.order = order
        self.method = None
    
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
            curr_order = self.order
            curr_order.cust.order(currTime) # customer makes order at time currTime
            assignment_method = self.method
            assignment_method.addOrder(curr_order)
            assignment_method.addCurrTime(currTime)
            # find best rider
            bestRider = assignment_method.assign()
            # if best rider can be found:
            if bestRider:
                # create "arrive at restaturant" event
                rest_arrival_time = bestRider.getRestArrivalTime(curr_order.index)
                e_arrival = Event(rest_arrival_time, 3, curr_order)
                triggeredEvent.append(e_arrival)
                # create "order delivered" event
                finishTime = bestRider.getOrderCompleteTime(curr_order.index)
                e_finish = Event(finishTime, 2, curr_order)
                triggeredEvent.append(e_finish)
            
        # case 2: an order is delivered
        if self.cat == 2:
            # update order status
            self.order.delivered(currTime)
            orderIndex = self.order.index
            # update rider
            rider = self.order.rider
            if rider: # check if rider is None
                rider.loc = self.order.rest.loc
                del rider.orderDict[orderIndex]
                rider.status = 0 if len(rider.orderDict) == 0 else 1
                rider.totalCurrOrder -= 1 
            elif rider is None: print("Error: Order delivered but cannot find its rider")
        # case 3: rider arrives at restaurant
        if self.cat == 3:
            #update rider location
            rest_loc = self.order.rest.loc
            rider = self.order.rider
            if rider:
                rider.loc = rest_loc
            elif rider is None: print("Error: Rider arrives at resturant but cannot find its rider")
        return triggeredEvent # a list of events to be added to the checkpoints EventQueue

    def addAssignmentMethod(self, method: AssignmentMethod):
        self.method = method      

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
        

