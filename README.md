# food-delivery

## How an order is allocated to a rider:

### Anticipative Method:
When an order comes in at time t, this method will find whoever can reach the restaurant the ealiest, regardless of the riders status, be it idle or busy.
In the implementation, we compute the R2R for all in function findR2RforAll(), where R2R is the ealiest possible time one can reach the restaurant.

There are two cases to consider for the computation:

1. Rider, r is idle at time t:
- R2R = dist(r, restaurant)/speed, where R2R is the time taken to travel
- the actuall R2R is R2R+t, since the current time now is t

2. Rider, r is busy at time t:
- get to know when he/she will be free -> r.nextAvailableTime, which is the time when he/she delivered the last order
- get to know his/her location at t = r.nextAvailableTime:
  - Assuming r stays at that customer's location, he will be at t.lastStop = prevOrder.cust.loc
- compute how long does it take, from his location at t = r.nextAvailableTime, aka the customer's place, to the restaurant
  - R2R = dist(r.lastStop, restaurant)/speed
- The actual R2R is R2R + r.nextAvailableTime

After obatin the R2R time for all, we pick the one with the smallest R2R.

### Default Method:
When an order comes in at time t, this method will firstly figure out who's available right now, then choose whoever is the nearest to the restaurant.

When there's no one available right now, assign the order to whoever can finish his/her current order(s) the ealiest.

## How information is updated:

