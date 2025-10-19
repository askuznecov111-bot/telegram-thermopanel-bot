import os
import sys
import json
import asyncio
from http.server import BaseHTTPRequestHandler

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Add project root to sys.path so we can import bot module
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Build Telegram application using the existing token
application = Application.builder().token(bot.TELEGRAM_TOKEN).build()


# Register handlers from bot
application.add_handler(CommandHandler("start", bot.start_command))
application.add_handler(CommandHandler("help", bot.help_command))
application.add_handler(CommandHandler("reset", bot.reset_command))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), bot.handle_message))
application.add_error_handler(bot.error_handler)

# Initialize the application
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
            self.wfile.write(b'{"ok":true}')
        except Exception:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'{"ok":false}')

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

    def log_message(self, *args):
        # Disable default logging to stdout
        return
