'''
Module for building model.
'''
from pathlib import Path
import logging
import argparse

import pandas as pd
from sklearn.model_selection import train_test_split

from starter.ml.data import process_data
from starter.ml.model import train_model, compute_model_metrics, inference

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def go(args):
    '''
    Main function for building model.
    '''
    PATH_DATA_CLEAN = Path.cwd().joinpath(args.data_clean)

    data = pd.read_csv(PATH_DATA_CLEAN)

    # Optional enhancement, use K-fold cross validation instead of a
    # train-test split.
    train, test = train_test_split(
        data,
        test_size=args.test_size,
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
    X_train, y_train, encoder, lb = process_data(
        train,
        categorical_features=cat_features,
        label='salary',
        training=True
    )
    X_test, y_test, encoder, lb = process_data(
        test,
        categorical_features=cat_features,
        label='salary',
        training=False,
        encoder=encoder,
        lb=lb
    )

    model = train_model(X_train, y_train, args.model_random_state)

    y_pred_proba = inference(model, X_test)
    y_pred = y_pred_proba[:, 1].round()

    precision, recall, fbeta = compute_model_metrics(y_test, y_pred)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='A very basic data cleaning')

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
        '--test_size',
        type=float,
        default=0.2,
        help='Test size for train-test split',
        required=True
    )

    parser.add_argument(
        '--model_random_state',
        type=int,
        help='Random seed for model',
        required=True
    )

    args = parser.parse_args()

    go(args)
