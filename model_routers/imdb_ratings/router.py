import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
from model_loader import load_model

router = APIRouter()

models = load_model("./saved/imdb_ratings/models")
tfidf_vectoriser = joblib.load("./saved/imdb_ratings/tfidf_vectoriser.joblib")

class ReviewTextModel(BaseModel):
    Review: str

@router.get("/models")
async def get_models():
    return [x[0] for x in models.items()]

@router.get('/features')
async def get_features():
    feature_names = [(field, str(field_obj.annotation.__name__)) for field, field_obj in ReviewTextModel.model_fields.items()]
    return feature_names

@router.post("/naive_bayes")
async def classify_naive_bayes(req: ReviewTextModel):
    vectorised_data = tfidf_vectoriser.transform(pd.Series([req.Review]))
    return models["naive_bayes"].predict(vectorised_data)[0]

@router.post("/logistic_regression")
async def classify_logistic_regression(req: ReviewTextModel):
    vectorised_data = tfidf_vectoriser.transform(pd.Series([req.Review]))
    return models["logistic_regression"].predict(vectorised_data)[0]

