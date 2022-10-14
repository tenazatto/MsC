from aif360.algorithms.inprocessing import MetaFairClassifier

from src.pipeline.pipe_filter.pipe import BaseFilter


class MetaFairClassifierFilter(BaseFilter):
    tau = 0.8
    classifier_type = 'fdr'

    def __init__(self, tau=0.8, classifier_type='fdr'):
        self.tau = tau
        self.classifier_type = classifier_type

    def meta_fair_classifier(self):
        att = self.input

        # sr: tau = 0.7
        # fdr: tau = 0.8
        debiased_model = MetaFairClassifier(tau=self.tau, sensitive_attr=att['protected_attribute_names'][0],
                                            type=self.classifier_type)

        debiased_model.fit(att['df_aif_tr'])

        result = debiased_model.predict(att['df_aif_te'])

        return result.labels

    def execute(self):
        y_pred = self.meta_fair_classifier()

        self.output = {
            'y_pred': y_pred
        }
