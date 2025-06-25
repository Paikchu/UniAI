from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field


class ScheduleRequest(BaseModel):
    """简化的日程规划请求模型 - 接受用户prompt"""
    prompt: str  # 用户的日程规划需求描述
    user_preferences: Optional[Dict[str, Any]] = None  # 用户偏好设置
    constraints: Optional[Dict[str, Any]] = None  # 约束条件
    request_id: str


class Event(BaseModel):
    """单个事件模型"""
    title: str
    description: str
    duration: int  # 分钟
    priority: str  # high, medium, low
    category: str
    suggested_time: Optional[str] = None  # morning, afternoon, evening
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class ScheduleResponse(BaseModel):
    """日程规划请求模型"""
    events: List[Event]
    total_events: int
    estimated_total_time: int  # 总预估时间（分钟）
    user_preferences: Optional[Dict[str, Any]] = None  # 用户偏好设置
    constraints: Optional[Dict[str, Any]] = None  # 约束条件
    request_id: str


# Pydantic model for LLM structured output
class ScheduleOptimizationResult(BaseModel):
    """AI-generated schedule optimization result with structured events."""
    
    events: List[Event] = Field(
        description="List of optimized events with scheduling details"
    )
    total_events: int = Field(
        description="Total number of events in the schedule"
    )
    estimated_total_time: int = Field(
        description="Total estimated time in minutes for all events including buffer time"
    )


class ScheduleEventOutput(BaseModel):
    """Individual event in the optimized schedule."""
    
    title: str = Field(
        description="Event title in the user's input language"
    )
    description: str = Field(
        description="Detailed description of what needs to be done on that day"
    )
    duration: int = Field(
        description="Duration in minutes considering practical feasibility",
        ge=1
    )
    priority: str = Field(
        description="Priority level based on importance and urgency",
        pattern="^(high|medium|low)$"
    )
    category: str = Field(
        description="Event category such as study, work, health, entertainment, personal, etc."
    )
    suggested_time: str = Field(
        description="Suggested time based on task nature and energy curve",
        pattern="^(morning|afternoon|evening)$"
    )
    start_date: str = Field(
        description="Start time in YYYY-MM-DD HH:MM format"
    )
    end_date: str = Field(
        description="End time in YYYY-MM-DD HH:MM format"
    )
