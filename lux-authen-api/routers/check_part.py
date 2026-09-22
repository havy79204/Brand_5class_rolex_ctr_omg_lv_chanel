import numpy as np
import cv2
from PIL import Image
from typing import Annotated
from fastapi import APIRouter, File, UploadFile, WebSocket, WebSocketDisconnect, Request, HTTPException
from fastapi.responses import JSONResponse
from routers.utils import round_prob, get_timestamp
import time
from core.logging import APP_LOGGER, MODEL_RESULTS_LOGGER
from config import settings
from routers.utils import get_model_setting, get_part_name, getImage, merge_position
from raiki_sdk import get_auth_feature

router = APIRouter()
v2_router = APIRouter()


@router.post("/",
summary= "[PRODUCTION] Check part of the product when a photo is taken.",
description="""
Check part of the product when a photo is taken.
- **Category**: `rolex`, `bag-lv`, `omg`, `chanel`, `ctr`
- **Part codes**: `P01`, `P02`, `P03`, `P04`, `P05`, `P08`, `P09`, `P10`, ...  
- **Validation**: Detect and validate part using YOLO model
"""
)
async def check_part(
    request: Request,
    checkfile: Annotated[UploadFile, File()],
    part: str,
    category: str = "rolex",
    frame: str = "0,0,1,1",
    check_real_prob: bool = True,
):
    image, file_name = await getImage(checkfile)
    request_id = request.state.request_id

    part_name = get_part_name(part, category)
    try:
        feature = get_auth_feature(category, part_name, get_model_setting(category, part_name, "version"), device=settings.device)
    except Exception as e:
        MODEL_RESULTS_LOGGER.warning(f"[/check/ {category} - {part}] - {request_id} - Feature load exception {file_name} - {str(e)}")
        return JSONResponse(
            content={
                "result": "failed",
                "position": None,
                "img_quality_validate": None,
                "score": None,
                "error": "model_load_error"
            }
        )

    detector = feature.detector
    authenticator = feature.authenticator

    # 2. YOLO detection
    try:
        detect_result = detector.detect(image)
    except Exception as e:
        MODEL_RESULTS_LOGGER.warning(f"[/check/ {category} - {part}] - {request_id} - Detector exception {file_name} - {str(e)}")
        return JSONResponse(
            content={
                "result": "failed",
                "position": None,
                "img_quality_validate": None,
                "score": None,
                "error": "yolo_error"
            }
        )

    if detect_result is None:
        MODEL_RESULTS_LOGGER.warning(f"[/check/ {category} - {part}] - {request_id} - YOLO fail {file_name}")
        return JSONResponse(
            content={
                "result": "failed",
                "position": None,
                "img_quality_validate": None,
                "score": None,
                "error": "detect_error"
            }
        )

    MODEL_RESULTS_LOGGER.info(f"[/check/ {category} - {part}] - {request_id} - YOLO ok {file_name}")

    # 4. Validate detector result
    validate_result = detector.validate(detect_result)
    if not validate_result.is_valid:
        MODEL_RESULTS_LOGGER.warning(f"[/check/ {category} - {part}] - {request_id} - Validate detector result failed {file_name}")
        return JSONResponse(
            content={
                "result": "failed",
                "position": None,
                "img_quality_validate": None,
                "score": None,
                "error": "detect_error"
            }
        )

    position = validate_result.position
    position_merged = merge_position(position)

    if isinstance(check_real_prob, str):
        check_real_prob = check_real_prob.lower() not in ("false", "0", "no", "none", "off")

    MODEL_RESULTS_LOGGER.info(f"[/check/ {category} - {part}] - {request_id} - check_real_prob={check_real_prob} {file_name}")

    image_quality_validate = "Pass"
    score = 1.0

    if check_real_prob:
        try:
            cropped_image = detector.crop(image, position)
            if cropped_image is None:
                raise ValueError("Failed to crop image for authentication")
            authentication_result = authenticator.forward(cropped_image)
            
            raw_label = str(getattr(authentication_result, "label", "fake"))
            probability = getattr(authentication_result, "probability", 0.5)
            
            if "-" in raw_label:
                parts = raw_label.split("-", 1)
                try:
                    probability = float(parts[0])
                    label = parts[1]
                except ValueError:
                    label = raw_label
            else:
                label = raw_label
            
        except Exception as e:
            MODEL_RESULTS_LOGGER.warning(f"[/check/ {category} - {part}] - {request_id} - Authenticator exception {file_name} - {e}")
            return JSONResponse(
                content={
                    "result": "failed",
                    "position": position,
                    "img_quality_validate": image_quality_validate,
                    "score": score,
                    "error": "auth_error"
                }
            )

    # Lấy ngưỡng IQA động từ config dựa trên category (brand) và part hiện tại
    current_iqa_threshold = settings.get_iqa_threshold(brand=category, part=part)

    return JSONResponse(
        content={
            "result": "ok",
            "position": position,
            "img_quality_validate": image_quality_validate,
            "score": score,
            "iqa_threshold": current_iqa_threshold,
            "error": None,
            "probability": round_prob(probability) if check_real_prob else None,
            "label": label if check_real_prob else None,
            "metadata": authentication_result.metadata if check_real_prob else None,
        }
    )


@v2_router.post("/",
summary="[DEVELOPMENT] Check part result when take a photo.",
description="""
[DEVELOPMENT] Check part result when take a photo.
Same as `/check_part`
""")
async def v2_check_part(
    checkfile: Annotated[UploadFile, File()],
    part: str,
    category: str = "rolex",
):
    start_req = time.time()
    APP_LOGGER.info(f"check part v2 {category} - {part}")

    image, file_name = await getImage(checkfile)
    part_name = get_part_name(part, category)
    feature = get_auth_feature(category, part_name, get_model_setting(category, part_name, "version"), device=settings.device)
    detector = feature.detector
    authenticator = feature.authenticator

    token = get_timestamp()
    detect_result = detector.detect(image)

    if detect_result is None:
        APP_LOGGER.warning(f"The Detector model can't detect {category} - {part} from the file upload ({file_name} [{token}])")
        return {"result": "failed"}
    
    validate_result = detector.validate(detect_result)
    if not validate_result.is_valid:
        APP_LOGGER.warning(f"The YOLO model can't validate {category} - {part} from the file upload ({file_name} [{token}])")
        return {"result": "failed"}
    
    position = validate_result.position
    position_merged = merge_position(position)
    cropped_image = detector.crop(image, position)
    authentication_result = authenticator.forward(cropped_image)
    
    return JSONResponse(
        content={
            "result": "ok",
            "real_prob": round_prob(authentication_result.probability),
            "label": authentication_result.label,
            "position": position,
            "img_quality_validate": "Pass",
            "score": 1.0
        }
    )


@v2_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    category: str,
):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            if len(data) < 62:
                await websocket.send_json({"result": "faild"})
                continue
            part = data[:3].decode("utf-8").strip()
            frame = data[3:26].decode("utf-8").strip()
            frame = frame.rstrip('\x00')
            uid = data[26:62].decode("utf-8").strip()
            image_data = data[62:]

            feature = get_auth_feature(category, part, get_model_setting(category, part, "version"), device=settings.device)
            detector = feature.detector

            np_array = np.frombuffer(image_data, dtype=np.uint8)
            image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

            if image is not None:
                detect_result = detector.detect(image)
                if detect_result is None:
                    await websocket.send_json({"result": "faild"})
                else:
                    validate_result = detector.validate(detect_result)
                    position = validate_result.position
                    if position is None:
                        await websocket.send_json({"result": "faild"})
                        continue  

                    await websocket.send_json({
                        "result": "ok",
                        "position": position,
                        "img_quality_validate": "Pass",
                        "score": 1.0,
                        "id": uid
                    })
            else:
                await websocket.send_json({"result": "faild"})
    except WebSocketDisconnect:
        print("Client disconnected")


@v2_router.post("/yolo_inference",
summary="[DEVELOPMENT] Yolo inference api",
description="""
[DEVELOPMENT] Yolo inference api
""")
async def yolo_inference(
    checkfile: Annotated[UploadFile, File()],
    part: str,
    category: str = "rolex",
):
    APP_LOGGER.info(f"check part v2 {category} - {part}")
    image, file_name = await getImage(checkfile)

    feature = get_auth_feature(category, part, get_model_setting(category, part, "version"), device=settings.device)
    detector = feature.detector

    detect_result = detector.detect(image)
    token = get_timestamp()

    if detect_result is None:
        APP_LOGGER.warning(f"The YOLO model can't detect {category} - {part} from the file upload ({file_name} [{token}])")
        return JSONResponse(content={"result": "failed"})
    
    validate_result = detector.validate(detect_result)
    position = validate_result.position

    return JSONResponse(
        content={
            "result": "ok",
            "position": position
        }
    )