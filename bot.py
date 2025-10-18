
#!/usr/bin/env python3
"""
Telegram бот с интеграцией Abacus.AI для продажи термопанелей
Production-ready версия с улучшенной обработкой ошибок и логированием
"""
import os
import sys
import logging
from typing import Dict
from datetime import datetime
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from dotenv import load_dotenv
from abacusai import ApiClient
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# Загрузка переменных окружения
load_dotenv()

# Настройка расширенного логирования
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()

# Логирование в файл и консоль
logging.basicConfig(
    format=log_format,
    level=getattr(logging, log_level, logging.INFO),
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Отключаем избыточное логирование от библиотек
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('telegram').setLevel(logging.WARNING)

# Конфигурация
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ABACUS_API_KEY = os.getenv('ABACUS_API_KEY')

# ПРАВИЛЬНЫЕ credentials для Abacus.AI
ABACUS_DEPLOYMENT_ID = os.getenv('ABACUS_DEPLOYMENT_ID', '7c388e8dc')
ABACUS_DEPLOYMENT_TOKEN = os.getenv('ABACUS_DEPLOYMENT_TOKEN', '7ee99cc13aff41c7b00d1b6d7bb45bd8')

# Health check конфигурация
HEALTH_CHECK_PORT = int(os.getenv('HEALTH_CHECK_PORT', '8080'))

# Хранилище контекста разговоров (в продакшене лучше использовать Redis или БД)
user_conversations: Dict[int, list] = {}

# Статус бота для health check
bot_status = {
    'is_running': False,
    'start_time': None,
    'last_message_time': None,
    'total_messages': 0,
    'errors_count': 0
}


class HealthCheckHandler(BaseHTTPRequestHandler):
    """HTTP обработчик для health check endpoint"""
    
    def do_GET(self):
        """Обработка GET запросов"""
        if self.path == '/health' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            uptime = None
            if bot_status['start_time']:
                uptime = (datetime.now() - bot_status['start_time']).total_seconds()
            
            response = {
                'status': 'healthy' if bot_status['is_running'] else 'starting',
                'uptime_seconds': uptime,
                'total_messages': bot_status['total_messages'],
                'errors_count': bot_status['errors_count'],
                'last_message_time': bot_status['last_message_time'].isoformat() if bot_status['last_message_time'] else None
            }
            
            import json
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Отключаем стандартное логирование HTTP сервера"""
        pass


def start_health_check_server():
    """Запуск HTTP сервера для health check в отдельном потоке"""
    try:
        server = HTTPServer(('0.0.0.0', HEALTH_CHECK_PORT), HealthCheckHandler)
        logger.info(f"🏥 Health check сервер запущен на порту {HEALTH_CHECK_PORT}")
        server.serve_forever()
    except Exception as e:
        logger.error(f"❌ Ошибка запуска health check сервера: {e}")


class AbacusAIClient:
    """Клиент для работы с Abacus.AI API через официальный SDK"""
    
    def __init__(self, api_key: str, deployment_id: str, deployment_token: str):
        self.api_key = api_key
        self.deployment_id = deployment_id
        self.deployment_token = deployment_token
        self.client = ApiClient(api_key)
        logger.info(f"Abacus.AI клиент инициализирован (Deployment ID: {deployment_id})")
    
    def send_message(self, message: str, conversation_history: list = None) -> dict:
        """
        Отправка сообщения в Abacus.AI чат-бот
        
        Args:
            message: Текст сообщения от пользователя
            conversation_history: История разговора (список сообщений)
        
        Returns:
            dict: Ответ от API с текстом ответа и обновленной историей
        """
        try:
            # Формируем историю сообщений
            messages = conversation_history if conversation_history else []
            messages.append({"is_user": True, "text": message})
            
            logger.info(f"📤 Отправка запроса в Abacus.AI: {message[:50]}...")
            logger.debug(f"История сообщений: {len(messages)} сообщений")
            
            # Вызываем API через SDK
            response = self.client.get_chat_response(
                deployment_token=self.deployment_token,
                deployment_id=self.deployment_id,
                messages=messages
            )
            
            logger.info(f"📥 Получен ответ от Abacus.AI")
            logger.debug(f"Структура ответа: {type(response)}")
            
            # Извлекаем ответ из структуры
            # Response имеет структуру: {'messages': [...], 'search_results': [...]}
            ai_response_text = None
            new_messages = messages.copy()
            
            if isinstance(response, dict):
                # Извлекаем последнее сообщение от AI
                if 'messages' in response:
                    all_messages = response['messages']
                    # Последнее сообщение должно быть от AI (is_user=False)
                    for msg in reversed(all_messages):
                        if not msg.get('is_user', True):
                            ai_response_text = msg.get('text', '')
                            logger.info(f"✅ Извлечен ответ AI: {ai_response_text[:100]}...")
                            break
                    
                    # Обновляем историю полными сообщениями
                    new_messages = all_messages
                
                # Дополнительное логирование для search_results
                if 'search_results' in response and response['search_results']:
                    logger.debug(f"🔍 Найдено {len(response['search_results'])} результатов поиска")
            
            # Если не удалось извлечь ответ, используем весь ответ как строку
            if not ai_response_text:
                logger.warning(f"⚠️ Не удалось извлечь текст ответа, использую полный ответ")
                ai_response_text = str(response)
            
            return {
                'response': ai_response_text,
                'conversation_history': new_messages,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"❌ Ошибка при обращении к Abacus.AI API: {e}")
            logger.exception("Полная трассировка ошибки:")
            return {
                'response': 'Извините, произошла ошибка при обработке запроса. Пожалуйста, попробуйте еще раз.',
                'conversation_history': conversation_history,
                'success': False
            }


# Создаем экземпляр клиента Abacus.AI
abacus_client = AbacusAIClient(ABACUS_API_KEY, ABACUS_DEPLOYMENT_ID, ABACUS_DEPLOYMENT_TOKEN)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка команды /start"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    # Сбрасываем контекст разговора
    if user_id in user_conversations:
        del user_conversations[user_id]
    
    welcome_message = (
        f"👋 Здравствуйте, {user_name}!\n\n"
        "🏠 Я AI-консультант по термопанелям.\n\n"
        "Я помогу вам:\n"
        "• Узнать о различных видах термопанелей\n"
        "• Подобрать подходящее решение для вашего дома\n"
        "• Ответить на вопросы о монтаже и характеристиках\n"
        "• Рассчитать необходимое количество материала\n\n"
        "💬 Просто напишите ваш вопрос, и я с радостью помогу!"
    )
    
    await update.message.reply_text(welcome_message)
    logger.info(f"Пользователь {user_id} ({user_name}) начал диалог")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка команды /help"""
    help_message = (
        "ℹ️ *Помощь по использованию бота*\n\n"
        "Доступные команды:\n"
        "/start - Начать диалог заново\n"
        "/help - Показать это сообщение\n"
        "/reset - Сбросить историю разговора\n\n"
        "💡 *Примеры вопросов:*\n"
        "• Какие бывают термопанели?\n"
        "• Сколько стоят термопанели для дома 100м²?\n"
        "• Как монтировать термопанели?\n"
        "• В чем преимущества термопанелей?\n\n"
        "Просто напишите ваш вопрос в чат!"
    )
    
    await update.message.reply_text(help_message, parse_mode='Markdown')


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка команды /reset - сброс контекста разговора"""
    user_id = update.effective_user.id
    
    if user_id in user_conversations:
        del user_conversations[user_id]
    
    await update.message.reply_text(
        "✅ История разговора сброшена. Можете начать новый диалог!"
    )
    logger.info(f"Пользователь {user_id} сбросил историю разговора")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка текстовых сообщений от пользователей"""
    try:
        user_id = update.effective_user.id
        user_message = update.message.text
        user_name = update.effective_user.first_name
        
        logger.info(f"💬 Получено сообщение от {user_id} ({user_name}): {user_message}")
        
        # Обновляем статистику
        bot_status['total_messages'] += 1
        bot_status['last_message_time'] = datetime.now()
        
        # Отправляем индикатор "печатает..."
        await update.message.chat.send_action(action="typing")
        
        # Получаем историю разговора для этого пользователя
        conversation_history = user_conversations.get(user_id, [])
        
        # Отправляем сообщение в Abacus.AI
        result = abacus_client.send_message(user_message, conversation_history)
        
        # Сохраняем обновленную историю разговора
        if result.get('conversation_history'):
            user_conversations[user_id] = result['conversation_history']
        
        # Отправляем ответ пользователю
        ai_response = result['response']
        
        # Разбиваем длинные сообщения (Telegram ограничивает 4096 символов)
        max_length = 4000
        if len(ai_response) > max_length:
            for i in range(0, len(ai_response), max_length):
                await update.message.reply_text(ai_response[i:i+max_length])
        else:
            await update.message.reply_text(ai_response)
        
        logger.info(f"✅ Отправлен ответ пользователю {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Ошибка обработки сообщения: {e}", exc_info=True)
        bot_status['errors_count'] += 1
        try:
            await update.message.reply_text(
                "😔 Извините, произошла ошибка при обработке вашего сообщения. "
                "Пожалуйста, попробуйте еще раз или обратитесь в поддержку."
            )
        except Exception as reply_error:
            logger.error(f"❌ Не удалось отправить сообщение об ошибке: {reply_error}")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка ошибок"""
    logger.error(f"Ошибка при обработке обновления: {context.error}", exc_info=context.error)
    bot_status['errors_count'] += 1
    
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "😔 Извините, произошла ошибка при обработке вашего сообщения. Попробуйте еще раз."
            )
        except Exception as e:
            logger.error(f"❌ Не удалось отправить сообщение об ошибке: {e}")


def main() -> None:
    """Основная функция запуска бота с автоматическим перезапуском при ошибках"""
    max_retries = 5
    retry_delay = 5  # секунды
    
    for attempt in range(max_retries):
        try:
            # Проверка наличия необходимых переменных окружения
            if not TELEGRAM_TOKEN:
                logger.error("❌ TELEGRAM_BOT_TOKEN не установлен!")
                sys.exit(1)
            
            if not ABACUS_API_KEY:
                logger.error("❌ ABACUS_API_KEY не установлен!")
                sys.exit(1)
            
            logger.info("="*60)
            logger.info("🚀 Запуск Telegram бота...")
            logger.info(f"📅 Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"🤖 Abacus.AI Deployment ID: {ABACUS_DEPLOYMENT_ID}")
            logger.info(f"🏥 Health check: http://0.0.0.0:{HEALTH_CHECK_PORT}/health")
            logger.info("="*60)
            
            # Запуск health check сервера в отдельном потоке
            health_thread = Thread(target=start_health_check_server, daemon=True)
            health_thread.start()
            
            # Обновляем статус бота
            bot_status['is_running'] = True
            bot_status['start_time'] = datetime.now()
            
            # Создание приложения
            application = Application.builder().token(TELEGRAM_TOKEN).build()
            
            # Регистрация обработчиков команд
            application.add_handler(CommandHandler("start", start_command))
            application.add_handler(CommandHandler("help", help_command))
            application.add_handler(CommandHandler("reset", reset_command))
            
            # Регистрация обработчика текстовых сообщений
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
            
            # Регистрация обработчика ошибок
            application.add_error_handler(error_handler)
            
            # Запуск бота
            logger.info("✅ Бот успешно запущен и готов к работе!")
            application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True,
                close_loop=False
            )
            
            # Если дошли сюда, значит бот остановлен нормально
            break
            
        except KeyboardInterrupt:
            logger.info("⚠️ Получен сигнал остановки (Ctrl+C)")
            bot_status['is_running'] = False
            sys.exit(0)
            
        except Exception as e:
            logger.error(f"❌ Критическая ошибка бота: {e}", exc_info=True)
            bot_status['errors_count'] += 1
            
            if attempt < max_retries - 1:
                logger.info(f"🔄 Перезапуск через {retry_delay} секунд... (попытка {attempt + 2}/{max_retries})")
                time.sleep(retry_delay)
                retry_delay *= 2  # Экспоненциальная задержка
            else:
                logger.error(f"❌ Превышено количество попыток перезапуска ({max_retries})")
                bot_status['is_running'] = False
                sys.exit(1)


if __name__ == '__main__':
    main()
