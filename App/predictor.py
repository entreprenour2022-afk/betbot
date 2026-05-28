import joblib

model = joblib.load(
    "App/models/betting_model.pkl"
)

def predict_probability(

    odd,
    team_rating,
    opponent_rating,
    home_advantage

):

    features = [[

        odd,
        team_rating,
        opponent_rating,
        home_advantage
    ]]

    probability = model.predict_proba(
        features
    )[0][1]

    return probability