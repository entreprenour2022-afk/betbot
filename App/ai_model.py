from team_stats import *

# =========================
# PROBABILIDAD IMPLÍCITA
# =========================

def implied_probability(odd):

    return 1 / odd

# =========================
# EXPECTED VALUE
# =========================

def calculate_ev(probability, odd):

    return (probability * odd) - 1

# =========================
# FUERZA EQUIPOS
# =========================

def calculate_team_strength(
    home,
    away,
    sport
):

    home_rating = get_team_rating(
        home,
        sport
    )

    away_rating = get_team_rating(
        away,
        sport
    )

    strength = (
        home_rating
        - away_rating
        + home_advantage()
    )

    return strength

# =========================
# IA PROBABILIDAD
# =========================

def ai_probability(
    odd,
    home,
    away,
    sport
):

    implied = implied_probability(
        odd
    )

    strength = calculate_team_strength(
        home,
        away,
        sport
    )

    probability = implied + strength

    # Limitar probabilidad
    if probability > 0.95:
        probability = 0.95

    if probability < 0.01:
        probability = 0.01

    return probability