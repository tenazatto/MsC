from aif360.metrics import ClassificationMetric

from src.pipeline.metrics.explainer import EnhancedMetricTextExplainer
from src.pipeline.pipe_filter.pipe import BaseFilter


class DisparateImpactRemoverMetricsFilter(BaseFilter):
    def disparate_impact_remover_metrics(self):
        att = self.input

        df_aif_te_pred = att['df_aif'].copy()
        df_aif_te_pred.labels = att['y_pred']

        metric = ClassificationMetric(att['df_aif'], df_aif_te_pred, att['unprivileged_group'],
                                      att['privileged_group'])
        explainer = EnhancedMetricTextExplainer(metric)

        return metric, explainer

    def execute(self):
        metric, explainer = self.disparate_impact_remover_metrics()

        self.output = {
            'y_test': self.input['y_test'],
            'y_pred': self.input['y_pred'],
            'metric': metric,
            'explainer': explainer
        }
