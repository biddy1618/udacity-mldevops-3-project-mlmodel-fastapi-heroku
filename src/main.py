'''
Module for starting FastAPI microframework.

Author: Dauren Baitursyn
Date: 02.09.22
'''
import logging
import yaml

import pandas as pd

from pathlib import Path
from joblib import load
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from .train_model.ml.model import inference
from .train_model.ml.data import process_data
from .api_models.models import Person, GenericResponse, Prediction
from .api_models import helper


logger = logging.getLogger('uvicorn')
try:
    with open(Path.cwd().joinpath('params.yaml'), 'rb') as f:
        params = yaml.safe_load(f)
    model_path = params['train_model']['model_path']
except FileNotFoundError as e:
    logger.error('`params.yaml` file not found.')
    raise e
except ValueError as e:
    logger.error(
        '`params.yaml` has no key `train_model.model_path` for model path')
    raise e

app = FastAPI()

logger.info(f'Loading model at `{model_path}`')
try:
    model = load(Path.cwd().joinpath(model_path))
except Exception as e:
    logger.error(
        f'Failed to load joblib file at `{model_path}`')
    raise e


@app.get('/', response_model=GenericResponse)
async def get_info():
    '''
    Path for retrieving greeting.

    Returns:
        dict: GenericResponse pydantic model.
    '''
    return {
        'message': (
            'To test, please, send `POST` request with data on the person '
            'to `/persons/` to get prediction on the salary.')
        }


@app.post('/persons/', response_model=Prediction)
async def create_item(person: Person) -> dict:
    '''
    Path for predicting if person earns more than 50k or less.

    Args:
        person (Person): Person pydantic model.

    Returns:
        dict: Prediction pydantic model.
    '''
    logger.info('Making prediction')
    person = pd.DataFrame(jsonable_encoder([person]))
    person['education_num'] = helper.map_education(person['education'])

    x, _, _, _ = process_data(
        data=person,
        training=False,
        preprocessor=model['preprocessor']
    )

    pred_proba = inference(model['classifier'], x)
    pred = pred_proba[:, 1].round()

    pred_label = model['target_encoder'].inverse_transform(pred)

    logger.info(f'Predicted - {pred_label[0]}')
    return {'prediction': pred_label[0]}
