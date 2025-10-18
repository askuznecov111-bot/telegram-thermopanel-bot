
#!/bin/bash

# Скрипт для остановки бота

echo "🛑 Остановка Telegram бота..."

# Поиск процесса бота
PID=$(pgrep -f "python.*bot.py")

if [ -z "$PID" ]; then
    echo "ℹ️  Бот не запущен"
    exit 0
fi

# Остановка процесса
kill $PID

echo "✅ Бот остановлен (PID: $PID)"
