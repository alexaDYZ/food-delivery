import pandas as pd
from config import args
import pickle



def main():
        def getMcOrderTime():
                mcdf = pd.read_csv('./McDonald_data/mc_data_processed.csv')
                order_time = []
                for i in range(len(mcdf["phTimeStart_s"])):
                        order_time.append(mcdf.iloc[i]['phTimeStart_s'])
                        args['numOrders'] = len(order_time)
                return order_time
        order_time = getMcOrderTime()
        ## save data
        with open('data_mc_orders.ls', 'wb') as data_file:
                pickle.dump(order_time, data_file)

        

if __name__ == "__main__":
        main()


        
