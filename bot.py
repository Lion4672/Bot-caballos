import telebot
import requests
from datetime import datetime
import os

# Token del bot desde config vars (Heroku o local)
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Comando /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "⚽ ¡Hola! 🧠 Soy tu bot de predicciones deportivas. Escribe /eventos para ver los partidos activos con predicción.")

# Comando /eventos
@bot.message_handler(commands=['eventos'])
def mostrar_eventos(message):
    try:
        # API pública de fútbol (últimos eventos del Arsenal como ejemplo)
        url = "https://www.thesportsdb.com/api/v1/json/1/eventslast.php?id=133604"
        response = requests.get(url)
        data = response.json()

        if not isinstance(data, dict) or "results" not in data:
            bot.reply_to(message, "❌ Error: respuesta inesperada del servidor.")
            return

        mensaje = "⚽ *Últimos partidos del Arsenal con predicción:* \n\n"
        total = 0

        for evento in data["results"]:
            nombre = evento.get("strEvent", "Sin nombre")
            liga = evento.get("strLeague", "Sin liga")
            fecha_raw = evento.get("dateEvent", "") + " " + evento.get("strTime", "")
            prediccion = "⚖️ Empate"  # predicción falsa por ahora (ejemplo)

            try:
                fecha = datetime.strptime(fecha_raw, "%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y %H:%M')
            except:
                fecha = "Sin hora"

            mensaje += f"📅 *{fecha}* - 🏆 {liga}\n🎯 {nombre}\n🔮 Predicción: {prediccion}\n\n"
            total += 1
            if total >= 5:
                break

        if total == 0:
            bot.reply_to(message, "❌ No se encontraron eventos.")
        else:
            bot.reply_to(message, mensaje, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"❌ Error al obtener los datos: {str(e)}")

# Ejecutar el bot
bot.polling()
