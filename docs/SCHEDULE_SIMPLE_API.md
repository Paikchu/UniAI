# 简化日程规划 API 文档

## 概述

简化日程规划 API 提供了一个更加用户友好的接口，允许用户通过自然语言描述来获得智能的日程优化建议。与标准日程规划 API 不同，用户无需提供结构化的日程数据，只需要用自然语言描述他们的安排和需求即可。

## API 端点

### POST `/api/v1/schedule/simple`

基于用户的自然语言描述进行智能日程规划和优化。

## 请求格式

### 请求体

```json
{
  "prompt": "string"
}
```

#### 字段说明

| 字段 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `prompt` | string | 是 | 用户的自然语言日程描述，包含时间安排、偏好和约束条件 |

### 请求示例

```json
{
  "prompt": "我明天有以下安排：上午9点开会，中午12点吃午餐，下午2点写代码，下午4点健身，晚上7点聚会。请帮我优化时间安排，我希望在会议和午餐之间有缓冲时间。"
}
```

## 响应格式

### 成功响应 (200 OK)

```json
{
  "success": true,
  "data": {
    "optimized_events": [
      {
        "title": "string",
        "start_time": "2024-01-15T09:00:00",
        "end_time": "2024-01-15T10:30:00",
        "location": "string",
        "description": "string",
        "priority": "high|medium|low",
        "optimization_reason": "string"
      }
    ],
    "optimization": {
      "overall_score": 8.5,
      "suggestions": [
        "建议在会议后安排15分钟缓冲时间",
        "考虑将健身时间调整到下午3点以避免高峰期"
      ],
      "potential_conflicts": [
        "午餐时间可能与下午会议冲突"
      ],
      "time_efficiency": 0.85,
      "stress_level": "medium"
    },
    "total_events": 5,
    "estimated_total_time": "8小时30分钟"
  },
  "message": "日程优化完成",
  "request_id": "req_123456789"
}
```

### 错误响应 (400/500)

```json
{
  "success": false,
  "error": {
    "code": "INVALID_PROMPT",
    "message": "无法从提供的描述中提取有效的日程信息",
    "details": "请提供更具体的时间和活动信息"
  }
}
```

## 使用示例

### Python 示例

```python
import requests
import json

# API 配置
api_url = "http://localhost:8000/api/v1/schedule/simple"

# 用户输入
user_prompt = """
我明天的安排：
1. 上午9点到10点半：团队会议
2. 中午12点到1点：客户午餐
3. 下午2点到4点：编程工作
4. 下午4点半到5点半：健身
5. 晚上7点到9点：朋友聚会

我希望能够合理安排时间，避免太紧张的日程。
"""

# 发送请求
response = requests.post(
    api_url,
    json={"prompt": user_prompt},
    headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    result = response.json()
    print("优化后的日程：")
    
    for event in result["data"]["optimized_events"]:
        print(f"- {event['title']}: {event['start_time']} - {event['end_time']}")
        if event.get('optimization_reason'):
            print(f"  优化原因: {event['optimization_reason']}")
    
    print(f"\n总体评分: {result['data']['optimization']['overall_score']}/10")
else:
    print(f"请求失败: {response.status_code}")
    print(response.text)
```

### cURL 示例

```bash
curl -X POST "http://localhost:8000/api/v1/schedule/simple" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "明天我需要：9点开会，12点吃午饭，2点写代码，4点健身。请帮我优化安排。"
  }'
```

### JavaScript 示例

```javascript
const scheduleOptimize = async (prompt) => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/schedule/simple', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt })
    });
    
    if (response.ok) {
      const result = await response.json();
      console.log('优化结果:', result.data);
      return result;
    } else {
      console.error('请求失败:', response.status);
    }
  } catch (error) {
    console.error('网络错误:', error);
  }
};

// 使用示例
const userPrompt = "我今天要开会、吃饭、运动，请帮我安排时间";
scheduleOptimize(userPrompt);
```

## Prompt 编写指南

### 有效的 Prompt 特征

1. **包含具体时间信息**
   - ✅ "上午9点开会"
   - ✅ "下午2点到4点写代码"
   - ❌ "早上开会"

2. **描述活动内容**
   - ✅ "团队会议讨论项目进展"
   - ✅ "和客户吃午餐"
   - ❌ "做事情"

3. **表达偏好和约束**
   - ✅ "我希望在会议之间有缓冲时间"
   - ✅ "我比较喜欢上午处理重要工作"
   - ✅ "避免午餐时间冲突"

4. **提供上下文信息**
   - ✅ "明天是工作日"
   - ✅ "这是我的周末计划"
   - ✅ "我需要准备考试"

### Prompt 模板

#### 工作日安排
```
我明天的工作安排：
1. [时间]: [活动描述]
2. [时间]: [活动描述]
...

我的偏好：
- [偏好1]
- [偏好2]

约束条件：
- [约束1]
- [约束2]
```

#### 学习计划
```
我需要制定学习计划：
- [科目1]: [时长] 
- [科目2]: [时长]
...

我希望：
- [学习偏好]
- [时间安排偏好]
```

#### 休闲活动
```
我的周末计划：
- [活动1]: [大概时间]
- [活动2]: [大概时间]
...

我想要一个[轻松/充实/平衡]的周末。
```

## 错误处理

### 常见错误类型

| 错误代码 | 描述 | 解决方案 |
|----------|------|----------|
| `INVALID_PROMPT` | 无法解析用户输入 | 提供更具体的时间和活动信息 |
| `EXTRACTION_FAILED` | 信息提取失败 | 重新组织描述，使用更清晰的表达 |
| `OPTIMIZATION_ERROR` | 优化过程出错 | 简化日程安排或减少约束条件 |
| `AI_SERVICE_ERROR` | AI 服务不可用 | 稍后重试或联系技术支持 |

### 错误处理最佳实践

```python
try:
    response = requests.post(api_url, json={"prompt": user_prompt})
    
    if response.status_code == 200:
        result = response.json()
        # 处理成功响应
    elif response.status_code == 400:
        error = response.json()["error"]
        print(f"输入错误: {error['message']}")
        print(f"建议: {error.get('details', '')}")
    else:
        print(f"服务器错误: {response.status_code}")
        
except requests.exceptions.RequestException as e:
    print(f"网络错误: {e}")
except json.JSONDecodeError:
    print("响应格式错误")
```

## 性能和限制

### 性能指标
- **响应时间**: 通常 3-8 秒
- **并发支持**: 最多 10 个并发请求
- **Prompt 长度**: 最大 2000 字符

### 使用限制
- 每个用户每分钟最多 20 次请求
- 单次请求最多处理 20 个事件
- 时间范围限制在 7 天内

### 优化建议
1. **缓存结果**: 对于相似的请求可以缓存结果
2. **批量处理**: 将多个相关的日程安排合并到一个请求中
3. **异步处理**: 对于非实时需求，考虑使用异步处理

## 技术实现

### 核心特性
1. **自然语言处理**: 使用 DeepSeek AI 进行语义理解
2. **两阶段处理**: 
   - 第一阶段：从自然语言中提取结构化信息
   - 第二阶段：基于提取的信息进行优化
3. **智能推理**: 考虑时间冲突、用户偏好和实际约束
4. **灵活输出**: 提供详细的优化建议和潜在问题提醒

### 与标准 API 的对比

| 特性 | 简化 API | 标准 API |
|------|----------|----------|
| 输入格式 | 自然语言 | 结构化 JSON |
| 使用难度 | 简单 | 中等 |
| 灵活性 | 高 | 中等 |
| 精确度 | 中等 | 高 |
| 适用场景 | 快速原型、用户友好界面 | 系统集成、精确控制 |

## 最佳实践

1. **清晰描述**: 使用具体的时间和活动描述
2. **表达偏好**: 明确说明你的时间偏好和约束
3. **提供上下文**: 说明是工作日、周末还是特殊场合
4. **合理期望**: 理解 AI 的建议是参考，需要根据实际情况调整
5. **迭代优化**: 根据结果反馈调整你的描述方式

## 更新日志

### v1.0.0 (2024-01-15)
- 🎉 首次发布简化日程规划 API
- ✨ 支持自然语言输入
- 🤖 集成 DeepSeek AI 进行智能分析
- 📊 提供详细的优化建议和评分
- 🔧 完整的错误处理和验证机制

---

如有问题或建议，请联系开发团队或查看项目文档。