import logging
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

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

async def info_author(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Автор бота: Ваше Имя")

async def repeat_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Прекратить повторять текст", callback_data='stop')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Теперь я буду повторять ваш текст. Отправьте мне что-нибудь!", reply_markup=reply_markup)
    
    # Устанавливаем состояние повторения текста
    context.user_data['repeating'] = True

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'stop':
        context.user_data['repeating'] = False  # Останавливаем повторение текста
        await query.edit_message_text(text="Повторение текста остановлено.")
        return

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('repeating', False):
        text = update.message.text
        await update.message.reply_text(text)
        save_message(text)
    else:
        await echo(update, context)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    await update.message.reply_text(text)
    
    save_message(text)
