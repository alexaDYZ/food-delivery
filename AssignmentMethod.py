from config import args
class AssignmentMethod():
    def __init__(self) -> None:
        self.order = None
        self.rider_list = None
        self.currTime = None
    def addOrder(self, newOrder):
        self.order = newOrder
    def addRiderList(self, rider_list):
        self.rider_list = rider_list
    def addCurrTime(self, currTime):
        self.currTime = currTime
    def find_eligible_candidates(self):
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
    # def generate_order_arrival_event(self):
    #     fmtime = self.order.rider.distance_to(self.order.rest.loc)/args["riderSpeed"]
    #     arrival_time = self.currTime + fmtime
    #     arrivalEvent = Event(arrival_time, 3, self.order)
    #     return arrivalEvent

    def assign(self):
        '''
        Input: a list of eligible riders
        Output: the best rider, Rider Object
        '''
        pass