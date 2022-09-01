'''

'''
import logging

import pandas as pd

from pydantic import BaseModel
from pathlib import Path
from joblib import load
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from typing import Optional
from .train_model.ml.model import inference
from .train_model.ml.data import process_data

PATH_MODEL = Path.cwd().joinpath('src/model/model.joblib')


class Person(BaseModel):
    age: Optional[int] = 35
    workclass: Optional[str] = None
    fnlgt: Optional[int] = 0
    education: Optional[str] = None
    education_num: Optional[int] = 0
    marital_status: Optional[str] = None
    occupation: Optional[str] = None
    relationship: Optional[str] = None
    race: Optional[str] = None
    sex: Optional[str] = None
    capital_gain: Optional[int] = 0
    capital_loss: Optional[int] = 0
    hours_per_week: Optional[int] = 0
    native_country: Optional[str] = None


logger = logging.getLogger("uvicorn")
app = FastAPI()

logger.info(f'Loading model at {PATH_MODEL}')
model = load(PATH_MODEL)


@app.get("/")
async def get_info() -> dict:

    return {'info':
            'To test, please, send `POST` request with data on the person...'}


@app.post("/persons/")
async def create_item(person: Person) -> dict:

    logger.info('Making prediction')
    person = pd.DataFrame(jsonable_encoder([person]))

    x, _, _, _ = process_data(
        person,
        categorical_features=model['cat_features'],
        training=False,
        cat_encoder=model['cat_encoder']
    )

    pred_proba = inference(model['classifier'], x)
    pred = pred_proba[:, 1].round()

    logger.info(f'Predicted - {pred[0]}')
    return {'Prediction': pred[0]}
