# report_sqlite.py
# Вывод всех вопросов с ответами в консоль и сохранение их в файл report.txt

import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('questions.db')
cursor = conn.cursor()

# Запрос на получение всех вопросов и ответов
cursor.execute('SELECT id, question, option_a, option_b, option_c, option_d, correct_answer FROM questions')
rows = cursor.fetchall()

# Создаем отчет
report_lines = []
for row in rows:
    qid, question, opt_a, opt_b, opt_c, opt_d, correct_answer = row
    report_line = f"ID: {qid}, Вопрос: {question}\n"
    variants = [opt_a, opt_b, opt_c, opt_d]
    for idx, variant in enumerate(variants):
        mark = '+' if idx == correct_answer else '-'
        report_line += f"\t{mark} {variant}\n"
    report_lines.append(report_line)

# Печать отчета в консоль
for line in report_lines:
    print(line)

# Запись отчета в файл "report.txt"
output_file = 'report.txt'
with open(output_file, 'w', encoding='utf-8') as file:
    file.writelines(report_lines)

print(f'\nОтчёт успешно записан в файл "{output_file}"!')

# Закрываем соединение с базой данных
conn.close()