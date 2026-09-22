"""
Configuration for Chanel P04 Model
"""
from raiki_sdk.utils import download_file_from_hf

# Model version
AUTH_MODEL_VERSION = "v1_1" 
YOLO_MODEL_VERSION = "v1_1"

# Model weights paths (tải từ Hugging Face repository của bạn cho Chanel P04)
YOLO_WEIGHTS = download_file_from_hf(
    repo_id="rikai-ai/chanel_p04_detect_v1.0_21092026",  # Thay bằng repo_id thực tế của bạn trên HF
    filename="chanel_p04_yolov3_best.pt"      # Thay bằng tên file weight detector thực tế
)

AUTH_WEIGHTS = download_file_from_hf(
    repo_id="rikai-ai/chanel_p04_detect_v1.0_21092026",      # Thay bằng repo_id thực tế của bạn trên HF
    filename="chanel_p04_auth_21092026.pth"         # Thay bằng tên file weight auth thực tế
)

# AUTH parameters
TARGET_SIZE = 512
AUTH_MODEL_NAME = "maxvit_tiny_tf_512.in1k"
AUTH_NUM_CLASSES = 2
AUTH_CLASS_LABELS = ['fake', 'real']

# Metadata
CATEGORY = "chanel"
PART = "P04"

# Package name
PACKAGE_NAME = "chanel_p04_v1_1"

# YOLO parameters
YOLO_CONF = 0.25
YOLO_IMGSZ = 640

# Resize parameters
COLOR_PADDING = (85, 85, 85)