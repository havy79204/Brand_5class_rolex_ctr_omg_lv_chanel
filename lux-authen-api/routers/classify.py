from fastapi import APIRouter, File, UploadFile, HTTPException
from core.cascade_service import LuxCascadeInference
import cv2
import numpy as np
import tempfile
import os

router = APIRouter()

# Khởi tạo instance cascade engine
cascade_engine = LuxCascadeInference(device="cpu")

@router.post("/run")
async def run_cascade_inference(checkfile: UploadFile = File(...)):
    try:
        # Đọc dữ liệu ảnh từ request upload lên
        contents = await checkfile.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Không thể đọc được file ảnh.")

        # Lưu file tạm để xử lý qua hàm process_image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
            temp.write(contents)
            temp_path = temp.name

        # Chạy pipeline cascade
        results = cascade_engine.process_image(temp_path)
        
        # Dọn dẹp file tạm
        os.remove(temp_path)

        return {
            "result": "ok",
            "predictions": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))