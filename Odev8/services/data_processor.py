import pandas as pd
from services.logger import get_logger

logger = get_logger(__name__)

class DataProcessor():
    def __init__(self, device):
        self.device = device
        logger.info("DataProcessor initialized . . .")    
    
    def transform_predict_to_df(self, results: list, labeles_dict: dict) -> pd.DataFrame:    
        logger.info("Transforming predictions to DataFrame...")
        try:
            # Log the type and attributes of the results object to understand its structure
            logger.debug("Results object type: %s", type(results))
            logger.debug("Results attributes: %s", dir(results))
            
            # get the all predictions
            predictiions = results[0].to(self.device).numpy()
            
            # Transform the Tensor to numpy array
            predict_bbox = pd.DataFrame(predictiions.boxes.xyxy, columns=['xmin', 'ymin', 'xmax','ymax'])
            logger.debug("DataFrame columns after transformation: %s", predict_bbox.columns)
            
            # Add the confidence of the prediction to the DataFrame
            predict_bbox['confidence'] = predictiions.boxes.conf
            logger.debug("Added confidence to DataFrame")
            
            # Add the class of the prediction to the DataFrame
            predict_bbox['class'] = (predictiions.boxes.cls).astype(int)
            logger.debug("Added class to DataFrame")
            
            # Replace the class number with the class name from the labeles_dict
            predict_bbox['name'] = predict_bbox["class"].replace(labeles_dict)
            logger.info("Transformation complete. DataFrame created with %d rows", len(predict_bbox))
            
            return predict_bbox
        except Exception as e:
            logger.error("Error while transforming predictions to DataFrame: %s", str(e))
            raise