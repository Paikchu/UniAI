# 统一日程规划 API 文档

## 概述

统一日程规划 API 提供了一个灵活的接口，支持两种输入方式：
1. **文本prompt输入**：用户用自然语言描述日程需求
2. **结构化数据输入**：用户提供详细的事件列表

无论使用哪种输入方式，API都会返回固定格式的日程安排结果。

## API 端点

### POST `/api/v1/schedule`

统一的日程规划端点，支持两种输入方式。

### GET `/api/v1/schedule/sample`

获取示例响应格式。

## 请求格式

### 方式1：文本Prompt输入

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
  "request_id": "req_123456789"
}
```

### 方式2：结构化数据输入

```json
{
  "events": [
    {
      "title": "团队会议",
      "description": "讨论项目进展和下周计划",
      "duration": 60,
      "priority": "high",
      "category": "work",
      "suggested_time": "morning",
      "start_date": "2025-01-16T09:00:00Z",
      "end_date": "2025-01-16T10:00:00Z"
    },
    {
      "title": "代码审查",
      "description": "审查新功能的代码实现",
      "duration": 90,
      "priority": "medium",
      "category": "work",
      "suggested_time": "afternoon",
      "start_date": "2025-01-16T14:00:00Z",
      "end_date": "2025-01-16T15:30:00Z"
    }
  ],
  "total_events": 2,
  "estimated_total_time": 150,
  "user_preferences": {
    "max_continuous_work": 120
  },
  "constraints": {
    "required_break_after_work": 15
  },
  "request_id": "req_123456789"
}
```

### 字段说明

#### 通用字段

| 字段 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `request_id` | string | 是 | 请求唯一标识符 |
| `user_preferences` | object | 否 | 用户偏好设置 |
| `constraints` | object | 否 | 约束条件 |

#### 文本输入方式字段

| 字段 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `prompt` | string | 是* | 用户的自然语言日程描述 |

#### 结构化输入方式字段

| 字段 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `events` | array | 是* | 事件列表 |
| `total_events` | integer | 否 | 事件总数（用于验证） |
| `estimated_total_time` | integer | 否 | 预估总时间（分钟） |

*注：`prompt` 和 `events` 必须提供其中一个，不能同时提供。

#### Event 对象字段

| 字段 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `title` | string | 是 | 事件标题 |
| `description` | string | 是 | 事件描述 |
| `duration` | integer | 是 | 持续时间（分钟） |
| `priority` | string | 是 | 优先级：high, medium, low |
| `category` | string | 是 | 事件类别 |
| `suggested_time` | string | 否 | 建议时间：morning, afternoon, evening |
| `start_date` | datetime | 是 | 开始时间（ISO 8601格式） |
| `end_date` | datetime | 是 | 结束时间（ISO 8601格式） |

## 响应格式

### 成功响应 (200 OK)

```json
{
  "code": 200,
  "message": "success",
  "data": {
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
      },
      {
        "title": "LeetCode刷题",
        "description": "完成10道中等难度的算法题，重点练习动态规划",
        "duration": 90,
        "priority": "high",
        "category": "study",
        "start_date": "2025-01-15T14:00:00Z",
        "end_date": "2025-01-15T15:30:00Z"
      }
    ],
    "total_events": 14,
    "estimated_total_time": 1680
  },
  "request_id": "req_123456789",
  "timestamp": 1705123456
}
```

### 错误响应 (400/500)

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Either 'prompt' or 'events' must be provided",
    "details": "请选择一种输入方式：文本prompt或结构化数据"
  }
}
```

## 使用示例

### Python 示例

#### 使用文本Prompt

```python
import requests

api_url = "http://localhost:8000/api/v1/schedule"

# 文本prompt输入
request_data = {
    "prompt": "我明天需要开会2小时，写代码3小时，健身1小时，请帮我安排。",
    "user_preferences": {
        "preferred_work_time": "morning"
    },
    "request_id": "prompt_example_001"
}

response = requests.post(api_url, json=request_data)

if response.status_code == 200:
    result = response.json()
    print(f"总事件数: {result['data']['total_events']}")
    print(f"总时间: {result['data']['estimated_total_time']} 分钟")
    
    for event in result['data']['events']:
        print(f"- {event['title']}: {event['duration']}分钟")
else:
    print(f"请求失败: {response.status_code}")
```

#### 使用结构化数据

```python
import requests
from datetime import datetime

api_url = "http://localhost:8000/api/v1/schedule"

# 结构化数据输入
request_data = {
    "events": [
        {
            "title": "项目会议",
            "description": "讨论新功能开发",
            "duration": 90,
            "priority": "high",
            "category": "work",
            "suggested_time": "morning",
            "start_date": "2025-01-16T09:00:00Z",
            "end_date": "2025-01-16T10:30:00Z"
        }
    ],
    "total_events": 1,
    "estimated_total_time": 90,
    "request_id": "structured_example_001"
}

response = requests.post(api_url, json=request_data)

if response.status_code == 200:
    result = response.json()
    print("日程安排成功创建!")
    print(f"请求ID: {result['request_id']}")
else:
    print(f"请求失败: {response.status_code}")
```

### cURL 示例

#### 文本Prompt输入

```bash
curl -X POST "http://localhost:8000/api/v1/schedule" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "明天我要开会、写代码、运动，请帮我安排时间",
    "request_id": "curl_test_001"
  }'
```

#### 结构化数据输入

```bash
curl -X POST "http://localhost:8000/api/v1/schedule" \
  -H "Content-Type: application/json" \
  -d '{
    "events": [
      {
        "title": "团队会议",
        "description": "周例会",
        "duration": 60,
        "priority": "high",
        "category": "work",
        "start_date": "2025-01-16T09:00:00Z",
        "end_date": "2025-01-16T10:00:00Z"
      }
    ],
    "total_events": 1,
    "estimated_total_time": 60,
    "request_id": "curl_test_002"
  }'
```

#### 获取示例数据

```bash
curl -X GET "http://localhost:8000/api/v1/schedule/sample"
```

### JavaScript 示例

```javascript
// 文本prompt输入
const scheduleWithPrompt = async (prompt) => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/schedule', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompt: prompt,
        request_id: `js_${Date.now()}`
      })
    });
    
    if (response.ok) {
      const result = await response.json();
      console.log('日程安排:', result.data);
      return result;
    } else {
      console.error('请求失败:', response.status);
    }
  } catch (error) {
    console.error('网络错误:', error);
  }
};

// 结构化数据输入
const scheduleWithEvents = async (events) => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/schedule', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        events: events,
        total_events: events.length,
        estimated_total_time: events.reduce((sum, e) => sum + e.duration, 0),
        request_id: `js_${Date.now()}`
      })
    });
    
    if (response.ok) {
      const result = await response.json();
      console.log('日程安排:', result.data);
      return result;
    } else {
      console.error('请求失败:', response.status);
    }
  } catch (error) {
    console.error('网络错误:', error);
  }
};

// 使用示例
scheduleWithPrompt("明天我要学习、工作、运动，请帮我安排");
```

## 输入验证规则

### 基本验证

1. **输入方式验证**：
   - 必须提供 `prompt` 或 `events` 其中一个
   - 不能同时提供两种输入方式

2. **字段验证**：
   - `request_id` 必须提供
   - `duration` 必须为正整数
   - `priority` 必须为 "high", "medium", "low" 之一
   - 日期时间必须为有效的 ISO 8601 格式

3. **逻辑验证**：
   - 如果提供 `total_events`，必须与 `events` 数组长度一致
   - `end_date` 必须晚于 `start_date`

### 错误处理

| 错误类型 | HTTP状态码 | 错误代码 | 描述 |
|----------|------------|----------|------|
| 输入方式错误 | 400 | VALIDATION_ERROR | 未提供输入或提供了多种输入方式 |
| 字段验证错误 | 400 | FIELD_VALIDATION_ERROR | 字段格式或值不正确 |
| 处理错误 | 500 | SCHEDULE_PROCESSING_ERROR | 服务器处理请求时发生错误 |

## 响应数据说明

### 固定返回格式

无论输入什么内容，API都会返回以下固定格式的数据：

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
    },
    {
      "title": "LeetCode刷题",
      "description": "完成10道中等难度的算法题，重点练习动态规划",
      "duration": 90,
      "priority": "high",
      "category": "study",
      "start_date": "2025-01-15T14:00:00Z",
      "end_date": "2025-01-15T15:30:00Z"
    }
  ],
  "total_events": 14,
  "estimated_total_time": 1680
}
```

这个设计允许前端开发者在开发阶段使用固定的数据进行测试，而不需要依赖复杂的AI处理逻辑。

## 性能和限制

### 性能指标
- **响应时间**: < 1秒（返回固定数据）
- **并发支持**: 最多 100 个并发请求
- **Prompt 长度**: 最大 5000 字符
- **事件数量**: 最多 50 个事件

### 使用限制
- 每个用户每分钟最多 60 次请求
- 单次请求最多处理 50 个事件
- 请求体大小限制：1MB

## 最佳实践

### 1. 选择合适的输入方式

- **使用文本prompt**：适合快速原型开发、用户友好的界面
- **使用结构化数据**：适合系统集成、精确控制

### 2. 错误处理

```python
try:
    response = requests.post(api_url, json=request_data)
    
    if response.status_code == 200:
        result = response.json()
        # 处理成功响应
    elif response.status_code == 400:
        error = response.json()["error"]
        print(f"输入错误: {error['message']}")
    else:
        print(f"服务器错误: {response.status_code}")
        
except requests.exceptions.RequestException as e:
    print(f"网络错误: {e}")
except json.JSONDecodeError:
    print("响应格式错误")
```

### 3. 请求ID管理

```python
import uuid

# 生成唯一请求ID
request_id = str(uuid.uuid4())

request_data = {
    "prompt": "用户输入",
    "request_id": request_id
}
```

### 4. 缓存策略

由于API返回固定数据，可以在客户端实现缓存：

```javascript
const cache = new Map();

const getCachedSchedule = (requestKey) => {
  if (cache.has(requestKey)) {
    return Promise.resolve(cache.get(requestKey));
  }
  
  return fetch('/api/v1/schedule', {
    method: 'POST',
    body: JSON.stringify(requestData)
  })
  .then(response => response.json())
  .then(data => {
    cache.set(requestKey, data);
    return data;
  });
};
```

## 迁移指南

### 从旧版API迁移

如果你之前使用的是分离的 `/schedule/optimize` 和 `/schedule/simple` 端点：

#### 旧版本 (schedule/simple)
```json
{
  "prompt": "用户描述"
}
```

#### 新版本 (统一接口)
```json
{
  "prompt": "用户描述",
  "request_id": "unique_id"
}
```

#### 旧版本 (schedule/optimize)
```json
{
  "events": [...],
  "total_events": 5,
  "estimated_total_time": 300,
  "request_id": "unique_id"
}
```

#### 新版本 (统一接口)
```json
{
  "events": [...],
  "total_events": 5,
  "estimated_total_time": 300,
  "request_id": "unique_id"
}
```

主要变化：
1. 统一端点：`/api/v1/schedule`
2. 文本输入需要添加 `request_id` 字段
3. 响应格式保持一致

## 技术实现

### 核心特性
1. **统一接口设计**：一个端点支持两种输入方式
2. **输入验证**：严格的数据验证和错误处理
3. **固定响应**：返回预定义的示例数据
4. **类型安全**：使用 Pydantic 进行数据验证
5. **文档完整**：自动生成的 OpenAPI 文档

### 架构优势
1. **简化维护**：只需维护一个API端点
2. **灵活输入**：支持多种使用场景
3. **一致响应**：统一的响应格式
4. **易于测试**：固定数据便于前端开发和测试

---

如有问题或建议，请联系开发团队或查看项目文档。