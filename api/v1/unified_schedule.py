from fastapi import APIRouter
from models.unified_schedule import UnifiedScheduleRequest, UnifiedScheduleResponse
from services.unified_schedule_service import UnifiedScheduleService

router = APIRouter()


@router.post(
    "/schedule",
    tags=["Schedule"],
    summary="Unified Schedule Planning",
    description="Unified schedule planning endpoint that accepts either text prompt or structured data and returns fixed format results.",
    response_model=UnifiedScheduleResponse,
)
def unified_schedule_planning(request: UnifiedScheduleRequest):
    """
    统一的日程规划端点
    
    支持两种输入方式：
    1. 文本prompt：用户用自然语言描述日程需求
    2. 结构化数据：用户提供详细的事件列表
    
    返回固定格式的日程安排结果
    """
    return UnifiedScheduleService.process_unified_schedule_request(request)


@router.get(
    "/schedule/sample",
    tags=["Schedule"],
    summary="Get Sample Schedule Response",
    description="Get a sample response format for schedule planning."
)
def get_sample_schedule():
    """
    获取示例响应格式
    """
    return UnifiedScheduleService.get_sample_response()