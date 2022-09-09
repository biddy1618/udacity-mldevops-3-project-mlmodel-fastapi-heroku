'''
Configuration for PyTest.

Author: Dauren Baitursyn
Date: 26.08.22
'''

import pytest
import yaml
import logging
import pandas as pd

from pathlib import Path
from joblib import load

logger = logging.getLogger()

try:
    with open(Path.cwd().joinpath('params.yaml'), 'rb') as f:
        params = yaml.safe_load(f)
    data_path = params['clean_data']['clean_data']
    model_path = params['train_model']['model_path']
except FileNotFoundError as e:
    logger.error('`params.yaml` file not found.')
    raise e
except ValueError as e:
    logger.error(
        '`params.yaml` has no key `clean_data.clean_data` for clean data')
    logger.error(
        '`params.yaml` has no key `train_model.model_path` for model')
    raise e


def pytest_addoption(parser):
    parser.addoption(
        '--data_path', action='store', default=data_path,
        help='Path for clean data')
    parser.addoption(
        '--model_path', action='store', default=model_path,
        help='Path for clean data')
    parser.addoption(
        '--dev', action='store_false', default=True,
        help='Running test in dev environment')


@pytest.fixture(scope='session')
def data(request):
    data_path = request.config.option.data_path

    if data_path is None:
        pytest.fail(
            'You must provide the `--data_path` option on the command line.')

    df = pd.read_csv(Path.cwd().joinpath(data_path))

    return df


@pytest.fixture(scope='session')
def model(request):
    model_path = request.config.option.model_path

    if model_path is None:
        pytest.fail(
            'You must provide the `--model_path` option on the command line.')

    model = load(Path.cwd().joinpath(model_path))

    return model


@pytest.fixture(scope='session')
def dev_env(request):
    dev_env = request.config.option.dev

    return dev_env


@pytest.fixture
def data_true():
    data = {
        'age': 45,
        'workclass': 'Private',
        'fnlgt': 1484705,
        'education': 'Doctorate',
        'education_num': 16,
        'marital_status': 'Married-csv-spouse',
        'occupation': 'Prof-specialty',
        'relationship': 'Husbanb',
        'race': 'White',
        'sex': 'Male',
        'capital_gain': 99999,
        'capital_loss': 0,
        'hours_per_week': 45,
        'native_country': 'United-States'
    }

    return data


@pytest.fixture
def data_false():
    data = {
        'age': 17,
        'workclass': 'Without-pay',
        'fnlgt': 12285,
        'education': '11th',
        'education_num': 7,
        'marital_status': 'Never-married',
        'occupation': 'Unknown',
        'relationship': 'Unmarried',
        'race': 'Other',
        'sex': 'Male',
        'capital_gain': 0,
        'capital_loss': 0,
        'hours_per_week': 45,
        'native_country': 'United-States'
    }

    return data


@pytest.fixture
def data_valid():
    data = [
        ({
            'age': 35,
            'workclass': 'Private',
            'fnlgt': 323143,
            'education': 'Assoc-voc',
            'education_num': 11,
            'marital_status': 'Married-csv-spouse',
            'occupation': 'Sales',
            'relationship': 'Husbanb',
            'race': 'White',
            'sex': 'Male',
            'capital_gain': 0,
            'capital_loss': 0,
            'hours_per_week': 45,
            'native_country': 'United-States'
        }, 'Valid data'),
        ({
            'age': 35,
            'sex': 'Male'
        }, 'Valid data with only mandatory fields'),
        ({
            'redundant': 'dauren',
            'age': 35,
            'sex': 'Male'
        }, 'Valid data with redundant field')
    ]

    return data


@pytest.fixture
def data_invalid():
    data = [
        ({}, 'Empty data'),
        ({
            'age': '35.3',
            'sex': 'Male'
        }, 'Invalid field type'),
        ({
            'workclass': 'string',
            'fnlgt': 0,
            'education': 'string',
            'education_num': 0,
            'marital_status': 'string',
            'occupation': 'string',
            'relationship': 'string',
            'race': 'string',
            'capital_gain': 0,
            'capital_loss': 0,
            'hours_per_week': 99,
            'native_country': 'string'
        }, 'Invalid data without mandatory fields'),
        ({
            'age': 16,
            'sex': 'Male'
        }, 'Invalid age data'),
        ({
            'age': 91,
            'sex': 'Male'
        }, 'Invalid age data'),
        ({
            'age': 35,
            'sex': 'Male',
            'education_num': -1,
        }, 'Invalid education_num data'),
        ({
            'age': 35,
            'sex': 'Male',
            'education_num': 17,
        }, 'Invalid education_num data'),
        ({
            'age': 35,
            'sex': 'Male',
            'capital_gain': -1,
        }, 'Invalid capital_gain data'),
        ({
            'age': 35,
            'sex': 'Male',
            'capital_gain': 100000,
        }, 'Invalid capital_gain data'),
        ({
            'age': 35,
            'sex': 'Male',
            'capital_loss': -1,
        }, 'Invalid capital_loss data'),
        ({
            'age': 35,
            'sex': 'Male',
            'capital_loss': 100000,
        }, 'Invalid capital_loss data'),
        ({
            'age': 35,
            'sex': 'Male',
            'hours_per_week': -1,
        }, 'Invalid hours_per_week data'),
        ({
            'age': 35,
            'sex': 'Male',
            'hours_per_week': 100,
        }, 'Invalid hours_per_week data')
    ]

    return data
