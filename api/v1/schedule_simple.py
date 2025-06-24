from fastapi import APIRouter
from models.schedule_simple import SimpleScheduleRequest, ScheduleResponse
from services.schedule_simple_service import ScheduleSimpleService

router = APIRouter()


@router.post(
    "/schedule/simple",
    tags=["Schedule"],
    summary="Simple Schedule Planning",
    description="Generate optimized schedule based on user's text prompt.",
    response_model=ScheduleResponse,
)
def simple_schedule_planning(request: SimpleScheduleRequest):
    """Simple schedule planning endpoint that accepts text prompt"""
    return ScheduleSimpleService.process_simple_schedule_request(request)