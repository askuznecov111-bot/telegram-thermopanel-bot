#!/usr/bin/env python3
"""
Запуск deployment и тестирование
"""
import os
import time
from dotenv import load_dotenv
from abacusai import ApiClient

load_dotenv()

API_KEY = os.getenv('ABACUS_API_KEY', 's2_a337cfbf99eb400fa20558122b95d310')

# Правильные credentials
PROJECT_ID = '117f38e11e'
DEPLOYMENT_ID = '7c388e8dc'
DEPLOYMENT_TOKEN = '7ee99cc13aff41c7b00d1b6d7bb45bd8'

print("="*60)
print("Запуск и тестирование deployment")
print("="*60)
print(f"Project ID: {PROJECT_ID}")
print(f"Deployment ID: {DEPLOYMENT_ID}")
print(f"Deployment Token: {DEPLOYMENT_TOKEN}")
print("="*60)

try:
    client = ApiClient(API_KEY)
    print("✅ Клиент инициализирован")
    
    # Проверяем статус
    print("\n📊 Проверка текущего статуса deployment:")
    deployment = client.describe_deployment(DEPLOYMENT_ID)
    print(f"Статус: {deployment.status}")
    
    # Запускаем deployment если он остановлен
    if deployment.status == 'STOPPED':
        print("\n🚀 Запуск deployment...")
        try:
            client.start_deployment(DEPLOYMENT_ID)
            print("✅ Команда запуска отправлена")
            
            # Ждем запуска (может занять время)
            print("⏳ Ожидание запуска (max 60 секунд)...")
            for i in range(12):  # 12 попыток по 5 секунд
                time.sleep(5)
                deployment = client.describe_deployment(DEPLOYMENT_ID)
                print(f"   Попытка {i+1}/12: Статус = {deployment.status}")
                if deployment.status == 'ACTIVE':
                    print("✅ Deployment активен!")
                    break
            else:
                print("⚠️ Deployment еще не активен, но продолжим тестирование...")
        except Exception as e:
            print(f"❌ Ошибка при запуске: {str(e)[:500]}")
    
    # Тестируем чат
    print("\n💬 Тестирование чата:")
    try:
        response = client.get_chat_response(
            deployment_token=DEPLOYMENT_TOKEN,
            deployment_id=DEPLOYMENT_ID,
            messages=[
                {"is_user": True, "text": "Привет! Расскажи кратко о термопанелях."}
            ]
        )
        print(f"✅ Получен ответ!")
        print(f"\nОтвет типа: {type(response)}")
        print(f"Содержимое: {response}")
        
        # Попробуем извлечь текст ответа
        if isinstance(response, dict):
            if 'content' in response:
                print(f"\n📝 Текст ответа:\n{response['content']}")
            elif 'response' in response:
                print(f"\n📝 Текст ответа:\n{response['response']}")
            elif 'text' in response:
                print(f"\n📝 Текст ответа:\n{response['text']}")
            else:
                print(f"\n📝 Полный ответ:\n{response}")
                
    except Exception as e:
        print(f"❌ Ошибка при получении ответа: {str(e)[:500]}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"❌ Критическая ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("Тестирование завершено")
print("="*60)
