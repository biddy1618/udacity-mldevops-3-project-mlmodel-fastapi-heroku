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

    @validator('sex')
    def c_match(cls, v):
        if v not in ['Male', 'Female']:
            raise ValueError('Sex must be in [Male, Female]')
        return v


class GenericResponse(BaseModel):
    message: str


class Prediction(BaseModel):
    prediction: str
