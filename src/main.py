'''

'''
import logging

import pandas as pd

from pydantic import BaseModel
from pathlib import Path
from joblib import load
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from .train_model.ml.model import inference
from .train_model.ml.data import process_data

logger = logging.getLogger()
PATH_MODEL = Path.cwd().joinpath('src/model/model.joblib')


class Person(BaseModel):
    age: int
    workclass: str
    fnlgt: int
    education: str
    education_num: int
    marital_status: str
    occupation: str
    relationship: str
    race: str
    sex: str
    capital_gain: int
    capital_loss: int
    hours_per_week: int
    native_country: str


app = FastAPI()

logger.info(f'Loading model at {PATH_MODEL}')
model = load(PATH_MODEL)


# This allows sending of data (our TaggedItem) via POST to the API.
@app.post("/persons/")
async def create_item(person: Person):
    print(person)
    person = pd.DataFrame(jsonable_encoder([person]))
    x, _, _, _ = process_data(
        person,
        categorical_features=model['cat_features'],
        training=False,
        cat_encoder=model['cat_encoder']
    )

    pred_proba = inference(model['classifier'], x)
    pred = pred_proba[:, 1].round()

    return pred
