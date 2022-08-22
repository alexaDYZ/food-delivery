
class Customer():
    def __init__(self, loc,args) -> None:
        self.loc = loc
        self.args = args
        self.wtimeList = []
        # assumption: 1 customer only has one order at one point of time
        self.orderInTime = -1
        self.orderDeliveredTime = -1
    
    def order(self,t):
        self.orderInTime = t
    
    def receivesOrder(self,t):
        self.orderDeliveredTime = t
        waiting_time = self.orderDeliveredTime - self.orderInTime
        self.wtimeList.append(waiting_time)
    
    def totalWaitingTime(self):
        return sum(self.wtimeList)