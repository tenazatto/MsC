import numpy as np
import pandas as pd

from aif360.algorithms.preprocessing.optim_preproc_helpers.distortion_functions import get_distortion_adult

from src.pipeline.processors.preprocessors.data.fairness import FairnessPreprocessor, FairnessPipe


class AdultSexFairnessPipe(FairnessPipe):
    privileged_group = [{'Female': 0}]
    unprivileged_group = [{'Female': 1}]

    label_names = ['income']
    protected_attribute_names = ['Female']

    optim_options = {
        "distortion_fun": get_distortion_adult,
        "epsilon": 0.05,
        "clist": [0.99, 1.99, 2.99],
        "dlist": [.1, 0.05, 0]
    }

    def __init__(self):
        super().__init__()


class AdultSexPreprocessor(FairnessPreprocessor):
    def dataset_preprocess(self, df):
        df.info()

        df.rename(columns={'capital-gain': 'capital gain', 'capital-loss': 'capital loss', 'native-country': 'country',
                           'hours-per-week': 'hours per week', 'marital-status': 'marital'}, inplace=True)
        df.columns

        df['country'] = df['country'].replace('?', np.nan)
        df['workclass'] = df['workclass'].replace('?', np.nan)
        df['occupation'] = df['occupation'].replace('?', np.nan)

        df.dropna(how='any', inplace=True)

        for c in df.columns:
            print("---- %s ---" % c)
            print(df[c].value_counts())

        df['income'] = df['income'].map({'<=50K': 0, '>50K': 1}).astype(int)
        print(pd.get_dummies(df['gender']))
        df = pd.concat([df, pd.get_dummies(df['gender'])], axis=1)
        df[["Male", "Female"]] = df[["Male", "Female"]].apply(pd.to_numeric)
        df = df.drop('gender', axis=1).drop('country', axis=1)
        print(df)
        df.info()

        df['race'] = df['race'].map(
            {'Black': 0, 'Asian-Pac-Islander': 1, 'Other': 2, 'White': 3, 'Amer-Indian-Eskimo': 4}).astype(int)
        df['marital'] = df['marital'].map(
            {'Married-spouse-absent': 0, 'Widowed': 1, 'Married-civ-spouse': 2, 'Separated': 3, 'Divorced': 4,
             'Never-married': 5, 'Married-AF-spouse': 6}).astype(int)
        df['workclass'] = df['workclass'].map(
            {'Self-emp-inc': 0, 'State-gov': 1, 'Federal-gov': 2, 'Without-pay': 3, 'Local-gov': 4, 'Private': 5,
             'Self-emp-not-inc': 6}).astype(int)
        df['education'] = df['education'].map(
            {'Some-college': 0, 'Preschool': 1, '5th-6th': 2, 'HS-grad': 3, 'Masters': 4, '12th': 5, '7th-8th': 6,
             'Prof-school': 7, '1st-4th': 8, 'Assoc-acdm': 9, 'Doctorate': 10, '11th': 11, 'Bachelors': 12, '10th': 13,
             'Assoc-voc': 14, '9th': 15}).astype(int)
        df['occupation'] = df['occupation'].map(
            {'Farming-fishing': 1, 'Tech-support': 2, 'Adm-clerical': 3, 'Handlers-cleaners': 4, 'Prof-specialty': 5,
             'Machine-op-inspct': 6, 'Exec-managerial': 7, 'Priv-house-serv': 8, 'Craft-repair': 9, 'Sales': 10,
             'Transport-moving': 11, 'Armed-Forces': 12, 'Other-service': 13, 'Protective-serv': 14}).astype(int)
        df['relationship'] = df['relationship'].map(
            {'Not-in-family': 0, 'Wife': 1, 'Other-relative': 2, 'Unmarried': 3, 'Husband': 4, 'Own-child': 5}).astype(
            int)

        df_x = df.drop('income', axis=1)
        df_y = pd.DataFrame(df.income)

        return df_x, df_y
