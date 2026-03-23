import logging
import httpx
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


async def get_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await detectar_admin(update, context):
        return

    # Definir los datos de la petición
    url = "http://127.0.0.1:8000/training/time_summary"
    parametros = {"fecha_inicio": "2026-01-01", "fecha_fin": "2026-04-01"}

    encabezados = {"accept": "application/json"}

    # Realizar la petición asíncrona
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=parametros, headers=encabezados)

        # Verificar el estado de la respuesta
        if response.status_code == 200:
            # Parsear el contenido de la respuesta como JSON
            data = response.json()
            print(data)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=data)
        else:
            print(f"Error {response.status_code}: {response.text}")


if __name__ == "__main__":
    application = ApplicationBuilder().token(TelegramBotConfig.API_KEY).build()
    start_handler = CommandHandler("start", start)
    training_handler = CommandHandler("training", get_stats)
    handlers = [start_handler, training_handler]
    application.add_handlers(handlers)
    application.run_polling()
