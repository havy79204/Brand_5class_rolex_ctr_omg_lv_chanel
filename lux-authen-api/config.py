import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Lux Authentication API"
    app_version: str = "0.1.0"
    app_description: str = "API for classifying and authenticating luxury products using AI"
    app_updated_at: str = "2025-12-10"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_reload: bool = True
    app_log_level: str = "info"
    app_log_folder: str = "logs"
    app_log_model_results_name: str = "model_results"
    app_log_request_name: str = "request"
    app_log_app_name: str = "app"
    app_log_tz_offset_hours: int = 7
    app_log_max_log_size: int = 20 * 1024 * 1024 # 20MB
    app_log_max_backup_file: int = 5
    
    device: str

    # Advanced Redframe check
    use_advanced_redframe: bool

    # Reload 
    reload: bool

    # Code confirm
    CODE_CONFIRM: str

    # LV model package versions
    lv_p00_version: str = "v1.5"
    lv_p01_version: str = "v1.6"
    lv_p02_version: str = "v1.6"
    lv_p03_version: str = "v1.2"
    lv_p04_version: str = "v1.3"
    lv_p04case4_version: str = "v1.5"
    lv_p05_version: str = "v1.2"
    lv_p06_version: str = "v1.1"
    lv_p09_version: str = "v1.1"

    # Rolex model package versions
    rolex_p00_version: str = "v1.7" 
    rolex_p01_version: str = "v1.4"
    rolex_p02_version: str = "v1.4"
    rolex_p03_version: str = "v1.4"
    rolex_p04_version: str = "v1.4"
    rolex_p05_version: str = "v1.4"
    rolex_p08_version: str = "v1.5"
    rolex_p09_version: str = "v1"
    rolex_p10_version: str = "v1.1"

    # Chanel model package versions
    chanel_p00_version: str = "v1.1"
    chanel_p04_version: str = "v1_1"

    # Omega model package versions
    omg_p00_version: str = "v1_3"
    omg_p01_version: str = "v1.2"
    omg_p02_version: str = "v1.3"
    omg_p03_version: str = "v1.4"
    omg_p05_version: str = "v1.3"
    omg_p06_version: str = "v1.2"

    # CTR model package versions
    ctr_p00_version: str = "v1.1"
    ctr_p01_version: str = "v1.1"
    ctr_p02_version: str = "v1.1"
    ctr_p03_version: str = "v1.1"
    ctr_p04_version: str = "v1.1"
    ctr_p05_version: str = "v1.1"
    ctr_p06_version: str = "v1.1"

    # LV model package redframe thresholds
    lv_p01_threshold: float = 2.5
    lv_p02_threshold: float = 2.0
    lv_p03_threshold: float = 1.0
    lv_p04_threshold: float = 1.0
    lv_p04case4_threshold: float = 1.0
    lv_p05_threshold: float = 2.7
    lv_p06_threshold: float = 2.0
    lv_p09_threshold: float = 2.7

    # Rolex model package redframe thresholds
    rolex_p01_threshold: float = 2.3
    rolex_p02_threshold: float = 2.3
    rolex_p03_threshold: float = 1.0
    rolex_p04_threshold: float = 2.3
    rolex_p05_threshold: float = 1.5
    rolex_p08_threshold: float = 1.3
    rolex_p09_threshold: float = 1.9
    rolex_p10_threshold: float = 1.9

    # Chanel model package redframe thresholds
    chanel_p00_threshold: float = 2.0
    chanel_p04_threshold: float = 2.0

    # Omega model package redframe thresholds
    omg_p01_threshold: float = 1.1
    omg_p02_threshold: float = 1.0
    omg_p03_threshold: float = 1.0
    omg_p05_threshold: float = 2.0
    omg_p06_threshold: float = 2.8

    # CTR model package redframe thresholds
    ctr_p01_threshold: float = 2.3
    ctr_p02_threshold: float = 2.3
    ctr_p03_threshold: float = 1.2
    ctr_p04_threshold: float = 1.2
    ctr_p05_threshold: float = 2.3
    ctr_p06_threshold: float = 2.3
    
    advanced_redframe_parts: dict[str, list[str]] = {
        "rolex": ["P01", "P02", "P03"],
        "bag-lv": [],
        "omg": [],
        "ctr": [],
        "chanel": [],
    }
    
    # Brand Mapping Dictionaries
    MAP_PART_LV: dict[str, str] = {
        "LV_P00": "lv_p00",
        "LV_P01": "lv_p01",
        "LV_P02": "lv_p02",
        "LV_P03": "lv_p03",
        "LV_P04": "lv_p04",
        "LV_P05": "lv_p05",
        "LV_P06": "lv_p06",
        "LV_P09": "lv_p09",
        "LV_P01_m2": "lv_p01",
        "LV_P02_m2": "lv_p02",
        "LV_P03_m2": "lv_p03",
        "LV_P04_m2": "lv_p04case4",
        "LV_P05_m2": "lv_p05",
        "LV_P01_Part1": "lv_p01",
        "LV_P01_Part2": "lv_p01",
        "LV_P01_Part3": "lv_p01",
        "LV_P01_Part4": "lv_p01",
        "LV_P01_Part5": "lv_p01",
        "LV_P03_Part6": "lv_p03",
        "LV_P03_Part7": "lv_p03",
        "LV_P03_Part8": "lv_p03",
        "LV_P03_Part9": "lv_p03",
        "LV_P03_Part10": "lv_p03",
        "LV_P03_Part11": "lv_p03",
        "LV_P03_Part12": "lv_p05",
        "LV_P03_Part13": "lv_p03",
        "LV_P02_Part14": "lv_p02",
        "LV_P02_Part15": "lv_p02",
        "LV_P02_Part16": "lv_p02",
        "LV_P02_Part17": "lv_p02",
        "LV_P05_Part18": "lv_p05",
        "LV_P06_Part19": "lv_p06",
        "LV_P07_Part20": "lv_p02",
        "LV_P04_Part21": "lv_p04",
        "LV_P04_Part22": "lv_p04",
        "LV_P04_Part23": "lv_p04",
        "LV_P04_Part24": "lv_p04case4",
        "LV_P04_Part25": "lv_p04",
        "LV_P08_Part26": "lv_p03",
        "LV_P09_Part27": "lv_p09"
    }

    MAP_PART_ROLEX: dict[str, str] = {
        "P00": "rolex_p00",
        "P01": "rolex_p01",
        "P02": "rolex_p02",
        "P03": "rolex_p03",
        "P04": "rolex_p04",
        "P05": "rolex_p05",
        "P08": "rolex_p08",
        "P09": "rolex_p09",
        "P10": "rolex_p10",
        "P10_1": "rolex_p10",
        "P10_2": "rolex_p10",
        "P10_3": "rolex_p10",
    }

    MAP_PART_CHANEL: dict[str, str] = {
        "P00": "chanel_p00",
        "CHANEL_P00": "chanel_p00",
        "P04": "chanel_p04",
        "p04": "chanel_p04",
        "CHANEL_P04": "chanel_p04",
    }

    MAP_PART_OMG: dict[str, str] = {
        "OMG_P00": "omg_p00",
        "OMG_P01": "omg_p01",
        "OMG_P02": "omg_p02",
        "OMG_P03": "omg_p03",
        "OMG_P05": "omg_p05",
        "OMG_P06": "omg_p06",
        "OMG_P01_Part1": "omg_p01",
        "OMG_P01_Part2": "omg_p01",
        "OMG_P01_Part3": "omg_p01",
        "OMG_P02_Part4": "omg_p02",
        "OMG_P03_Part5": "omg_p03",
        "OMG_P05_Part6": "omg_p05",
        "OMG_P06_Part7": "omg_p06",
        "OMG_P06_Part8": "omg_p06",
    }

    MAP_PART_CTR: dict[str, str] = {
        "CTR_P01": "ctr_p01",
        "CTR_P02": "ctr_p02",
        "CTR_P03": "ctr_p03",
        "CTR_P04": "ctr_p04",
        "CTR_P05": "ctr_p05",
        "CTR_P06": "ctr_p06",
        "CTR_P01_Part1": "ctr_p01",
        "CTR_P01_Part2": "ctr_p01",
        "CTR_P02_Part3": "ctr_p02",
        "CTR_P02_Part4": "ctr_p02",
        "CTR_P03_Part5": "ctr_p03",
        "CTR_P03_Part6": "ctr_p03",
        "CTR_P04_Part7": "ctr_p04",
        "CTR_P05_Part8": "ctr_p05",
        "CTR_P06_Part9": "ctr_p06",
    }

    @property
    def category_brand(self) -> dict[str, dict]:
        return {
            "bag-lv": {
                "version_name": "lv",
                "full_name": "Louis Vuitton",
                "map_part": self.MAP_PART_LV
            },
            "rolex": {
                "version_name": "rolex",
                "full_name": "Rolex",
                "map_part": self.MAP_PART_ROLEX
            },
            "chanel": {
                "version_name": "chanel",
                "full_name": "Chanel",
                "map_part": self.MAP_PART_CHANEL
            },
            "omg": {
                "version_name": "omg",
                "full_name": "Omega",
                "map_part": self.MAP_PART_OMG
            },
            "ctr": {
                "version_name": "ctr",
                "full_name": "Cartier",
                "map_part": self.MAP_PART_CTR
            }
        }

    def get_iqa_threshold(self, brand: str, part: str) -> float:
        """
        Tự động tra cứu và lấy trực tiếp giá trị threshold tương ứng 
        từ các biến đã khai báo (ví dụ: chanel_p04_threshold).
        """
        brand_key = brand.lower()
        part_key = part.lower()
        field_name = f"{brand_key}_{part_key}_threshold"
        return getattr(self, field_name)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()