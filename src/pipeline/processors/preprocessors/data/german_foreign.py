import pandas as pd
from aif360.algorithms.preprocessing.optim_preproc_helpers.distortion_functions import get_distortion_german

from src.pipeline.processors.preprocessors.data.fairness import FairnessPreprocessor, FairnessPipe


class GermanForeignFairnessPipe(FairnessPipe):
    privileged_group = [{'foreign': 0}]
    unprivileged_group = [{'foreign': 1}]

    label_names = ['risk']
    protected_attribute_names = ['foreign']

    optim_options = {
        "distortion_fun": get_distortion_german,
        "epsilon": 0.05,
        "clist": [0.99, 1.99, 2.99],
        "dlist": [.1, 0.05, 0]
    }

    def __init__(self):
        super().__init__()


class GermanForeignPreprocessor(FairnessPreprocessor):
    def dataset_preprocess(self, df):
        df.info()

        df['checking_account'] = df['checking_account'].map(
            {'<0': 1, '0<=x<200': 2, '>=200': 3, 'None': 0}).astype(str)
        df['credit_history'] = df['credit_history'].map(
            {'no_credits_taken': 1, 'all_credits_paid_bank': 2,
             'existing_credits_paid': 3, 'delay_in_past': 4, 'critical': 5}).astype(str)
        df['purpose'] = df['purpose'].map(
            {'car_new': 1, 'car_used': 2, 'furniture/equipment': 3, 'radio/tv': 4,
             'domestic_appliances': 5, 'repairs': 6, 'education': 7, 'vacation': 8, 'retraining': 9,
             'business': 10, 'others': 11}).astype(str)
        df['savings_account'] = df['savings_account'].map(
            {'<100': 1, '100<=x<500': 2, '500<=x<1000': 3, '>=1000': 4, 'unknown': 0}).astype(int)
        df['present_employment_since'] = df['present_employment_since'].map(
            {'unemployed': 0, '<1': 1, '1<=x<4': 2, '4<=x<7': 3, '>=7': 4}).astype(int)
        df['personal_status_sex'] = df['personal_status_sex'].map(
            {'male_divorced/separated': 1, 'female_divorced/separated/married': 2, 'male_single': 3,
             'male_married/widowed': 4, 'female_single': 5}).astype(int)
        df['other_debtors_guarantors'] = df['other_debtors_guarantors'].map(
            {'None': 0, 'co-applicant': 1, 'guarantor': 2}).astype(int)
        df['property'] = df['property'].map(
            {'real_estate': 1, 'savings_insurance': 2, 'car_other': 3, 'unknown': 0}).astype(int)
        df['installment_plans'] = df['installment_plans'].map(
            {'bank': 1, 'stores': 2, 'None': 3}).astype(int)
        df['housing'] = df['housing'].map(
            {'rent': 1, 'own': 2, 'for_free': 3}).astype(int)
        df['job'] = df['job'].map(
            {'unemployed': 0, 'unskilled': 1, 'skilled': 2, 'management': 3}).astype(int)
        df['telephone'] = df['telephone'].map(
            {'yes': 1, 'none': 0}).astype(int)
        df['foreign'] = df['foreign'].map(
            {'yes': 1, 'no': 0}).astype(int)
        df['risk'] = df['risk'].map(
            {'good': 1, 'bad': 0}).astype(int)

        df_x = df.drop('risk', axis=1)
        df_y = pd.DataFrame(df.risk)

        return df_x, df_y
