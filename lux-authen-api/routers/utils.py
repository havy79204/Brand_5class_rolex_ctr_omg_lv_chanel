from typing import Annotated
from fastapi import APIRouter, Depends, File, UploadFile
import cv2
import os
import numpy as np
import datetime
from raiki_sdk.core import _normalize_category_str, _normalize_part_str
from config import settings
from fastapi import HTTPException
async def getImage(uploadfile: Annotated[UploadFile, File()]):
    contents = uploadfile.file.read()
    nparr = np.frombuffer(contents, np.int8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    file_name = uploadfile.filename
    
    await uploadfile.close()
    return image, file_name

def round_prob(prob):
    return max(0.01, min(round(prob, 2), 0.99))

import psutil
import subprocess
import xml.etree.ElementTree as ET
import platform

def get_cpu_info():
    return {
        "model": platform.processor(),
        "cores": psutil.cpu_count(logical=False),
        "threads": psutil.cpu_count(logical=True),
        "usage_percent": psutil.cpu_percent(interval=1)
    }

def merge_position(position) -> list:
    if isinstance(position, list):
        return position
    if isinstance(position, dict):
        x1, y1, x2, y2 = 1000000, 1000000, -1, -1
        for key, value in position.items():
            if value is not None and 'box' in value:
                b = value['box']
                x1 = min(x1, b[0])
                y1 = min(y1, b[1])
                x2 = max(x2, b[2])
                y2 = max(y2, b[3])
        position = [x1, y1, x2, y2]

    return position

def get_ram_info():
    ram = psutil.virtual_memory()
    return {
        "total": f"{ram.total / 1e9:.2f} GB",
        "used": f"{ram.used / 1e9:.2f} GB",
        "available": f"{ram.available / 1e9:.2f} GB",
        "percent": ram.percent
    }


def get_nvidia_smi_info():
    """Lấy tất cả thông tin từ nvidia-smi dưới dạng dictionary."""
    try:
        # Chạy nvidia-smi và lấy kết quả dưới dạng XML
        result = subprocess.run(["nvidia-smi", "-q", "-x"], capture_output=True, text=True, check=True)
        xml_output = result.stdout

        # Phân tích XML
        root = ET.fromstring(xml_output)
        data = {}

        # Duyệt qua toàn bộ thông tin
        def parse_element(element):
            if len(element) == 0:  # Nếu là node lá
                return element.text.strip() if element.text else None
            return {child.tag: parse_element(child) for child in element}

        for child in root:
            data[child.tag] = parse_element(child)

        return data

    except Exception as e:
        return {"error": str(e)}

def get_disk_info():
    disk = psutil.disk_usage("/")
    return {
        "total": f"{disk.total / 1e9:.2f} GB",
        "used": f"{disk.used / 1e9:.2f} GB",
        "free": f"{disk.free / 1e9:.2f} GB",
        "percent": disk.percent
    }

def get_network_info():
    net_io = psutil.net_io_counters()
    return {
        "bytes_sent": f"{net_io.bytes_sent / 1e6:.2f} MB",
        "bytes_received": f"{net_io.bytes_recv / 1e6:.2f} MB"
    }

def get_os_info():
    return {
        "os": platform.system(),
        "power": subprocess.getoutput("cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"),  
        "version": platform.version(),
        "release": platform.release(),
        "kernel": platform.uname().version,
        "uptime": subprocess.getoutput("uptime -p")  # Thời gian hoạt động của server
    }

def get_system_info():
    return {
        "os": get_os_info(),
        "cpu": get_cpu_info(),
        "ram": get_ram_info(),
        "gpu": get_nvidia_smi_info(),
        "disk": get_disk_info(),
        "network": get_network_info()
    }


def get_timestamp():
    return str(int(datetime.datetime.now().timestamp()))


def get_model_setting(category: str, part: str, setting_type: str):
    normalized = _normalize_category_str(category.lower())
    return getattr(settings, f"{normalized}_{part}_{setting_type}".lower())

def get_list_parts(category: str):
    list_parts = None
    # if category.lower() == "rolex":
    #     list_parts = settings.MAP_PART_ROLEX
    # elif category.lower() == "bag-lv":
    #     list_parts = settings.MAP_PART_LV
    # elif category.lower() == "omg":
    #     list_parts = settings.MAP_PART_OMG
    if category.lower() in settings.category_brand:
        list_parts = settings.category_brand[category.lower()]["map_part"]
    if not list_parts:
        raise HTTPException(status_code=404, detail=f"Category {category} not found")
    return list_parts

def get_part_name(part: str, category: str):
    list_parts = get_list_parts(category)
    part_name = list_parts[part]
    normalized_part = _normalize_part_str(part_name.lower())

    return normalized_part
