import numpy as np
import uuid
from collections import namedtuple
from typing import Optional, Callable
from fastapi import APIRouter, File, UploadFile, Request, HTTPException
from fastapi.responses import JSONResponse
from config import settings
from core.logging import APP_LOGGER, MODEL_RESULTS_LOGGER
from raiki_sdk import get_auth_feature 
from routers.utils import getImage, round_prob, get_part_name, get_list_parts
import time
from typing import Dict, Union
import starlette
import starlette.datastructures
router = APIRouter()


PredictResult = namedtuple("PredictResult", ["part_name", "real_prob", "label", "file_name"])

class Predict():
    def __init__(self, part_name: str, feature: Callable, upload_file: UploadFile):
        self.part_name = part_name
        self.feature = feature
        self.upload_file = upload_file

    async def run(self) -> PredictResult:
        if self.feature is None:
            return PredictResult(self.part_name, 0.01, "Can't not load feature", None)
        
        image, file_name = await getImage(self.upload_file)

        detect_result = self.feature.detector.detect(image)
        if detect_result is None:
            APP_LOGGER.warning(f"The Detector model can't detect {self.part_name} from the file upload ({file_name})")
            return PredictResult(self.part_name, 0.01, "Unable detect part", file_name)
        
        validate_result = self.feature.detector.validate(detect_result)
        if not validate_result.is_valid:
            APP_LOGGER.warning(f"The Detector model can't validate {self.part_name} from the file upload ({file_name})")
            return PredictResult(self.part_name, 0.01, "Unable validate part", file_name)
        
        cropped_image = self.feature.detector.crop(image, validate_result.position)
        if cropped_image is None:
            APP_LOGGER.warning(f"The Detector model can't detect {self.part_name} from the file upload ({file_name})")
            return PredictResult(self.part_name, 0.01, "Unable crop part", file_name)
        
        authentication_result = self.feature.authenticator.forward(cropped_image)

        return PredictResult(self.part_name, round_prob(authentication_result.probability), authentication_result.label, file_name)

@router.post("/{category}",
summary="[DEPLOPMENT] Upload part images for a specific category (template-based matching).",
description="""
**DEPLOPMENT**  
Upload part images for a specific category (template-based matching).

**Steps:**
1. Get images from the request  
2. Extract features using category and part name  
3. Predict each part and return the result
""")
async def upload_part(
    category: Optional[str],
    P01: Union[UploadFile, str, None] = File(None),
    P02: Union[UploadFile, str, None] = File(None),
    P03: Union[UploadFile, str, None] = File(None),
    P04: Union[UploadFile, str, None] = File(None),
    P05: Union[UploadFile, str, None] = File(None),
    P08: Union[UploadFile, str, None] = File(None),
    P09: Union[UploadFile, str, None] = File(None),
    P10: Union[UploadFile, str, None] = File(None),
    LV_P01: Union[UploadFile, str, None] = File(None),
    LV_P02: Union[UploadFile, str, None] = File(None),
    LV_P03: Union[UploadFile, str, None] = File(None),
    LV_P04: Union[UploadFile, str, None] = File(None),
    LV_P04_m2: Union[UploadFile, str, None] = File(None),
    LV_P05: Union[UploadFile, str, None] = File(None),
    LV_P06: Union[UploadFile, str, None] = File(None),
    LV_P09: Union[UploadFile, str, None] = File(None),
    OMG_P01: Union[UploadFile, str, None] = File(None),
    OMG_P02: Union[UploadFile, str, None] = File(None),
    OMG_P03: Union[UploadFile, str, None] = File(None),
    OMG_P05: Union[UploadFile, str, None] = File(None),
    OMG_P06: Union[UploadFile, str, None] = File(None)
):
    try:
        start_req = time.time()
        handle_items: list[Predict] = []

        if category == "rolex":
            if P01 and isinstance(P01, starlette.datastructures.UploadFile):
                handle_items.append(Predict("P01", get_auth_feature(category, "P01", getattr(settings, f"rolex_p01_version"), device=settings.device), P01))
            if P02 and isinstance(P02, starlette.datastructures.UploadFile):
                handle_items.append(Predict("P02", get_auth_feature(category, "P02", getattr(settings, f"rolex_p02_version"), device=settings.device), P02))
            if P03 and isinstance(P03, starlette.datastructures.UploadFile):
                handle_items.append(Predict("P03", get_auth_feature(category, "P03", getattr(settings, f"rolex_p03_version"), device=settings.device), P03))
            if P04 and isinstance(P04, starlette.datastructures.UploadFile):
                handle_items.append(Predict("P04", get_auth_feature(category, "P04", getattr(settings, f"rolex_p04_version"), device=settings.device), P04))
            if P05 and isinstance(P05, starlette.datastructures.UploadFile):
                handle_items.append(Predict("P05", get_auth_feature(category, "P05", getattr(settings, f"rolex_p05_version"), device=settings.device), P05))
            if P08 and isinstance(P08, starlette.datastructures.UploadFile):
                handle_items.append(Predict("P08", get_auth_feature(category, "P08", getattr(settings, f"rolex_p08_version"), device=settings.device), P08))
            if P09 and isinstance(P09, starlette.datastructures.UploadFile):
                handle_items.append(Predict("P09", get_auth_feature(category, "P09", getattr(settings, f"rolex_p09_version"), device=settings.device), P09))
            if P10 and isinstance(P10, starlette.datastructures.UploadFile):
                handle_items.append(Predict("P10", get_auth_feature(category, "P10", getattr(settings, f"rolex_p10_version"), device=settings.device), P10))

        elif category == "bag-lv":
            if LV_P01 and isinstance(LV_P01, starlette.datastructures.UploadFile):
                handle_items.append(Predict("LV_P01", get_auth_feature(category, "LV_P01", getattr(settings, f"lv_p01_version"), device=settings.device), LV_P01))
            if LV_P02 and isinstance(LV_P02, starlette.datastructures.UploadFile):
                handle_items.append(Predict("LV_P02", get_auth_feature(category, "LV_P02", getattr(settings, f"lv_p02_version"), device=settings.device), LV_P02))
            if LV_P03 and isinstance(LV_P03, starlette.datastructures.UploadFile):
                handle_items.append(Predict("LV_P03", get_auth_feature(category, "LV_P03", getattr(settings, f"lv_p03_version"), device=settings.device), LV_P03))
            if LV_P04 and isinstance(LV_P04, starlette.datastructures.UploadFile):
                handle_items.append(Predict("LV_P04", get_auth_feature(category, "LV_P04", getattr(settings, f"lv_p04_version"), device=settings.device), LV_P04))
            if LV_P04_m2 and isinstance(LV_P04_m2, starlette.datastructures.UploadFile):
                handle_items.append(Predict("LV_P04_m2", get_auth_feature(category, "LV_P04_m2", getattr(settings, f"lv_p04_version"), device=settings.device), LV_P04_m2))
            if LV_P05 and isinstance(LV_P05, starlette.datastructures.UploadFile):
                handle_items.append(Predict("LV_P05", get_auth_feature(category, "LV_P05", getattr(settings, f"lv_p05_version"), device=settings.device), LV_P05))
            if LV_P06 and isinstance(LV_P06, starlette.datastructures.UploadFile):
                handle_items.append(Predict("LV_P06", get_auth_feature(category, "LV_P06", getattr(settings, f"lv_p06_version"), device=settings.device), LV_P06))
            if LV_P09 and isinstance(LV_P09, starlette.datastructures.UploadFile):
                handle_items.append(Predict("LV_P09", get_auth_feature(category, "LV_P09", getattr(settings, f"lv_p09_version"), device=settings.device), LV_P09))
            
        elif category == "omg":
            if OMG_P01 and isinstance(OMG_P01, starlette.datastructures.UploadFile):
                handle_items.append(Predict("OMG_P01", get_auth_feature(category, "OMG_P01", getattr(settings, f"omg_p01_version"), device=settings.device), OMG_P01))
            if OMG_P02 and isinstance(OMG_P02, starlette.datastructures.UploadFile):
                handle_items.append(Predict("OMG_P02", get_auth_feature(category, "OMG_P02", getattr(settings, f"omg_p02_version"), device=settings.device), OMG_P02))
            if OMG_P03 and isinstance(OMG_P03, starlette.datastructures.UploadFile):
                handle_items.append(Predict("OMG_P03", get_auth_feature(category, "OMG_P03", getattr(settings, f"omg_p03_version"), device=settings.device), OMG_P03))
            if OMG_P05 and isinstance(OMG_P05, starlette.datastructures.UploadFile):
                handle_items.append(Predict("OMG_P05", get_auth_feature(category, "OMG_P05", getattr(settings, f"omg_p05_version"), device=settings.device), OMG_P05))
            if OMG_P06 and isinstance(OMG_P06, starlette.datastructures.UploadFile):
                handle_items.append(Predict("OMG_P06", get_auth_feature(category, "OMG_P06", getattr(settings, f"omg_p06_version"), device=settings.device), OMG_P06))

        predict_results: list[PredictResult] = []
        for handle_item in handle_items:
            result = await handle_item.run()
            predict_results.append(result)

        mean_prob = round_prob(np.array([item.real_prob for item in predict_results]).mean()) if predict_results else 0.01
        transaction = str(uuid.uuid4())
        logstr = []
        logstr.append(f"transaction: {transaction}")
        logstr.append(f"real_prob_mean: {mean_prob}")
        parts = []

        for result in predict_results:
            logstr.append(f"{result.part_name}: (file_name: {result.file_name}, prob: {result.real_prob}, label: {result.label})")
            parts.append({
                "part": result.part_name,
                "prob": result.real_prob,
                "label": result.label
            })

        end_req = time.time()
        MODEL_RESULTS_LOGGER.info(f"test - upload part {category} time: {end_req - start_req}" + "\n".join(logstr))
        APP_LOGGER.info(f"upload part {category} time: {end_req - start_req}")
        return JSONResponse(
            content={
                "transaction": transaction,
                "real_prob_mean": mean_prob,
                "parts": parts,
            }
        ) 
    except Exception as e:
        import traceback
        traceback.print_exc()
        MODEL_RESULTS_LOGGER.error(f"Error in upload_part: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/v2/{category}",
summary="[PRODUCTION] Upload part images for a specific category (no template matching).",
description="""
**PRODUCTION**  
Upload part images for a specific category (no template matching).

**Steps:**
1. Get images from the request  
2. Extract features using category and part name  
3. Predict each part and return the result
""")
async def upload_part_v2( category: str, request: Request):
    start_req = time.time()
    form = await request.form()
    request_id = request.state.request_id

    files: Dict[str, starlette.datastructures.UploadFile] = {}
    handle_items: list[Predict] = []

    # Get images from request; ignore additional metadata
    for key, value in form.items():
        if isinstance(value, starlette.datastructures.UploadFile):
            files[key] = value

    list_parts = get_list_parts(category)
    # Predict each part, if part or file not found, return 0.01
    for key, file in files.items():
        if key in list_parts:
            part_name = list_parts[key]
            try:
                feature = get_auth_feature(category, part_name, getattr(settings, f"{part_name}_version"), device=settings.device)
                handle_items.append(Predict(key, feature, file))
            except Exception as e:
                handle_items.append(Predict(key, None, None))

    
    predict_results: list[PredictResult] = []
    for handle_item in handle_items:
        result = await handle_item.run()
        predict_results.append(result)

    mean_prob = round_prob(np.array([item.real_prob for item in predict_results]).mean())
    transaction = str(uuid.uuid4())
    parts = []
    for result in predict_results:
        parts.append({
            "part": result.part_name,
            "prob": result.real_prob,
            "label": result.label
        })
    processing_time = time.time() - start_req

    data_response = {
        "transaction": transaction,
        "processing_time": processing_time,
        "real_prob_mean": mean_prob,
        "parts": parts,
    }
    MODEL_RESULTS_LOGGER.info(f"[/upload-part/v2/{category}] - {request_id} - from {list(form.keys())} to {data_response}")
    # MODEL_RESULTS_LOGGER.info(f"upload part {category} input: {list(form.keys())}, output: {data_response}.")
    return JSONResponse(
        content=data_response
    ) 
    