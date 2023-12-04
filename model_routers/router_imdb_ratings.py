import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
from model_loader import load_model

router = APIRouter()

models = load_model("./saved/imdb_ratings/models")
tfidf_vectoriser = joblib.load("./saved/imdb_ratings/tfidf_vectoriser.joblib")

class ReviewTextModel(BaseModel):
    review: str

@router.get("/models")
async def get_models():
    return [x[0] for x in models.items()]

@router.post("/naive_bayes")
async def classify_naive_bayes(req: ReviewTextModel):
    vectorised_data = tfidf_vectoriser.transform(pd.Series([req.review]))
    return models["naive_bayes"].predict(vectorised_data)[0]

@router.post("/logistic_regression")
async def classify_logistic_regression(req: ReviewTextModel):
    vectorised_data = tfidf_vectoriser.transform(pd.Series([req.review]))
    return models["logistic_regression"].predict(vectorised_data)[0]
