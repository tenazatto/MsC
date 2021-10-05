import pandas as pd
from aif360.datasets import BinaryLabelDataset

from pipeline.pipe_filter.pipe import BaseFilter


class PrejudiceRemoverUnbiasAlgorithm(BaseFilter):

    def prejudice_remover_preprocess(self):
        att = self.input

        df_aif_tr = BinaryLabelDataset(df=pd.concat((att['x_train'], att['y_train']), axis=1), label_names=att['label_names'],
                                    protected_attribute_names=att['protected_attribute_names'])
        print(df_aif_tr)

        df_aif_te = BinaryLabelDataset(df=pd.concat((att['x_test'], att['y_test']), axis=1), label_names=att['label_names'],
                                    protected_attribute_names=att['protected_attribute_names'])
        print(df_aif_te)

        return df_aif_tr, df_aif_te

    def execute(self):
        df_aif_tr, df_aif_te = self.prejudice_remover_preprocess()

        self.output = {
            'df_aif_tr': df_aif_tr,
            'df_aif_te': df_aif_te,
            'y_test': self.input['y_test']
        }
