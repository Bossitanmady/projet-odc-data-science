from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import numpy as np
import pandas as pd
import joblib
from pydantic import BaseModel

# Classe pour valider les entrées
class InputVars(BaseModel):
    checking_account_status: str
    duration_months: int
    credit_history: str
    purpose: str
    credit_amount: int
    savings_account: str
    employment_duration: str
    installment_rate: int
    personal_status_sex: str
    other_debtors: str
    present_residence_years: int
    property: str
    age_years: int
    other_installment_plans: str
    housing: str
    number_of_credits: int
    job: str
    dependents: int
    telephone: str
    foreign_worker: str

# Création de l'application
app = FastAPI()
templates = Jinja2Templates(directory='templates')

# Monter le répertoire des fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

# Chargement des modèles
try:
    logistic_regression_model = joblib.load('logistic_regression_model.pkl')
    scaler = joblib.load('scaling.pkl')
    le = joblib.load('labeling.pkl')
except Exception as e:
    raise RuntimeError(f"Erreur lors du chargement des modèles : {str(e)}")

# Colonnes catégorielles
categorical_columns = [
    'checking_account_status', 'credit_history', 'purpose', 'savings_account', 
    'personal_status_sex', 'other_debtors', 'property', 'other_installment_plans',
    'housing', 'job', 'telephone', 'foreign_worker', 'employment_duration'
]

# Route principale
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Endpoint pour la prédiction
@app.post('/predict')
async def predict(request: Request,
                   checking_account_status: str = Form(...),
                   duration_months: int = Form(...),
                   credit_history: str = Form(...),
                   purpose: str = Form(...),
                   credit_amount: int = Form(...),
                   savings_account: str = Form(...),
                   employment_duration: str = Form(...), 
                   installment_rate: int = Form(...),
                   personal_status_sex: str = Form(...),
                   other_debtors: str = Form(...),
                   present_residence_years: int = Form(...),
                   property: str = Form(...),
                   age_years: int = Form(...),
                   other_installment_plans: str = Form(...), 
                   housing: str = Form(...),
                   number_of_credits: int = Form(...),
                   job: str = Form(...),
                   dependents: int = Form(...),
                   telephone: str = Form(...),
                   foreign_worker: str = Form(...)):
    try:
        # Création du DataFrame
        columns = [
            'checking_account_status', 'duration_months', 'credit_history', 'purpose',
            'credit_amount', 'savings_account', 'employment_duration', 'installment_rate',
            'personal_status_sex', 'other_debtors', 'present_residence_years', 'property',
            'age_years', 'other_installment_plans', 'housing', 'number_of_credits',
            'job', 'dependents', 'telephone', 'foreign_worker'
        ]
        
        data = [
            checking_account_status, duration_months, credit_history, purpose, credit_amount,
            savings_account, employment_duration, installment_rate, personal_status_sex,
            other_debtors, present_residence_years, property, age_years,
            other_installment_plans, housing, number_of_credits, job, dependents,
            telephone, foreign_worker
        ]
        df = pd.DataFrame([data], columns=columns)

        # Encodage des colonnes catégorielles
        for col in categorical_columns:
            if col in df.columns:
                if df[col].iloc[0] in le.classes_:
                    df[col] = le.transform([df[col].iloc[0]])[0]  # Transforme la valeur
                else:
                    df[col] = -1  # Valeur par défaut pour les valeurs inconnues

        # Conversion en float et mise à l'échelle
        numeric_data = df.astype(float)
        scaled_data = scaler.transform(numeric_data)

        # Prédiction
        prediction = logistic_regression_model.predict(scaled_data)
  
        result_message = "Il y a un risque que l'individu ne rembourse pas à temps" if prediction[0] == 1 else "Pas de risque, l'individu peut rembourser à temps"

        return templates.TemplateResponse("home.html", {"request": request, "prediction_text": result_message})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {str(e)}")

# Lancement du serveur
if __name__ == '__main__':
    uvicorn.run(app)
