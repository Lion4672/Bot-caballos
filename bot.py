import os
import requests
from telebot import TeleBot

# 🧪 Tokens desde las variables de entorno (Config Vars en Heroku)
BOT_TOKEN = os.environ['BOT_TOKEN']
BETSAPI_TOKEN = os.environ['BETSAPI_TOKEN']

bot = TeleBot(BOT_TOKEN)

# 🧠 Comando /start para iniciar
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🐎 ¡Hola! Soy tu bot de carreras y eventos en vivo de Bet365.\nEscribe /eventos para ver los que están activos.")

# 📡 Comando /eventos para ver eventos en vivo
@bot.message_handler(commands=['eventos'])
def eventos_en_vivo(message):
    url = f'https://api.b365api.com/v1/bet365/inplay?token={BETSAPI_TOKEN}'

    try:
        response = requests.get(url)
        data = response.json()

        if 'results' in data and len(data['results']) > 0:
            mensaje = "🎯 Eventos en vivo:\n"
            for evento in data['results'][:5]:  # Limita a 5 eventos
league = evento.get('league')
home = evento.get('home')
away = evento.get('away')

nombre = league['name'] if isinstance(league, dict) and 'name' in league else 'Sin nombre'
home_name = home['name'] if isinstance(home, dict) and 'name' in home else ''
away_name = away['name'] if isinstance(away, dict) and 'name' in away else ''

teams = f"{home_name} vs {away_name}"
mensaje += f"🎰 {nombre}: {teams}\n"
        else:
            mensaje = "No hay eventos activos ahora mismo."

    except Exception as e:
        mensaje = f"❌ Error al obtener los datos: {e}"

    bot.send_message(message.chat.id, mensaje)

# 🚀 Inicia el bot
bot.polling()
