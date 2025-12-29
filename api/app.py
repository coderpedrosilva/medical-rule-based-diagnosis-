from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import pandas as pd
import os

from src.preprocess import load_data
from src.majority import MajorityClassifier
from src.oner import OneR
from src.prism import Prism

# ======================================
# Caminhos absolutos (padrão profissional)
# ======================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "api", "static")

# ======================================
# Inicialização da API
# ======================================
app = FastAPI(title="Medical Rule-Based Diagnosis")

# ======================================
# Treinar modelos
# ======================================
X_train, X_test, y_train, y_test = load_data()

majority = MajorityClassifier()
majority.fit(y_train)

oner = OneR()
oner.fit(X_train, y_train)

prism = Prism()
prism.fit(X_train, y_train)

# ======================================
# Modelo de entrada
# ======================================
class Patient(BaseModel):
    Pregnancies: float = 0
    Glucose: float
    BloodPressure: float = 70
    SkinThickness: float = 20
    Insulin: float = 80
    BMI: float
    DiabetesPedigreeFunction: float = 0.5
    Age: float

# ======================================
# Endpoint de predição
# ======================================
@app.post("/predict/{model}")
def predict(model: str, p: Patient):

    X = pd.DataFrame([[
        p.Pregnancies,
        p.Glucose,
        p.BloodPressure,
        p.SkinThickness,
        p.Insulin,
        p.BMI,
        p.DiabetesPedigreeFunction,
        p.Age
    ]], columns=X_train.columns)

    if model == "majority":
        pred = majority.predict(X)[0]
        rule = "Classe majoritária da base"
    elif model == "oner":
        pred = oner.predict(X)[0]
        rule = f"Regra única baseada em {oner.best_feature}"
    else:
        pred = prism.predict(X)[0]
        rule = "Conjunto de regras PRISM"

    return {
        "prediction": int(pred),
        "rule": rule
    }

# ======================================
# Frontend (UI)
# ======================================
app.mount("/ui", StaticFiles(directory=STATIC_DIR, html=True), name="static")

# ======================================
# Redirecionar raiz para a interface
# ======================================
@app.get("/")
def root():
    return RedirectResponse("/ui")
