import pandas as pd
from aif360.algorithms.preprocessing import DisparateImpactRemover
from aif360.datasets import BinaryLabelDataset

from src.pipeline.pipe_filter.pipe import BaseFilter


class DisparateImpactRemoverUnbiasAlgorithm(BaseFilter):

    def disparate_impact_preprocess(self):
        att = self.input

        df_aif_tr = BinaryLabelDataset(df=pd.concat((att['x_train'], att['y_train']), axis=1), label_names=att['label_names'],
                                    protected_attribute_names=att['protected_attribute_names'])
        print(df_aif_tr)

        df_aif_te = BinaryLabelDataset(df=pd.concat((att['x_test'], att['y_test']), axis=1), label_names=att['label_names'],
                                    protected_attribute_names=att['protected_attribute_names'])
        print(df_aif_te)

        di = DisparateImpactRemover(repair_level=1)
        df_aif_di_tr = di.fit_transform(df_aif_tr)
        df_aif_di_te = di.fit_transform(df_aif_te)

        x_di_train = df_aif_di_tr.features
        x_di_test = df_aif_di_te.features
        y_di_train = df_aif_di_tr.labels.ravel()

        return x_di_train, x_di_test, y_di_train, df_aif_te

    def execute(self):
        x_di_train, x_di_test, y_di_train, df_aif_te = self.disparate_impact_preprocess()

        self.output = {
            'x_train': x_di_train,
            'x_test': x_di_test,
            'y_train': y_di_train,
            'y_test': self.input['y_test'],
            'df_aif': df_aif_te,
            'checksum': self.input['checksum']
        }
