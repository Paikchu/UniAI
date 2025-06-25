import json
from datetime import datetime, timedelta
from typing import Dict, Any
import time

from core.exceptions import ProviderException
from models.schedule import ScheduleRequest, ScheduleResponse, Event, ScheduleOptimizationResult
from providers.deepseek import DeepSeekProvider


class ScheduleService:
    @staticmethod
    def process_schedule_request(request: ScheduleRequest) -> ScheduleResponse:
        """处理基于prompt的简化日程规划请求"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
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
                6. **日程规划**：根据用户需求和偏好，规划日程安排
                7. **任务时长**: 评估当前用户想计划的事情，需要多长的时间才能完成，根据任务的难度和复杂度，以及用户的需求和偏好，给出合理的任务时长

                ## 分析维度
                - **时间合理性**：任务时长是否合理？是否需要休息时间？
                - **优先级排序**：重要且紧急的任务是否优先安排？
                - **精力管理**：是否考虑了人的精力曲线（上午精力充沛，下午相对较低）？
                - **任务关联性**：相似类型的任务是否可以集中处理？
                - **缓冲时间**：是否预留了应对突发情况的缓冲时间？
                - **可持续性**：这个计划是否可持续执行？
                - **任务数量**：任务数量是否合理？是否需要减少任务数量？
                - **任务难度**：任务难度是否合理？是否需要降低难度？
                - **任务细分化**：任务是否可以细分？是否需要细分？请不要把多个任务合并为一个任务，任务需要按照天数来规划到每天的任务

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
                - 使用与用户输入相同的语言
                - 在描述中说明为什么这样安排以及如何提高执行效率
                - 请不要把多个任务合并为一个任务，任务需要按照天数来规划到每天的任务
                - 可以提出众多的Event，Event之间可以出现重复，但是需要保证每个Event的开始和结束时间不重叠
                """

                # 准备输入变量
                variables = {
                    "user_prompt": request.prompt,
                    "user_preferences": json.dumps(request.user_preferences or {}, ensure_ascii=False),
                    "constraints": json.dumps(request.constraints or {}, ensure_ascii=False)
                }

                # 使用结构化输出调用AI服务
                structured_result = provider.get_structured_response(
                    template=template,
                    input_variables=variables,
                    response_schema=ScheduleOptimizationResult,
                    temperature=0.3,
                    max_tokens=2000
                )

                # 转换为Event对象列表
                events = []
                for event_data in structured_result.events:
                    event = Event(
                        title=event_data.title,
                        description=event_data.description,
                        duration=event_data.duration,
                        priority=event_data.priority,
                        category=event_data.category,
                        suggested_time=event_data.suggested_time,
                        start_date=event_data.start_date,
                        end_date=event_data.end_date
                    )
                    events.append(event)

                # 创建ScheduleResponse对象
                return ScheduleResponse(
                    events=events,
                    total_events=structured_result.total_events,
                    estimated_total_time=structured_result.estimated_total_time,
                    user_preferences=request.user_preferences,
                    constraints=request.constraints,
                    request_id=request.request_id
                )

            except Exception as e:
                retry_count += 1
                
                if retry_count >= max_retries:
                    raise ProviderException("schedule_service", f"Failed after {max_retries} attempts: {str(e)}")
                
                # 等待一段时间后重试
                time.sleep(1)
                continue

        # 如果所有重试都失败了
        raise ProviderException("schedule_service", f"Failed after {max_retries} attempts")
