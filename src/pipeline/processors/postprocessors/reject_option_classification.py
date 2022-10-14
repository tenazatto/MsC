import tensorflow as tf

from aif360.algorithms.inprocessing import PrejudiceRemover, AdversarialDebiasing
from aif360.algorithms.postprocessing import RejectOptionClassification

from src.pipeline.pipe_filter.pipe import BaseFilter


class RejectOptionClassificationFilter(BaseFilter):

    def reject_option_classification(self):
        att = self.input

        ROC = RejectOptionClassification(unprivileged_groups=att['unprivileged_group'],
                                         privileged_groups=att['privileged_group'])

        df_aif_val_pred = att['df_aif_val'].copy()
        df_aif_val_pred.labels = att['y_pred']
        df_aif_val_pred.scores = att['scores']

        ROC.fit(att['df_aif_val'], df_aif_val_pred)

        result = ROC.predict(att['df_aif_te'])

        return result.labels

    def execute(self):
        y_pred = self.reject_option_classification()

        self.output = {
            'y_pred': y_pred
        }
