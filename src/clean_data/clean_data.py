'''
Module for cleaning the raw data.

Author: Dauren Baitursyn
Date: 26.08.22
'''
import logging
import argparse
from pathlib import Path

import pandas as pd

from .helper import trim, mark_question_row

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def go(args):
    '''
    Main function for cleaning.
    '''

    logger.info('Starting cleaning data...')

    PATH_RAW_DATA = Path.cwd().joinpath(args.raw_data)
    PATH_CLEAN_DATA = Path.cwd().joinpath(args.clean_data)

    logger.info(f'Loading raw data at {PATH_RAW_DATA}')
    df = pd.read_csv(PATH_RAW_DATA)

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

    logger.info(f'Saving clean data at {PATH_CLEAN_DATA}')
    df.to_csv(PATH_CLEAN_DATA, index=False)
    logger.info('Finished cleaning data')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='A very basic data cleaning')

    parser.add_argument(
        '--raw_data',
        type=str,
        help='File path of the input data to clean',
        required=True
    )

    parser.add_argument(
        '--clean_data',
        type=str,
        help='File path of the data to save after cleaning',
        required=True
    )

    args = parser.parse_args()

    go(args)
