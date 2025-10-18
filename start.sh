
#!/bin/bash

# Скрипт для запуска Telegram бота

echo "🚀 Запуск Telegram бота для термопанелей..."

# Переход в директорию проекта
cd "$(dirname "$0")"

# Проверка наличия виртуального окружения
if [ ! -d "venv" ]; then
    echo "❌ Виртуальное окружение не найдено!"
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
    echo "✅ Виртуальное окружение создано"
fi

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Проверка и установка зависимостей
if [ ! -f "venv/lib/python*/site-packages/telegram/__init__.py" ]; then
    echo "📦 Установка зависимостей..."
    pip install -r requirements.txt
    echo "✅ Зависимости установлены"
fi

# Проверка наличия .env файла
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден!"
    echo "📝 Создайте файл .env на основе .env.example"
    exit 1
fi

# Проверка API ключа
if grep -q "your_api_key_here" .env; then
    echo "⚠️  ВНИМАНИЕ: В файле .env не установлен API ключ Abacus.AI!"
    echo "📝 Пожалуйста, замените 'your_api_key_here' на ваш реальный API ключ"
    read -p "Продолжить запуск? (y/n): " choice
    if [ "$choice" != "y" ]; then
        exit 1
    fi
fi

# Запуск бота
echo "✅ Запуск бота..."
python bot.py
