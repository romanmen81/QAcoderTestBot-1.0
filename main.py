# main.py
# Точка входа в приложение, регистрация хэндлеров и запуск бота. Запуск программы

from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from bot_handlers import start, handle_message, handle_answer
from config import TOKEN

# Основной цикл бота
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_answer))
    app.run_polling()

if __name__ == '__main__':
    main()