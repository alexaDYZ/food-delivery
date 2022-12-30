Goal:

1. Simple Moving Average（SAM） for Waiting Time:
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
