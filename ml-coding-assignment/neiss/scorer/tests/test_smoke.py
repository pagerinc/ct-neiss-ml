import pytest
import numpy as np
from etl_utils.etl_constants import ColNames as cols
from scorer.scorer import Scorer

def test_smoke():
    """
    Simple smoke test, designed to see if anything is critically wrong with MVP functionality. Only expectation is that
    model predicts a class given an input.
    :return: None
    """
    # test that model scores on pre-engineered feature data
    sample_feats = np.reshape([5.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                               0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,
                               0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
                               0.0,0.0,0.0,1.0,6,0.00258081716229,0.00137894457704,0.00221744814915,0.00140578204266,
                               0.00103914097679,0.000878734622144,0.00714285714286,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,
                               0.0,1.0,0.0,0.0,1.0,0.0,0.0], newshape=(1,-1))
    s = Scorer()
    assert s.model.predict(sample_feats)[0] in {1,2,4,5,6,8,9} # no 3 or 7 codes in coding scheme

    # test on raw input data
    test_data = {cols.TRMT_DATE: ['11/12/2013'],
                 cols.STRATUM: ['V'],
                 cols.AGE: [20],
                 cols.SEX: [1],
                 cols.RACE: [5],
                 cols.DIAG: [59],
                 cols.BODY_PART: [77],
                 cols.LOCATION: [4],
                 cols.PROD1: [1807]}
    assert s.score(test_data)[0] in {1, 2, 4, 5, 6, 8, 9}

    # trying a little harder to break it
    test_data = {cols.TRMT_DATE: ['11/12/2013'],
                 cols.STRATUM: [np.nan],
                 cols.AGE: [20],
                 cols.SEX: [np.nan],
                 cols.RACE: [np.nan],
                 cols.DIAG: [np.nan],
                 cols.BODY_PART: [np.nan],
                 cols.LOCATION: [np.nan],
                 cols.PROD1: [np.nan]}
    result = s.score(test_data)
    assert s.score(test_data)[0] in {1, 2, 4, 5, 6, 8, 9}

    #  try string ints
    test_data = {cols.TRMT_DATE: ['11/12/2013'],
                 cols.STRATUM: [np.nan],
                 cols.AGE: ['20'],
                 cols.SEX: [np.nan],
                 cols.RACE: [np.nan],
                 cols.DIAG: [np.nan],
                 cols.BODY_PART: [np.nan],
                 cols.LOCATION: [np.nan],
                 cols.PROD1: [np.nan]}
    result = s.score(test_data)[0]
    assert result in {1, 2, 4, 5, 6, 8, 9}

    #  try expdcting a prediction other than one (model-dependent test)
    test_data = {cols.TRMT_DATE: ['11/12/2013'],
                 cols.STRATUM: ['S'],
                 cols.AGE: ['20'],
                 cols.SEX: ['1'],
                 cols.RACE: ['1'],
                 cols.DIAG: ['62'],
                 cols.BODY_PART: ['31'],
                 cols.LOCATION: ['1'],
                 cols.PROD1: ['1411']}
    result = s.score(test_data)[0]
    assert result != 1



if __name__ == '__main__':
    test_smoke()