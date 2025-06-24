import json
from typing import Dict, Any
from datetime import datetime, timedelta

from core.config import settings
from core.exceptions import ModelNotSupportedException, ProviderException
from utils.time_utils import get_current_timestamp
from providers.deepseek import DeepSeekProvider
from models.schedule_simple import SimpleScheduleRequest
from models.schedule import (
    ScheduleResponse, ScheduleResponseData, ScheduleOptimization, 
    OptimizedEvent, Event, ScheduleRequest
)


class ScheduleSimpleService:
    @staticmethod
    def process_simple_schedule_request(request: SimpleScheduleRequest) -> ScheduleResponse:
        """处理基于prompt的简化日程规划请求"""
        try:
            # 创建DeepSeek提供者实例
            provider = DeepSeekProvider()
            
            # 构建提示模板 - 分两步处理
            # 第一步：从用户prompt中提取结构化信息
            extraction_template = """
            你是一个专业的日程规划AI助手。请根据用户的描述，提取出结构化的日程信息。
            
            用户描述：{user_prompt}
            
            用户偏好：{user_preferences}
            约束条件：{constraints}
            
            请分析用户的需求，提取出以下信息并以JSON格式返回：
            
            {{
                "events": [
                    {{
                        "title": "事件标题",
                        "description": "详细描述",
                        "duration": 持续时间（分钟）,
                        "priority": "优先级（high/medium/low）",
                        "category": "类别（study/work/health/entertainment等）",
                        "suggested_time": "建议时间（morning/afternoon/evening）"
                    }}
                ],
                "total_events": 事件总数,
                "estimated_total_time": 总预估时间（分钟）
            }}
            
            注意：
            1. 根据用户描述推断合理的事件优先级
            2. 为每个事件分配合适的类别
            3. 根据事件性质建议最佳时间段
            4. 确保时间估算合理
            5. 返回有效的JSON格式
            """
            
            # 准备第一步的输入变量
            extraction_variables = {
                "user_prompt": request.prompt,
                "user_preferences": json.dumps(request.user_preferences or {}, ensure_ascii=False),
                "constraints": json.dumps(request.constraints or {}, ensure_ascii=False)
            }
            
            # 第一步：提取结构化信息
            extraction_response = provider.get_response_with_custom_template(
                template=extraction_template,
                input_variables=extraction_variables,
                temperature=0.3,  # 较低温度确保结构化输出
                max_tokens=1500
            )
            
            # 解析提取的结构化信息
            extracted_data = parse_extraction_response(extraction_response.content)
            
            # 创建完整的ScheduleRequest对象
            schedule_request = create_schedule_request_from_extracted_data(
                extracted_data, request
            )
            
            # 第二步：优化日程安排
            optimization_template = """
            你是一个专业的日程规划AI助手。请根据以下结构化的日程信息，优化日程安排，提高效率并解决潜在冲突。
            
            ## 当前日程信息
            {schedule_json}
            
            ## 用户原始需求
            {original_prompt}
            
            ## 任务
            1. 分析当前日程安排的合理性
            2. 根据优先级和类别优化事件顺序
            3. 安排合适的时间段（考虑用户偏好）
            4. 添加必要的休息时间
            5. 提供优化建议和分析
            
            ## 输出格式
            请以JSON格式返回优化后的日程，包含以下字段：
            {{
                "optimized_events": [
                    {{
                        "title": "事件标题",
                        "description": "详细描述",
                        "duration": 持续时间（分钟）,
                        "priority": "优先级",
                        "category": "类别",
                        "suggested_time": "建议时间段",
                        "start_date": "开始时间（ISO格式）",
                        "end_date": "结束时间（ISO格式）",
                        "optimization_reason": "优化原因",
                        "conflicts_resolved": ["解决的冲突列表"]
                    }}
                ],
                "total_optimized_time": 优化后的总时间,
                "time_saved": 节省的时间,
                "efficiency_score": 效率评分(0-100),
                "optimization_summary": "优化总结",
                "suggestions": ["额外建议列表"],
                "ai_analysis": "详细分析报告"
            }}
            
            请确保：
            1. 时间安排合理，避免冲突
            2. 考虑用户的偏好和约束
            3. 高优先级任务优先安排
            4. 相似类别的任务可以集中安排
            5. 返回有效的JSON格式
            """
            
            # 准备第二步的输入变量
            optimization_variables = {
                "schedule_json": json.dumps(schedule_request.dict(), default=datetime_serializer, ensure_ascii=False, indent=2),
                "original_prompt": request.prompt
            }
            
            # 第二步：优化日程
            optimization_response = provider.get_response_with_custom_template(
                template=optimization_template,
                input_variables=optimization_variables,
                temperature=0.7,
                max_tokens=2500
            )
            
            # 解析AI返回的优化结果
            ai_response = parse_optimization_response(optimization_response.content)
            
            # 构建响应数据
            response_data = ScheduleResponseData(
                original_schedule=schedule_request,
                optimized_schedule=ai_response["optimized_schedule"],
                ai_analysis=ai_response["ai_analysis"],
                model_info={
                    "name": "deepseek-chat",
                    "provider": "deepseek",
                    "version": optimization_response.response_metadata.get('model_name', 'unknown'),
                    "temperature": optimization_response.response_metadata.get('temperature', 0.7),
                    "original_prompt": request.prompt
                }
            )
            
            return ScheduleResponse(
                data=response_data,
                request_id=request.request_id,
                timestamp=get_current_timestamp()
            )
            
        except Exception as e:
            raise ProviderException("schedule_simple_service", str(e))


def parse_extraction_response(content: str) -> Dict[str, Any]:
    """解析AI返回的结构化信息提取结果"""
    try:
        # 提取JSON部分
        json_start = content.find('{')
        json_end = content.rfind('}')
        
        if json_start == -1 or json_end == -1:
            raise ValueError("No valid JSON found in the extraction response")
            
        json_content = content[json_start:json_end+1]
        return json.loads(json_content)
        
    except Exception as e:
        raise ValueError(f"Failed to parse extraction response: {str(e)}")


def create_schedule_request_from_extracted_data(
    extracted_data: Dict[str, Any], 
    original_request: SimpleScheduleRequest
) -> ScheduleRequest:
    """从提取的数据创建完整的ScheduleRequest对象"""
    try:
        # 获取当前时间作为基准
        base_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        
        events = []
        current_time = base_time
        
        for event_data in extracted_data.get("events", []):
            # 计算事件的开始和结束时间
            duration_minutes = event_data.get("duration", 60)
            start_time = current_time
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            # 创建Event对象
            event = Event(
                title=event_data.get("title", "未命名事件"),
                description=event_data.get("description", ""),
                duration=duration_minutes,
                priority=event_data.get("priority", "medium"),
                category=event_data.get("category", "other"),
                suggested_time=event_data.get("suggested_time"),
                start_date=start_time,
                end_date=end_time
            )
            
            events.append(event)
            
            # 为下一个事件预留15分钟间隔
            current_time = end_time + timedelta(minutes=15)
        
        # 创建ScheduleRequest对象
        return ScheduleRequest(
            events=events,
            total_events=len(events),
            estimated_total_time=extracted_data.get("estimated_total_time", sum(e.duration for e in events)),
            user_preferences=original_request.user_preferences,
            constraints=original_request.constraints,
            request_id=original_request.request_id
        )
        
    except Exception as e:
        raise ValueError(f"Failed to create ScheduleRequest from extracted data: {str(e)}")


def parse_optimization_response(content: str) -> Dict[str, Any]:
    """解析AI返回的优化结果"""
    try:
        # 提取JSON部分
        json_start = content.find('{')
        json_end = content.rfind('}')
        
        if json_start == -1 or json_end == -1:
            raise ValueError("No valid JSON found in the optimization response")
            
        json_content = content[json_start:json_end+1]
        response_dict = json.loads(json_content)
        
        # 构建优化后的事件列表
        optimized_events = []
        for event in response_dict.get("optimized_events", []):
            # 如果没有提供时间，使用当前时间作为基准
            if not event.get("start_date") or not event.get("end_date"):
                base_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
                duration = event.get("duration", 60)
                event["start_date"] = base_time.isoformat()
                event["end_date"] = (base_time + timedelta(minutes=duration)).isoformat()
            
            # 转换日期字符串为datetime对象
            if isinstance(event.get("start_date"), str):
                event["start_date"] = datetime.fromisoformat(event["start_date"].replace('Z', '+00:00'))
            if isinstance(event.get("end_date"), str):
                event["end_date"] = datetime.fromisoformat(event["end_date"].replace('Z', '+00:00'))
            
            optimized_events.append(OptimizedEvent(**event))
        
        # 构建优化结果
        optimized_schedule = ScheduleOptimization(
            optimized_events=optimized_events,
            total_optimized_time=response_dict.get("total_optimized_time", 0),
            time_saved=response_dict.get("time_saved", 0),
            efficiency_score=response_dict.get("efficiency_score", 0.0),
            optimization_summary=response_dict.get("optimization_summary", ""),
            suggestions=response_dict.get("suggestions", [])
        )
        
        return {
            "optimized_schedule": optimized_schedule,
            "ai_analysis": response_dict.get("ai_analysis", "")
        }
        
    except Exception as e:
        raise ValueError(f"Failed to parse optimization response: {str(e)}")


def datetime_serializer(obj):
    """处理datetime序列化"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")