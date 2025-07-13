import telebot
import requests
from datetime import datetime
import os

# Obtener el token del entorno
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Comando /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🐎 ¡Hola! 🏁 Soy tu bot de apuestas. Usa /eventos para ver predicciones en vivo de Bet365. ✅")

# Comando /eventos
@bot.message_handler(commands=['eventos'])
def mostrar_eventos(message):
    try:
        url = "https://api.b365api.com/v1/bet365/inplay?token=225739-82FzmJVirx8lAk"
        response = requests.get(url)
        data = response.json()

        if not isinstance(data, dict):
            bot.reply_to(message, "❌ Error: respuesta inesperada del servidor.")
            return

        if data.get("success") != 1:
            bot.reply_to(message, "❌ No se pudieron obtener los eventos (API falló).")
            return

        mensaje = "🏆 *Top 10 Eventos con Predicción (Bet365)*:\n\n"
        total_eventos = 0

        for evento in data.get("results", []):
            if isinstance(evento, dict):
                nombre = evento.get("NA", "Sin nombre")
                liga = evento.get("L3", "Sin liga")
                fecha_raw = evento.get("TU", "")
                odds = evento.get("O1")  # Normalmente aquí vendrían las cuotas

                # Convertir timestamp
                try:
                    fecha = datetime.utcfromtimestamp(int(fecha_raw)).strftime('%d-%m-%Y %H:%M')
                except:
                    fecha = "Sin hora"

                # Predicción real si hay cuotas
                cuotas = evento.get("OD", {})  # Intentar obtener cuotas reales
                prediccion = "No disponible"
                if isinstance(cuotas, dict):
                    casa = cuotas.get("1", 0)
                    empate = cuotas.get("X", 0)
                    visita = cuotas.get("2", 0)
                    if casa and visita:
                        if casa < visita and casa < empate:
                            prediccion = "Gana el local"
                        elif visita < casa and visita < empate:
                            prediccion = "Gana el visitante"
                        elif empate < casa and empate < visita:
                            prediccion = "Empate"
                        else:
                            prediccion = "Muy igualado"
                    else:
                        prediccion = "Cuotas incompletas"

                mensaje += f"📅 *{fecha}* - 🏆 _{liga}_\n🎯 *{nombre}*\n🔮 Predicción: {prediccion}\n\n"
                total_eventos += 1

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
