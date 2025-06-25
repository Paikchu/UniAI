from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ScheduleRequest(BaseModel):
    """简化的日程规划请求模型 - 接受用户prompt"""
    prompt: str  # 用户的日程规划需求描述
    user_preferences: Optional[dict] = None  # 用户偏好设置
    constraints: Optional[dict] = None  # 约束条件
    request_id: str


class Event(BaseModel):
    """单个事件模型"""
    title: str
    description: str
    duration: int  # 分钟
    priority: str  # high, medium, low
    category: str
    suggested_time: Optional[str] = None  # morning, afternoon, evening
    start_date: datetime
    end_date: datetime


class ScheduleResponse(BaseModel):
    """日程规划请求模型"""
    events: List[Event]
    total_events: int
    estimated_total_time: int  # 总预估时间（分钟）
    user_preferences: Optional[dict] = None  # 用户偏好设置
    constraints: Optional[dict] = None  # 约束条件
    request_id: str
