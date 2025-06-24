import json
from typing import Dict, Any
from datetime import datetime

from core.config import settings
from core.exceptions import ModelNotSupportedException, ProviderException
from utils.time_utils import get_current_timestamp
from providers.deepseek import DeepSeekProvider
from models.schedule import ScheduleRequest, ScheduleResponse, ScheduleResponseData, ScheduleOptimization, OptimizedEvent


class ScheduleService:
    @staticmethod
    def process_schedule_request(request: ScheduleRequest) -> ScheduleResponse:
        """处理日程规划请求"""
        try:
            # 创建DeepSeek提供者实例
            provider = DeepSeekProvider()
            
            # 构建提示模板
            template = """
            你是一个专业的日程规划AI助手。请根据以下日程信息，优化日程安排，提高效率并解决潜在冲突。
            
            ## 当前日程信息
            {schedule_json}
            
            ## 任务
            1. 分析当前日程安排
            2. 识别并解决时间冲突
            3. 根据优先级和类别优化日程
            4. 提供更高效的日程安排
            5. 给出优化建议和分析
            
            ## 输出格式
            请以JSON格式返回优化后的日程，包含以下字段：
            - optimized_events: 优化后的事件列表
            - total_optimized_time: 优化后的总时间
            - time_saved: 节省的时间
            - efficiency_score: 效率评分(0-100)
            - optimization_summary: 优化总结
            - suggestions: 额外建议列表
            - ai_analysis: 详细分析报告
            
            请确保返回的JSON格式正确，可以被解析。
            """
            
            # 准备输入变量
            input_variables = {
                "schedule_json": json.dumps(request.dict(), default=datetime_serializer, ensure_ascii=False, indent=2)
            }
            
            # 调用DeepSeek API
            response = provider.get_response_with_custom_template(
                template=template,
                input_variables=input_variables,
                temperature=0.7,
                max_tokens=2000
            )
            
            # 解析AI返回的JSON响应
            ai_response = parse_ai_response(response.content)
            
            # 构建响应数据
            response_data = ScheduleResponseData(
                original_schedule=request,
                optimized_schedule=ai_response["optimized_schedule"],
                ai_analysis=ai_response["ai_analysis"],
                model_info={
                    "name": "deepseek-chat",
                    "provider": "deepseek",
                    "version": response.response_metadata.get('model_name', 'unknown'),
                    "temperature": response.response_metadata.get('temperature', 0.7),
                }
            )
            
            return ScheduleResponse(
                data=response_data,
                request_id=request.request_id,
                timestamp=get_current_timestamp()
            )
            
        except Exception as e:
            raise ProviderException("schedule_service", str(e))


def datetime_serializer(obj):
    """处理datetime序列化"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def parse_ai_response(content: str) -> Dict[str, Any]:
    """解析AI返回的JSON响应"""
    try:
        # 提取JSON部分（防止AI返回额外文本）
        json_start = content.find('{')
        json_end = content.rfind('}')
        
        if json_start == -1 or json_end == -1:
            raise ValueError("No valid JSON found in the response")
            
        json_content = content[json_start:json_end+1]
        response_dict = json.loads(json_content)
        
        # 构建优化后的日程
        optimized_events = []
        for event in response_dict.get("optimized_events", []):
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
        raise ValueError(f"Failed to parse AI response: {str(e)}")