# UniAI 项目架构说明

## 项目结构

```
app/
├── __init__.py
├── main.py                 # FastAPI应用入口
├── api/                    # API路由层
│   ├── __init__.py
│   └── v1/
│       ├── __init__.py
│       └── chat.py         # 聊天接口
├── core/                   # 核心配置和异常
│   ├── __init__.py
│   ├── config.py           # 配置管理
│   └── exceptions.py       # 自定义异常
├── middleware/             # 中间件
│   ├── __init__.py
│   └── exception_handler.py # 异常处理中间件
├── models/                 # 数据模型
│   ├── __init__.py
│   ├── request.py          # 请求模型
│   └── response.py         # 响应模型
├── providers/              # AI提供商适配器
│   ├── __init__.py
│   └── deepseek.py         # DeepSeek适配器
├── services/               # 业务逻辑层
│   ├── __init__.py
│   └── chat_service.py     # 聊天服务
└── utils/                  # 工具函数
    ├── __init__.py
    └── time_utils.py       # 时间工具
```

## 架构设计原则

### 1. 分层架构
- **API层**: 处理HTTP请求和响应
- **服务层**: 包含业务逻辑
- **数据层**: 数据模型定义
- **提供商层**: 外部AI服务适配

### 2. 职责分离
- **models/**: 数据模型按请求/响应分离
- **services/**: 业务逻辑与API控制器分离
- **core/**: 核心配置和异常管理
- **utils/**: 通用工具函数

### 3. 异常处理
- 统一的异常处理机制
- 自定义异常类型
- 标准化的错误响应格式

### 4. 配置管理
- 环境变量配置
- 类型安全的配置类
- 支持动态配置加载

## 主要改进

1. **模块化**: 将原来混合在一个文件中的代码按功能拆分
2. **类型安全**: 使用Pydantic进行数据验证和类型检查
3. **异常处理**: 统一的异常处理机制
4. **可扩展性**: 易于添加新的AI提供商和功能
5. **可维护性**: 清晰的代码结构和职责分离

## 使用说明

### 启动应用
```bash
uvicorn app.main:app --reload
```

### 环境变量配置
```env
DEEPSEEK_API_KEY=your_api_key
SCENE_PROMPTS={"scene_1": "You are a translator", "scene_2": "You are a code optimizer"}
SUPPORTED_MODELS=["deepseek-chat"]
```

### API调用示例
```bash
curl -X POST "http://localhost:8000/api/v1/chat/completions" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "deepseek-chat",
       "parameters": {
         "prompt": "Hello, world!",
         "prompt_id": "scene_1"
       },
       "user_info": {
         "user_id": "user123",
         "user_role": "user"
       },
       "request_id": "req123"
     }'
```