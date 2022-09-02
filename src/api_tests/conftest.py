'''
Configuration for PyTest.

Author: Dauren Baitursyn
Date: 26.08.22
'''

import pytest


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


@pytest.fixture(scope='session')
def prod():
    prod = request.config.option.prod

    return prod
