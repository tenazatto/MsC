from sklearn import metrics

from src.pipeline.pipe_filter.pipe import BaseFilter


class MetricsPrintFilter(BaseFilter):
    def print_metrics(self, y_test, y_pred, explainer, is_biased):
        dataset_str = 'BIASED DATASET' if is_biased else 'UNBIASED DATASET'

        print('------------' + dataset_str + '--------------')
        print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
        print("Precision:", metrics.precision_score(y_test, y_pred))
        print("Recall:", metrics.recall_score(y_test, y_pred))
        print("F1-Score:", metrics.f1_score(y_test, y_pred))
        print("Fairness Score:", self.fairness_score(explainer))
        print("Score-ML+F:", self.ml_fairness_score(y_test, y_pred, explainer))
        print('----------------------------------------')

    # verificar média harmônica TODO
    def ml_fairness_score(self, y_test, y_pred, explainer):
        return 0.33 * metrics.accuracy_score(y_test, y_pred) + 0.33 * metrics.f1_score(y_test, y_pred) + \
               0.34 * self.fairness_score(explainer)


    def fairness_score(self, explainer):
        return float(0.2 * self.normalize_diff(abs(explainer.metric.average_abs_odds_difference())) +
                     0.2 * self.normalize_ratio(explainer.metric.disparate_impact()) +
                     0.2 * self.normalize_diff(abs(explainer.metric.equal_opportunity_difference())) +
                     0.2 * self.normalize_diff(abs(explainer.metric.theil_index())) +
                     0.2 * self.normalize_diff(abs(explainer.metric.statistical_parity_difference())))


    def normalize_ratio(self, metric):
        return 1 / metric if metric > 1 else metric


    def normalize_diff(self, metric):
        return abs(1-metric)

    def execute(self):
        metrics_summary = self.input['explainer'].explain_dict()
        metrics_summary['metrics']['f1_score'] = {
            'name': 'F1-Score',
            'value': metrics.f1_score(self.input['y_test'], self.input['y_pred']),
            'explanation': 'the harmonic mean of the precision and recall (2 * precision * recall / (precision + recall))'
        }
        metrics_summary['metrics']['auc'] = {
            'name': 'AUC Score',
            'value': metrics.roc_auc_score(self.input['y_test'], self.input['y_pred']),
            'explanation': 'Area Under the ROC Curve'
        }
        print(metrics_summary)
        self.print_metrics(self.input['y_test'], self.input['y_pred'], self.input['explainer'], True)

        self.output = self.input
        self.output['metrics_summary'] = metrics_summary['metrics']
