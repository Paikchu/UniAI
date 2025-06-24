#!/usr/bin/env python3
"""
统一日程规划API使用示例

这个示例展示了如何使用新的统一日程规划API，
支持两种输入方式：文本prompt和结构化数据。
"""

import requests
import json
from datetime import datetime

# API配置
API_BASE_URL = "http://localhost:8000/api/v1"
SCHEDULE_ENDPOINT = f"{API_BASE_URL}/schedule"
SAMPLE_ENDPOINT = f"{API_BASE_URL}/schedule/sample"

def test_prompt_input():
    """
    测试使用文本prompt输入
    """
    print("🔤 测试文本prompt输入方式")
    print("="*50)
    
    # 使用文本prompt
    request_data = {
        "prompt": "我明天需要复习算法基础2小时，刷LeetCode 1.5小时，还要做项目开发3小时，健身1小时。请帮我安排一个高效的日程。",
        "user_preferences": {
            "preferred_study_time": "morning",
            "preferred_work_time": "afternoon"
        },
        "request_id": "prompt_test_001"
    }
    
    try:
        response = requests.post(
            SCHEDULE_ENDPOINT,
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 请求成功!")
            print(f"📅 返回的事件数量: {result['data']['total_events']}")
            print(f"⏱️ 总预估时间: {result['data']['estimated_total_time']} 分钟")
            
            print("\n📋 事件列表:")
            for i, event in enumerate(result['data']['events'], 1):
                print(f"{i}. {event['title']}")
                print(f"   描述: {event['description']}")
                print(f"   时长: {event['duration']} 分钟")
                print(f"   优先级: {event['priority']}")
                print(f"   类别: {event['category']}")
                print(f"   开始时间: {event['start_date']}")
                print(f"   结束时间: {event['end_date']}")
                if event.get('suggested_time'):
                    print(f"   建议时间: {event['suggested_time']}")
                print()
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ 错误: {e}")

def test_structured_input():
    """
    测试使用结构化数据输入
    """
    print("\n📊 测试结构化数据输入方式")
    print("="*50)
    
    # 使用结构化数据
    request_data = {
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
        "request_id": "structured_test_001"
    }
    
    try:
        response = requests.post(
            SCHEDULE_ENDPOINT,
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 请求成功!")
            print(f"📅 返回的事件数量: {result['data']['total_events']}")
            print(f"⏱️ 总预估时间: {result['data']['estimated_total_time']} 分钟")
            print(f"🆔 请求ID: {result['request_id']}")
            print(f"⏰ 时间戳: {result['timestamp']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ 错误: {e}")

def test_sample_endpoint():
    """
    测试示例端点
    """
    print("\n📖 测试示例端点")
    print("="*50)
    
    try:
        response = requests.get(SAMPLE_ENDPOINT)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 获取示例数据成功!")
            print(f"📅 示例事件数量: {result['total_events']}")
            print(f"⏱️ 示例总时间: {result['estimated_total_time']} 分钟")
            
            print("\n📋 示例事件:")
            for i, event in enumerate(result['events'], 1):
                print(f"{i}. {event['title']} ({event['duration']}分钟)")
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 错误: {e}")

def test_validation_errors():
    """
    测试输入验证错误
    """
    print("\n⚠️ 测试输入验证")
    print("="*50)
    
    # 测试1: 既不提供prompt也不提供events
    print("测试1: 空输入")
    request_data = {
        "request_id": "validation_test_001"
    }
    
    try:
        response = requests.post(
            SCHEDULE_ENDPOINT,
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"状态码: {response.status_code}")
        if response.status_code != 200:
            print(f"预期的验证错误: {response.text[:100]}...")
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试2: 同时提供prompt和events
    print("\n测试2: 同时提供两种输入")
    request_data = {
        "prompt": "测试prompt",
        "events": [
            {
                "title": "测试事件",
                "description": "测试描述",
                "duration": 60,
                "priority": "medium",
                "category": "test",
                "start_date": "2025-01-16T09:00:00Z",
                "end_date": "2025-01-16T10:00:00Z"
            }
        ],
        "total_events": 1,
        "estimated_total_time": 60,
        "request_id": "validation_test_002"
    }
    
    try:
        response = requests.post(
            SCHEDULE_ENDPOINT,
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"状态码: {response.status_code}")
        if response.status_code != 200:
            print(f"预期的验证错误: {response.text[:100]}...")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    print("🚀 统一日程规划API测试")
    print("="*60)
    
    # 测试示例端点
    test_sample_endpoint()
    
    # 测试文本prompt输入
    test_prompt_input()
    
    # 测试结构化数据输入
    test_structured_input()
    
    # 测试输入验证
    test_validation_errors()
    
    print("\n✨ 测试完成!")
    print("\n💡 使用说明:")
    print("1. 可以使用 'prompt' 字段提供自然语言描述")
    print("2. 可以使用 'events' 字段提供结构化数据")
    print("3. 两种方式不能同时使用")
    print("4. 无论哪种输入方式，都会返回固定格式的结果")