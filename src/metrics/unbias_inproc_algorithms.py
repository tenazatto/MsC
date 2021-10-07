from aif360.metrics import ClassificationMetric

from metrics.explainer import EnhancedMetricTextExplainer
from pipeline.pipe_filter.pipe import BaseFilter


class UnbiasInProcAlgorithmMetricsFilter(BaseFilter):
    def prejudice_remover_metrics(self):
        att = self.input

        dataset_te_pred = att['df_aif_te'].copy()
        dataset_te_pred.labels = att['y_pred']

        print('------------UNBIASED DATASET--------------')
        metric = ClassificationMetric(att['df_aif_te'], dataset_te_pred, att['unprivileged_group'],
                                      att['privileged_group'])
        explainer = EnhancedMetricTextExplainer(metric)
        explainer.explain()
        print('----------------------------------------')

        return metric, explainer

    def execute(self):
        metric, explainer = self.prejudice_remover_metrics()

        self.output = {
            'metric': metric,
            'explainer': explainer
        }