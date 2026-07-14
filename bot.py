import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ChatJoinRequestHandler,
    ContextTypes,
)

# ==============================
#  НАСТРОЙКИ
# ==============================
BOT_TOKEN = "8408970367:AAEmn9-g833b_r4mjIvRTBlLBHLSpY946t8"

# Путь к фото (должно лежать рядом с bot.py)
PHOTO_PATH = os.path.join(os.path.dirname(__file__), "photo_2026-07-12_03-14-11.jpg")

# Текст сообщения (HTML-форматирование)
MSG_TEXT = (
    "👋 <b>Добро пожаловать в David Trade!</b> 🤖📈\n"
    "\n"
    "Спасибо за подписку! Добро пожаловать в наше сообщество.\n"
    "\n"
    "🔥 <b>Что вы получите:</b>\n"
    "\n"
    "🤖 AI-бот с торговыми сигналами\n"
    "📊 Ежедневные торговые сессии\n"
    "🎥 Прямые эфиры с разбором рынка\n"
    "📚 Бесплатное обучение с нуля\n"
    "📈 Готовые сигналы и аналитику\n"
    "💬 Закрытый чат с командой\n"
    "👨‍🏫 Личную поддержку и помощь\n"
    "🚀 Полезные материалы для новичков и опытных трейдеров\n"
    "\n"
    "Нажмите кнопку «ХОЧУ БОТА» 👇\n"
    "И получите доступ к AI-боту и нашей команде."
)

# Ссылка на приватную группу — ЗАМЕНИ НА СВОЮ
GROUP_INVITE_LINK = "https://t.me/David_Space11"
# ==============================

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)


async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    chat_id = update.chat_join_request.chat.id

    # Одобряем заявку
    await context.bot.approve_chat_join_request(chat_id, user.id)

    # Кнопка
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 ХОЧУ БОТА", url=GROUP_INVITE_LINK)]
    ])

    # Отправляем фото + текст
    with open(PHOTO_PATH, "rb") as photo:
        await context.bot.send_photo(
            chat_id=user.id,
            photo=photo,
            caption=MSG_TEXT,
            parse_mode="HTML",
            reply_markup=keyboard,
        )

    logging.info(f"Новый участник: {user.full_name} (ID: {user.id})")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 ХОЧУ БОТА", url=GROUP_INVITE_LINK)]
    ])
    with open(PHOTO_PATH, "rb") as photo:
        await update.message.reply_photo(
            photo=photo,
            caption=MSG_TEXT,
            parse_mode="HTML",
            reply_markup=keyboard,
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    app.add_handler(CommandHandler("start", start))
    print("Бот запущен. Нажми Ctrl+C для остановки.")
    app.run_polling()


if __name__ == "__main__":
    main()
