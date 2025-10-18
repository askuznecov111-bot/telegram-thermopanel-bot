#!/usr/bin/env python3
"""
Тестовый скрипт для проверки правильного endpoint Abacus.AI API
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('ABACUS_API_KEY', 's2_a337cfbf99eb400fa20558122b95d310')
DEPLOYMENT_ID = os.getenv('ABACUS_APP_ID', '1f9935b84')

print("="*60)
print("Тестирование Abacus.AI API")
print("="*60)
print(f"API Key: {API_KEY[:10]}...")
print(f"Deployment ID: {DEPLOYMENT_ID}")
print("="*60)

# Тестовое сообщение
test_message = "Привет! Расскажи о термопанелях."

# Заголовки для запросов
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Вариант 1: deployment_conversations/createDeploymentConversation
print("\n1️⃣ Тестирование: deployment_conversations/createDeploymentConversation")
url1 = "https://api.abacus.ai/deployment_conversations/createDeploymentConversation"
payload1 = {
    "deploymentId": DEPLOYMENT_ID,
    "message": test_message
}
print(f"URL: {url1}")
print(f"Payload: {json.dumps(payload1, indent=2, ensure_ascii=False)}")
try:
    response = requests.post(url1, headers=headers, json=payload1, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"❌ Ошибка: {e}")

# Вариант 2: ai_chat/createChatSession  
print("\n2️⃣ Тестирование: ai_chat/createChatSession")
url2 = "https://api.abacus.ai/ai_chat/createChatSession"
payload2 = {
    "deploymentId": DEPLOYMENT_ID,
    "message": test_message
}
print(f"URL: {url2}")
print(f"Payload: {json.dumps(payload2, indent=2, ensure_ascii=False)}")
try:
    response = requests.post(url2, headers=headers, json=payload2, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"❌ Ошибка: {e}")

# Вариант 3: predict/getChatResponse
print("\n3️⃣ Тестирование: predict/getChatResponse")
url3 = "https://api.abacus.ai/predict/getChatResponse"
payload3 = {
    "deploymentId": DEPLOYMENT_ID,
    "messages": [
        {
            "is_user": True,
            "text": test_message
        }
    ]
}
print(f"URL: {url3}")
print(f"Payload: {json.dumps(payload3, indent=2, ensure_ascii=False)}")
try:
    response = requests.post(url3, headers=headers, json=payload3, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"❌ Ошибка: {e}")

# Вариант 4: Используя Abacus Client Tool (если доступен)
print("\n4️⃣ Тестирование: Прямой вызов с deployment token")
url4 = f"https://api.abacus.ai/api/v0/deployments/{DEPLOYMENT_ID}/predict"
payload4 = {
    "query": test_message
}
print(f"URL: {url4}")
print(f"Payload: {json.dumps(payload4, indent=2, ensure_ascii=False)}")
try:
    response = requests.post(url4, headers=headers, json=payload4, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"Response Text: {response.text}")
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("\n" + "="*60)
print("Тестирование завершено")
print("="*60)
