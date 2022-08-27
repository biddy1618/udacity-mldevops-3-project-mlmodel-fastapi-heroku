'''
Module for processing cleaned data.

Author: Dauren Baitursyn
Date: 26.08.22
'''
import numpy as np
from sklearn.preprocessing import LabelBinarizer, OneHotEncoder


def process_data(
        X,
        categorical_features=[],
        target=None,
        training=True,
        cat_encoder=None,
        target_encoder=None):
    '''
    Process the data used in the machine learning pipeline.

    Processes the data using one hot encoding for the categorical features and
    a label binarizer for the labels. This can be used in either training or
    inference/validation.

    Note: depending on the type of model used, you may want to add in
    functionality that scales the continuous data.

    Args
        X (pd.DataFrame):
            Dataframe containing the features and label. Columns in
            `categorical_features`.
        categorical_features (list[str]):
            List containing the names of the categorical features.
            Defaults to empty list.
        target (str):
            Name of the label column in `X`. If None, then an empty array
            will be returned for y. Defaults to None.
        training (bool):
            Indicator if training mode or inference/validation mode.
            Defaults to True.
        cat_encoder (sklearn.preprocessing.OneHotEncoder):
            Trained sklearn OneHotEncoder, only used if training=False.
            Defaults to None.
        target_encoder (sklearn.preprocessing.LabelBinarizer):
            Trained sklearn LabelBinarizer, only used if training=False.
            Defaults to None.

    Returns:
        np.array:
            Processed data.
        np.array:
            Processed labels if labeled=True, otherwise empty np.array.
        sklearn.preprocessing.OneHotEncoder:
            Trained OneHotEncoder if training is True, otherwise returns the
            encoder passed in.
        sklearn.preprocessing.LabelBinarizer:
            Trained LabelBinarizer if training is True, otherwise returns the
            binarizer passed in.
    '''

    if target is not None:
        y = X[target]
        X = X.drop([target], axis=1)
    else:
        y = np.array([])

    X_categorical = X[categorical_features].values
    X_continuous = X.drop(*[categorical_features], axis=1)

    if training is True:
        cat_encoder = OneHotEncoder(sparse=False, handle_unknown="ignore")
        target_encoder = LabelBinarizer()
        X_categorical = cat_encoder.fit_transform(X_categorical)
        y = target_encoder.fit_transform(y.values).ravel()
    else:
        X_categorical = cat_encoder.transform(X_categorical)
        try:
            y = target_encoder.transform(y.values).ravel()
        # Catch the case where y is None because we're doing inference.
        except AttributeError:
            pass

    X = np.concatenate([X_continuous, X_categorical], axis=1)
    return X, y, cat_encoder, target_encoder
