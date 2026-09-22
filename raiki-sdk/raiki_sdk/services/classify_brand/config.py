from raiki_sdk.utils.hf_lib import download_file_from_hf

MODEL_VERSION = "v1.2"

# Tải cả 2 file weights .pt của bạn lên
WATCH_CLASSIFY_WEIGHTS = download_file_from_hf(
    repo_id="rikai-ai/brand-classify-v1-2",
    filename="model_2_watch_brands.pt",
)
BAG_CLASSIFY_WEIGHTS = download_file_from_hf(
    repo_id="rikai-ai/brand-classify-v1-2",
    filename="model_3_bag_brands(2).pt",
)

TARGET_SIZE = 384
MODEL_NAME = "convnext_small.in12k_ft_in1k_384"
NUM_CLASSES = 5  # Tổng số brand (Rolex, Omega, Cartier, Chanel, LV)

# Danh sách đầy đủ 5 nhãn brand mà hệ thống hỗ trợ
CLASS_LABELS = ["rolex", "omg", "ctr", "chanel", "bag-lv"]
NUM_CLASSES = len(CLASS_LABELS)
CONFIDENCE_THRESHOLD = 0.65