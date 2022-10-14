import tensorflow as tf
from aif360.algorithms.inprocessing import AdversarialDebiasing

from src.pipeline.pipe_filter.pipe import BaseFilter


class AdversarialDebiasingFilter(BaseFilter):
    num_epochs = 10

    def __init__(self, num_epochs=10):
        self.num_epochs = num_epochs

    def adversarial_debiasing(self):
        att = self.input

        sess = tf.compat.v1.Session()
        tf.compat.v1.disable_eager_execution()

        debiased_model = AdversarialDebiasing(privileged_groups=att['privileged_group'],
                                              unprivileged_groups=att['unprivileged_group'],
                                              scope_name='debiased_classifier',
                                              num_epochs=self.num_epochs,
                                              debias=True,
                                              sess=sess)

        debiased_model.fit(att['df_aif_tr'])

        result = debiased_model.predict(att['df_aif_te'])

        return result.labels

    def execute(self):
        y_pred = self.adversarial_debiasing()

        self.output = {
            'y_pred': y_pred
        }
