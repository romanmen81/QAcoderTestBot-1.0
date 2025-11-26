# add_sqlite.py
# Добавление вопросов к базе данных

import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('questions.db')
cursor = conn.cursor()

# Функция для вывода списка вопросов
def show_all_questions():
    cursor.execute('SELECT id, question FROM questions')
    rows = cursor.fetchall()
    if not rows:
        print("В базе данных нет вопросов.")
        return
    print("Список вопросов:")
    for row in rows:
        print(f"ID: {row[0]}, Вопрос: {row[1]}")

# Основной цикл добавления вопросов
while True:
    show_all_questions()  # Выводим список вопросов перед вводом нового

    print("\nВведите новый вопрос...")
    question = input("Вопрос: ")
    opt_a = input("Вариант 1: ")
    opt_b = input("Вариант 2: ")
    opt_c = input("Вариант 3: ")
    opt_d = input("Вариант 4: ")

    while True:
        try:
            correct_answer = int(input("Номер правильного ответа (1-4): "))
            if 1 <= correct_answer <= 4:
                break
            else:
                print("Ошибка: введите число от 1 до 4.")
        except ValueError:
            print("Ошибка: введите число от 1 до 4.")

    # Конвертирование правильного ответа для базы данных (0-3)
    correct_answer -= 1  # Потому что в базе храним от 0 до 3

    # Вставка данных в базу
    cursor.execute('''
        INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_answer)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (question, opt_a, opt_b, opt_c, opt_d, correct_answer))

    conn.commit()

    print("Вопрос успешно добавлен в базу данных.")

# Закрываем соединение с базой данных
conn.close()