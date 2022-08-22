from queue import PriorityQueue 
from Event import Event
from Order import Order
from Rider import Rider
from Restaurant import Restaurant
from Customer import Customer
from config import args


class EventQueue(PriorityQueue):
    def _put(self, item):
        return super()._put((self._get_priority(item), item))
    def _get(self):
        return super()._get()[1]
    def _get_priority(self, item): 
        return item.time

# r = Rider(1, [0,0], args)
# rest = Restaurant(1, [5,0], 10,args)
# cust = Customer([10,0],args )
# o = Order(1, 100, cust, rest)
# e_1 = Event(100, 1, o)
# e_2 = Event(110, 3, o)
# e_3 = Event(125, 2, o)
# e_100 = Event(10000, 2, o)


# # c = EventQueue() 
# events = [e_100,e_3,e_1,e_2]
# events.sort()

# for e in events:
#     e.print()

# c.get().print()
# c.get().print()
# c.get().print()
# c.get().print()