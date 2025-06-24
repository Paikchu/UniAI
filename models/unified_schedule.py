from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, field_validator, model_validator


class EventResult(BaseModel):
    """返回的事件模型"""
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


class Event(BaseModel):
    """输入的事件模型（用于结构化输入）"""
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


class UnifiedScheduleRequest(BaseModel):
    """统一的日程规划请求模型 - 支持两种输入方式"""
    # 方式1: 直接提供prompt（简化输入）
    prompt: Optional[str] = None
    
    # 方式2: 提供结构化数据（详细输入）
    events: Optional[List[Event]] = None
    total_events: Optional[int] = None
    estimated_total_time: Optional[int] = None  # 总预估时间（分钟）
    
    # 通用字段
    user_preferences: Optional[dict] = None  # 用户偏好设置
    constraints: Optional[dict] = None  # 约束条件
    request_id: str

    @field_validator('total_events')
    @classmethod
    def validate_total_events(cls, v, info):
        if v is not None and 'events' in info.data and info.data['events'] is not None:
            if len(info.data['events']) != v:
                raise ValueError("Total events count doesn't match events list length")
        return v

    @model_validator(mode='after')
    def validate_input_method(self):
        """验证输入方式"""
        if not self.prompt and not self.events:
            raise ValueError("Either 'prompt' or 'events' must be provided")
        if self.prompt and self.events:
            raise ValueError("Cannot provide both 'prompt' and 'events', choose one input method")
        return self


class UnifiedScheduleResponseData(BaseModel):
    """统一的日程规划响应数据"""
    events: List[EventResult]
    total_events: int
    estimated_total_time: int  # 总时间（分钟）


class UnifiedScheduleResponse(BaseModel):
    """统一的日程规划响应模型"""
    code: int = 200
    message: str = "success"
    data: UnifiedScheduleResponseData
    request_id: str
    timestamp: int

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "message": "success",
                "data": {
                    "events": [
                        {
                            "title": "算法基础复习",
                            "description": "复习数据结构和算法基础知识，重点关注数组、链表、栈和队列",
                            "duration": 120,
                            "priority": "high",
                            "category": "study",
                            "suggested_time": "morning",
                            "start_date": "2025-01-15T09:00:00Z",
                            "end_date": "2025-01-15T11:00:00Z"
                        },
                        {
                            "title": "LeetCode刷题",
                            "description": "完成10道中等难度的算法题，重点练习动态规划",
                            "duration": 90,
                            "priority": "high",
                            "category": "study",
                            "start_date": "2025-01-15T14:00:00Z",
                            "end_date": "2025-01-15T15:30:00Z"
                        }
                    ],
                    "total_events": 14,
                    "estimated_total_time": 1680
                },
                "request_id": "req_123456789",
                "timestamp": 1705123456
            }
        }