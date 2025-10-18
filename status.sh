
#!/bin/bash

# Скрипт для проверки статуса бота

echo "📊 Проверка статуса Telegram бота..."
echo ""

# Проверка процесса
PID=$(pgrep -f "python.*bot.py")

if [ -z "$PID" ]; then
    echo "❌ Бот не запущен"
else
    echo "✅ Бот запущен (PID: $PID)"
    echo ""
    echo "📈 Использование ресурсов:"
    ps aux | grep $PID | grep -v grep
    echo ""
fi

# Проверка последних логов
if [ -f "bot.log" ]; then
    echo "📝 Последние 10 строк из лога:"
    echo "================================"
    tail -n 10 bot.log
fi
