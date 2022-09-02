'''
Module for helper functions for cleaning data.

Author: Dauren Baitursyn
Date: 26.08.22
'''


def trim_replace(dataset):
    '''
    Clean dataset by removing leading and trailing whitespace
    and replacing hypens with underscores in columns.

    Args:
        dataset (pd.DataFrame): Input data.

    Returns:
        pd.DataFrame: Data without trailing and leading whitespace.
    '''
    dataset.columns = [col.strip() for col in dataset.columns]
    dataset.columns = [col.replace('-', '_') for col in dataset.columns]
    return dataset.applymap(
        lambda value: value.strip() if isinstance(value, str) else value)


def mark_question_row(row):
    '''
    Mark rows that have `?` mark in any of the columns.

    Args:
        row (pandas.Series): Single row of pandas.DataFrame

    Returns:
        numpy.array: Boolean values if row contains `?`.
    '''
    return row.astype(str).str.contains('?', regex=False).any()
