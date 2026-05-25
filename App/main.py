import asyncio
import requests
import os

from dotenv import load_dotenv
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("ODDS_API_KEY")

bot = Bot(token=TOKEN)

# Guardar IDs ya enviados
sent_games = set()

sports = [

    # NBA
    "basketball_nba",

    # Liga Peruana
    "soccer_peru_liga_1",

    # Brasileirao
    "soccer_brazil_campeonato",

    # Liga Argentina
    "soccer_argentina_primera_division",

    # MLS
    "soccer_usa_mls",

    # MLB
    "baseball_mlb",

    # Tenis ATP
    "tennis_atp_french_open",

    # Tenis WTA
    "tennis_wta_french_open"
]

async def send_games():

    print("Buscando partidos...")

    for sport in sports:

        print(f"DEPORTE: {sport}")

        url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={API_KEY}&regions=us&markets=h2h"

        response = requests.get(url)

        print("STATUS:", response.status_code)

        data = response.json()

        if not data:
            print("No hay partidos disponibles")
            continue

        for game in data[:3]:

            try:

                # ID único del partido
                game_id = game.get("id")

                # Evitar duplicados
                if game_id in sent_games:
                    print("Partido ya enviado")
                    continue

                bookmakers = game.get("bookmakers", [])

                if not bookmakers:
                    continue

                outcomes = bookmakers[0]["markets"][0]["outcomes"]

                team1 = outcomes[0]["name"]
                odd1 = outcomes[0]["price"]

                team2 = outcomes[1]["name"]
                odd2 = outcomes[1]["price"]

                message = f"""
🔥 BETBOT MULTIDEPORTE

🏆 {sport}

⚔️ {team1} vs {team2}

📊 Cuotas:
🏠 {team1} → {odd1}
✈️ {team2} → {odd2}
"""

                await bot.send_message(
                    chat_id=CHAT_ID,
                    text=message
                )

                print(message)

                # Guardar partido enviado
                sent_games.add(game_id)

            except Exception as e:

                print("ERROR:", e)

async def main():

    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        send_games,
        "interval",
        minutes=5
    )

    scheduler.start()

    print("BOT MULTIDEPORTE INICIADO")

    await send_games()

    await asyncio.Event().wait()

asyncio.run(main())