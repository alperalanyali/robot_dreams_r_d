import json
import pandas as pd
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi import FastAPI, status, HTTPException, File, UploadFile
from ultralytics import YOLO
from torchvision import transforms
from services.detector import Detector
from services.logger import get_logger
from services.image_processor import ImageProcessor
from services.visualizer import Visualizer

MODEL_PATH = "./weights/yolo11x.pt"
device = "cpu"
logger = get_logger(__name__)
detector = Detector(model_path=MODEL_PATH,device=device)
image_processor = ImageProcessor()
visualizer = Visualizer()

# Load a model
model = YOLO("yolo11n.pt")

app = FastAPI(
    title="Yolo11 Object Detection FastAPI Service",
    description="""This API allows you to obtain object detection values 
            from an image, returning both the image and a JSON result.""",
    version="v1.0",
)

@app.get("/", include_in_schema=False)
async def redirect_to_docs() -> RedirectResponse:
    """Redirect root URL to API documentation."""
   
    return RedirectResponse("/docs")


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
def perform_healthcheck() -> dict:
    
    logger.info("Healthcheck endpoint hit.")
    return {"healthcheck": "Everything OK!"}


@app.post("/detect-objects-json")
async def detect_objects_json(file:UploadFile = File(...)) -> dict:
    
    logger.info("Detect Objects JSON endpoint hit.")
    result = {"detect_objects": None, "detect_objects_names": None}
    input_image = image_processor.load_image(await file.read())
    logger.info("Image file converted to image object.")
    predictions = detector.make_prediction_from_image(input_image)
    
    detection_results = predictions[['name', 'confidence']]
    detected_objects = detection_results['name'].tolist()
    result["detect_objects_names"] = ', '.join(detected_objects)
    result["detect_objects"] = detection_results.to_dict(orient="records")
    
    logger.info("Detection results: %s", result)
    return result
    # Nesne tespiti ve çizim işlemi
    
@app.post("/detect-objects")
async def detect_objects(file:UploadFile = File(...)) -> StreamingResponse:
    logger.info("Detect Objects endpoint hit.")
    
    input_image = image_processor.load_image(await file.read())
    logger.info("Image file converted to image object.")
    
    predictions = detector.make_prediction_from_image(
        input_image=input_image,
        save=False,
        image_size=640,
        conf=0.5,
        augment=False
    )
    processed_image = visualizer.draw_bounding_boxes(image=input_image,predictions=predictions)
    logger.info("Bounding boxes drawn on image.")
    
    image_stream = image_processor.get_bytes_from_image(processed_image)
    
    return  StreamingResponse(image_stream,media_type='image/jpg')
    


    