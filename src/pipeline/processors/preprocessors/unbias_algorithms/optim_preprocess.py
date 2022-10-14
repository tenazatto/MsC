import pandas as pd
from aif360.algorithms.preprocessing import OptimPreproc
from aif360.algorithms.preprocessing.optim_preproc_helpers.opt_tools import OptTools
from aif360.datasets import BinaryLabelDataset

from src.pipeline.pipe_filter.pipe import BaseFilter


class OptimizedPreprocessingUnbiasAlgorithm(BaseFilter):

    def optim_preprocess(self):
        att = self.input

        df_aif = BinaryLabelDataset(df=pd.concat((att['x_train'], att['y_train']), axis=1), label_names=att['label_names'],
                                    protected_attribute_names=att['protected_attribute_names'])
        print(df_aif)

        OP = OptimPreproc(OptTools, att['optim_options'], att['unprivileged_group'], att['privileged_group'])
        df_aif_op = OP.fit_transform(df_aif)
        df_aif_op = df_aif.align_datasets(df_aif_op)

        return df_aif_op

    def execute(self):
        df_aif_op = self.optim_preprocess()

        self.output = {
            'x_train': self.input['x_train'],
            'x_test': self.input['x_test'],
            'y_train': self.input['y_train'],
            'y_test': self.input['y_test'],
            'df_aif': df_aif_op,
            'checksum': self.input['checksum']
        }
