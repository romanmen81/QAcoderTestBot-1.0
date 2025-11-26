# optim_sqlite.py
# ВНИМАНИЕ!!! Данный модуль работает не корректно.
# СДЕЛАЙТЕ КОПИЮ БАЗЫ ДАННЫХ
# Оптимизация базы данных

import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('questions.db')
cursor = conn.cursor()

# Проверяем, существует ли таблица, если нет — создаём её
cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        correct_answer INTEGER CHECK(correct_answer BETWEEN 0 AND 3)
    );
''')

# Создаем временную таблицу с последовательными номерами
cursor.execute('''
    CREATE TEMPORARY TABLE temp_questions AS
    SELECT ROW_NUMBER() OVER () AS id, question, option_a, option_b, option_c, option_d, correct_answer
    FROM questions
    ORDER BY id ASC
''')

# Проверяем временные данные
cursor.execute('SELECT COUNT(*) FROM temp_questions')
count_temp = cursor.fetchone()[0]

# Удаляем старую таблицу
cursor.execute('DROP TABLE questions')

# Переименовываем временную таблицу обратно в оригинальную
cursor.execute('ALTER TABLE temp_questions RENAME TO questions')

# Проверяем результат
cursor.execute('SELECT COUNT(*) FROM questions')
count_new = cursor.fetchone()[0]

if count_temp == count_new:
    print("База данных успешно реорганизована, ID теперь идут подряд.")
else:
    print("Ошибка при реорганизации базы данных.")

# Выводим обновлённую базу данных в консоль
cursor.execute('SELECT id, question, option_a, option_b, option_c, option_d, correct_answer FROM questions')
rows = cursor.fetchall()

print("\nОбновлённая база данных:")
for row in rows:
    qid, question, opt_a, opt_b, opt_c, opt_d, correct_answer = row
    print(f"ID: {qid}, Вопрос: {question}")
    print(f"\tВарианты ответов: {opt_a}, {opt_b}, {opt_c}, {opt_d}")
    print(f"\tПравильный ответ: {correct_answer}\n")

# Закрываем соединение с базой данных
conn.commit()
conn.close()