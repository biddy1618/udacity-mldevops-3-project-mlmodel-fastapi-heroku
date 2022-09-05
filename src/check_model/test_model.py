'''
Tests for model pipeline checks.

Author: Dauren Baitursyn
Data: 05.09.22
'''
from ..train_model.ml.data import process_data
from ..train_model.ml.model import inference
from .. import constants


def test_process_data(data):
    X, y, preprocessor, target_encoder = process_data(
        data, training=True
    )
    n_rows, _ = X.shape
    n_targets = y.shape[0]
    assert n_rows == n_targets == data.shape[0], 'Number of rows is different'
    assert set(y) == set([0, 1]), 'Target encoder has more than 2 values'
    assert preprocessor.feature_names_in_.tolist() == \
        list(constants.ind_fields), 'Input features are not in order'
    assert set(target_encoder.classes_) == constants.salary, \
        'Target labels differ'


def test_inference(data, model):
    X, _, _, _ = process_data(
        data,
        training=False,
        preprocessor=model['preprocessor'],
        target_encoder=model['target_encoder']
    )

    pred_proba = inference(model['classifier'], X)
    pred = pred_proba[:, 1].round()

    pred_label = model['target_encoder'].inverse_transform(pred)

    assert set(pred) == set([0, 1]), 'Target encoder has more than 2 values'
    assert set(pred_label) == constants.salary, 'Target labels differ'
