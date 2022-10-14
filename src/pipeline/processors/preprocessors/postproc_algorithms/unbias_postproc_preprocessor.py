import pandas as pd
from aif360.datasets import BinaryLabelDataset

from src.pipeline.pipe_filter.pipe import BaseFilter


class UnbiasPostProcPreprocessor(BaseFilter):

    def unbias_postproc_preprocessor_with_validation(self):
        att = self.input

        df_aif_val = BinaryLabelDataset(df=pd.concat((att['x_val'], att['y_val']), axis=1),
                                        label_names=att['label_names'],
                                        protected_attribute_names=att['protected_attribute_names'])
        print(df_aif_val)

        df_aif_te = BinaryLabelDataset(df=pd.concat((att['x_test'], att['y_test']), axis=1),
                                       label_names=att['label_names'],
                                       protected_attribute_names=att['protected_attribute_names'])
        print(df_aif_te)

        return df_aif_val, df_aif_te

    def unbias_postproc_preprocessor(self):
        att = self.input

        df_aif_te = BinaryLabelDataset(df=pd.concat((att['x_test'], att['y_test']), axis=1),
                                       label_names=att['label_names'],
                                       protected_attribute_names=att['protected_attribute_names'])
        print(df_aif_te)

        return df_aif_te

    def execute(self):
        if 'x_val' in self.input.keys() and 'y_val' in self.input.keys():
            df_aif_val, df_aif_te = self.unbias_postproc_preprocessor_with_validation()

            self.output = {
                'x_train': self.input['x_train'],
                'y_train': self.input['y_train'],
                'x_test': self.input['x_test'],
                'df_aif_val': df_aif_val,
                'df_aif_te': df_aif_te,
                'y_test': self.input['y_test'],
                'checksum': self.input['checksum']
            }
        else:
            df_aif_te = self.unbias_postproc_preprocessor()

            self.output = {
                'x_train': self.input['x_train'],
                'y_train': self.input['y_train'],
                'x_test': self.input['x_test'],
                'df_aif_te': df_aif_te,
                'y_test': self.input['y_test'],
                'checksum': self.input['checksum']
            }
