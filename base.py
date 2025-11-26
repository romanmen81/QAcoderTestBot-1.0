# base.py
# Создание базы данных из первых стандартных 10 вопросов, для примера

import sqlite3

# Подключение к базе данных (создастся новый файл, если его нет)
conn = sqlite3.connect('questions.db')
cursor = conn.cursor()

# Уничтожаем старую таблицу, если она существует
cursor.execute('DROP TABLE IF EXISTS questions')

# Создаём новую таблицу для вопросов
cursor.execute('''
    CREATE TABLE questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        correct_answer INTEGER CHECK(correct_answer BETWEEN 0 AND 3)
    );
''')

# Список вопросов
questions = [
    {
        'question': 'Что означает аббревиатура QA?',
        'answers': ['Quality Assurance', 'Quick Action', 'Quality Analysis', 'Question Answer'],
        'correct': 0
    },
    {
        'question': 'Что характеризует хороший тест-кейс?',
        'answers': ['Маленький объем', 'Четкая цель и шаги', 'Ручное выполнение', 'Дефекты в программе'],
        'correct': 1
    },
    {
        'question': 'Что такое баг в контексте тестирования?',
        'answers': ['Новая функция', 'Ошибка или дефект в системе', 'Тестовый случай', 'Скрипт автоматизации'],
        'correct': 1
    },
    {
        'question': 'Что такое регрессионное тестирование?',
        'answers': [
            'Тестирование новых функций',
            'Проверка исправлений и изменений для предотвращения новых ошибок',
            'Тестирование только интерфейса',
            'Проверка производительности'
        ],
        'correct': 1
    },
    {
        'question': 'Что такое тест-план?',
        'answers': [
            'Документ, описывающий все тестовые сценарии и планы',
            'Код автоматических тестов',
            'Всплывающее окно для тестирования',
            'Облако для хранения тестовых данных'
        ],
        'correct': 0
    },
    {
        'question': 'Что такое smoke-test (дымовое тестирование)?',
        'answers': [
            'Тестирование только интерфейса',
            'Быстрый тест для проверки основных функций системы',
            'Тест на безопасность',
            'Тестирование на нагрузку'
        ],
        'correct': 1
    },
    {
        'question': 'Что такое баг-репорт?',
        'answers': [
            'Отчет о найденных ошибках',
            'Отчет о выполненных тестах',
            'Статистика тестирования',
            'Обзор требований'
        ],
        'correct': 0
    },
    {
        'question': 'Что означает понятие "чувствительность теста"?',
        'answers': [
            'Способность теста выявлять дефекты',
            'Легкость автоматизации',
            'Быстрота выполнения',
            'Объем тестирования'
        ],
        'correct': 0
    },
    {
        'question': 'Что такое "тестовые данные"?',
        'answers': [
            'Данные, используемые для проверки системы',
            'Исходный код программы',
            'Результаты тестирования',
            'Отчёты о дефектах'
        ],
        'correct': 0
    },
    {
        'question': 'Что входит в обязанности тестировщика QA?',
        'answers': [
            'Разработка программного обеспечения',
            'Тестирование, анализ дефектов, создание тестовых сценариев',
            'Дизайн интерфейса',
            'Администрирование сервера'
        ],
        'correct': 1
    }
]

# Вставка данных в таблицу
for item in questions:
    cursor.execute('''
        INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_answer)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (item['question'], item['answers'][0], item['answers'][1], item['answers'][2], item['answers'][3], item['correct']))

# Запрашиваем вопросы из базы данных и выводим их в консоль
cursor.execute('SELECT id, question, option_a, option_b, option_c, option_d, correct_answer FROM questions')
rows = cursor.fetchall()

print("\nОбновлённая база данных:")
for row in rows:
    qid, question, opt_a, opt_b, opt_c, opt_d, correct_answer = row
    print(f"ID: {qid}, Вопрос: {question}")
    print(f"\tВарианты ответов: {opt_a}, {opt_b}, {opt_c}, {opt_d}")
    print(f"\tПравильный ответ: {correct_answer}\n")

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()