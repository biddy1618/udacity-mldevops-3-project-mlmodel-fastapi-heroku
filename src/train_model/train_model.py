'''
Module for building model.
'''
import logging
import argparse
from pathlib import Path
from joblib import dump


import pandas as pd
from sklearn.model_selection import train_test_split

from ml.data import process_data
from ml.model import train_model, compute_model_metrics, inference

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def go(args):
    '''
    Main function for building model.
    '''
    logger.info('Starting training model...')

    PATH_DATA_CLEAN = Path.cwd().joinpath(args.data_clean)
    PATH_MODEL = Path.cwd().joinpath(args.model)

    logger.info(f'Loading clean data at {PATH_DATA_CLEAN}')
    data = pd.read_csv(PATH_DATA_CLEAN)

    # Optional enhancement, use K-fold cross validation instead of a
    # train-test split.

    logger.info(f'Splitting data with test size {args.split_test_size}')
    train, test = train_test_split(
        data,
        test_size=args.split_test_size,
        random_state=args.split_random_state
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

    logger.info('Processing train data')
    X_train, y_train, cat_encoder, target_encoder = process_data(
        train,
        categorical_features=cat_features,
        target='salary',
        training=True
    )

    logger.info('Processing test data')
    X_test, y_test, _, _ = process_data(
        test,
        categorical_features=cat_features,
        target='salary',
        training=False,
        cat_encoder=cat_encoder,
        target_encoder=target_encoder
    )

    logger.info('Training model on train data')
    model = train_model(X_train, y_train, args.train_random_state)

    logger.info('Making inference on test data')
    y_pred_proba = inference(model, X_test)
    y_pred = y_pred_proba[:, 1].round()

    precision, recall, fbeta = compute_model_metrics(y_test, y_pred)

    logger.info('Metrics on test data:')
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
        '--data_clean',
        type=str,
        help='Path of the data to save after cleaning',
        required=True
    )

    parser.add_argument(
        '--split_random_state',
        type=int,
        help='Random seed for train-test split',
        required=True
    )

    parser.add_argument(
        '--split_test_size',
        type=float,
        default=0.2,
        help='Test size for train-test split',
        required=True
    )

    parser.add_argument(
        '--train_random_state',
        type=int,
        help='Random seed for model',
        required=True
    )

    parser.add_argument(
        '--model',
        type=str,
        help='Path to save the trained model',
        required=True
    )

    args = parser.parse_args()

    go(args)
