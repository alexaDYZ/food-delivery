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

### Patient Anticipatory Method:

Stalling time = k seconds
pending orders: orders received, stored in the batch, not assigned yet

When an order arrives in the system at time t, check if there are pending orders:
Case 1: no pending order 
- start a new batch
- set cutoff time of assignment = t + k
Case 2 there are pending orders, but t < the cutoff time of assignment set earlier
- append the order to the current batch

When t = cutoff time of assignment, assign all orders.

Assignment method:
- Convert the problem to min_cost_max_flow problem, with source node as the sink node as dummy node, a bipartite graph of orders set and riders set, and apply the algorithm for the min_cost_max_flow to solve this problem.






## Analysis of Performance:

### Interval Average(IA) of Waiting Time 
- For orders generated within this interval, compute the average waiting time
    - note: intervals are non-overlapping
- Implementation:
    - interval length is *"IA_interval"* in args
    - to plot for 1 simulation, call **plot_interval_avg_by_time()**
    - to plot for multiple simulations, call **plot_ia_distribution_by_time()**
        - stats obtained for each non-overlapping time interval
        - null values are ignored during computation
        - 
### Simple Moving Average（SAM) for Waiting Time:
- average waiting time of the previous n order. 
- Computation: https://en.wikiversity.org/wiki/Moving_Average/Simple_Moving_Average
- Implementation: 
    - n is the window size, *"SMA_batchsize"* in args
    - to plot for 1 simulation, call **plot_sma_by_numOrders()**
        - This plot overlay the moving average of waiting time of the orders, with the original waiting time per order
        - For each order index > "SMA_batchsize", it has a moving average value, that is the average for the previous n orders
    - to plot for multiple simulations, call **plot_sma_distribution_by_numOrders()**
        - This plot plot the mean, median, upper quantile, lower quantile of the waiting time for each window

## Sensitivity Analysis

#### Vary the lambda of the order arrival process
- original parameter: "orderArrivalRate" = 30, which is the mean interarrival time between 2 orders, in seconds
    - hence lambda of the arrival process = 1/30
- Variation: "orderArrivalRate" = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    - We fix the number of riders to 30

#### Probalistic Distribution of Food Preparation Time(FPT)
- original FPT = 300 s
- distribution: Truncated normal
    - mean = 300, sd = 100, range = [100, 500 ]
    <!-- - mean = 15*60, sd = 2*60, range = [5*60, 30*60] -->
- Implementation:
    ***config.py***
    - boolean variavle, sd, lower bound, upper bound
        - *"if_truncated_normal"*
        - *"FPT_sd"*
        - *"FPT_lower"*
        - *"FPT_upper"*
    ***generateData.py***




## Run algorithms with McDonald Data:
1. Get order arrival time from the dataset
   - Pre-processed and saved as **data_mc_orders.ls**
   - Otherwise, call **generate_mc_order_arrivals.py** to generate the list
2. Set args["useMcData"]=1
3. Perform as per normal






# A list of Algorithms:
1. Greedy(drop) - Default_1a
2. Greedy(keep) - Default_1b
3. Greedy Anticipative Method
4. Patient Anticipative - batching
5. Greedy Anticipative Method(Assign Later)
6. ClosestToFPT

