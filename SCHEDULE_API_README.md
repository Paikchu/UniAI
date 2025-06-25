# Schedule API Documentation

## Overview

The Schedule API has been simplified to use a clean input/output model:

- **Input**: `ScheduleRequest` with a text prompt
- **Output**: `ScheduleResponse` with structured events

## API Endpoint

```
POST /api/v1/schedule/plan
```

## Request Model (ScheduleRequest)

```python
class ScheduleRequest(BaseModel):
    prompt: str                    # User's schedule planning description
    user_preferences: Optional[dict] = None  # User preferences
    constraints: Optional[dict] = None       # Constraints
    request_id: str                # Unique request identifier
```

## Response Model (ScheduleResponse)

```python
class ScheduleResponse(BaseModel):
    events: List[Event]            # List of scheduled events
    total_events: int              # Total number of events
    estimated_total_time: int      # Total estimated time in minutes
    user_preferences: Optional[dict] = None
    constraints: Optional[dict] = None
    request_id: str
```

## Event Model

```python
class Event(BaseModel):
    title: str                     # Event title
    description: str               # Event description
    duration: int                  # Duration in minutes
    priority: str                  # high, medium, low
    category: str                  # study, work, health, entertainment, etc.
    suggested_time: Optional[str]  # morning, afternoon, evening
    start_date: datetime           # Start time
    end_date: datetime             # End time
```

## Example Usage

### Request Example

```json
{
    "prompt": "我明天需要复习算法基础2小时，刷LeetCode 1.5小时，还要做项目开发3小时，健身1小时。请帮我安排一个高效的日程。",
    "user_preferences": {
        "preferred_study_time": "morning",
        "preferred_work_time": "afternoon"
    },
    "constraints": {
        "max_continuous_work": 120
    },
    "request_id": "example_001"
}
```

### Response Example

```json
{
    "events": [
        {
            "title": "算法基础复习",
            "description": "复习算法基础知识，包括排序、搜索等",
            "duration": 120,
            "priority": "high",
            "category": "study",
            "suggested_time": "morning",
            "start_date": "2025-01-16T09:00:00",
            "end_date": "2025-01-16T11:00:00"
        },
        {
            "title": "LeetCode刷题",
            "description": "刷LeetCode算法题，提高编程能力",
            "duration": 90,
            "priority": "medium",
            "category": "study",
            "suggested_time": "afternoon",
            "start_date": "2025-01-16T14:00:00",
            "end_date": "2025-01-16T15:30:00"
        }
    ],
    "total_events": 2,
    "estimated_total_time": 210,
    "user_preferences": {
        "preferred_study_time": "morning",
        "preferred_work_time": "afternoon"
    },
    "constraints": {
        "max_continuous_work": 120
    },
    "request_id": "example_001"
}
```

## Running the API

1. **Start the server**:
   ```bash
   python main.py
   ```

## Key Changes Made

1. **Simplified Models**: Removed complex nested models and used simple `ScheduleRequest`/`ScheduleResponse`
2. **Fixed Imports**: Corrected import statements to use `models.schedule` instead of non-existent modules
3. **Streamlined Service**: Simplified `ScheduleService` to work with basic models
4. **Updated Main App**: Fixed router imports in `main.py`
5. **JSON Response**: Ensured the API returns proper JSON responses

## Files Modified

- `api/v1/schedule.py` - Fixed imports and endpoint
- `services/schedule_service.py` - Simplified service logic
- `main.py` - Fixed router imports
- `models/schedule.py` - Already had correct models

## Dependencies

Make sure you have the required environment variables:
- `DEEPSEEK_API_KEY` - Your DeepSeek API key
- `PORT` - Server port (default: 8000)

## Error Handling

The API includes proper error handling for:
- Invalid JSON responses from AI provider
- Missing API keys
- Network errors
- Validation errors

All errors return appropriate HTTP status codes and error messages. 