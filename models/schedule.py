from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field


class ScheduleRequest(BaseModel):
    prompt: str 
    request_id: str


class Event(BaseModel):
    title: str
    description: str
    duration: int  # 分钟
    priority: str  # high, medium, low
    category: str
    suggested_time: Optional[str] = None  # morning, afternoon, evening
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class LLMResponse(BaseModel):
    events: list[Event]

class ScheduleResponse(BaseModel):
    """日程规划请求模型"""
    events: List[Event]
    request_id: str
