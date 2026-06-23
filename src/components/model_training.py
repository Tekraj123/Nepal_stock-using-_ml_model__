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
            data=data[['Open', 'High', 'Low', 'Close', 'VWAP','Vol', "Daily_return","SMA_20","EMA_20","RSI_14","MACD"]]
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



                # df contains:
                # Open, High, Low, Close, Volume

                # =====================
                # Future Return (using shift(-1))
                # =====================
                latest_data["Future_Return"] = (
                    latest_data["Close"] - latest_data["Close"].shift(-1)
                ) / latest_data["Close"].shift(-1)

                # =====================
                # SMA(20)
                # =====================
                latest_data["SMA_20"] = latest_data["Close"].rolling(window=20).mean()

                # =====================
                # EMA(20)
                # =====================
                latest_data["EMA_20"] = latest_data["Close"].ewm(span=20, adjust=False).mean()

                # =====================
                # RSI(14) using shift(-1)
                # =====================
                delta = latest_data["Close"] - latest_data["Close"].shift(-1)

                gain = delta.clip(lower=0)
                loss = -delta.clip(upper=0)

                avg_gain = gain.rolling(window=14).mean()
                avg_loss = loss.rolling(window=14).mean()

                rs = avg_gain / avg_loss

                latest_data["RSI_14"] = 100 - (100 / (1 + rs))

                # =====================
                # MACD
                # =====================
                ema12 = latest_data["Close"].ewm(span=12, adjust=False).mean()
                ema26 = latest_data["Close"].ewm(span=26, adjust=False).mean()

                latest_data["MACD"] = ema12 - ema26

                # =====================
                # ATR(14) using shift(-1)
                # =====================
                tr1 = latest_data["High"] - latest_data["Low"]

                tr2 = abs(latest_data["High"] - latest_data["Close"].shift(-1))
                tr3 = abs(latest_data["Low"] - latest_data["Close"].shift(-1))

                tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

                latest_data["ATR_14"] = tr.rolling(window=14).mean()


           
                
            logging.info(f'the predicted calue are {stock_predicted_price}')

            return stock_predicted_price


        except Exception as e :
            raise CustomException(e,sys)    