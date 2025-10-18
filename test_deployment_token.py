#!/usr/bin/env python3
"""
Тестирование с deployment_token
"""
import os
import inspect
from dotenv import load_dotenv
from abacusai import ApiClient

load_dotenv()

API_KEY = os.getenv('ABACUS_API_KEY', 's2_a337cfbf99eb400fa20558122b95d310')
DEPLOYMENT_TOKEN = os.getenv('ABACUS_APP_ID', '1f9935b84')

print("="*60)
print("Тестирование с Deployment Token")
print("="*60)
print(f"API Key: {API_KEY[:15]}...")
print(f"Deployment Token: {DEPLOYMENT_TOKEN}")
print("="*60)

try:
    client = ApiClient(API_KEY)
    print("✅ Клиент инициализирован")
    
    # Проверяем сигнатуру get_chat_response
    print("\n📋 Сигнатура get_chat_response:")
    sig = inspect.signature(client.get_chat_response)
    print(f"Параметры: {sig}")
    
    # Проверяем сигнатуру create_deployment_conversation
    print("\n📋 Сигнатура create_deployment_conversation:")
    sig2 = inspect.signature(client.create_deployment_conversation)
    print(f"Параметры: {sig2}")
    
    # Вариант 1: Попробуем get_chat_response с deployment_token
    print("\n1️⃣ Тестирование get_chat_response с deployment_token:")
    try:
        response = client.get_chat_response(
            deployment_token=DEPLOYMENT_TOKEN,
            messages=[
                {"is_user": True, "text": "Привет! Расскажи о термопанелях."}
            ]
        )
        print(f"✅ Успех! Response: {response}")
        if hasattr(response, '__dict__'):
            print(f"Response attributes: {response.__dict__}")
    except Exception as e:
        print(f"❌ Ошибка: {str(e)[:500]}")
        import traceback
        traceback.print_exc()
    
    # Вариант 2: Попробуем create_deployment_conversation
    print("\n2️⃣ Тестирование create_deployment_conversation:")
    try:
        # Сначала узнаем правильные параметры
        help_text = help(client.create_deployment_conversation)
        print(f"Help: {help_text}")
    except:
        pass
    
    try:
        conversation = client.create_deployment_conversation(
            deployment_token=DEPLOYMENT_TOKEN,
            name="Test Conversation"
        )
        print(f"✅ Conversation создан: {conversation}")
        
        # Теперь попробуем отправить сообщение
        if hasattr(conversation, 'deployment_conversation_id'):
            conv_id = conversation.deployment_conversation_id
            print(f"\nОтправка сообщения в conversation {conv_id}...")
            # Здесь нужно использовать другой метод для отправки сообщений
    except Exception as e:
        print(f"❌ Ошибка: {str(e)[:500]}")
    
    # Вариант 3: Проверим create_chat_session
    print("\n3️⃣ Тестирование create_chat_session:")
    sig3 = inspect.signature(client.create_chat_session)
    print(f"Параметры: {sig3}")
    try:
        session = client.create_chat_session(
            name="Test Session"
        )
        print(f"✅ Session создана: {session}")
    except Exception as e:
        print(f"❌ Ошибка: {str(e)[:500]}")

except Exception as e:
    print(f"❌ Критическая ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("Тестирование завершено")
print("="*60)
