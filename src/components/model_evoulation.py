import os
from src.exception import CustomException
from src.logger import logging
import sys
import numpy as np
from sklearn.metrics import (mean_absolute_error, 
                             root_mean_squared_error,
                              mean_squared_error,
                              mean_absolute_percentage_error,
                              r2_score)
from src.utils import load_obj
from src.utils import save_obj
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
)
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor

from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor

from sklearn.linear_model import LogisticRegression






# class modelEvoationConfig :
#     def __init__(self,symbol):
#         self.symbol=symbol
#         self.model_path=os.path.join('artifacts',f"{self.symbol}","model.pkl")             


class modelEvoulation:
    def __init__ (self,symbol):
        self.symbol=symbol 
        # self.model_path=modelEvoationConfig(self.symbol)


    def model_evoulation(self,file_path,train,test):
        try:
            preprocessor=load_obj(file_path)
            logging.info("in the model Evoulation ")



            for day in range(1,8):

                train[f'Target_Day{day}']=train['Close'].shift(-day)
                test[f'Target_Day{day}']=test['Close'].shift(-day)
                trains=train.dropna()
                tests=test.dropna()
                logging.info (f"the columns are {train.isnull().sum()}")  
                logging.info (f"the columns are {test.isnull().sum()}")  

                x_train=preprocessor.fit_transform(trains)
                logging.info(f"preprocessed x_train shape {x_train.shape}")
                x_test=preprocessor.transform(tests)
                logging.info(f"preprocessed x_test shape {x_test.shape}")

                y_train=trains[f'Target_Day{day}']
                logging.info(f"preprocessed y_train shape {y_train.shape}")

                y_test=np.array(tests[f'Target_Day{day}'])
                logging.info(f"preprocessed y_test shape {y_test.shape}")

            
                param= {
                        'n_estimators': [100, 200],
                        'max_depth': [10, 20, None],
                        'min_samples_split': [2, 5],
                }
                model=RandomForestRegressor()
                grid=GridSearchCV(estimator=model,param_grid=param,cv=5,n_jobs=-1) 
                model=grid.fit (x_train,y_train)   
                model.best_estimator_
                model.fit (x_train,y_train)         

                # models[f'Day{day}'] = model
                model_path=os.path.join('artifacts',f"{self.symbol}",f"model_{self.symbol}_{day}.pkl")    
                save_obj(model,model_path)  
                logging.info(f"{model_path}") 

                predicted_value=model.predict(x_test)
                mae  = mean_absolute_error(y_test,predicted_value)
                rmse = np.sqrt(mean_squared_error(y_test, predicted_value))
                mape = mean_absolute_percentage_error(y_test, predicted_value) * 100
                r2   = r2_score(y_test, predicted_value)
                
                actual_dir = (y_test[1:] > y_test[:-1])
                pred_dir   = (predicted_value[1:]  > predicted_value[:-1])
                dir_acc    = (actual_dir == pred_dir).mean() * 100

                logging.info(f"{self.symbol} Day {day} | MAE={mae:.2f} | RMSE={rmse:.2f} | "
                f"MAPE={mape:.2f}% | R²={r2:.4f}  |  DirAcc={dir_acc:.1f}%")     

        except Exception as e:
            raise CustomException(e,sys)

