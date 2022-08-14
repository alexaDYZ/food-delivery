from queue import PriorityQueue 
from Event import Event


class EventQueue(PriorityQueue):
    def _put(self, item):
        return super()._put((self._get_priority(item), item))
    def _get(self):
        return super()._get()[1]
    def _get_priority(self, item): 
        return item.time

# c = EventQueue() 
# time = [300,29,50]
# for t in time:
#     e = Event(t, 1)
#     c.put(e)

# c.get().print()
# c.get().print()
# c.get().print()