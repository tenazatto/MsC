import pandas as pd
from aif360.algorithms.preprocessing.optim_preproc_helpers.distortion_functions import get_distortion_german

from src.pipeline.processors.preprocessors.data.fairness import FairnessPreprocessor, FairnessPipe


class LendingclubIncomeFairnessPipe(FairnessPipe):
    privileged_group = [{'annual_inc': 1}]
    unprivileged_group = [{'annual_inc': 0}]

    label_names = ['loan_status']
    protected_attribute_names = ['annual_inc']

    optim_options = {
        "distortion_fun": get_distortion_german,
        "epsilon": 0.05,
        "clist": [0.99, 1.99, 2.99],
        "dlist": [.1, 0.05, 0]
    }

    def __init__(self):
        super().__init__()


class LendingclubIncomePreprocessor(FairnessPreprocessor):
    def dataset_preprocess(self, df):
        df.info()

        SAMPLE_PERCENTAGE = 10
        df_sample_nok = df[df['loan_status'] == 'Charged Off'].sample(frac=SAMPLE_PERCENTAGE/100)
        df_sample_ok = df[df['loan_status'] == 'Fully Paid'].sample(frac=SAMPLE_PERCENTAGE / 100)
        df_sample = pd.concat([df_sample_ok, df_sample_nok])

        df_x = df_sample.drop('loan_status', axis=1)
        df_y = pd.DataFrame(df_sample.loan_status)

        annual_minimum_wage = 15312
        label_feature_columns = ['term', 'grade', 'sub_grade', 'emp_title', 'emp_length', 'home_ownership',
                                 'verification_status', 'issue_d', 'purpose', 'zip_code', 'addr_state',
                                 'earliest_cr_line', 'initial_list_status', 'last_pymnt_d', 'last_credit_pull_d',
                                 'application_type', 'verification_status_joint', 'sec_app_earliest_cr_line',
                                 'hardship_type', 'hardship_reason', 'hardship_status', 'hardship_start_date',
                                 'hardship_end_date', 'payment_plan_start_date', 'hardship_loan_status',
                                 'disbursement_method', 'debt_settlement_flag', 'debt_settlement_flag_date',
                                 'settlement_status', 'settlement_date']

        label_feature_columns = list(filter(lambda col: col in df_x.columns, label_feature_columns))

        labels = [(col, df_x[col].astype('category').cat.categories) for col in label_feature_columns]
        labels_encoded = {col: {cat: (n if '0.0' in category else n + 1)
                                for n, cat in enumerate(category)}
                          for col, category in labels}

        for label_column in label_feature_columns:
            df_x[label_column] = df_x[label_column].map(labels_encoded[label_column]).astype(int)

        df_x['annual_inc'] = df_x['annual_inc'].map(lambda inc: 0 if inc <= annual_minimum_wage else 1).astype(int)

        df_y['loan_status'] = df_y['loan_status'].map(
            {'Fully Paid': 1, 'Charged Off': 0}).astype(int)

        return df_x, df_y
