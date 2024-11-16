import pandas as pd
import numpy as np
import numpy as np
from services.logger import get_logger
from ultralytics import YOLO
from PIL import Image
from services.data_processor import DataProcessor

logger = get_logger(__name__)

class Detector:
    def __init__(self, model_path: str,device):
        # YOLO modelini yükle
        self.model = YOLO(model_path)
        self.model_path = model_path
        self.device = device
        self.data_processor = None

        logger.debug(f"Initializing detector with model path: {self.model_path}")
        self.__init_resource()
    
 
    def __init_resource(self):
        """Initialize the DataProcessor resources """
        try:
            logger.info("Initializing resources for the detector . . .")
            # Initializing the model
            self.model = YOLO(self.model_path)
            logger.info(f"Model loaded successfully from {self.model_path}.")
            
            # Initializing the data processor
            self.data_processor = DataProcessor(self.device)
            logger.info(f"DataProcessor initialized for device: {self.device}.")
            
        except Exception as e:
            logger.error(f"Error initializing resources: {e}")
            raise

    def make_prediction_from_image(self, input_image: Image, save: bool = False, image_size: int = 1248, conf: float = 0.5, augment: bool = False) -> pd.DataFrame:
        try:
            
            logger.info(f"Making predictions on image with size: {input_image.size}, confidence threshold: {conf}")
            
            predictions = self.model.predict(
                imgsz=image_size,
                source=input_image,
                conf=conf,
                save=save,
                augment=augment,
                flipud=0.0,
                fliplr=0.0,
                mosaic=0.0,
            )
            logger.info("Predictions made successfully.")
            predictions_df = self.data_processor.transform_predict_to_df(predictions, self.model.names)
            logger.debug(f"Predictions converted to dataframe with {len(predictions_df)} entries.")
            
            return predictions_df
            
        except Exception as e:
            logger.error(f"Error making predictions: {e}")
            raise
        
   