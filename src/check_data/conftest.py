'''
Configuration for PyTest.

Author: Dauren Baitursyn
Date: 26.08.22
'''

import pytest
import pandas as pd


def pytest_addoption(parser):
    parser.addoption('--data_path', action='store')
    parser.addoption('--prod', action='store_false')


@pytest.fixture(scope='session')
def data(request):
    data_path = request.config.option.data_path

    if data_path is None:
        pytest.fail(
            'You must provide the `--data_path` option on the command line.')

    df = pd.read_csv(data_path)

    return df


@pytest.fixture(scope='session')
def prod(request):
    prod = request.config.option.prod

    return prod
