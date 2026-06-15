import os
from sklearn.preprocessing import StandardScaler
import pandas as pd
import sys
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from src.logger import logging
from sklearn.pipeline import Pipeline
from src.exception import CustomException
from src.utils import save_obj


class DataTransformationConfig:
    def __init__(self,symbol):
        self.symbol=symbol
        self.preprocessor_path = os.path.join('artifacts',f'{self.symbol}','preprocessor.pkl') 

class dataTransformation:
        
        def __init__ (self,symbol):
            self.symbol=symbol
            self.preprocessor_path=DataTransformationConfig(symbol)

        
        def data_transforamtion(self,train_path,test_path):
             try:
               logging.info("entered into the data_transformation")

               train = pd.read_csv(train_path)
               logging.info(f"the shape of the trained data is {train.shape}") 
               test = pd.read_csv(test_path) 
               logging.info(f"the shape of the test data is {test.shape}")

               logging.info("Train Test data read from their path")

               # for day in range(1, 8):
               #      train[f'Target_Day{day}'] = train['Close'].shift(-day)
               #      test[f'Target_Day{day}'] = train['Close'].shift(-day)
                       
              


               columns= ['Open', 'High', 'Low', 'Close', 'VWAP', 
                    'Vol', 'Prev. Close', 'Turnover', 'Trans.', 'Diff', 'Range', 'Diff %',
                    'Range %', 'VWAP %', '120 Days', '180 Days', '52 Weeks High',
                    '52 Weeks Low']
               

               

               
               pipeline=Pipeline(
                    steps=[
                         ('imputer',SimpleImputer(strategy='median')),
                         ('standardscaler',StandardScaler())
                    ]
               )

               logging.info("make the pipeline")

               preprocessor_obj=ColumnTransformer([
                    ('colum',pipeline,columns)
               ])

               logging.info("make the conumn transfer ")

               save_obj(
                    obj=preprocessor_obj,
                    file_path=self.preprocessor_path.preprocessor_path
               )

               logging.info(f"preprocessor for {self.symbol} is saved")

              

               # train_arr=preprocessor_obj.fit_transform(train)

               # logging.info("preprocessed train")
          
               # test_arr=preprocessor_obj.transform(test)

               # logging.info("preprocessed train")

               # logging.info('test arr shape ',test_arr.shape) 

               return (
                    self.preprocessor_path.preprocessor_path,
                    train,
                    test,
               )  
             
             except Exception as e :
                  raise CustomException (e,sys)
          


# if __name__ == "__main__":  
#      obj = data_transformation('NABIL') 
#      obj.data_transforamtion_obj()
#      obj.data_transforamtion("E:\\stock\\artifacts\\SAHAS\\SAHAS_train.csv","E:\\stock\\artifacts\\SAHAS\\SAHAS_test.csv")




