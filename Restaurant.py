import scipy.stats as stats

class Restaurant():
    FPT_cat = {
        0: 'fast',
        1: 'normal',
        2: 'slow',
        3: 'very_slow',
    }
    def __init__(self,index, loc, prepTime, args) -> None:
        self.loc = loc
        self.index = index
        self.args = args
        # self.prepTime = prepTime 
        self.order_FPT_dict = {} # key = order index, value = FPT. 
        self.FPT_cat = None
    
    def add_FPT_cat(self, FPT_cat_name):
        self.FPT_cat = Restaurant.FPT_cat[FPT_cat_name]
    
    def generate_a_FPT(self):
        '''Generate a FPT for the restaurant'''
        means = [i*60 for i in [10, 20, 40, 60]]
        stds = [i*60 for i in [2, 5, 5, 10]]
        upper = [i*60 for i in [20, 40, 60, 100]]
        lower = [i*60 for i in [5, 10, 20, 40]]

        i = self.FPT_cat
        FPT = stats.truncnorm((lower[i] - means[i]) / stds[i],
                                            (upper[i] - means[i]) / stds[i], 
                                            loc=means[i], scale=stds[i]).rvs(1).tolist()[0]
        return FPT
    
    def addOrder_FPT(self, order_index, FPT):
        '''Add the order index and FPT to the restaurant's order_FPT_dict'''
        self.order_FPT_dict[order_index] = FPT
    
    def getinfo(self):
        print("Restaurant ", self.index, " loc: ", self.loc)
        print("Order_FPT_dict: ")
        for key, value in self.order_FPT_dict.items():
            print(key, value)
