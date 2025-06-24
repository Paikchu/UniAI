from fastapi import APIRouter
from models.schedule import ScheduleRequest, ScheduleResponse
from services.schedule_service import ScheduleService

router = APIRouter()


@router.post(
    "/schedule/optimize",
    tags=["Schedule"],
    summary="Schedule Optimization",
    description="Optimize schedule using AI to improve efficiency and resolve conflicts.",
    response_model=ScheduleResponse,
)
def optimize_schedule(request: ScheduleRequest):
    """Schedule optimization endpoint"""
    return ScheduleService.process_schedule_request(request)