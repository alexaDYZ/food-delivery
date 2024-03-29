from config import args
class AssignmentMethod():
    WALKING_RULE = {
        "No Walking": 0 ,
        "Nearest Restaurant": 1,
        "Probabilistic":2,
    }
    accuracy_of_prediction = {
        "full": 1,
        "partial": 0.5,
        "poor_short": 0,
        "poor_long": 2,
    }
    def __init__(self) -> None:
        self.order = None
        self.rider_list = None
        self.rest_list = None
        self.currTime = None
        self.name = self.__class__.__name__
        self.walking_rule = 0 # default is no walking
        
    def addOrder(self, newOrder):
        self.order = newOrder
    def addRiderList(self, rider_list):
        self.rider_list = rider_list
    def addRestList(self, rest_list):
        self.rest_list = rest_list
    def addCurrTime(self, currTime):
        self.currTime = currTime
    def setWalkingRule(self, rule_name):
        self.walking_rule = AssignmentMethod.WALKING_RULE[rule_name]
        self.name = self.__class__.__name__ + "_" + rule_name
    def setFPT_pred_accuracy(self, level):
        # level can be "full", "partial", "poor"
        if level in AssignmentMethod.accuracy_of_prediction.keys():
            self.FPT_knowledge = AssignmentMethod.accuracy_of_prediction[level]
        else:
            raise Exception("Invalid FPT knowledge level")
    def find_candidates(self):
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
        '''
        Find 
        1) best rider 
        2) earliest time for him/her to start working on this order
        3)R2R
        '''
        pass

