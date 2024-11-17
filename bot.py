import logging
from telegram import Update
from telegram.ext import CallbackQueryHandler, Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TOKEN
from handlers import start, handle_message

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def handle_inline_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Подтверждаем нажатие кнопки

    if query.data == 'inline_1':
        await query.edit_message_text(text="Нажатие на кнопка 1")
    elif query.data == 'inline_2':
        await query.edit_message_text(text="Нажатие на кнопка 2")

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    
    # Обработчик для текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Добавляем обработчик для inline-кнопок
    application.add_handler(CallbackQueryHandler(handle_inline_button))

    application.run_polling(allowed_updates=None)

if __name__ == "__main__":
    main()