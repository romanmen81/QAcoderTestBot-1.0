# config.py
# Конфигурационные данные (токен бота, путь к базе данных)

from dotenv import load_dotenv
from os import environ

# Загрузка токена из переменных окружения
load_dotenv()
TOKEN = environ.get('TELEGRAM_BOT_TOKEN')

# Словарь для хранения данных пользователей
user_sessions = {}