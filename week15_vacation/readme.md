Goal:

1. Simple Moving Average（SAM) for Waiting Time:
    - average waiting time of the previous n order. 
    - Computation: https://en.wikiversity.org/wiki/Moving_Average/Simple_Moving_Average
    - Implementation: 
        - n is the window size, *"SMA_batchsize"* in args
        - to plot for 1 simulation, call **plot_sma_by_numOrders()**
            - This plot overlay the moving average of waiting time of the orders, with the original waiting time per order
            - For each order index > "SMA_batchsize", it has a moving average value, that is the average for the previous n orders
        - to plot for multiple simulations, call **plot_sma_distribution_by_numOrders()**
            - This plot plot the mean, median, upper quantile, lower quantile of the waiting time for each window

2. Interval Average(IA) for Waiting Time:
    - For orders delivered within this interval, compute the average waiting time
        - note: intervals are non-overlapping
    - Implementation:
        - interval length is *"IA_interval"* in args
        - to plot for 1 simulation, call **plot_interval_avg_by_time()**
        - to plot for multiple simulations, call **plot_ia_distribution_by_time()**
            - stats obtained for each non-overlapping time interval
            - null values are ignored during computation

3. Vary the lambda of the order arrival process
    - original parameter: "orderArrivalRate" = 30, which is the mean interarrival time between 2 orders, in seconds
        - hence lambda of the arrival process = 1/30
    - Variation: "orderArrivalRate" = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        - We fix the number of riders to 30

3. Probalistic Distribution of Food Preparation Time(FPT)
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
