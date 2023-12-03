from fastapi import FastAPI, Query
from typing import List
import pandas as pd
import uvicorn

app = FastAPI()

# Load the data
df = pd.read_csv("kg3.csv")

# Goes to the first page
@app.get("/")
async def read_item():
    return {"message": "Welcome to our app"}

@app.get("/diagnosis")
async def get_diagnosis_list(symptom_ids: List[int] = Query(...)):
    dat = df[df['y_index'].isin(symptom_ids)]

    return {'diagnosis_ids': dat['x_index'].unique().tolist()}

@app.get("/symptoms")
async def get_symptom_list(diagnosis_ids: List[int] = Query(...), excluded_symptom_ids: List[int] = Query(...)):
    dat = df[df['x_index'].isin(diagnosis_ids)]

    if excluded_symptom_ids:
        dat = dat[~dat['y_index'].isin(excluded_symptom_ids)]

    return {'symptom_ids': dat['y_index'].unique().tolist()}