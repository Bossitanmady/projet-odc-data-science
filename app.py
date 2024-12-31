from fastapi import FastAPI
import uvicorn
import numpy as np 
import pandas as pd 
import joblib
import json
from pydantic import BaseModel

class InputVars(BaseModel):
    checking_account_status: float 
    duration_months: float 
    credit_history: float
    purpose: float 
    credit_amount: float 
    savings_account: float
    employment_duration: float 
    installment_rate: float 
    personal_status_sex: float 
    other_debtors: float 
    present_residence_years: float 
    property: float 
    age_years: float 
    other_installment_plans: float 
    housing: float 
    number_of_credits: float 
    job: float 
    dependents: float 
    telephone: float 
    foreign_worker: float 


# Création de l'api 
app=FastAPI()

# Chargement des modèle dépuis le disque 
logistic_regression_model=joblib.load(open('logistic_regression_model.pkl','rb'))
scaler=joblib.load(open('scaling.pkl','rb'))

# Création de l'endepoint avec la methode GET 
@app.get('/')
def index():
    return {'Message':'Hello World'}

# Création de l'endepoint avec la methode POST 
@app.post('/predict')
def prediction(Data: InputVars):
    data=pd.json_normalize(Data)

# Chargement de l'application 

if __name__=='__main__':
    uvicorn.run(app)