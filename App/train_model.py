import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

import joblib

# =========================
# CARGAR DATASET
# =========================

data = pd.read_csv(
    "App/historical_data.csv"
)
# =========================
# FEATURES
# =========================

X = data[[
    "odd",
    "team_rating",
    "opponent_rating",
    "home_advantage"
]]

# =========================
# TARGET
# =========================

y = data["result"]

# =========================
# SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.2,
    random_state=42
)

# =========================
# MODELO IA
# =========================

model = RandomForestClassifier(

    n_estimators=100,
    random_state=42
)

# =========================
# ENTRENAR
# =========================

model.fit(
    X_train,
    y_train
)

# =========================
# PREDICCIONES
# =========================

predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    "ACCURACY:",
    accuracy
)

# =========================
# GUARDAR MODELO
# =========================

joblib.dump(

    model,
    "App/models/betting_model.pkl"
)

print(
    "MODELO ENTRENADO"
)