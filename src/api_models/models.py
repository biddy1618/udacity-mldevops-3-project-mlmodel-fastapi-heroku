'''
Module for pydantic model definitions.

Author: Dauren Baitursyn
Date: 02.09.22

'''
from pydantic import BaseModel, Field, validator
from typing import Optional


class Person(BaseModel):
    age: int = Field(title='`age` field (required)', ge=17, le=90)
    workclass: Optional[str] = Field(
        default=None, title='`workclass` field')
    fnlgt: Optional[int] = Field(
        default=0, title='`fnlgt` field')
    education: Optional[str] = Field(
        default=None, title='`education` field')
    education_num: Optional[int] = Field(
        default=0,
        title='`education_num` field for ordinal number for educaiton',
        ge=1, le=16)
    marital_status: Optional[str] = Field(
        default=None, title='`marital_status` field')
    occupation: Optional[str] = Field(
        default=None, title='`occupation` field')
    relationship: Optional[str] = Field(
        default=None, title='`relationship` field')
    race: Optional[str] = Field(
        default=None, title='`race` field')
    sex: str = Field(title='`sex` field (required)')
    capital_gain: Optional[int] = Field(
        default=0, title='`capital_gain` field', ge=0, le=99999)
    capital_loss: Optional[int] = Field(
        default=0, title='`capital_loss` field', ge=0, le=99999)
    hours_per_week: Optional[int] = Field(
        default=None, title='`hours_per_week` field', ge=1, le=99)
    native_country: Optional[str] = Field(
        default=None, title='`native_country` field')

    class Config:
        schema_extra = {
            'example': {
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
        }

    @validator('sex')
    def c_match(cls, v):
        if v not in ['Male', 'Female']:
            raise ValueError('Sex must be in [Male, Female]')
        return v


class GenericResponse(BaseModel):
    message: str

    class Config:
        schema_extra = {
            'example': {
                'message': (
                    'To test, please, send `POST` request with '
                    'data on the person to `/persons/` to get prediction '
                    'on the salary.'
                )
            }
        }


class Prediction(BaseModel):
    prediction: str

    class Config:
        schema_extra = {
            'example': {
                'prediction': '>50K | <=50K'
            }
        }
