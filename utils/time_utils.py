"""Time-related utility functions"""
import time
from datetime import datetime
from typing import Union

def get_current_timestamp() -> int:
    """Get current timestamp"""
    return int(time.time())

def get_current_datetime() -> datetime:
    """Get current datetime"""
    return datetime.now()

def format_timestamp(timestamp: Union[int, float], format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format timestamp"""
    return datetime.fromtimestamp(timestamp).strftime(format_str)