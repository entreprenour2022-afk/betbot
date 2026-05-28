# =========================
# RATINGS NBA
# =========================

NBA_RATINGS = {

    "Boston Celtics": 0.10,
    "Denver Nuggets": 0.09,
    "Los Angeles Lakers": 0.07,
    "Golden State Warriors": 0.06
}

# =========================
# RATINGS MLB
# =========================

MLB_RATINGS = {

    "New York Yankees": 0.09,
    "Los Angeles Dodgers": 0.10,
    "Houston Astros": 0.08
}

# =========================
# RATINGS FÚTBOL
# =========================

SOCCER_RATINGS = {

    "Palmeiras": 0.08,
    "Flamengo": 0.07,
    "River Plate": 0.07,
    "Universitario": 0.05,
    "Alianza Lima": 0.04
}

# =========================
# RATINGS TENIS
# =========================

TENNIS_RATINGS = {

    "Carlos Alcaraz": 0.10,
    "Jannik Sinner": 0.09,
    "Novak Djokovic": 0.08
}

# =========================
# OBTENER RATING
# =========================

def get_team_rating(
    team,
    sport
):

    if sport == "basketball_nba":

        return NBA_RATINGS.get(
            team,
            0.03
        )

    elif sport == "baseball_mlb":

        return MLB_RATINGS.get(
            team,
            0.03
        )

    elif "soccer" in sport:

        return SOCCER_RATINGS.get(
            team,
            0.03
        )

    elif "tennis" in sport:

        return TENNIS_RATINGS.get(
            team,
            0.03
        )

    return 0.03

# =========================
# LOCALÍA
# =========================

def home_advantage():

    return 0.03