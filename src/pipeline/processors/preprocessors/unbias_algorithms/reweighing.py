from aif360.datasets import BinaryLabelDataset
from aif360.algorithms.preprocessing import Reweighing

from src.pipeline.pipe_filter.pipe import BaseFilter

import pandas as pd


class ReweighingUnbiasAlgorithm(BaseFilter):

    def reweighing_preprocess(self):
        att = self.input

        df_aif = BinaryLabelDataset(df=pd.concat((att['x_train'], att['y_train']), axis=1), label_names=att['label_names'],
                                    protected_attribute_names=att['protected_attribute_names'])
        print(df_aif)

        RW = Reweighing(att['unprivileged_group'], att['privileged_group'])
        df_aif_rw = RW.fit_transform(df_aif)

        return df_aif_rw

    def execute(self):
        df_aif_rw = self.reweighing_preprocess()

        self.output = {
            'x_train': self.input['x_train'],
            'x_test': self.input['x_test'],
            'y_train': self.input['y_train'],
            'y_test': self.input['y_test'],
            'df_aif': df_aif_rw,
            'checksum': self.input['checksum']
        }
