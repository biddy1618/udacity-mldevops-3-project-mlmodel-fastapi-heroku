'''
Module for splitting data to training and test sets.

Author: Dauren Baitursyn
Date: 26.08.22
'''
import logging
import argparse
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def go(args):
    '''
    Main function for splitting data.
    '''
    logger.info('Starting splitting data...')

    PATH_CLEAN_DATA = Path.cwd().joinpath(args.clean_data)
    PATH_SPLIT_TRAIN = Path.cwd().joinpath(args.split_train)
    PATH_SPLIT_TEST = Path.cwd().joinpath(args.split_test)

    logger.info(f'Loading clean data at {PATH_CLEAN_DATA}')
    data = pd.read_csv(PATH_CLEAN_DATA)

    logger.info(f'Splitting data with test size {args.split_test_size}')
    split_train, split_test = train_test_split(
        data,
        test_size=args.split_test_size,
        random_state=args.split_random_state
    )

    logger.info(f'Saving train split at {PATH_SPLIT_TRAIN}')
    split_train.to_csv(PATH_SPLIT_TRAIN, index=False)

    logger.info(f'Saving test split at {PATH_SPLIT_TEST}')
    split_test.to_csv(PATH_SPLIT_TEST, index=False)

    logger.info('Finished splitting data')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Split clean data')

    parser.add_argument(
        '--clean_data',
        type=str,
        help='File path of the clean data',
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
        '--split_train',
        type=str,
        help='File path to save the train split',
        required=True
    )

    parser.add_argument(
        '--split_test',
        type=str,
        help='File path to save the test split',
        required=True
    )

    args = parser.parse_args()

    go(args)
