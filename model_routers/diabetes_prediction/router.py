import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
from model_loader import load_model

router = APIRouter()

models = load_model('./saved/diabetes_prediction/models')

class DiabetesPredictionModel(BaseModel):
    Pregnancies: int
    Glucose: int
    BloodPressure: int
    SkinThickness: int
    Insulin: int
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int
    Outcome: int

@router.get('/models')
async def get_models():
    return [x[0] for x in models.items()]

@router.get('/features')
async def get_features():
    feature_names = [(field, str(field_obj.annotation.__name__)) for field, field_obj in DiabetesPredictionModel.model_fields.items()]
    return feature_names

@router.post("/random_forest")
async def classifiy_random_forest(req: DiabetesPredictionModel):
    input_data = pd.DataFrame([req.modeldump()])
    return models["random_forest"].predict(input_data)