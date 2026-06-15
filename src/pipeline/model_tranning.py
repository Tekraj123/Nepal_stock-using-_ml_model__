from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import dataTransformation
from src.components.model_evoulation import modelEvoulation
from src.components.model_training import modelTranning
from src.logger import logging


ingestion= DataIngestion("NABIL")
data_path,train_path,test_path=ingestion.initiate_data_ingestion()   


logging.info("ajhjkahjhadjhdsjhjkhjhsajhash")     


transformation= dataTransformation("NABIL")    
preprocessor_path,Train,Test= transformation.data_transforamtion(train_path,test_path)       


tranning = modelEvoulation("NABIL")   
tranning.model_evoulation(preprocessor_path,Train,Test)  



model_trann=modelTranning('NABIL')
model_trann.model_tranning(data_path,preprocessor_path)





