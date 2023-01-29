
class Restaurant():
    def __init__(self,index, loc, prepTime, args) -> None:
        self.loc = loc
        self.index = index
        self.args = args
        # self.prepTime = prepTime 
        self.order_FPT_dict = {} # key = order index, value = FPT. 
    
    def addOrder_FPT(self, order_index, FPT):
        '''Add the order index and FPT to the restaurant's order_FPT_dict'''
        self.order_FPT_dict[order_index] = FPT