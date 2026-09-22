import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone, timedelta
import os
from config import Settings

# ===============================
# Logging Configuration
# ===============================

settings = Settings()
FOLDER_LOGS_SAVE = settings.app_log_folder
APP_LOGGER_FILE = f"{FOLDER_LOGS_SAVE}/{settings.app_log_app_name}.log"
MODEL_RESULTS_LOGGER_FILE = f"{FOLDER_LOGS_SAVE}/{settings.app_log_model_results_name}.log"
REQUEST_LOGGER_FILE = f"{FOLDER_LOGS_SAVE}/{settings.app_log_request_name}.log"
APP_LOGGER_NAME = settings.app_log_app_name
MODEL_RESULTS_LOGGER_NAME = settings.app_log_model_results_name
REQUEST_LOGGER_NAME = settings.app_log_request_name
TZ_OFFSET_HOURS = settings.app_log_tz_offset_hours
MAX_LOG_SIZE = settings.app_log_max_log_size
MAX_BACKUP_FILE = settings.app_log_max_backup_file

os.makedirs(FOLDER_LOGS_SAVE, exist_ok=True)

# ===============================
# Timezone Formatter
# ===============================
class TZFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, tz_offset_hours=0):
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.tzinfo = timezone(timedelta(hours=tz_offset_hours))

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=self.tzinfo)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()

# ===============================
# Create Logger
# ===============================
def create_logger(
    name: str,
    log_file: str,
    formatter_str: str,
    tz_offset_hours: int = 0,
    max_bytes: int = MAX_LOG_SIZE,
    backup_count: int = MAX_BACKUP_FILE,
    to_console: bool = False
):
    logger = logging.getLogger(name)

    if not logger.handlers:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )

        formatter = TZFormatter(formatter_str, tz_offset_hours=tz_offset_hours)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        if to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        logger.setLevel(logging.INFO)

    return logger

# ===============================
# Logger Initialization
# ===============================
APP_LOGGER = create_logger(
    name=APP_LOGGER_NAME,
    log_file=APP_LOGGER_FILE,
    formatter_str="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    tz_offset_hours=TZ_OFFSET_HOURS,
    to_console=True
)

MODEL_RESULTS_LOGGER = create_logger(
    name=MODEL_RESULTS_LOGGER_NAME,
    log_file=MODEL_RESULTS_LOGGER_FILE,
    formatter_str="%(asctime)s - %(levelname)s - %(message)s",
    tz_offset_hours=TZ_OFFSET_HOURS,
    to_console=False
)
REQUEST_LOGGER = create_logger(
    name=REQUEST_LOGGER_NAME,
    log_file=REQUEST_LOGGER_FILE,
    formatter_str="%(asctime)s - %(message)s",
    tz_offset_hours=TZ_OFFSET_HOURS,
    to_console=False
)   