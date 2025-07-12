import os
import requests
from telebot import TeleBot

# Tokens desde las variables de entorno (Heroku Config Vars)
BOT_TOKEN = os.environ['BOT_TOKEN']
BETSAPI_TOKEN = os.environ['BETSAPI_TOKEN']

bot = TeleBot(BOT_TOKEN)

# Comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🐎 ¡Hola! Soy tu bot de carreras y eventos en vivo de Bet365.\nEscribe /eventos para ver los que están activos.")

# Comando /eventos
@bot.message_handler(commands=['eventos'])
def eventos_en_vivo(message):
    url = f'https://api.b365api.com/v1/bet365/inplay?token={BETSAPI_TOKEN}'

    try:
        response = requests.get(url)
        data = response.json()

        if 'results' in data and len(data['results']) > 0:
            mensaje = "🎯 Eventos en vivo:\n"
            for evento in data['results'][:5]:  # Solo muestra 5 eventos
                league = evento.get('league', {})
                home = evento.get('home', {})
                away = evento.get('away', {})

                nombre = league.get('name', 'Sin nombre')
                home_name = home.get('name', '')
                away_name = away.get('name', '')

                mensaje += f"🎰 {nombre}: {home_name} vs {away_name}\n"
        else:
            mensaje = "No hay eventos activos ahora mismo."

    except Exception as e:
        mensaje = f"❌ Error al obtener los datos: {e}"

    bot.send_message(message.chat.id, mensaje)

# Ejecutar el bot
bot.polling()