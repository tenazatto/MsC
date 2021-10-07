import tensorflow as tf

from aif360.algorithms.inprocessing import PrejudiceRemover, AdversarialDebiasing

from pipeline.pipe_filter.pipe import BaseFilter


class AdversarialDebiasingFilter(BaseFilter):
    max_iter = 10000
    weighed = False

    def __init__(self, max_iter=10000, weighed=False):
        self.max_iter = max_iter
        self.weighed = weighed

    def adversarial_debiasing(self):
        att = self.input

        sess = tf.compat.v1.Session()
        tf.compat.v1.disable_eager_execution()

        debiased_model = AdversarialDebiasing(privileged_groups=att['privileged_group'],
                                              unprivileged_groups=att['unprivileged_group'],
                                              scope_name='debiased_classifier',
                                              num_epochs=10,
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
