import os 
import re
import joblib

def load_model(model_path):

    models = {}

    for filename in os.listdir(model_path):
        if not re.search(r"\.joblib$", filename):
            continue
        models[re.sub(r"\.joblib$", "", filename)] = joblib.load(f"{model_path}/{filename}")

    # Testing
    first_key = next(iter(models))
    return models
