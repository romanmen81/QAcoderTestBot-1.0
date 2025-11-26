# bot_handlers.py
# Вспомогательные функции для обработки сообщений и команд

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from config import user_sessions
from db_utils import connect_db, fetch_random_question

# Максимальная глубина вопросов
MAX_QUESTIONS = 10

# Основная функция старта
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Основное меню с кнопками
    keyboard = [
        ['Старт'],
        ['Об викторине']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Добро пожаловать в мир Тестов QA!\n"
        "Для запуска теста, нажмите: 'Старт'",
        reply_markup=reply_markup
    )

# Функционал для обработки сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.effective_chat.id

    if text == 'Об викторине':
        await update.message.reply_text(
            "Это викторина по различным вопросам.\n"
            "Выберите 'Старт' для начала теста."
        )
    elif text == 'Старт':
        # Инициализация сессии пользователя
        user_sessions[chat_id] = {
            'score': 0,
            'current_question': None,
            'used_questions': [],  # Список уже использованных вопросов
            'num_questions': 0  # Новое поле для счёта вопросов
        }
        # Начинаем викторину
        await send_question(update, context, chat_id)
    elif chat_id in user_sessions:
        await update.message.reply_text("Пожалуйста, выберите вариант ответа.")
    else:
        await update.message.reply_text("Пожалуйста, сначала выберите 'Об викторине' или 'Старт'.")

# Отправка вопроса пользователю
async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id):
    # Проверяем, не достигли ли мы максимума вопросов
    if user_sessions[chat_id].get('num_questions', 0) >= MAX_QUESTIONS:
        score = user_sessions[chat_id]['score']
        await context.bot.send_message(chat_id=chat_id, text=f"Тестирование завершено, вы верно ответили на {score} вопросов из {MAX_QUESTIONS}.")
        del user_sessions[chat_id]  # Завершаем сессию
        return

    cursor, conn = connect_db()

    # Получаем список вопросов, исключая уже использованные
    used_ids = tuple(user_sessions[chat_id]['used_questions'])
    sql_query = '''
        SELECT *
        FROM questions
        WHERE id NOT IN ({})
        ORDER BY RANDOM()
        LIMIT 1
    '''.format(','.join(map(str, used_ids))) if used_ids else '''
        SELECT *
        FROM questions
        ORDER BY RANDOM()
        LIMIT 1
    '''

    cursor.execute(sql_query)

    question_row = cursor.fetchone()
    if question_row is None:
        await context.bot.send_message(chat_id=chat_id, text="Вопросы исчерпаны!")
        return

    _, question, opt_a, opt_b, opt_c, opt_d, correct_answer = question_row

    # Формируем полный текст вопроса с вариантами ответов
    full_question = f'{question}\n\nВарианты ответов:\n1. {opt_a}\n2. {opt_b}\n3. {opt_c}\n4. {opt_d}'

    # Формируем клавиатуру с полными вариантами ответов
    keyboard = [
        [InlineKeyboardButton(opt_a, callback_data="0")],  # только индекс варианта
        [InlineKeyboardButton(opt_b, callback_data="1")],
        [InlineKeyboardButton(opt_c, callback_data="2")],
        [InlineKeyboardButton(opt_d, callback_data="3")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем вопрос пользователю
    await context.bot.send_message(chat_id=chat_id, text=full_question, reply_markup=reply_markup)

    # Запоминаем текущий вопрос
    user_sessions[chat_id]['current_question'] = question_row

    # Добавляем ID вопроса в список использованных
    user_sessions[chat_id]['used_questions'].append(question_row[0])

    # Увеличиваем счётчик вопросов
    user_sessions[chat_id]['num_questions'] = user_sessions[chat_id].get('num_questions', 0) + 1

# Обрабатываем ответ пользователя
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id
    message_id = query.message.message_id

    if chat_id not in user_sessions:
        await context.bot.send_message(chat_id=chat_id, text="Пожалуйста, начните тест командой /start.")
        return

    current_question = user_sessions[chat_id].get('current_question')
    if not current_question:
        await context.bot.send_message(chat_id=chat_id, text="Ошибка: нет активного вопроса.")
        return

    # Разбираем ответ пользователя
    index = int(query.data)  # берём только индекс

    # Определяем правильность ответа
    _, _, opt_a, opt_b, opt_c, opt_d, correct_answer = current_question
    if index == correct_answer:
        user_sessions[chat_id]['score'] += 1
        reply_text = 'Правильно!'
    else:
        right_answer = [opt_a, opt_b, opt_c, opt_d][correct_answer]
        reply_text = f'Ошибочка! Правильный ответ: {right_answer}.'

    # Удаляем активные кнопки и отправляем результат
    await context.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)
    await context.bot.send_message(chat_id=chat_id, text=reply_text)

    # Продолжаем викторину
    await send_question(update, context, chat_id)