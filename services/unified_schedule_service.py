import time
from datetime import datetime
from typing import List
from models.unified_schedule import (
    UnifiedScheduleRequest, 
    UnifiedScheduleResponse, 
    UnifiedScheduleResponseData,
    EventResult
)
from core.exceptions import UniAIException


class UnifiedScheduleService:
    """统一的日程规划服务"""
    
    @staticmethod
    def process_unified_schedule_request(request: UnifiedScheduleRequest) -> UnifiedScheduleResponse:
        """
        处理统一的日程规划请求
        不管输入是prompt还是结构化数据，都返回固定的结果格式
        """
        try:
            # 返回固定的示例数据，不进行AI处理
            fixed_events = [
                EventResult(
                    title="算法基础复习",
                    description="复习数据结构和算法基础知识，重点关注数组、链表、栈和队列",
                    duration=120,
                    priority="high",
                    category="study",
                    suggested_time="morning",
                    start_date=datetime.fromisoformat("2025-01-15T09:00:00+00:00"),
                    end_date=datetime.fromisoformat("2025-01-15T11:00:00+00:00")
                ),
                EventResult(
                    title="LeetCode刷题",
                    description="完成10道中等难度的算法题，重点练习动态规划",
                    duration=90,
                    priority="high",
                    category="study",
                    suggested_time=None,
                    start_date=datetime.fromisoformat("2025-01-15T14:00:00+00:00"),
                    end_date=datetime.fromisoformat("2025-01-15T15:30:00+00:00")
                )
            ]
            
            # 构建响应数据
            response_data = UnifiedScheduleResponseData(
                events=fixed_events,
                total_events=14,
                estimated_total_time=1680
            )
            
            # 构建完整响应
            response = UnifiedScheduleResponse(
                code=200,
                message="success",
                data=response_data,
                request_id=request.request_id,
                timestamp=int(time.time())
            )
            
            return response
            
        except Exception as e:
            raise UniAIException(
                code="SCHEDULE_PROCESSING_ERROR",
                message=f"处理日程规划请求时发生错误: {str(e)}",
                details={"request_id": request.request_id}
            )
    
    @staticmethod
    def get_sample_response() -> dict:
        """
        获取示例响应数据
        """
        return {
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
        }