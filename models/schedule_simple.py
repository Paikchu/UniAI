from typing import Optional

from pydantic import BaseModel

from .schedule import ScheduleResponseData, ScheduleResponse


class SimpleScheduleRequest(BaseModel):
    """简化的日程规划请求模型 - 接受用户prompt"""
    prompt: str  # 用户的日程规划需求描述
    user_preferences: Optional[dict] = None  # 用户偏好设置
    constraints: Optional[dict] = None  # 约束条件
    request_id: str

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "我明天需要复习算法基础2小时，刷LeetCode 1.5小时，还要做项目开发3小时，健身1小时。请帮我安排一个高效的日程。",
                "user_preferences": {
                    "preferred_study_time": "morning",
                    "preferred_work_time": "afternoon",
                    "preferred_break_duration": 15
                },
                "constraints": {
                    "max_continuous_work": 120,
                    "required_break_after_work": 15
                },
                "request_id": "unique-request-id"
            }
        }


# 重新导出响应模型以保持一致性
__all__ = [
    "SimpleScheduleRequest",
    "ScheduleResponseData", 
    "ScheduleResponse"
]