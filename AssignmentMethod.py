from config import args
class AssignmentMethod():
    def __init__(self) -> None:
        self.order = None
        self.rider_list = None
        self.currTime = None
        self.name = self.__class__.__name__
        
    def addOrder(self, newOrder):
        self.order = newOrder
    def addRiderList(self, rider_list):
        self.rider_list = rider_list
    def addCurrTime(self, currTime):
        self.currTime = currTime
    def find_idle_candidates(self):
        '''
        Input: a list of all riders
        Output: a list of eligible riders, eligibility is defined accordingly
        '''
        pass
    def find_best_rider(self):
        '''
        Input: a list of eligible riders
        Output: the best rider, Rider Object
        '''
        pass

class AssignmentMethod_Batching():
    def __init__(self) -> None:
        self.order_ls = [] # store all the orders
        self.pending_order_dict = {} # store all the orders that are not assigned yet, aka within the current stalling period. key: order index, value: order object
        self.rider_list = None
        self.currTime = None
        self.name = self.__class__.__name__
    def addOrder(self, newOrder):
        self.order_ls.append(newOrder)
    def addPendingOrder(self, newOrder):
        self.pending_order_dict[newOrder.index] = newOrder
    def clearPendingOrders(self):
        self.pending_order_dict = {}
    # only at the end of x min
    def addRiderList(self, rider_list):
        self.rider_list = rider_list
    # only at the end of x min
    def addCurrTime(self, currTime):
        self.currTime = currTime
    
    def find_best_rider(self):
        '''
        Input: a list of eligible riders
        Output: the best rider, Rider Object
        '''
        pass

