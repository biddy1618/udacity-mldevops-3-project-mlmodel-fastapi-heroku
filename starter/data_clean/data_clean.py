'''
Module for cleaning the raw data.

Author: Dauren Baitursyn
Date: 26.08.22
'''
import logging
from pathlib import Path

import pandas as pd


PATH_DATA_RAW = Path(__file__).parents[1] / 'data/census.csv'
PATH_DATA_CLEAN = Path(__file__).parents[1] / 'data/census_clean.csv'

logging.basicConfig(level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def clean_data():

    def _trim(dataset):
        def trim(x): return x.strip() if isinstance(x, str) else x
        dataset.columns = [trim(col) for col in dataset.columns]
        return dataset.applymap(trim)

    def _find_question_mark(row):
        return row.astype(str).str.contains('?', regex=False).any()

    df = pd.read_csv(PATH_DATA_RAW)
    df.head()

    logger.info(f'Trailing spaces: \n{df.columns.tolist()[:5]} ...')
    df = _trim(df)
    logger.info(f'Removing spaces: \n{df.columns.tolist()[:5]} ...')

    logger.info(
        f'Number of rows containing `?`: \
            {df.apply(_find_question_mark, axis=1).sum()}')
    df.replace({'?': 'Unknown'}, inplace=True)
    logger.info(
        f'Number of rows containing `?` after replacement: \
            {df.apply(_find_question_mark, axis=1).sum()}')

    logger.info(f'Number of rows: {df.shape[0]}')
    df.drop_duplicates(inplace=True)
    logger.info(f'Number of rows after duplicates drop: {df.shape[0]}')

    df.to_csv(PATH_DATA_CLEAN, index=False)


if __name__ == '__main__':
    clean_data()
