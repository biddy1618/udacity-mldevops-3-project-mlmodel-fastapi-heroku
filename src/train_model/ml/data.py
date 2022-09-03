'''
Module for processing cleaned data.

Author: Dauren Baitursyn
Date: 26.08.22
'''
import numpy as np
from sklearn.preprocessing import LabelBinarizer, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

from ... import constants


def process_data(
        data,
        training=True,
        preprocessor=None,
        target_encoder=None):
    '''
    Process the data used in the machine learning pipeline.

    Processes the data using one hot encoding for the categorical features and
    a label binarizer for the labels. This can be used in either training or
    inference/validation.

    Note: depending on the type of model used, you may want to add in
    functionality that scales the continuous data.

    Args
        data (pd.DataFrame):
            Dataframe containing the features and label.
        training (bool):
            Indicator if training mode or inference/validation mode.
            Defaults to True.
        preprocessor (sklearn.compose.ColumnTransformer):
            Trained sklearn ColumnTransformer, only used if training=False.
            Defaults to None.
        target_encoder (sklearn.preprocessing.LabelBinarizer):
            Trained sklearn LabelBinarizer, only used if training=False.
            Defaults to None.

    Returns:
        np.array:
            Processed data.
        np.array:
            Processed labels if training=True or testing case,
            otherwise empty np.array.
        sklearn.compose.ColumnTransformer:
            Trained ColumnTransformer if training is True, otherwise
            returns the encoder passed in.
        sklearn.preprocessing.LabelBinarizer:
            Trained LabelBinarizer if training is True, otherwise
            returns the binarizer passed in.
    '''

    X = data[constants.ind_fields]
    y = np.array([])
    if training:
        categorical = constants.cat_fields
        categorical_preproc = OneHotEncoder(
            sparse=False, handle_unknown='ignore')

        zero_imputed = constants.zero_imputed
        zero_imputer = SimpleImputer(strategy='constant', fill_value=0)

        median_imputed = constants.median_imputed
        median_imputer = SimpleImputer(strategy='median')

        preprocessor = ColumnTransformer(
            transformers=[
                ('categorical', categorical_preproc, categorical),
                ('zero_imputed', zero_imputer, zero_imputed),
                ('median_imputed', median_imputer, median_imputed)
            ],
            remainder='passthrough',
        )
        X = preprocessor.fit_transform(X)

        y = data[constants.target_field]
        target_encoder = LabelBinarizer()
        y = target_encoder.fit_transform(y).ravel()
    else:
        X = preprocessor.transform(X)
        # to pass validation mode and catch exceptions for inference mode
        try:
            y = data[constants.target_field]
            y = target_encoder.transform(y).ravel()
        except (ValueError, AttributeError, KeyError):
            pass

    return X, y, preprocessor, target_encoder
