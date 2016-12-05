import pandas as pd
import numpy as np
from etl_constants import FeConstants as fec, ColNames as col, FeatNames as fnames

class FeatureExtractor:
    """
    # TODO: document
    """

    def __init__(self, patient_data):
        """
        # TODO: doc
        :param patient_data:
        """
        self.raw_df = self._validate_inputs(patient_data)
        self.processed_df = None

    def extract_features(self, keep_weight_vector=False):
        """
        ### TODO: doc
        :param keep_weight_vector:
        :return:
        """
        # extract month information from dates
        self.raw_df[fnames.MONTH] = self.raw_df[col.TRMT_DATE].apply(self._extract_month)

        # NEISS encodes age in months as 2XX where XX is the number of months
        self._standardize_age()

        # convert categorical/nominal variables into binary indicators
        self.processed_df = self._nominal_to_dummies(fec.NOMINAL_FEATS)

        # transform product codes -->
        self._extract_product_code_info()

        # combine extracted binary features with transformed features we want to keep
        self._consolidate_df(keep_weight_vector)

        return self.processed_df

    def _extract_product_code_info(self):
        """
        Convert product codes into vectors of their conditional likelihood (frequency in data given each outcome)
        :return: None
        """
        import pickle, os
        # TODO: parameterize all the strings in this function
        etl_rec_dir = 'etl_utils/resources/'
        neiss_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        load_path = os.path.join(neiss_path,etl_rec_dir, 'total_outcome_freqs.pkl')
        outcome_df = pickle.load(open(load_path, 'rb+'))
        for target in sorted(fec.VALID_DISPOSITIONS):
            new_col = 'prod_targ_{0}'.format(target)
            load_path = os.path.join(neiss_path, etl_rec_dir, '{0}.pkl'.format(new_col))
            # load dictionary of products and their observed frequencies with these outcomes
            disp_dict = pickle.load(open(load_path, 'rb+'))
            total_target = float(outcome_df[target][0])
            self.processed_df[new_col] = [disp_dict[prod] / total_target if prod in disp_dict
                                     else 1 / total_target
                                     for prod in self.raw_df['prod1'].values]

    def _consolidate_df(self, keep_weight_vector):
        """
        # combine extracted binary features with transformed features we want to keep
        :param keep_weight_vector: bool indicating whether or not weight vector should be included in processed df
        :return: None
        """
        # combine extracted binary features with transformed features we want to keep
        for feat in fec.TO_ADD + keep_weight_vector*[col.WEIGHT]: # only include weight vector if explictly asked
            self.processed_df[feat] = self.raw_df[feat]

        # sort column names alphabetically, for consistency of input ordering expected by models
        all_ext_features = sorted([n.lower() for n in dir(fnames) if '__' not in n])
        all_ext_features.remove(fnames.DISPOSITION)
        self.processed_df = self.processed_df[all_ext_features]


    def _extract_month(self, dt_str, fmt=fec.DT_FMT):
        """
        extract month information from dates
        :param date_str: ### TODO: doc
        :param fmt: ### TODO: doc
        :return:
        """
        from datetime import datetime as dt
        try:
            val = int(dt.strptime(dt_str, fmt).strftime(fec.MONTH_FMT))
        except TypeError:
            val = np.nan
        return val

    def _standardize_age(self):
        """
        NEISS encodes age in months as 2XX where XX is the number of months.
        :return: standardized float vector representing age in years
        """
        standardize_age = lambda age: (age - 200) / 12.0 if age > 200 else float(age)
        self.raw_df[col.AGE] = self.raw_df[col.AGE].apply(standardize_age)

    def _nominal_to_dummies(self, nom_features):
        """
        convert categorical/nominal variables into binary indicators
        :param nom_features:
        :return:
        """
        # decomposition of observed values
        safe_tostr = lambda val: str(val) if pd.notnull(val) else val
        for nom in nom_features:
            self.raw_df.loc[:, nom] = self.raw_df[nom].apply(safe_tostr)
        dummy_df = pd.get_dummies(self.raw_df.loc[:, nom_features])

        # ensure that unobserved values are still decomposed and added to the dataframe
        all_ext_features = [s.lower() for s in dir(fnames)]
        cols_needed = set([feat for feat in all_ext_features if '_'.join(feat.split('_')[:-1]) in col.TO_DECOMPOSE])
        missing_cols = cols_needed.difference(set(dummy_df.columns))
        for missing in list(missing_cols):
            # unobserved variables have a dummy value of zero for all indices
            dummy_df[missing.lower()] = 0

        return dummy_df

    def _validate_inputs(self, inputs):
        """
        Validate that inputs can be parsed into features, and throw the appropriate error if note
        :param inputs: input data as passed to the model
        :return: None
        """
        try:
            inputs = inputs if isinstance(inputs, pd.DataFrame) else pd.DataFrame(inputs)
        except ValueError:
            raise ValueError('Could not cast inputs to pandas DataFrame.')

        # check that all the important columns are there
        missing_cols = col.CRITICAL_COLS.difference(set(inputs.columns))
        if missing_cols:
            raise ValueError('These data are missing the following columns that are '
                             'critical to feature extraction transformations:\n\t{cols}'.format(cols=missing_cols))

        # ensure that all data is of the correct type:
        for feat in fec.FLOAT_FEATS:
            try:
                inputs[feat] = [float(val) for val in inputs[feat].values] if feat in inputs.columns else np.nan
            except ValueError:
                raise ValueError('Could not convert {f} to float'.format(f=feat))
        for feat in fec.INT_FEATS + [col.PROD1, col.PROD2]:
            try:
                inputs[feat] = [int(val) if pd.notnull(val) else np.nan
                                for val in inputs[feat].values] if feat in inputs.columns else np.nan
            except ValueError as v:
                raise ValueError('Could not convert {i} to int\n\t{m}'.format(i=feat, m=v.message))


        return inputs



