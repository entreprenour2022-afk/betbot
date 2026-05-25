import requests
import os
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("ODDS_API_KEY")

bot = Bot(token=TOKEN)

url = f"https://api.the-odds-api.com/v4/sports/soccer_epl/odds/?apiKey={API_KEY}&regions=eu&markets=h2h"

response = requests.get(url)
data = response.json()

for game in data[:3]:
    home = game["home_team"]
    away = game["away_team"]

    message = f"⚽ {home} vs {away}"

    bot.send_message(chat_id=CHAT_ID, text=message)

print("Mensajes enviados")
