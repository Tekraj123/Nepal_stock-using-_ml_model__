import os
from src.exception import CustomException
from src.logger import logging
import sys
from src.utils import load_obj
import pandas as pd
import numpy as np

class modelTranning:

    def __init__(self,symbol):
        self.symbol=symbol
    def model_tranning(self,data_path,preprocessor_path):
        try:
            data=pd.read_csv(data_path)
            data=data[['Symbol','Date','Open', 'High', 'Low', 'Close', 'VWAP', 
                    'Vol', 'Prev. Close', 'Turnover', 'Trans.', 'Diff', 'Range', 'Diff %',
                    'Range %', 'VWAP %', '120 Days', '180 Days', '52 Weeks High',
                    '52 Weeks Low']]
            latest_data=data.iloc[-1]
            latest_data = data.tail(1)
            logging.info(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.............................................")
            logging.info(latest_data.shape)
            stock_predicted_price={ }
            preprocessor=load_obj(preprocessor_path)


            for day in range (1,8):
                # logging.info(f"latest_data.shape  {latest_data.shape}       ,       latest_data.columns {latest_data.columns} ")      
                model_path=os.path.join('artifacts',f"{self.symbol}",f"model_{self.symbol}_{day}.pkl")
                model=load_obj(model_path)  
                preprocessor.fit_transform(data)  
                prerprocessed_data=preprocessor.transform(latest_data)

                predicted_value=model.predict(prerprocessed_data)  
                stock_predicted_price[f'Day {day}']=predicted_value  

                latest_data['Open']=latest_data['Close']

                latest_data['High']=latest_data['Close']*1.01

                latest_data['Low'] =latest_data['Close']*0.99

                latest_data['Close'] = predicted_value

                latest_data['VWAP'] = (latest_data['High'] + latest_data['Low'] + latest_data['Close'])/3

                latest_data['prev. Close']=latest_data['Close']             ## hijo ko close ===prev .Close ===latest_data['Close']

                latest_data['Diff']=predicted_value-latest_data['Close']

                latest_data['Diff %']=(latest_data['Diff']/latest_data['Close'])*100

                latest_data['Range']=latest_data['High']=latest_data['Low']

                latest_data['Range %']=(latest_data['Range']/latest_data['Close'])*100

                latest_data['VWAP %']=((latest_data['VWAP']-latest_data['Close'])/latest_data['Close'])*100

                # latest_data['120 Days']= predicted_value if predicted_value >= latest_data['Close'] \
                #       else latest_data['120 Days']  ## have to cahnge ...........................................................................
                
                # latest_data['180 Days']= predicted_value if predicted_value >= latest_data['Close'] \
                #       else latest_data['180 Days'] ## have to change ...............................................................................
                
                predicted_price = predicted_value[0]
                close_price = latest_data['Close'].iloc[0]

                if predicted_price >= close_price:
                    latest_data.loc[:, '120 Days'] = predicted_price
                else:
                    latest_data.loc[:, '120 Days'] = latest_data['120 Days'].iloc[0]

                if predicted_price >= close_price:
                    latest_data.loc[:, '180 Days'] = predicted_price
                else:
                    latest_data.loc[:, '180 Days'] = latest_data['180 Days'].iloc[0]





                latest_data['52 Weeks High'] = max(latest_data['52 Weeks High'].values[0],predicted_value)
           
                latest_data['52 Weeks Low'] = max(latest_data['52 Weeks Low'].values[0],predicted_value)

            logging.info(f'the predicted calue are {stock_predicted_price}')

            return stock_predicted_price


        except Exception as e :
            raise CustomException(e,sys)    