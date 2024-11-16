from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from services.logger import get_logger
import numpy as np

logger = get_logger(__name__)

class Visualizer:
    
    def _generate_class_color(self, class_name: str) -> str:
        # Örnek olarak basit bir renk dönüşümü fonksiyonu
        return (255, 0, 0)  # Kırmızı renk

    def draw_bounding_boxes(self, image: np.ndarray, predictions: pd.DataFrame) -> Image.Image:
        logger.info("Starting to draw bounding boxes on image")
        
        if predictions.empty:
            logger.warning("No predictions to process")
            return image
        
        # Eğer image bir numpy.ndarray ise, bunu PIL.Image nesnesine çeviriyoruz
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        draw = ImageDraw.Draw(image)  # Sadece bir kez tanımlanmalı
        font = ImageFont.load_default()  # Default font; özelleştirilebilir
        
        for _, row in predictions.iterrows():
            try:
                # Sınıf adı ve kutu koordinatlarını çıkar
                xmin, ymin, xmax, ymax = row['xmin'], row['ymin'], row['xmax'], row['ymax']
                label = f"{row['name']} ({row['confidence']:.2f})"
                
                # Sınıfa özgü renk oluştur
                color = self._generate_class_color(row['name'])
                
                # Kutu çiz
                draw.rectangle([(xmin, ymin), (xmax, ymax)], outline=color, width=2)
                
                # Etiketin boyutunu hesapla
                text_bbox = draw.textbbox((0, 0), label, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                # Etiketin pozisyonunu belirle
                text_position = (xmin, ymin - text_height if ymin > text_height else ymin)
                
                # Etiketin okunabilirliği için arka planı dolgu yap
                draw.rectangle(
                    [text_position, (text_position[0] + text_width, text_position[1] + text_height)],
                    fill=color
                )
                
                # Etiketi yazdır
                draw.text(text_position, label, fill="white", font=font)

            except Exception as e:
                logger.error("Error processing bounding box at row %d: %s", _, str(e))

        logger.info("Finished drawing bounding boxes on image")
        return image  # Döngü dışında sadece bir kez döndürülmeli
