'''
Configuration for PyTest.

Author: Dauren Baitursyn
Date: 26.08.22
'''

import pytest
import yaml
import logging
from pathlib import Path
import pandas as pd

logger = logging.getLogger()

try:
    with open(Path.cwd().joinpath('params.yaml'), 'rb') as f:
        params = yaml.safe_load(f)
    data_path = params['clean_data']['clean_data']
except FileNotFoundError as e:
    logger.error('`params.yaml` file not found.')
    raise e
except ValueError as e:
    logger.error(
        '`params.yaml` has no key `clean_data.clean_data` for clean data')
    raise e


def pytest_addoption(parser):
    parser.addoption(
        '--data_path', action='store', default=data_path,
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

    df = pd.read_csv(data_path)

    return df


@pytest.fixture(scope='session')
def dev_env(request):
    dev_env = request.config.option.dev

    return dev_env


@pytest.fixture
def data_valid():
    data = {
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
    }

    return data
