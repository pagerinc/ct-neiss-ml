import pytest
from etl_utils.etl_constants import ColNames as cols, FeConstants as fec
from etl_utils.feature_extractor import FeatureExtractor
import pandas as pd

def test_extract_features():
    """
    Test feature_extractor.extract_features
    :return: None
    """
    test_data = {cols.TRMT_DATE: ['11/12/2013'],
                 cols.STRATUM: ['V'],
                 cols.AGE: [20],
                 cols.SEX: [1],
                 cols.RACE: [5],
                 cols.DIAG: [59],
                 cols.BODY_PART: [77],
                 cols.LOCATION: [4],
                 cols.PROD1: [1807]}
    feat = FeatureExtractor(test_data)
    expected = pd.read_csv('expected/extract_features.tsv', sep='\t')
    observed = feat.extract_features()
    assert all([round(exp,6) == round(obs,6) for exp, obs in zip(expected.ix[0].values, observed.ix[0].values)])

    # TODO: add more cases to try to break fxn

def test_extract_month():
    """
    Test feature_extractor._extract_month
    :return: None
    """
    # TODO: inplement

def test_standardize_age():
    """
    Test feature_extractor._standardize_age
    :return: None
    """
    # TODO: inplement

def test_nominal_to_dummies():
    """
    Test feature_extractor._nominal_to_dummies
    :return: None
    """
    test_data = {cols.TRMT_DATE: ['11/12/2013'],
                 cols.STRATUM: ['V'],
                 cols.AGE: [20],
                 cols.SEX: [1],
                 cols.RACE: [5],
                 cols.DIAG: [59],
                 cols.BODY_PART: ['77'],
                 cols.LOCATION: [4],
                 cols.PROD1: [1807]}
    feat = FeatureExtractor(test_data)
    expected_vals = pd.read_csv('expected/nominal_to_dummies.tsv', sep='\t')
    observed = feat._nominal_to_dummies(fec.NOMINAL_FEATS)

    assert all([exp == obs for exp,obs in zip(expected_vals.ix[0].values,observed.ix[0].values)])

    # TODO: add more cases to try to break fxn

def test_validate_inputs():
    """
    Test feature_extractor._validate_inputs
    :return: None
    """
    # TODO: inplement

def test_consolidate_df():
    """
    Test feature_extractor._validate_inputs
    :return: None
    """
    # TODO: inplement

if __name__ == '__main__':
    # uncomment the functions below when implemented
    test_extract_features()
    # test_extract_month()
    # test_standardize_age()
    test_nominal_to_dummies()
    # test consolidate_df(