import json
import logging
import os
from typing import Dict, List, Optional

def get_logger(module: Optional[str] = None) -> logging.Logger:
    logger_name = "hashfunc32"
    if module is not None:
        logger_name += f".{module}"
    logger = logging.getLogger(logger_name)
    if logger.hasHandlers():
        return logger
    
    formatter = logging.Formatter("%(name)s %(levelname)s: %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger

def get_sys32() -> str:
    module_dir = os.path.dirname(__file__)
    return os.path.join(module_dir, "System32.json")

def open_sys32() -> Dict[str, List[str]]:
    return json.load(open(get_sys32(), "r", encoding="utf-8"))
