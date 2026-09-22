from raiki_sdk import DetectorBase, YoloResult, YoloValidation
from raiki_sdk import padding_crop_yolo
from .config import YOLO_CONF, YOLO_IMGSZ, PADD_CROP, COLOR_PADDING, TARGET_SIZE
from PIL import Image
import cv2
from raiki_sdk.services import get_brand_detection_service

class ChanelP00Detector(DetectorBase):
    def __init__(self, device: str):
        self.model = get_brand_detection_service(device=device)
        self.yolo_conf = YOLO_CONF
        self.yolo_imgsz = YOLO_IMGSZ
        self.padd_crop = PADD_CROP
        self.color_padding = COLOR_PADDING
        self.image_detect = None
        self.iqa_image = None
        self.output_size = TARGET_SIZE

    def detect(self, image) -> YoloResult:
        pass

    def validate(self, results) -> YoloValidation:
        pass

    def crop(self, image, position) -> Image.Image:
        cropped_image = padding_crop_yolo(image, position, p=self.padd_crop)
        self.image_detect = cropped_image
        return Image.fromarray(cv2.cvtColor(self.image_detect, cv2.COLOR_BGR2RGB))

    def run_pipeline(self, image: any, is_crop: bool = True) -> YoloValidation:
        result = self.model.detect(image=image)
        if result.category.lower() != "chanel":
            return YoloValidation(is_valid=False)
        
        return YoloValidation(
            is_valid=True,
            position=result.bbox,
            image_crop=result.cropped_image
        )