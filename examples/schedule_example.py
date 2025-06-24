import json
import requests
import uuid
from datetime import datetime, timedelta

# API端点
API_URL = "http://localhost:8000/api/v1/schedule/optimize"

# 创建示例日程数据
def create_sample_schedule():
    # 当前时间
    now = datetime.now()
    
    # 创建事件列表
    events = [
        {
            "title": "算法基础复习",
            "description": "复习数据结构和算法基础知识，重点关注数组、链表、栈和队列",
            "duration": 120,  # 分钟
            "priority": "high",
            "category": "study",
            "suggested_time": "morning",
            "start_date": (now + timedelta(days=1)).replace(hour=9, minute=0, second=0).isoformat(),
            "end_date": (now + timedelta(days=1)).replace(hour=11, minute=0, second=0).isoformat()
        },
        {
            "title": "LeetCode刷题",
            "description": "完成10道中等难度的算法题，重点练习动态规划",
            "duration": 90,
            "priority": "high",
            "category": "study",
            "start_date": (now + timedelta(days=1)).replace(hour=14, minute=0, second=0).isoformat(),
            "end_date": (now + timedelta(days=1)).replace(hour=15, minute=30, second=0).isoformat()
        },
        {
            "title": "项目开发",
            "description": "完成Web应用的用户认证模块",
            "duration": 180,
            "priority": "medium",
            "category": "work",
            "start_date": (now + timedelta(days=1)).replace(hour=16, minute=0, second=0).isoformat(),
            "end_date": (now + timedelta(days=1)).replace(hour=19, minute=0, second=0).isoformat()
        },
        {
            "title": "健身",
            "description": "进行有氧运动和力量训练",
            "duration": 60,
            "priority": "medium",
            "category": "health",
            "suggested_time": "evening",
            "start_date": (now + timedelta(days=1)).replace(hour=19, minute=30, second=0).isoformat(),
            "end_date": (now + timedelta(days=1)).replace(hour=20, minute=30, second=0).isoformat()
        }
    ]
    
    # 创建请求数据
    request_data = {
        "events": events,
        "total_events": len(events),
        "estimated_total_time": sum(event["duration"] for event in events),
        "user_preferences": {
            "preferred_study_time": "morning",
            "preferred_work_time": "afternoon",
            "preferred_break_duration": 15  # 分钟
        },
        "constraints": {
            "max_continuous_work": 120,  # 最长连续工作时间（分钟）
            "required_break_after_work": 15  # 工作后需要休息的时间（分钟）
        },
        "request_id": str(uuid.uuid4())
    }
    
    return request_data

# 发送请求到API
def optimize_schedule(schedule_data):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    response = requests.post(API_URL, json=schedule_data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# 打印优化结果
def print_optimization_results(response_data):
    if not response_data:
        return
    
    data = response_data.get("data", {})
    optimized = data.get("optimized_schedule", {})
    
    print("\n===== 日程优化结果 =====")
    print(f"效率评分: {optimized.get('efficiency_score', 0)}/100")
    print(f"节省时间: {optimized.get('time_saved', 0)}分钟")
    print(f"优化总结: {optimized.get('optimization_summary', '')}")
    
    print("\n优化后的日程:")
    for i, event in enumerate(optimized.get("optimized_events", []), 1):
        start = datetime.fromisoformat(event["start_date"].replace('Z', '+00:00'))
        end = datetime.fromisoformat(event["end_date"].replace('Z', '+00:00'))
        
        print(f"\n事件 {i}: {event['title']}")
        print(f"时间: {start.strftime('%Y-%m-%d %H:%M')} - {end.strftime('%H:%M')}")
        print(f"持续时间: {event['duration']}分钟")
        print(f"优先级: {event['priority']}")
        print(f"类别: {event['category']}")
        if event.get("optimization_reason"):
            print(f"优化原因: {event['optimization_reason']}")
    
    print("\n额外建议:")
    for i, suggestion in enumerate(optimized.get("suggestions", []), 1):
        print(f"{i}. {suggestion}")
    
    print("\n===== AI分析报告 =====")
    print(data.get("ai_analysis", ""))

# 主函数
def main():
    print("创建示例日程...")
    schedule_data = create_sample_schedule()
    
    print("发送优化请求...")
    response = optimize_schedule(schedule_data)
    
    if response:
        print_optimization_results(response)
    else:
        print("优化失败，请检查API服务是否运行。")

if __name__ == "__main__":
    main()