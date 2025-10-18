#!/usr/bin/env python3
"""
Тестирование правильных Abacus.AI API endpoints
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('ABACUS_API_KEY', 's2_a337cfbf99eb400fa20558122b95d310')
APP_ID = os.getenv('ABACUS_APP_ID', '1f9935b84')

print("="*60)
print("Тестирование ПРАВИЛЬНЫХ Abacus.AI API endpoints")
print("="*60)
print(f"API Key: {API_KEY[:10]}...")
print(f"App/Deployment ID: {APP_ID}")
print("="*60)

test_message = "Привет! Расскажи о термопанелях."

# Вариант 1: predict/getChatResponse (базовая аутентификация)
print("\n1️⃣ Тестирование: predict/getChatResponse с Basic Auth")
url1 = "https://api.abacus.ai/api/v0/predict/getChatResponse"
headers1 = {
    'Content-Type': 'application/json'
}
# Используем базовую аутентификацию с API ключом
auth1 = (API_KEY, '')
payload1 = {
    "deploymentId": APP_ID,
    "messages": [
        {
            "is_user": True,
            "text": test_message
        }
    ]
}
print(f"URL: {url1}")
print(f"Auth: Basic {API_KEY[:10]}...")
print(f"Payload: {json.dumps(payload1, indent=2, ensure_ascii=False)}")
try:
    response = requests.post(url1, headers=headers1, auth=auth1, json=payload1, timeout=30)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"❌ Response Text: {response.text[:500]}")
except Exception as e:
    print(f"❌ Ошибка: {e}")

# Вариант 2: predict/getChatResponse (Bearer token)
print("\n2️⃣ Тестирование: predict/getChatResponse с Bearer token")
url2 = "https://api.abacus.ai/api/v0/predict/getChatResponse"
headers2 = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}
payload2 = {
    "deploymentId": APP_ID,
    "messages": [
        {
            "is_user": True,
            "text": test_message
        }
    ]
}
print(f"URL: {url2}")
print(f"Payload: {json.dumps(payload2, indent=2, ensure_ascii=False)}")
try:
    response = requests.post(url2, headers=headers2, json=payload2, timeout=30)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"❌ Response Text: {response.text[:500]}")
except Exception as e:
    print(f"❌ Ошибка: {e}")

# Вариант 3: llm_apps/getLLMAppResponse
print("\n3️⃣ Тестирование: llm_apps/getLLMAppResponse с Basic Auth")
url3 = "https://api.abacus.ai/api/v0/llm_apps/getLLMAppResponse"
headers3 = {
    'Content-Type': 'application/json'
}
auth3 = (API_KEY, '')
payload3 = {
    "appId": APP_ID,
    "query": test_message
}
print(f"URL: {url3}")
print(f"Auth: Basic {API_KEY[:10]}...")
print(f"Payload: {json.dumps(payload3, indent=2, ensure_ascii=False)}")
try:
    response = requests.post(url3, headers=headers3, auth=auth3, json=payload3, timeout=30)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"❌ Response Text: {response.text[:500]}")
except Exception as e:
    print(f"❌ Ошибка: {e}")

# Вариант 4: llm_apps/getLLMAppResponse с conversations
print("\n4️⃣ Тестирование: llm_apps/getLLMAppResponse с messages array")
url4 = "https://api.abacus.ai/api/v0/llm_apps/getLLMAppResponse"
headers4 = {
    'Content-Type': 'application/json'
}
auth4 = (API_KEY, '')
payload4 = {
    "appId": APP_ID,
    "messages": [
        {
            "is_user": True,
            "text": test_message
        }
    ]
}
print(f"URL: {url4}")
print(f"Auth: Basic {API_KEY[:10]}...")
print(f"Payload: {json.dumps(payload4, indent=2, ensure_ascii=False)}")
try:
    response = requests.post(url4, headers=headers4, auth=auth4, json=payload4, timeout=30)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"❌ Response Text: {response.text[:500]}")
except Exception as e:
    print(f"❌ Ошибка: {e}")

# Вариант 5: Используя только API key в header
print("\n5️⃣ Тестирование: predict/getChatResponse с APIKEY header")
url5 = "https://api.abacus.ai/api/v0/predict/getChatResponse"
headers5 = {
    'APIKEY': API_KEY,
    'Content-Type': 'application/json'
}
payload5 = {
    "deploymentId": APP_ID,
    "messages": [
        {
            "is_user": True,
            "text": test_message
        }
    ]
}
print(f"URL: {url5}")
print(f"Headers: APIKEY: {API_KEY[:10]}...")
print(f"Payload: {json.dumps(payload5, indent=2, ensure_ascii=False)}")
try:
    response = requests.post(url5, headers=headers5, json=payload5, timeout=30)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"❌ Response Text: {response.text[:500]}")
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("\n" + "="*60)
print("Тестирование завершено")
print("="*60)
