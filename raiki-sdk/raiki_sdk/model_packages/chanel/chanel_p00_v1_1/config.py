"""
Configuration for Chanel P00 Models Version 1.1
"""
from raiki_sdk.utils import download_file_from_hf

# Model version
CLASSIFIER_MODEL_VERSION = "v1.1"
YOLO_MODEL_VERSION = "v1.1"

# Đường dẫn tới file trọng số Classifier (.pth) và file database embedding (.pkl) của bạn
# Nếu bạn để file trực tiếp trong thư mục package, có thể trỏ đường dẫn cục bộ hoặc dùng hàm download
CLASSIFIER_WEIGHTS = "chanel_p00_classify_v1.1.pth"  # Thay bằng tên file thực tế của bạn
EMBEDDING_STORAGE_PKL = "chanel_p00_vector_storage.pkl"  # Thay bằng tên file .pkl thực tế của bạn

# Classifier model parameters
TARGET_SIZE = 256
CLASSIFIER_MODEL_NAME = "vit_base_patch16_dinov3.lvd1689m"
CLASSIFIER_NUM_CLASSES = 5  # Số lượng class (5 brand hoặc số lớp chi tiết của bạn)
CLASSIFIER_EMBEDDING_SIZE = 512

# Metadata
CATEGORY = "chanel"
PART = "P00"

# Package name
PACKAGE_NAME = "chanel_p00_v1_1"

# YOLO parameters (Dùng chung bộ thông số chuẩn của hệ thống)
YOLO_CONF = 0.55
YOLO_IMGSZ = 640
PADD_CROP = 0.05

COLOR_PADDING = (255, 255, 255)