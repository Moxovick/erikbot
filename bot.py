import asyncio
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
BOT1_TOKEN = os.environ.get("BOT1_TOKEN", "")
BOT2_TOKEN = os.environ.get("BOT2_TOKEN", "")

BASE_DIR = os.path.dirname(__file__)

# --- Бот 1: David Trade (RU) ---
BOT1_PHOTO = os.path.join(BASE_DIR, "photo_2026-07-12_03-14-11.jpg")
BOT1_TEXT = (
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
BOT1_LINK = "https://t.me/m/bTPp38E_YTcx"
BOT1_BTN = "🚀 ХОЧУ БОТА"

# --- Бот 2: Erik Trade (UA) ---
BOT2_PHOTO = os.path.join(BASE_DIR, "photo_2026-07-15_18-14-16.jpg")
BOT2_TEXT = (
    "👋 <b>Вітаємо в Erik Trade!</b> 📈\n"
    "\n"
    "Ми — команда трейдерів, яка щодня працює в реальному часі "
    "та допомагає новачкам освоїти трейдинг.\n"
    "\n"
    "🎯 <b>У нашій команді ви отримаєте:</b>\n"
    "\n"
    "📺 Щоденні прямі ефіри\n"
    "📈 Торгові сесії в реальному часі\n"
    "🎓 Повне навчання від А до Я\n"
    "🧠 Закриту VIP-групу з усіма матеріалами\n"
    "📊 Готові сигнали та аналіз ринку\n"
    "💬 Особисту підтримку на кожному етапі\n"
    "👥 Спільноту однодумців\n"
    "\n"
    "🚀 Натискайте кнопку «Хочу в команду» нижче "
    "та почнемо працювати разом! 👇"
)
BOT2_LINK = "https://t.me/Ericktrade_98"
BOT2_BTN = "🚀 Хочу в команду"

# ==============================

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)


def make_handlers(photo_path, msg_text, link, btn_text):
    """Create join-request and /start handlers for a bot."""

    async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.chat_join_request.from_user
        chat_id = update.chat_join_request.chat.id

        await context.bot.approve_chat_join_request(chat_id, user.id)

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(btn_text, url=link)]
        ])

        with open(photo_path, "rb") as photo:
            await context.bot.send_photo(
                chat_id=user.id,
                photo=photo,
                caption=msg_text,
                parse_mode="HTML",
                reply_markup=keyboard,
            )

        logging.info(f"Новый участник: {user.full_name} (ID: {user.id})")

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(btn_text, url=link)]
        ])
        with open(photo_path, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=msg_text,
                parse_mode="HTML",
                reply_markup=keyboard,
            )

    return handle_join_request, start


async def main():
    apps = []

    if BOT1_TOKEN:
        app1 = Application.builder().token(BOT1_TOKEN).build()
        join1, start1 = make_handlers(BOT1_PHOTO, BOT1_TEXT, BOT1_LINK, BOT1_BTN)
        app1.add_handler(ChatJoinRequestHandler(join1))
        app1.add_handler(CommandHandler("start", start1))
        apps.append(app1)
        print("Бот 1 (David Trade) запущен.")

    if BOT2_TOKEN:
        app2 = Application.builder().token(BOT2_TOKEN).build()
        join2, start2 = make_handlers(BOT2_PHOTO, BOT2_TEXT, BOT2_LINK, BOT2_BTN)
        app2.add_handler(ChatJoinRequestHandler(join2))
        app2.add_handler(CommandHandler("start", start2))
        apps.append(app2)
        print("Бот 2 (Erik Trade) запущен.")

    if not apps:
        print("Ошибка: не указаны токены ботов (BOT1_TOKEN, BOT2_TOKEN)")
        return

    # Запускаем все боты параллельно
    for app in apps:
        await app.initialize()
        await app.start()
        await app.updater.start_polling()

    print("Все боты работают. Ctrl+C для остановки.")

    # Держим процесс живым
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        for app in apps:
            await app.updater.stop()
            await app.stop()
            await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
