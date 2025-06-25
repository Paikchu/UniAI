
# 通用AI后台平台需求文档

## 1. 项目概述

搭建一套通用的AI基础平台，当前业务涉及多个AI平台（如OpenAI、文心一言、自研模型）的集成调用，去解决不同app开发不同后端的问题。为提升AI能力复用效率，降低集成成本，需构建一套通用AI后台平台，实现多AI平台的统一管理与调用。


## 2. API接口

### Base Chat Service
#### api/v1/chat/completions
#### ChatRequest
```json
{
  "model": "gpt-4",
  "parameters": {
    "prompt": "你好，世界",
    "temperature": 0.7,
    "max_tokens": 100,
    "prompt_id" : "scene_1"
  },
  "user_info": {
    "user_id": "123456",
    "user_role": "admin"
  },
  "request_id": "uuid-1234567890"
}
```

#### Response
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "result": "你好！有什么可以帮助你的吗？",
    "model_info": {
      "name": "gpt-4",
      "provider": "openai",
      "version": "0613"
    },
    "usage": {
      "prompt_tokens": 5,
      "completion_tokens": 10,
      "total_tokens": 15
    }
  },
  "request_id": "uuid-1234567890",
  "timestamp": 1689567890
}
```


### Schedule Plan

#### POST /api/v1/schedule/plan

#### Request

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

#### Response

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

# TODO
- [ ] 实现模型调用日志记录
- [ ] 实现角色权限管理
- [ ] 实现线上模型动态选择，降低API成本
- [ ] 实现调用记录查询
- [ ] 实现系统配置接口
- [x] 实现健康检查接口
- [ ] 实现模型并发控制
- [ ] 实现模型调用超时处理
- [ ] 实现模型调用失败重试
- [ ] 实现模型调用失败熔断
- [ ] 实现模型调用负载均衡
- [ ] 实现模型调用缓存