import cv2
from ultralytics import YOLO
from raiki_sdk.utils import download_file_from_hf

class LuxCascadeInference:
    def __init__(self, device: str = "cpu"):
        self.device = device
        print("Đang tải các mô hình từ Hugging Face Hub...")
        
        # 1. Tải Model Detector từ Hugging Face
        detector_path = download_file_from_hf(
            repo_id="rikai-ai/brand_detector_v1.7", 
            filename="detector_best.pt"
        )
        self.detector_model = YOLO(detector_path).to(self.device)

        # 2. Tải Model phân loại Bag từ Hugging Face
        bag_path = download_file_from_hf(
            repo_id="rikai-ai/brand-classify-v1-2", 
            filename="model_3_bag_brands(2).pt"
        )
        self.bag_classifier = YOLO(bag_path).to(self.device)

        # 3. Tải Model phân loại Watch từ Hugging Face
        watch_path = download_file_from_hf(
            repo_id="rikai-ai/brand-classify-v1-2", 
            filename="model_2_watch_brands.pt"
        )
        self.watch_classifier = YOLO(watch_path).to(self.device)

        # Từ điển ánh xạ nhánh phân loại giúp dễ dàng mở rộng sau này
        self.classifiers = {
            "bag": self.bag_classifier,
            "watch": self.watch_classifier,
            "brand-watch": self.watch_classifier
        }

        print("Tải mô hình hoàn tất từ Hugging Face!\n")

    def process_image(self, image_path: str):
        img = cv2.imread(image_path)
        if img is None:
            print("Không thể đọc ảnh, vui lòng kiểm tra lại đường dẫn!")
            return None

        print(f"--- Đang phân tích ảnh: {image_path} ---")
        
        # BƯỚC 1: Dùng Detector phát hiện và khoanh vùng vật thể trong ảnh
        results = self.detector_model.predict(img, conf=0.5, verbose=False)
        predictions = []

        found_object = False
        for r in results:
            for box in r.boxes:
                found_object = True
                # Lấy tọa độ khung chữ nhật
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # Lấy tên class do Detector nhận diện (bag hoặc brand-watch)
                cls_id = int(box.cls[0])
                cls_name = self.detector_model.names[cls_id].lower()
                
                # Cắt phần hình ảnh chứa vật thể ra khỏi ảnh gốc
                cropped_img = img[y1:y2, x1:x2]
                if cropped_img.shape[0] == 0 or cropped_img.shape[1] == 0:
                    continue

                brand_name = "Unknown"
                
                # BƯỚC 2: Rẽ nhánh đưa vào model chuyên gia (Classifier) dựa trên kết quả Detector
                if "bag" in cls_name:
                    # Nếu detector nhận diện là túi -> gọi model chuyên phân loại hãng túi
                    cls_results = self.bag_classifier.predict(cropped_img, verbose=False)
                    top_idx = cls_results[0].probs.top1
                    brand_name = self.bag_classifier.names[top_idx]
                    
                elif "watch" in cls_name or "brand-watch" in cls_name:
                    # Nếu detector nhận diện là đồng hồ -> gọi model chuyên phân loại hãng đồng hồ
                    cls_results = self.watch_classifier.predict(cropped_img, verbose=False)
                    top_idx = cls_results[0].probs.top1
                    brand_name = self.watch_classifier.names[top_idx]

                predictions.append({
                    "detected_object": cls_name,  # bag hoặc watch từ detector
                    "box": [x1, y1, x2, y2],
                    "predicted_brand": brand_name  # Thương hiệu cụ thể từ classifier
                })
                print(f"-> Phát hiện vật thể: [{cls_name.upper()}] | Thương hiệu dự đoán: [{brand_name.upper()}]")

        if not found_object:
            print("-> Không tìm thấy túi xách hay đồng hồ nào trong ảnh!")

        return predictions