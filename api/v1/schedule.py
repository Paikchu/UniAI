from fastapi import APIRouter
from models.schedule import ScheduleRequest, ScheduleResponse
from services.schedule_service import ScheduleService

router = APIRouter()


@router.post(
    "/schedule/plan",
    tags=["Schedule"],
    summary="Schedule Planning",
    description="Generate optimized schedule based on user's text prompt.",
    response_model=ScheduleResponse,
)
def schedule_planning(request: ScheduleRequest) -> ScheduleResponse:
    return ScheduleService.process_schedule_request(request)