from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model_routers.router_imdb_ratings import router as router_imdb_ratings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
models = {
    "IMDB Ratings": { "router": router_imdb_ratings, "path": "/model/imdb_ratings"},
}

for key in models:
    app.include_router(models[key]["router"], prefix=models[key]["path"], tags=[models[key]["path"].split("/")[-1]])

#app.include_router(router_imdb_ratings, prefix="/model/imdb_ratings", tags=["imdb_ratings"])

@app.get("/")
def get_root():
    return { "Intro": "Intro message" }
