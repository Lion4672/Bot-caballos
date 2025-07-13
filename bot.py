import telebot
import requests
from datetime import datetime
import os

# Obtener el token del entorno (Heroku config var)
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Comando /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🐎 ¡Hola! 🏁 Soy tu bot de apuestas. Usa /eventos para ver los eventos en vivo. ✅")

# Comando /eventos
@bot.message_handler(commands=['eventos'])
def mostrar_eventos(message):
    try:
        # Llamada a la API de Bet365 (reemplaza con tu token si cambia)
        url = "https://api.b365api.com/v1/bet365/inplay?token=225739-82FzmJYirxBlAk"
        response = requests.get(url)
        data = response.json()

        # Validar que la respuesta sea un diccionario
        if not isinstance(data, dict):
            bot.reply_to(message, "❌ Error: respuesta inesperada del servidor.")
            return

        if data.get("success") != 1:
            bot.reply_to(message, "❌ No se pudieron obtener los eventos (API falló).")
            return

        mensaje = "🏆 *Top 10 Eventos en Vivo (Bet365)*:\n\n"
        total_eventos = 0

        for grupo in data["results"]:
            for evento in grupo:
                if isinstance(evento, dict):
                    nombre = evento.get("NA", "Sin nombre")
                    liga = evento.get("L3", "Sin liga")
                    fecha_raw = evento.get("TU", "")

                    # Convertir timestamp (si es válido)
                    try:
                        fecha = datetime.utcfromtimestamp(int(fecha_raw)).strftime('%d-%m-%Y %H:%M')
                    except:
                        fecha = "Sin hora"

                    mensaje += f"📅 *{fecha}* - 🏆 _{liga}_\n🎯 *{nombre}*\n\n"
                    total_eventos += 1

                    if total_eventos >= 10:
                        break
            if total_eventos >= 10:
                break

        if total_eventos == 0:
            bot.reply_to(message, "❌ No se encontraron eventos en este momento.")
        else:
            bot.reply_to(message, mensaje, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"❌ Error al obtener los datos: {str(e)}")

# Ejecutar el bot
bot.polling()
