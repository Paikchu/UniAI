from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, field_validator


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

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v):
        if v not in ['high', 'medium', 'low']:
            raise ValueError("Priority must be one of: high, medium, low")
        return v

    @field_validator('duration')
    @classmethod
    def validate_duration(cls, v):
        if v <= 0:
            raise ValueError("Duration must be positive")
        return v


class ScheduleRequest(BaseModel):
    """日程规划请求模型"""
    events: List[Event]
    total_events: int
    estimated_total_time: int  # 总预估时间（分钟）
    user_preferences: Optional[dict] = None  # 用户偏好设置
    constraints: Optional[dict] = None  # 约束条件
    request_id: str

    @field_validator('total_events')
    @classmethod
    def validate_total_events(cls, v, info):
        if 'events' in info.data and len(info.data['events']) != v:
            raise ValueError("Total events count doesn't match events list length")
        return v


class OptimizedEvent(BaseModel):
    """优化后的事件模型"""
    title: str
    description: str
    duration: int
    priority: str
    category: str
    suggested_time: str
    start_date: datetime
    end_date: datetime
    optimization_reason: Optional[str] = None  # AI优化建议的原因
    conflicts_resolved: Optional[List[str]] = None  # 解决的冲突列表


class ScheduleOptimization(BaseModel):
    """日程优化建议"""
    optimized_events: List[OptimizedEvent]
    total_optimized_time: int
    time_saved: int  # 节省的时间（分钟）
    efficiency_score: float  # 效率评分 0-100
    optimization_summary: str  # 优化总结
    suggestions: List[str]  # 额外建议


class ScheduleResponseData(BaseModel):
    """日程规划响应数据"""
    original_schedule: ScheduleRequest
    optimized_schedule: ScheduleOptimization
    ai_analysis: str  # AI分析报告
    model_info: dict


class ScheduleResponse(BaseModel):
    """日程规划响应模型"""
    code: int = 200
    message: str = "success"
    data: ScheduleResponseData
    request_id: str
    timestamp: int