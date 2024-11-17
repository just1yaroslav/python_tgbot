import logging
import json
import os

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

JSON_FILE = 'messages.json'

# Функция для сохранения сообщений в файл JSON
def save_message(text: str) -> None:
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            messages = json.load(f)
    else:
        messages = []

    messages.append(text)

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    # Создаем кнопки для клавиатуры
    keyboard = [
        [KeyboardButton("Повторяй ")],
        [KeyboardButton("Информация")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Выберите действие:",
        reply_markup=reply_markup,
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    if user_message == "Повторяй":
        context.user_data['repeat_mode'] = True  # Включаем режим повтора
        await update.message.reply_text("Принято! Теперь вводите текст для повторения. Нажмите 'Прекратить' чтобы остановить.")
        
        # Обновляем клавиатуру
        keyboard = [
            [KeyboardButton("Прекратить")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text("Введите текст для повторения:", reply_markup=reply_markup)

    elif user_message == "Информация":
        await update.message.reply_text("Это информация о боте. Он может повторять ваши сообщения или предоставлять информацию.")
    
    elif user_message == "Прекратить":
        context.user_data['repeat_mode'] = False  # Отключаем режим повтора
        await update.message.reply_text("Режим повтора отключен. Выберите действие:")
        
        # Возвращаем основную клавиатуру
        keyboard = [
            [KeyboardButton("Повторяй")],
            [KeyboardButton("Информация")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

    else:
        # Если пользователь ввел текст после нажатия "Повторяй"
        if context.user_data.get('repeat_mode'):
            await update.message.reply_text(f"Вы сказали: {user_message}")
            save_message(user_message)
        else:
            await update.message.reply_text("Пожалуйста, выберите действие с помощью кнопок.")

def main() -> None:
    application = Application.builder().token("8020671241:AAE_syEvcOG-TvD1fNF9OFL8U40DZgk_-UY").build()

    application.add_handler(CommandHandler("start", start))
    
    # Обработчик для текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()