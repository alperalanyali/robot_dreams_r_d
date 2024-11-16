import cv2
import numpy as np
from services.logger import get_logger
from fastapi.responses import StreamingResponse
import io
from PIL import Image

logger = get_logger(__name__)

class ImageProcessor:
    
    def __init(self):
        logger.info("Image Processor initailize...")
        
    def load_image(self, image_bytes: bytes) -> np.ndarray:
        """Yüklenen dosyayı NumPy dizisine dönüştür."""
        np_image = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
        return image
    
    def get_bytes_from_image(self, image: Image) -> bytes:
 
        try:
            return_image = io.BytesIO()
            image.save(return_image, format='JPEG', quality=85)  # save the image in JPEG format with quality 85
            return_image.seek(0)  # set the pointer to the beginning of the file
            logger.info("Image successfully converted to bytes.")
        except Exception as e:
            logger.error("Error converting image to bytes: %s", e)
            raise
        return return_image

    