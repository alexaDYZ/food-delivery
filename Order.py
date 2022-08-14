
class Order():
    """
    This class is about the order generated by customers.
    """
    status = {
        1: 'ORDERED',
        2: 'DELIVERING',
        3: 'DELIVERED',
    }

    def __init__(self, index, t, customer, restaurant):
        self.index = index
        self.t = t
        self.cust = customer
        self.rest= restaurant
        self.rider = None
        self.status = 1

    def getOrderStatus(self):
        return Order.status[self.status]

    def foundRider(self):
        self.status = 2
        print("------ Order #" , self.index, "is assigned to Rider #", self.rider.index , "order is ", self.getOrderStatus() )
    
    def delivered(self):
        self.status = 3
        self.rider.totalOrderDelivered += 1
        print("------ Order #" , self.index, "is", self.getOrderStatus())
    
    def print(self):
        print("------ Order #" , self.index, "is ", self.getOrderStatus(), "\n Customer:", self.customer.loc, "Restaurant:", self.restaurant.loc)


# o = Order()
# o.getOrderStatus()

