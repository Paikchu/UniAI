#!/usr/bin/env python3
"""
简化日程规划API使用示例

这个示例展示了如何使用新的简化日程规划API，
用户只需要提供一个自然语言的prompt，系统会自动提取日程信息并进行优化。
"""

import requests
import json
from datetime import datetime

# API配置
API_BASE_URL = "http://localhost:8000/api/v1"
SCHEDULE_ENDPOINT = f"{API_BASE_URL}/schedule/simple"

def test_simple_schedule_api():
    """
    测试简化日程规划API
    """
    
    # 示例用户prompt
    user_prompt = """
    我明天有以下安排需要优化：
    
    1. 上午9点到10点半开会讨论项目进展
    2. 中午12点到1点和客户吃午餐
    3. 下午2点到4点写代码
    4. 下午4点半到5点半健身
    5. 晚上7点到9点参加朋友聚会
    
    我希望能够合理安排时间，避免冲突，并且在会议和午餐之间留出一些缓冲时间。
    另外，我比较喜欢上午处理重要工作，下午做一些轻松的活动。
    """
    
    # 构建请求数据
    request_data = {
        "prompt": user_prompt
    }
    
    try:
        print("发送请求到简化日程规划API...")
        print(f"请求URL: {SCHEDULE_ENDPOINT}")
        print(f"用户Prompt: {user_prompt[:100]}...")
        print("\n" + "="*50)
        
        # 发送POST请求
        response = requests.post(
            SCHEDULE_ENDPOINT,
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        # 检查响应状态
        if response.status_code == 200:
            result = response.json()
            print("✅ API调用成功!")
            print("\n📅 优化后的日程安排:")
            
            # 显示优化结果
            if "data" in result and "optimized_events" in result["data"]:
                events = result["data"]["optimized_events"]
                
                for i, event in enumerate(events, 1):
                    print(f"\n{i}. {event['title']}")
                    print(f"   时间: {event['start_time']} - {event['end_time']}")
                    print(f"   地点: {event.get('location', '未指定')}")
                    print(f"   优先级: {event.get('priority', '中等')}")
                    
                    if event.get('description'):
                        print(f"   描述: {event['description']}")
                    
                    if event.get('optimization_reason'):
                        print(f"   优化原因: {event['optimization_reason']}")
            
            # 显示优化建议
            if "data" in result and "optimization" in result["data"]:
                optimization = result["data"]["optimization"]
                print(f"\n💡 优化建议:")
                print(f"   总体评分: {optimization.get('overall_score', 'N/A')}/10")
                
                if optimization.get('suggestions'):
                    print("   具体建议:")
                    for suggestion in optimization['suggestions']:
                        print(f"   - {suggestion}")
                
                if optimization.get('potential_conflicts'):
                    print("   ⚠️ 潜在冲突:")
                    for conflict in optimization['potential_conflicts']:
                        print(f"   - {conflict}")
        
        else:
            print(f"❌ API调用失败")
            print(f"状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求错误: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
    except Exception as e:
        print(f"❌ 未知错误: {e}")

def test_multiple_scenarios():
    """
    测试多种场景的日程规划
    """
    
    scenarios = [
        {
            "name": "工作日安排",
            "prompt": "明天我需要：9点开晨会，10点写报告，12点吃午饭，2点客户会议，4点代码审查，6点下班。请帮我优化时间安排。"
        },
        {
            "name": "周末计划",
            "prompt": "这个周六我想：上午去健身房，中午和朋友吃饭，下午看电影，晚上在家休息。请帮我安排一个轻松的周末。"
        },
        {
            "name": "学习计划",
            "prompt": "我需要准备考试：上午复习数学2小时，下午学英语1.5小时，晚上做练习题1小时。请帮我制定高效的学习计划。"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🎯 测试场景: {scenario['name']}")
        print("="*60)
        
        request_data = {"prompt": scenario['prompt']}
        
        try:
            response = requests.post(
                SCHEDULE_ENDPOINT,
                json=request_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ 成功获取优化建议")
                
                if "data" in result and "optimization" in result["data"]:
                    optimization = result["data"]["optimization"]
                    print(f"评分: {optimization.get('overall_score', 'N/A')}/10")
                    
                    if optimization.get('suggestions'):
                        print("建议:")
                        for suggestion in optimization['suggestions'][:2]:  # 只显示前2个建议
                            print(f"  - {suggestion}")
            else:
                print(f"❌ 失败 (状态码: {response.status_code})")
                
        except Exception as e:
            print(f"❌ 错误: {e}")

if __name__ == "__main__":
    print("🚀 简化日程规划API测试")
    print("="*50)
    
    # 基本功能测试
    test_simple_schedule_api()
    
    print("\n" + "="*50)
    print("🔄 多场景测试")
    
    # 多场景测试
    test_multiple_scenarios()
    
    print("\n✨ 测试完成!")