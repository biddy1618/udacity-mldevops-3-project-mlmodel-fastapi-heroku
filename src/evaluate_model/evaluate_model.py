'''
Module for evaluating model on test data.

Author: Dauren Baitursyn
Date: 26.08.22
'''
import logging
import argparse
import json
from pathlib import Path
from joblib import load

import pandas as pd

from src.train_model.ml.data import process_data
from src.train_model.ml.model import compute_model_metrics, inference, \
        get_precision_recall_curve

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def _compute_model_metrics_slice(model, data):
    '''
    Compute the trained machine learning model metrics on
    data slices using precision, recall, and F1.

    Args:
        model (dict):
            Dictionary with classifier, categorical features,
            categorical encoder and target encoder.
        data (pd.DataFrame):
            Dataframe containing the features and label.
    '''
    slice_metrics = {}
    slice_cols = ['relationship', 'race', 'sex']

    for col in slice_cols:
        slice_metrics[col] = {}
        for value in data[col].unique():
            slice_data = data[data[col] == value]

            X_test, y_test, _, _ = process_data(
                slice_data,
                training=False,
                preprocessor=model['preprocessor'],
                target_encoder=model['target_encoder']
            )

            y_pred_proba = inference(model['classifier'], X_test)
            y_pred = y_pred_proba[:, 1].round()

            precision, recall, fbeta = compute_model_metrics(y_test, y_pred)

            _, _, aps_score = get_precision_recall_curve(
                y_test, y_pred_proba[:, 1])

            slice_metrics[col][value] = {
                'Precision': precision,
                'Recall': recall,
                'F1 score': fbeta,
                'Average precision': aps_score,
                'Number of observations': slice_data.shape[0]
            }

    return slice_metrics


def _get_slice_metrics_txt(metrics):
    '''
    Format slice metrics to txt format.

    Args:
        metrics (dict): Dictionary with slice metrics.

    Returns:
        pd.DataFrame: DataFrame with slice scores.
    '''

    precision = []
    recall = []
    f1_score = []
    av_precision = []
    num_observations = []

    index = []

    for col in metrics:
        for val in metrics[col]:
            precision.append(metrics[col][val]['Precision'])
            recall.append(metrics[col][val]['Recall'])
            f1_score.append(metrics[col][val]['F1 score'])
            av_precision.append(metrics[col][val]['Average precision'])
            num_observations.append(
                metrics[col][val]['Number of observations'])
            index.append(col + ' - ' + val)

    return pd.DataFrame(
            index=index,
            data={
                'Precision': precision,
                'Recall': recall,
                'F1 score': f1_score,
                'Average precision': av_precision,
                'Number of observations': num_observations}
            ).round(3)


def go(args):
    '''
    Main function for evaluating model.
    '''
    logger.info('Starting evaluating model...')

    PATH_TEST_DATA = Path.cwd().joinpath(args.test_data)
    PATH_MODEL = Path.cwd().joinpath(args.model)
    PATH_METRICS_FOLDER = Path.cwd().joinpath(args.metrics)
    Path(PATH_METRICS_FOLDER).mkdir(parents=True, exist_ok=True)

    logger.info(f'Loading test data at {PATH_TEST_DATA}')
    data = pd.read_csv(PATH_TEST_DATA)

    logger.info(f'Loading model at {PATH_MODEL}')
    model = load(PATH_MODEL)

    logger.info('Processing test data')
    X_test, y_test, _, _ = process_data(
        data,
        training=False,
        preprocessor=model['preprocessor'],
        target_encoder=model['target_encoder']
    )

    logger.info('Making inference on test data')
    y_pred_proba = inference(model['classifier'], X_test)
    y_pred = y_pred_proba[:, 1].round()

    precision, recall, fbeta = compute_model_metrics(y_test, y_pred)

    logger.info('Metrics on test data:')
    logger.info(f'Precision score: {precision:.3f}')
    logger.info(f'Recall score: {recall:.3f}')
    logger.info(f'F1 score: {fbeta:.3f}')

    precisions, recalls, aps_score = \
        get_precision_recall_curve(y_test, y_pred_proba[:, 1])
    prc = pd.DataFrame(data={
        'precisions': precisions,
        'recalls': recalls,
    })
    prc.to_csv(
        Path(PATH_METRICS_FOLDER).joinpath('precision_recall_curve.csv'),
        index=False)

    logger.info('Making inference on slices of test data')
    model_slice_metrics = _compute_model_metrics_slice(model, data)

    slice_txt = _get_slice_metrics_txt(model_slice_metrics)

    logger.info(f'Saving slice metrics to {PATH_METRICS_FOLDER} folder')
    with open(Path(PATH_METRICS_FOLDER).joinpath('slice_output.txt'), 'w') \
            as slice_file:
        slice_txt.to_string(slice_file)
    logger.info('Saved slice metrics')

    model_metrics = {
        'Precision': precision,
        'Recall': recall,
        'F1 score': fbeta,
        'Average precision': aps_score,
        'Slice metrics': model_slice_metrics
    }
    with open(Path(PATH_METRICS_FOLDER).joinpath('metrics.json'), 'w') \
            as jsonfile:
        json.dump(model_metrics, jsonfile)

    cm = pd.DataFrame(data={
        'actual': y_test,
        'predicted': y_pred
    })
    cm.to_csv(
        Path(PATH_METRICS_FOLDER).joinpath('predictions.csv'),
        index=False)

    logger.info('Finished evaluating model')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Evaluate trained model on test data')

    parser.add_argument(
        '--model',
        type=str,
        help='Path to trained model',
        required=True
    )

    parser.add_argument(
        '--test_data',
        type=str,
        help='File path of the test data',
        required=True
    )

    parser.add_argument(
        '--metrics',
        type=str,
        help='Folder to save metrics',
        required=True
    )

    args = parser.parse_args()

    go(args)
