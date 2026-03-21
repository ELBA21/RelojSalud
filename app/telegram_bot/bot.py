import logging, httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from app.config import TelegramBotConfig

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def detectar_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    if user != int(TelegramBotConfig.USER_ID):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Usuario no admitido"
        )
        return False
    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Obtener tu ID para que lo copies y lo pegues en tu .env si quieres
    if not await detectar_admin(update, context):
        return

    mensaje = (
        "🤖 **Bot de RelojSalud Activo**\n\n"
        "**Comandos disponibles:**\n"
        "/training - Ver entrenamientos de la semana\n"
        "/stats - Ver estadísticas rápidas"
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=mensaje, parse_mode="Markdown"
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(TelegramBotConfig.API_KEY).build()
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    application.run_polling()
