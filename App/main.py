import asyncio
import requests
import os

from dotenv import load_dotenv
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from predictor import predict_probability

# =========================
# VARIABLES .ENV
# =========================

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("ODDS_API_KEY")

bot = Bot(token=TOKEN)

# =========================
# ARCHIVO ANTI DUPLICADOS
# =========================

SENT_FILE = "App/sent_games.txt"

if not os.path.exists(SENT_FILE):

    with open(SENT_FILE, "w") as f:
        pass

with open(SENT_FILE, "r") as f:

    sent_games = set(
        line.strip() for line in f
    )

# =========================
# DEPORTES
# =========================

sports = [

    "basketball_nba",

    "soccer_peru_liga_1",

    "soccer_brazil_campeonato",

    "soccer_argentina_primera_division",

    "soccer_usa_mls",

    "baseball_mlb"
]

# =========================
# RATINGS BASE
# =========================

def get_team_rating(team, sport):

    ratings = {

        # NBA
        "Boston Celtics": 0.10,
        "Denver Nuggets": 0.09,
        "Los Angeles Lakers": 0.08,
        "Golden State Warriors": 0.07,

        # Soccer
        "Palmeiras": 0.09,
        "Flamengo": 0.08,
        "River Plate": 0.08,
        "Universitario": 0.06,
        "Alianza Lima": 0.05,

        # MLB
        "New York Yankees": 0.09,
        "Los Angeles Dodgers": 0.10,
        "Houston Astros": 0.08
    }

    return ratings.get(team, 0.05)

# =========================
# HEARTBEAT
# =========================

async def heartbeat():

    try:

        await bot.send_message(

            chat_id=CHAT_ID,
            text="✅ BOT ONLINE"
        )

        print("HEARTBEAT OK")

    except Exception as e:

        print("ERROR HEARTBEAT:", e)

# =========================
# ESCANEO
# =========================

async def scan_games():

    print("ESCANEO EJECUTADO")

    for sport in sports:

        try:

            print(f"DEPORTE: {sport}")

            url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={API_KEY}&regions=us&markets=h2h"

            response = requests.get(url)

            print("STATUS:", response.status_code)

            if response.status_code == 429:

                print("LIMITE API")
                continue

            if response.status_code != 200:

                print("ERROR API")
                continue

            data = response.json()

            if not data:

                print("SIN PARTIDOS")
                continue

            for game in data[:5]:

                try:

                    game_id = game["id"]

                    if game_id in sent_games:

                        print("YA ENVIADO")
                        continue

                    home = game["home_team"]
                    away = game["away_team"]

                    bookmakers = game.get(
                        "bookmakers",
                        []
                    )

                    if len(bookmakers) < 2:

                        print("POCOS BOOKMAKERS")
                        continue

                    outcomes1 = bookmakers[0]["markets"][0]["outcomes"]
                    outcomes2 = bookmakers[1]["markets"][0]["outcomes"]

                    for i in range(2):

                        team = outcomes1[i]["name"]

                        odd1 = outcomes1[i]["price"]
                        odd2 = outcomes2[i]["price"]

                        best_odd = max(
                            odd1,
                            odd2
                        )

                        # =========================
                        # RATINGS IA
                        # =========================

                        team_rating = get_team_rating(
                            team,
                            sport
                        )

                        opponent = away if team == home else home

                        opponent_rating = get_team_rating(
                            opponent,
                            sport
                        )

                        # =========================
                        # MACHINE LEARNING
                        # =========================

                        probability = predict_probability(

                            best_odd,
                            team_rating,
                            opponent_rating,
                            1
                        )

                        # =========================
                        # EV
                        # =========================

                        ev = (
                            probability * best_odd
                        ) - 1

                        print("TEAM:", team)
                        print("ODD:", best_odd)
                        print("PROB:", probability)
                        print("EV:", ev)

                        # =========================
                        # FILTRO VALUE
                        # =========================

                        if ev <= -0.10:

                            print("NO VALUE")
                            continue

                        # =========================
                        # MENSAJE
                        # =========================

                        message = f"""
🔥 VALUE BET IA

🏆 {sport}

⚔️ {home} vs {away}

🎯 PICK:
{team}

📊 CUOTA:
{best_odd}

🧠 PROBABILIDAD IA:
{round(probability * 100, 1)}%

📈 EV:
{round(ev, 2)}
"""

                        await bot.send_message(

                            chat_id=CHAT_ID,
                            text=message
                        )

                        print("MENSAJE ENVIADO")

                        sent_games.add(game_id)

                        with open(SENT_FILE, "a") as f:

                            f.write(
                                game_id + "\n"
                            )

                except Exception as e:

                    print("ERROR PARTIDO:", e)

        except Exception as e:

            print("ERROR DEPORTE:", e)

# =========================
# MAIN
# =========================

async def main():

    scheduler = AsyncIOScheduler()

    # ESCANEO 30 MIN
    scheduler.add_job(

        scan_games,
        "interval",
        minutes=30
    )

    # HEARTBEAT 1 HORA
    scheduler.add_job(

        heartbeat,
        "interval",
        hours=1
    )

    scheduler.start()

    print("BOT IA INICIADO")

    await heartbeat()

    await scan_games()

    await asyncio.Event().wait()

# =========================
# INICIAR
# =========================

asyncio.run(main())