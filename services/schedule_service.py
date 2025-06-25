import json
from datetime import datetime, timedelta
from typing import Dict, Any

from core.exceptions import ProviderException
from models.schedule import ScheduleRequest, ScheduleResponse, Event
from providers.deepseek import DeepSeekProvider


class ScheduleService:
    @staticmethod
    def process_schedule_request(request: ScheduleRequest) -> ScheduleResponse:
        """处理基于prompt的简化日程规划请求"""
        try:
            # 创建DeepSeek提供者实例
            provider = DeepSeekProvider()

            # 构建提示模板
            template = """
            你是一个专业的日程规划AI助手，具有丰富的心理学和时间管理知识。你的任务是帮助用户制定切实可行、高效且个性化的日程安排。

            ## 用户需求分析
            用户描述：{user_prompt}
            用户偏好：{user_preferences}
            约束条件：{constraints}

            ## 你的任务
            1. **深度分析用户需求**：理解用户的真实意图和目标
            2. **可行性评估**：评估计划的现实性和可执行性
            3. **智能优化建议**：基于时间管理最佳实践提供改进建议
            4. **个性化调整**：考虑用户偏好和约束条件
            5. **语言一致性**：使用与用户输入相同的语言回复

            ## 分析维度
            - **时间合理性**：任务时长是否合理？是否需要休息时间？
            - **优先级排序**：重要且紧急的任务是否优先安排？
            - **精力管理**：是否考虑了人的精力曲线（上午精力充沛，下午相对较低）？
            - **任务关联性**：相似类型的任务是否可以集中处理？
            - **缓冲时间**：是否预留了应对突发情况的缓冲时间？
            - **可持续性**：这个计划是否可持续执行？

            ## 输出要求
            请以JSON格式返回优化后的日程安排，包含以下字段：

            {{
                "events": [
                    {{
                        "title": "事件标题（使用用户输入语言）",
                        "description": "详细描述（包含优化建议和可行性说明）",
                        "duration": 持续时间（分钟，考虑实际可行性）,
                        "priority": "优先级（high/medium/low，基于重要性和紧急性）",
                        "category": "类别（study/work/health/entertainment/personal等）",
                        "suggested_time": "建议时间（morning/afternoon/evening，基于任务性质和精力曲线）"
                    }}
                ],
                "total_events": 事件总数,
                "estimated_total_time": 总预估时间（分钟，包含缓冲时间）
            }}

            ## 优化原则
            1. **SMART原则**：确保每个任务都是具体、可衡量、可达成、相关、有时限的
            2. **帕累托原则**：80%的成果来自20%的努力，优先安排高价值任务
            3. **时间块管理**：将相似任务集中处理，减少切换成本
            4. **精力匹配**：将需要高专注度的任务安排在精力充沛的时间段
            5. **现实缓冲**：预留15-20%的缓冲时间应对意外情况
            6. **渐进式安排**：避免过度安排，确保计划可持续执行

            ## 注意事项
            - 如果用户的需求明显不现实，请提供合理的调整建议
            - 考虑用户的个人偏好和约束条件
            - 确保返回的JSON格式完全正确
            - 使用与用户输入相同的语言
            - 在描述中说明为什么这样安排以及如何提高执行效率
            """

            # 准备输入变量
            variables = {
                "user_prompt": request.prompt,
                "user_preferences": json.dumps(request.user_preferences or {}, ensure_ascii=False),
                "constraints": json.dumps(request.constraints or {}, ensure_ascii=False)
            }

            # 调用AI服务
            response = provider.get_response_with_custom_template(
                template=template,
                input_variables=variables,
                temperature=0.3,
                max_tokens=1500
            )

            # 解析AI返回的结果
            parsed_data = parse_ai_response(response.content)
            
            # 验证解析结果的基本结构
            if not isinstance(parsed_data, dict):
                raise ValueError("AI response is not a valid JSON object")
            
            if "events" not in parsed_data:
                raise ValueError("AI response missing 'events' field")
            
            if not isinstance(parsed_data["events"], list):
                raise ValueError("'events' field must be a list")
            
            # 创建Event对象列表
            events = []
            base_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
            current_time = base_time
            
            for event_data in parsed_data.get("events", []):
                # 验证事件数据的必需字段
                required_fields = ["title", "description", "duration", "priority", "category"]
                for field in required_fields:
                    if field not in event_data:
                        raise ValueError(f"Event missing required field: {field}")
                
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
            
            # 创建ScheduleResponse对象
            return ScheduleResponse(
                events=events,
                total_events=len(events),
                estimated_total_time=parsed_data.get("estimated_total_time", sum(e.duration for e in events)),
                user_preferences=request.user_preferences,
                constraints=request.constraints,
                request_id=request.request_id
            )

        except Exception as e:
            raise ProviderException("schedule_service", str(e))


def parse_ai_response(content: str) -> Dict[str, Any]:
    """解析AI返回的JSON响应"""
    try:
        # 提取JSON部分
        json_start = content.find('{')
        json_end = content.rfind('}')

        if json_start == -1 or json_end == -1:
            raise ValueError("No valid JSON found in the AI response")

        json_content = content[json_start:json_end + 1]
        return json.loads(json_content)

    except Exception as e:
        raise ValueError(f"Failed to parse AI response: {str(e)}")
