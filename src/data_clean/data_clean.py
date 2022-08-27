'''
Module for cleaning the raw data.

Author: Dauren Baitursyn
Date: 26.08.22
'''
import logging
import argparse
from pathlib import Path

import pandas as pd

from helper import trim, mark_question_row

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def go(args):
    '''
    Main function for cleaning.
    '''

    logger.info('Starting cleaning data...')

    PATH_DATA_RAW = Path.cwd().joinpath(args.data_raw)
    PATH_DATA_CLEAN = Path.cwd().joinpath(args.data_clean)

    logger.info(f'Loading raw data at {PATH_DATA_RAW}')
    df = pd.read_csv(PATH_DATA_RAW)

    logger.info(f'Trailing and leading spaces: {df.columns.tolist()[:5]} ...')
    df = trim(df)
    logger.info(f'Removing spaces: {df.columns.tolist()[:5]} ...')

    logger.info(
        ('Number of rows containing `?`: '
         f'{df.apply(mark_question_row, axis=1).sum()}'))
    df.replace({'?': 'Unknown'}, inplace=True)
    logger.info(
        ('Number of rows containing `?` after replacement: '
         f'{df.apply(mark_question_row, axis=1).sum()}'))

    logger.info(f'Number of rows: {df.shape[0]}')
    df.drop_duplicates(inplace=True)
    logger.info(f'Number of rows after duplicates drop: {df.shape[0]}')

    logger.info(f'Saving clean data at {PATH_DATA_CLEAN}')
    df.to_csv(PATH_DATA_CLEAN, index=False)
    logger.info('Finished cleaning data')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='A very basic data cleaning')

    parser.add_argument(
        '--data_raw',
        type=str,
        help='Path of the input data to clean',
        required=True
    )

    parser.add_argument(
        '--data_clean',
        type=str,
        help='Path of the data to save after cleaning',
        required=True
    )

    args = parser.parse_args()

    go(args)
