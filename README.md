import os
import sys
import json
import asyncio
from http.server import BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Добавляем корень проекта в sys.path, чтобы импортировать bot.py
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import bot

# Создаём Telegram-приложение с использованием существующего токена
application = Application.builder().token(bot.TELEGRAM_TOKEN).build()

# Регистрируем обработчики из bot.py
application.add_handler(CommandHandler("start", bot.start_command))
application.add_handler(CommandHandler("help", bot.help_command))
application.add_handler(CommandHandler("reset", bot.reset_command))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), bot.handle_message))
application.add_error_handler(bot.error_handler)

# Инициализируем приложение (для python-telegram-bot v20)
asyncio.run(application.initialize())

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body.decode('utf-8'))
            update = Update.de_json(data, application.bot)
            asyncio.run(application.process_update(update))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"ok": true}')
        except Exception:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'{"ok": false}')

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

    def log_message(self, *args):
        # Отключаем стандартный вывод логов
        return
