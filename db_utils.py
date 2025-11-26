# db_utils
# Содержит функции для работы с базой данных (подключение, получение вопросов)

import sqlite3

# Функция подключения к базе данных
def connect_db():
    conn = sqlite3.connect('questions.db')
    return conn.cursor(), conn

# Функция для получения случайного вопроса из базы данных
def fetch_random_question(cursor):
    cursor.execute('SELECT * FROM questions ORDER BY RANDOM() LIMIT 1')
    return cursor.fetchone()