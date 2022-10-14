from aif360.datasets import BinaryLabelDataset
from aif360.algorithms.preprocessing import Reweighing

from src.pipeline.pipe_filter.pipe import BaseFilter

import pandas as pd


class LFRUnbiasAlgorithm(BaseFilter):

    def learning_fair_representations_preprocess(self):
        att = self.input

        df_aif = BinaryLabelDataset(df=pd.concat((att['x_train'], att['y_train']), axis=1), label_names=att['label_names'],
                                    protected_attribute_names=att['protected_attribute_names'])
        print(df_aif)

        LFR_preproc = Reweighing(att['unprivileged_group'], att['privileged_group'])
        df_aif_lfr = LFR_preproc.fit_transform(df_aif)

        return df_aif_lfr

    def execute(self):
        df_aif_lfr = self.learning_fair_representations_preprocess()

        self.output = {
            'x_train': self.input['x_train'],
            'x_test': self.input['x_test'],
            'y_train': self.input['y_train'],
            'y_test': self.input['y_test'],
            'df_aif': df_aif_lfr,
            'checksum': self.input['checksum']
        }
