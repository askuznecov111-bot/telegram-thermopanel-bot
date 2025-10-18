#!/usr/bin/env python3
"""
Тестирование Abacus.AI SDK для чат-бота
"""
import os
from dotenv import load_dotenv
from abacusai import ApiClient

load_dotenv()

API_KEY = os.getenv('ABACUS_API_KEY', 's2_a337cfbf99eb400fa20558122b95d310')
ID = os.getenv('ABACUS_APP_ID', '1f9935b84')

print("="*60)
print("Тестирование Abacus.AI SDK")
print("="*60)
print(f"API Key: {API_KEY[:15]}...")
print(f"ID: {ID}")
print("="*60)

try:
    # Инициализация клиента
    client = ApiClient(API_KEY)
    print("✅ Клиент успешно инициализирован")
    
    # Попробуем разные методы, чтобы понять, что такое наш ID
    
    # Вариант 1: Попробовать как deployment ID
    print("\n1️⃣ Попытка использовать как Deployment ID:")
    try:
        deployment = client.describe_deployment(ID)
        print(f"✅ Это deployment! Info: {deployment}")
    except Exception as e:
        print(f"❌ Не deployment: {str(e)[:200]}")
    
    # Вариант 2: Попробовать как App ID (для LLM apps)
    print("\n2️⃣ Попытка использовать для получения LLM App Response:")
    try:
        # Метод для получения ответа от LLM App
        response = client.get_llm_app_response(
            app_id=ID,
            query="Привет! Расскажи о термопанелях."
        )
        print(f"✅ Получен ответ: {response}")
    except Exception as e:
        print(f"❌ Ошибка: {str(e)[:500]}")
    
    # Вариант 3: Попробовать через predict с chat
    print("\n3️⃣ Попытка использовать через predict/getChatResponse:")
    try:
        response = client.get_chat_response(
            deployment_id=ID,
            messages=[
                {"is_user": True, "text": "Привет! Расскажи о термопанелях."}
            ]
        )
        print(f"✅ Получен ответ: {response}")
    except Exception as e:
        print(f"❌ Ошибка: {str(e)[:500]}")
    
    # Вариант 4: Попробуем создать deployment conversation
    print("\n4️⃣ Попытка создать deployment conversation:")
    try:
        conversation = client.create_deployment_conversation(
            deployment_id=ID,
            message="Привет! Расскажи о термопанелях."
        )
        print(f"✅ Conversation создан: {conversation}")
    except Exception as e:
        print(f"❌ Ошибка: {str(e)[:500]}")
    
    # Вариант 5: Список доступных методов клиента
    print("\n5️⃣ Доступные методы для работы с чатом:")
    chat_methods = [method for method in dir(client) if 'chat' in method.lower() or 'llm' in method.lower() or 'conversation' in method.lower()]
    print(f"Найдено методов: {len(chat_methods)}")
    for method in chat_methods[:20]:  # Показываем первые 20
        print(f"  - {method}")

except Exception as e:
    print(f"❌ Критическая ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("Тестирование завершено")
print("="*60)
