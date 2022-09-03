'''
Tests for data validation.

Author: Dauren Baitursyn
Date: 26.08.22
'''

import pandas as pd
import numpy as np

from .. import constants
# import scipy.stats


def test_column_names(data: pd.DataFrame, prod: bool):
    '''
    Test columns correspondence and order.
    '''

    expected_colums = constants.ind_fields

    if prod:
        expected_colums += [constants.target_field]

    these_columns = data.columns.values

    # This also enforces the same order
    assert list(expected_colums) == list(these_columns)


def test_cat_columns_values(data: pd.DataFrame, prod: bool):
    '''
    Test data for invalid values.
    '''

    workclass = constants.workclass
    education = constants.education
    marital_status = constants.marital_status
    occupation = constants.occupation
    relationship = constants.relationship
    sex = constants.sex
    native_country = constants.native_country
    salary = constants.salary

    errors = []
    workclass_data = set(data['workclass'].unique())
    education_data = set(data['education'].unique())
    marital_status_data = set(data['marital_status'].unique())
    occupation_data = set(data['occupation'].unique())
    relationship_data = set(data['relationship'].unique())
    sex_data = set(data['sex'].unique())
    native_country_data = set(data['native_country'].unique())

    if prod:
        salary = constants.salary
        salary_data = set(data['salary'].unique())

    if not workclass_data.issubset(workclass):
        errors.append(
            ('`workclass` contains unknown values - '
             f'{workclass_data.difference(workclass)}.'))
    if not education_data.issubset(education):
        errors.append(
            ('`education` contains unknown values - '
             f'{education_data.difference(education)}.'))
    if not marital_status_data.issubset(marital_status):
        errors.append(
            ('`marital_status` contains unknown values - '
             f'{marital_status_data.difference(marital_status)}.'))
    if not occupation_data.issubset(occupation):
        errors.append(
            ('`occupation` contains unknown values - '
             f'{occupation_data.difference(occupation)}.'))
    if not relationship_data.issubset(relationship):
        errors.append(
            ('`relationship` contains unknown values - '
             f'{relationship_data.difference(relationship)}.'))
    if not sex_data.issubset(sex):
        errors.append(
            f'`sex` contains unknown values - {sex_data.difference(sex)}.')
    if not native_country_data.issubset(native_country):
        errors.append(
            ('`native_country` contains unknown values - '
             f'{native_country_data.difference(native_country)}.'))
    if prod and not salary_data.issubset(salary):
        errors.append(
            ('`salary` contains unknown values - '
             f'{salary_data.difference(salary)}.'))

    assert not errors, "errors occured:\n{}".format("\n".join(errors))


def test_proper_boundaries(data: pd.DataFrame):
    '''
    Test numeric field boundaries.
    '''
    age = data['age'].between(17, 90)
    capital_gain = data['capital_gain'].between(0, 99999)
    capital_loss = data['capital_loss'].between(0, 99999)
    hours_per_week = data['hours_per_week'].between(1, 99)

    errors = []
    if not np.sum(~age) == 0:
        errors.append('`age` contains out of range values.')
    if not np.sum(~capital_gain) == 0:
        errors.append('`capital_gain` contains out of range values.')
    if not np.sum(~capital_loss) == 0:
        errors.append('`capital_loss` contains out of range values.')
    if not np.sum(~hours_per_week) == 0:
        errors.append('`hours_per_week` contains out of range values.')

    assert not errors, "errors occured:\n{}".format("\n".join(errors))
