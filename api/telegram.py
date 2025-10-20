import os
import json
import requests
from http.server import BaseHTTPRequestHandler

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')


def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(length)
        try:
            update = json.loads(body.decode('utf-8'))
            chat_id = update.get('message', {}).get('chat', {}).get('id')
            if chat_id:
                send_message(chat_id, 'Привет! Ваш бот развернут на Vercel.')
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
        return
