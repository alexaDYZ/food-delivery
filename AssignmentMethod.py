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

