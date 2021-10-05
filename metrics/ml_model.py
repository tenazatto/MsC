import pandas as pd

from aif360.datasets import BinaryLabelDataset
from aif360.metrics import ClassificationMetric

from metrics.explainer import EnhancedMetricTextExplainer
from pipeline.pipe_filter.pipe import BaseFilter


class MLModelMetricsFilter(BaseFilter):
    def ml_model_metrics(self):
        att = self.input

        df_aif = BinaryLabelDataset(df=pd.concat((att['x_test'], att['y_test']), axis=1), label_names=att['label_names'],
                                    protected_attribute_names=att['protected_attribute_names'])
        print(df_aif)

        y_pred_df = pd.DataFrame(att['y_pred'], columns=att['label_names'], index=att['y_test'].index)
        df_aif_pred = BinaryLabelDataset(df=pd.concat((att['x_test'], y_pred_df), axis=1),
                                         label_names=att['label_names'],
                                         protected_attribute_names=att['protected_attribute_names'])
        print(df_aif_pred)

        print('------------UNBIASED DATASET--------------')
        metric = ClassificationMetric(df_aif, df_aif_pred, att['unprivileged_group'],
                                      att['privileged_group'])
        explainer = EnhancedMetricTextExplainer(metric)
        explainer.explain()
        print('----------------------------------------')

        return metric, explainer

    def execute(self):
        metric, explainer = self.ml_model_metrics()

        self.output = {
            'metric': metric,
            'explainer': explainer
        }
