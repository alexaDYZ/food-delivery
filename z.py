import copy
import matplotlib.pyplot as plt

events = [(1,5,7), (2,4), (3,10)]
plt.eventplot(events,linelengths = 0.5, colors=['C{}'.format(i) for i in range(len(events))])
plt.ylabel("OrderNumber")
plt.xlabel("Time")
plt.title("Events acorss time")
plt.show()