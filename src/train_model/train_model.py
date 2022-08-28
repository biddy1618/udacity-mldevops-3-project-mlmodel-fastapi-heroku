'''
Module for building model.
'''
import logging
import argparse
from pathlib import Path
from joblib import dump

import pandas as pd
from sklearn.model_selection import train_test_split

from .ml.data import process_data
from .ml.model import train_model, compute_model_metrics, inference

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def go(args):
    '''
    Main function for building model.
    '''
    logger.info('Starting training model...')

    PATH_TRAIN_DATA = Path.cwd().joinpath(args.train_data)
    PATH_MODEL = Path.cwd().joinpath(args.model)

    logger.info(f'Loading train data at {PATH_TRAIN_DATA}')
    data = pd.read_csv(PATH_TRAIN_DATA)

    logger.info(f'Splitting data with validation size {args.valid_size}')
    train, valid = train_test_split(
        data,
        test_size=args.valid_size,
        random_state=args.valid_random_state
    )

    cat_features = [
        'workclass',
        'education',
        'marital-status',
        'occupation',
        'relationship',
        'race',
        'sex',
        'native-country',
    ]

    logger.info('Processing training data')
    X_train, y_train, cat_encoder, target_encoder = process_data(
        train,
        categorical_features=cat_features,
        target='salary',
        training=True
    )

    logger.info('Processing validation data')
    X_test, y_test, _, _ = process_data(
        valid,
        categorical_features=cat_features,
        target='salary',
        training=False,
        cat_encoder=cat_encoder,
        target_encoder=target_encoder
    )

    logger.info('Training model on training data')
    model = train_model(X_train, y_train, args.model_random_state)

    logger.info('Making inference on validation data')
    y_pred_proba = inference(model, X_test)
    y_pred = y_pred_proba[:, 1].round()

    precision, recall, fbeta = compute_model_metrics(y_test, y_pred)

    logger.info('Metrics on validation data:')
    logger.info(f'Precision score: {precision:.3f}')
    logger.info(f'Recall score: {recall:.3f}')
    logger.info(f'F1 score: {fbeta:.3f}')

    model = {
        'cat_features': cat_features,
        'cat_encoder': cat_encoder,
        'target_encoder': target_encoder,
        'classifier': model
    }

    logger.info(f'Saving model at {PATH_MODEL}')
    dump(model, PATH_MODEL)

    logger.info('Finished training model')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Train and save trained model')

    parser.add_argument(
        '--train_data',
        type=str,
        help='File path of the training data',
        required=True
    )

    parser.add_argument(
        '--valid_size',
        type=float,
        default=0.2,
        help='Validation size for training data',
        required=True
    )

    parser.add_argument(
        '--valid_random_state',
        type=int,
        default=48,
        help='Random seed for validation',
        required=True
    )

    parser.add_argument(
        '--model_random_state',
        type=int,
        help='Random seed for model',
        required=True
    )

    parser.add_argument(
        '--model',
        type=str,
        help='File path to save the trained model',
        required=True
    )

    args = parser.parse_args()

    go(args)
