'''
Molule for helper functions.

Author: Dauren Baitursyn
Date: 05.09.22
'''
from .. import constants


def map_education(education):
    '''
    Map education to its ordinal integer (number).

    Args:
        df (pd.Series): Education series.

    Returns:
        pd.Series: Integener-mapped series for education column.
    '''
    return education.map(constants.education_map)
