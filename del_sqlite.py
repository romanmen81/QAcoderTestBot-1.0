# del_sqlite.py
# Удаление вопросов из базы данных

import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('questions.db')
cursor = conn.cursor()


# Функция для просмотра всех вопросов
def show_all_questions():
    cursor.execute('SELECT id, question FROM questions')
    rows = cursor.fetchall()
    if not rows:
        print("В базе данных нет вопросов.")
        return
    print("Список вопросов:")
    for row in rows:
        print(f"ID: {row[0]}, Вопрос: {row[1]}")


# Функция для удаления вопроса по ID
def delete_question_by_id(id_to_delete):
    # Проверяем, существует ли вопрос с указанным ID
    cursor.execute('SELECT COUNT(*) FROM questions WHERE id=?', (id_to_delete,))
    exists = cursor.fetchone()[0]
    if exists == 0:
        print(f"Нет вопроса с ID={id_to_delete}. Попробуйте ещё раз.")
        return False

    # Если вопрос существует, удаляем его
    cursor.execute('DELETE FROM questions WHERE id=?', (id_to_delete,))
    conn.commit()
    return True


# Основной цикл программы
show_all_questions()  # Сразу выводим список вопросов при запуске

while True:
    action = input("Введите ID вопроса для удаления или введите '0' для вывода списка вопросов: ").strip()
    if action.lower() == '0':
        show_all_questions()
    else:
        try:
            id_to_delete = int(action)
            deleted = delete_question_by_id(id_to_delete)
            if deleted:
                # Если вопрос успешно удалён, выводим обновлённый список и сообщение
                show_all_questions()
                print(f"Вопрос с ID={id_to_delete} успешно удалён.")
        except ValueError:
            print("Неверный ввод. Введите число или '0'.")

# Закрываем соединение с базой данных
conn.close()