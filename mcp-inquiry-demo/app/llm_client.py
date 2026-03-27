# 大模型调用客户端
import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取qwen模型配置
QWEN_API_KEY = os.getenv('QWEN_API_KEY')
QWEN_BASE_URL = os.getenv('QWEN_BASE_URL', 'https://api.qwen.com')

def generate_response(inquiry):
    """生成大模型响应"""
    content = inquiry.get('content', '')
    
    # 构建请求数据
    payload = {
        "model": "qwen-turbo",
        "messages": [
            {
                "role": "system",
                "content": "你是一个专业的B2B询盘助手，负责处理客户的询盘请求并提供专业的回复。"
            },
            {
                "role": "user",
                "content": content
            }
        ],
        "temperature": 0.7
    }
    
    # 构建请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {QWEN_API_KEY}"
    }
    
    try:
        # 调用qwen API
        response = requests.post(
            f"{QWEN_BASE_URL}/v1/chat/completions",
            json=payload,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content']
            return {
                "reply": reply,
                "processed_at": "2026-03-26"
            }
        else:
            # API调用失败，返回默认回复
            return {
                "reply": f"感谢您的询盘，我们会尽快处理您的需求：{content}",
                "processed_at": "2026-03-26"
            }
    except Exception as e:
        # 异常处理，返回默认回复
        return {
            "reply": f"感谢您的询盘，我们会尽快处理您的需求：{content}",
            "processed_at": "2026-03-26"
        }
