
# 🤖 Telegram Бот для термопанелей с интеграцией Abacus.AI

Этот проект представляет собой Telegram бота, интегрированного с AI чат-ботом на платформе Abacus.AI. Бот предоставляет консультации по термопанелям, отвечает на вопросы клиентов и помогает с выбором продукции.

## 📋 Возможности

- ✅ Интеграция с Telegram Bot API через polling
- ✅ Подключение к Abacus.AI для AI-ответов
- ✅ Поддержка контекста разговора для каждого пользователя
- ✅ Обработка команд `/start`, `/help`, `/reset`
- ✅ Обработка ошибок и таймаутов
- ✅ Логирование всех действий
- ✅ Разделение длинных сообщений (Telegram ограничение 4096 символов)

## 🛠 Требования

- Python 3.8 или выше
- Telegram Bot Token
- Abacus.AI API Key
- Интернет-соединение

## 📦 Установка

### 1. Клонирование и переход в директорию

```bash
cd ~/telegram_thermopanel_bot
```

### 2. Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте файл `.env` и добавьте ваши данные:

```env
TELEGRAM_BOT_TOKEN=8063298485:AAHWZ0o3YhtoD_e0vtteXL8x_oqYsjXkYl8
ABACUS_API_KEY=ваш_api_ключ_abacus
ABACUS_APP_ID=1f9935b84
```

**Как получить Abacus.AI API Key:**
1. Войдите на https://abacus.ai
2. Перейдите в настройки профиля (Settings)
3. Найдите раздел API Keys
4. Создайте новый ключ или скопируйте существующий

## 🚀 Запуск бота

### Обычный запуск (для тестирования)

```bash
python bot.py
```

### Запуск в фоновом режиме с помощью nohup

```bash
nohup python bot.py > bot.log 2>&1 &
```

### Запуск в фоновом режиме с помощью screen

```bash
# Создать новую screen сессию
screen -S telegram_bot

# Запустить бота
python bot.py

# Отсоединиться от screen: Ctrl+A, затем D

# Вернуться к боту
screen -r telegram_bot
```

### Запуск как systemd сервис (рекомендуется для продакшена)

Создайте файл `/etc/systemd/system/telegram-bot.service`:

```ini
[Unit]
Description=Telegram Thermopanel Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/telegram_thermopanel_bot
Environment="PATH=/home/ubuntu/telegram_thermopanel_bot/venv/bin"
ExecStart=/home/ubuntu/telegram_thermopanel_bot/venv/bin/python /home/ubuntu/telegram_thermopanel_bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Затем:

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot.service
sudo systemctl start telegram-bot.service
sudo systemctl status telegram-bot.service
```

## 📊 Проверка статуса

### Просмотр логов (nohup)

```bash
tail -f bot.log
```

### Просмотр логов (systemd)

```bash
sudo journalctl -u telegram-bot.service -f
```

### Остановка бота

```bash
# Если запущен через nohup
pkill -f "python bot.py"

# Если запущен через systemd
sudo systemctl stop telegram-bot.service
```

## 💬 Использование бота

После запуска, найдите вашего бота в Telegram и начните диалог:

1. **Команда `/start`** - Начать диалог с ботом
2. **Команда `/help`** - Получить справку
3. **Команда `/reset`** - Сбросить историю разговора

Просто отправьте текстовое сообщение с вопросом, и бот ответит, используя AI от Abacus.AI.

### Примеры вопросов:

- "Какие бывают термопанели?"
- "Сколько стоят термопанели для дома 100м²?"
- "Как монтировать термопанели?"
- "В чем преимущества термопанелей перед другими материалами?"

## 🏗 Архитектура

```
telegram_thermopanel_bot/
├── bot.py                 # Основной скрипт бота
├── .env                   # Конфигурация (не включен в git)
├── .env.example           # Пример конфигурации
├── requirements.txt       # Зависимости Python
├── .gitignore            # Игнорируемые файлы для git
└── README.md             # Документация
```

### Основные компоненты:

1. **AbacusAIClient** - Класс для взаимодействия с Abacus.AI API
2. **Command Handlers** - Обработчики команд `/start`, `/help`, `/reset`
3. **Message Handler** - Обработчик текстовых сообщений
4. **Error Handler** - Централизованная обработка ошибок
5. **User Conversations** - Хранилище контекста разговоров

## 🔧 Конфигурация

### Переменные окружения:

- `TELEGRAM_BOT_TOKEN` - Токен Telegram бота
- `ABACUS_API_KEY` - API ключ Abacus.AI
- `ABACUS_APP_ID` - ID приложения в Abacus.AI (по умолчанию: 1f9935b84)

### API Endpoints:

- Abacus.AI Chat API: `https://api.abacus.ai/v0/chatLlm`

## 🐛 Отладка

### Проблемы с подключением к Telegram

```bash
# Проверить доступность Telegram API
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

### Проблемы с Abacus.AI API

Проверьте логи бота на наличие ошибок API. Убедитесь, что:
- API ключ правильный и активный
- App ID соответствует вашему чат-боту
- У вас есть доступ к API

### Общие проблемы

1. **Бот не отвечает**: Проверьте, что процесс запущен
2. **Ошибки API**: Проверьте правильность ключей в `.env`
3. **Таймауты**: Увеличьте timeout в `AbacusAIClient.send_message()`

## 📝 Логирование

Бот логирует все важные события:
- Запуск и остановка бота
- Получение и отправка сообщений
- Ошибки API и исключения
- Действия пользователей

Уровень логирования: `INFO`

## 🔒 Безопасность

- ⚠️ **Никогда не коммитьте файл `.env` в git**
- 🔐 Храните API ключи в безопасности
- 🛡️ Используйте HTTPS для API запросов
- 🔄 Регулярно обновляйте зависимости

## 📈 Масштабирование

Для продакшена рекомендуется:

1. **База данных** - Redis или PostgreSQL для хранения контекста
2. **Webhook** - Использовать webhook вместо polling для лучшей производительности
3. **Мониторинг** - Добавить мониторинг и алерты (Sentry, Prometheus)
4. **Load Balancer** - При большой нагрузке
5. **Docker** - Контейнеризация для простого деплоя

## 🆘 Поддержка

При возникновении проблем:
1. Проверьте логи бота
2. Убедитесь, что все зависимости установлены
3. Проверьте правильность конфигурации в `.env`

## 📄 Лицензия

Этот проект создан для интеграции с Abacus.AI.

---

**Создано с ❤️ для продажи термопанелей**
