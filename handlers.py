import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils import save_message

# Настройка логирования
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    keyboard = [
        [KeyboardButton("Повторяй 🐒")],
        [KeyboardButton("Информация 👽")],
        [KeyboardButton("Клавиатура 🎹")]  # Новая кнопка
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Выберите действие:",
        reply_markup=reply_markup,
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    if user_message == "Повторяй 🐒":
        context.user_data['repeat_mode'] = True
        await update.message.reply_text("Принято! Вы можете ввести ниже любой текст и я повторю за вами, или нажмите/напишите 'Прекратить' чтобы остановить.")
        
        keyboard = [[KeyboardButton("Прекратить 💔")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text("Введите текст для повторения:", reply_markup=reply_markup)

    elif user_message == "Информация 👽":
        await update.message.reply_text("Это тестовый бот от https://t.me/helloyaroslav")

    elif user_message == "Клавиатура 🎹":
        await update.message.reply_text("Нажмите кнопку ниже, чтобы показать клавиатуру:", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Показать клавиатуру")]], resize_keyboard=True))

    elif user_message == "Показать клавиатуру":
        keyboard = [
            [KeyboardButton("Кнопка 1")],
            [KeyboardButton("Кнопка 2")],
            [KeyboardButton("Назад 🔙")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        # Создание inline-клавиатуры
        inline_keyboard = [
            [InlineKeyboardButton("Inline Кнопка 1", callback_data='inline_1')],
            [InlineKeyboardButton("Inline Кнопка 2", callback_data='inline_2')]
        ]
        inline_reply_markup = InlineKeyboardMarkup(inline_keyboard)

        await update.message.reply_text("Онлайн клавиатура:", reply_markup=reply_markup)
        await update.message.reply_text("Второй тип клавиатуры", reply_markup=inline_reply_markup)

    elif user_message == "Прекратить":
        context.user_data['repeat_mode'] = False
        await update.message.reply_text("🔱 Режим повтора отключен. Выберите действие:")
        
        keyboard = [
            [KeyboardButton("Повторяй 🐒")],
            [KeyboardButton("Информация 👽")],
            [KeyboardButton("Клавиатура 🎹")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

    elif user_message == "Кнопка 1":
        await update.message.reply_text("Вы нажали Кнопка 1!")

    elif user_message == "Кнопка 2":
        await update.message.reply_text("Вы нажали Кнопка 2!")

    elif user_message == "Назад 🔙":
        keyboard = [
            [KeyboardButton("Повторяй 🐒")],
            [KeyboardButton("Информация 👽")],
            [KeyboardButton("Клавиатура 🎹")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

    else:
        if context.user_data.get('repeat_mode'):
            await update.message.reply_text(f"Принято. {user_message}")
            save_message(user_message)
        else:
            await update.message.reply_text("Выберите действие с имеющихся кнопок помощью кнопок.")
