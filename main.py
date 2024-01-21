from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from model_routers.router_imdb_ratings import router as router_imdb_ratings
from model_routers.router_diabetes_prediction import router as router_diabetes_prediction

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.mount("/static", StaticFiles(directory="saved"), name="static")

models = {
    "IMDB Ratings": { "router": router_imdb_ratings, "path": "/model/imdb_ratings"},
    "Diabetes Prediction": {"router": router_diabetes_prediction, "path": "/model/diabetes_prediction"},
}

# for key in models:
#     app.include_router(models[key]["router"], prefix=models[key]["path"], tags=[models[key]["path"].split("/")[-1]])

app.include_router(router_imdb_ratings, prefix="/model/imdb_ratings", tags=["imdb_ratings"])
app.include_router(router_diabetes_prediction, prefix="/model/diabetes_prediction", tags=["diabetes_prediction"])

@app.get("/")
def get_root():
    return { "Intro": "Intro message" }
