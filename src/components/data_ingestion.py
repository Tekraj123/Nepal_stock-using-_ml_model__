import pandas as pd
import zipfile
import pandas as pd
import os
import sys
from src.logger import logging
from src.exception import CustomException
# from sklearn.model_selection import train_test_split

all_dfs = []

class DataIngestionConfig:
    def __init__(self, symbol):
        self.symbol = symbol
        self.data_path = os.path.join('artifacts', f"{self.symbol}" , f"{self.symbol}_data.csv")  
        self.train_path = os.path.join('artifacts', f"{self.symbol}" , f"{self.symbol}_train.csv")  
        self.test_path = os.path.join('artifacts', f"{self.symbol}" , f"{self.symbol}_test.csv")  


class DataIngestion:

    def __init__(self, symbol):
        self.symbol = symbol
        self.data_ingestion_path = DataIngestionConfig(symbol=self.symbol)

    def initiate_data_ingestion(self):
        try:
            with zipfile.ZipFile("E:\\stock\\notebook\\nepse_data_all.zip", 'r') as z:     
                
                # सबै CSV files को list लिने
                csv_files = sorted([f for f in z.namelist() if f.endswith('.csv')]) 
                print(f"Total files: {len(csv_files)}") 
                
                for filename in csv_files: 
                    with z.open(filename) as f: 
                        df = pd.read_csv(f, thousands=',') 
                        
                        # filename बाट date बनाउने 
                        # "2026_06_06.csv" → "2026-06-06" 
                        date_str = filename.replace('.csv', '').replace('_', '-') 
                        df['Date'] = pd.to_datetime(date_str) 
                        
                        all_dfs.append(df)

            # सबै files एकै DataFrame मा जोड्ने
            combined = pd.concat(all_dfs, ignore_index=True)
            combined.replace('-', pd.NA, inplace=True)
            # सबै files एकै DataFrame मा जोड्ने

            combined=combined[['Symbol','Date','Open', 'High', 'Low', 'Close', 'VWAP', 
                    'Vol', 'Prev. Close', 'Turnover', 'Trans.', 'Diff', 'Range', 'Diff %',
                    'Range %', 'VWAP %', '120 Days', '180 Days', '52 Weeks High',
                    '52 Weeks Low']]
            
            combined=combined.dropna()
        

            logging.info("ZIP file read successfully ")


            # print(combined.shape)        # (264194, 25)
            # print(combined['Date'].nunique())   # 825 days
            # print(combined['Symbol'].nunique()) # 502 companies

            name_of_column = combined[combined['Symbol']==self.symbol]   #  VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV

            cutoff = int(len(name_of_column)*0.8)
            Train = name_of_column[:cutoff]
            test = name_of_column[cutoff:]
          


                # df['close'] = df['close'].interpolate(method='nearest')

            logging.info("Train Test split successfully")


            os.makedirs(os.path.dirname(self.data_ingestion_path.data_path), exist_ok=True)
            name_of_column.to_csv(os.path.join(self.data_ingestion_path.data_path), index=False)

            Train.to_csv(os.path.join(self.data_ingestion_path.train_path), index=False)

            logging.info("Train file saved")

            test.to_csv(os.path.join(self.data_ingestion_path.test_path), index=False)

            logging.info("Test file saved")

            return (  
                self.data_ingestion_path.data_path,
                self.data_ingestion_path.train_path,
                self.data_ingestion_path.test_path
            )

        except Exception as e :
            raise CustomException(e,sys)



# if __name__ == "__main__":
#     for symbol in ('NABIL','AKJCL','AVYAN'):
#         data_ingestion = DataIngestion(symbol)  
#         data_ingestion.initiate_data_ingestion()  
