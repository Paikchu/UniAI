# 日程规划API文档

## 概述

日程规划API使用DeepSeek AI模型来智能优化用户的日程安排，提高效率并解决时间冲突。

## API端点

### POST /api/v1/schedule/optimize

优化日程安排

#### 请求格式

```json
{
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
    }
  ],
  "total_events": 1,
  "estimated_total_time": 120,
  "user_preferences": {
    "preferred_study_time": "morning",
    "preferred_work_time": "afternoon",
    "preferred_break_duration": 15
  },
  "constraints": {
    "max_continuous_work": 120,
    "required_break_after_work": 15
  },
  "request_id": "unique-request-id"
}
```

#### 请求字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| events | Array | 是 | 事件列表 |
| total_events | Integer | 是 | 事件总数 |
| estimated_total_time | Integer | 是 | 预估总时间（分钟） |
| user_preferences | Object | 否 | 用户偏好设置 |
| constraints | Object | 否 | 约束条件 |
| request_id | String | 是 | 请求唯一标识 |

#### Event对象字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | String | 是 | 事件标题 |
| description | String | 是 | 事件描述 |
| duration | Integer | 是 | 持续时间（分钟） |
| priority | String | 是 | 优先级：high/medium/low |
| category | String | 是 | 事件类别 |
| suggested_time | String | 否 | 建议时间：morning/afternoon/evening |
| start_date | DateTime | 是 | 开始时间 |
| end_date | DateTime | 是 | 结束时间 |

#### 响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "original_schedule": {
      // 原始日程数据
    },
    "optimized_schedule": {
      "optimized_events": [
        {
          "title": "算法基础复习",
          "description": "复习数据结构和算法基础知识，重点关注数组、链表、栈和队列",
          "duration": 120,
          "priority": "high",
          "category": "study",
          "suggested_time": "morning",
          "start_date": "2025-01-15T09:00:00Z",
          "end_date": "2025-01-15T11:00:00Z",
          "optimization_reason": "保持在最佳学习时间段",
          "conflicts_resolved": []
        }
      ],
      "total_optimized_time": 120,
      "time_saved": 30,
      "efficiency_score": 85.5,
      "optimization_summary": "通过重新安排事件顺序，提高了整体效率",
      "suggestions": [
        "建议在学习间隙安排短暂休息",
        "可以将相似类别的任务安排在一起"
      ]
    },
    "ai_analysis": "详细的AI分析报告...",
    "model_info": {
      "name": "deepseek-chat",
      "provider": "deepseek",
      "version": "deepseek-chat",
      "temperature": 0.7
    }
  },
  "request_id": "unique-request-id",
  "timestamp": 1642694400
}
```

## 使用示例

### Python示例

```python
import requests
import json
from datetime import datetime, timedelta

# API端点
url = "http://localhost:8000/api/v1/schedule/optimize"

# 创建请求数据
data = {
    "events": [
        {
            "title": "算法基础复习",
            "description": "复习数据结构和算法基础知识",
            "duration": 120,
            "priority": "high",
            "category": "study",
            "suggested_time": "morning",
            "start_date": "2025-01-15T09:00:00Z",
            "end_date": "2025-01-15T11:00:00Z"
        }
    ],
    "total_events": 1,
    "estimated_total_time": 120,
    "request_id": "test-request-123"
}

# 发送请求
response = requests.post(url, json=data)

if response.status_code == 200:
    result = response.json()
    print("优化成功！")
    print(f"效率评分: {result['data']['optimized_schedule']['efficiency_score']}")
else:
    print(f"请求失败: {response.status_code}")
```

### cURL示例

```bash
curl -X POST "http://localhost:8000/api/v1/schedule/optimize" \
  -H "Content-Type: application/json" \
  -d '{
    "events": [
      {
        "title": "算法基础复习",
        "description": "复习数据结构和算法基础知识",
        "duration": 120,
        "priority": "high",
        "category": "study",
        "suggested_time": "morning",
        "start_date": "2025-01-15T09:00:00Z",
        "end_date": "2025-01-15T11:00:00Z"
      }
    ],
    "total_events": 1,
    "estimated_total_time": 120,
    "request_id": "test-request-123"
  }'
```

## 错误处理

### 常见错误码

| 错误码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 500 | 服务器内部错误 |
| 503 | DeepSeek API服务不可用 |

### 错误响应格式

```json
{
  "code": 400,
  "message": "Invalid request parameters",
  "request_id": "test-request-123",
  "timestamp": 1642694400
}
```

## 最佳实践

1. **合理设置优先级**：确保重要任务设置为high优先级
2. **提供详细描述**：描述越详细，AI优化效果越好
3. **设置用户偏好**：根据个人习惯设置偏好时间段
4. **考虑约束条件**：设置合理的工作时长和休息时间
5. **处理异常情况**：始终检查API响应状态并处理错误

## 技术实现

- **AI模型**：使用DeepSeek Chat模型进行智能分析
- **Prompt工程**：采用结构化的prompt模板确保输出质量
- **数据验证**：使用Pydantic进行严格的数据验证
- **错误处理**：完善的异常处理机制
- **可扩展性**：支持自定义模板和参数配置