
import os
from telegram.ext import ApplicationBuilder, CommandHandler

BOT_TOKEN = os.environ["BOT_TOKEN"]

app = ApplicationBuilder().token(BOT_TOKEN).build()

async def start(update, context):
    await update.message.reply_text("¡Hola! Soy tu bot de carreras de caballos 🐎")

app.add_handler(CommandHandler("start", start))
app.run_polling()
