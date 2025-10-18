
# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота
COPY bot.py .

# Создаем директорию для логов
RUN mkdir -p /app/logs

# Открываем порт для health check
EXPOSE 8080

# Устанавливаем переменную окружения для Python (unbuffered output)
ENV PYTHONUNBUFFERED=1

# Запускаем бот
CMD ["python", "bot.py"]
