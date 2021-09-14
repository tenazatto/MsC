import pandas as pd

from aif360.datasets import BinaryLabelDataset
from aif360.metrics import ClassificationMetric
from sklearn import metrics

from metrics.explainer import EnhancedMetricTextExplainer


def disparate_impact_remover_metrics(df_aif_te, y_pred, preprocessor):
    df_aif_te_pred = df_aif_te.copy()
    df_aif_te_pred.labels = y_pred

    print('------------UNBIASED DATASET--------------')
    metric = ClassificationMetric(df_aif_te, df_aif_te_pred, preprocessor.unprivileged_group, preprocessor.privileged_group)
    explainer = EnhancedMetricTextExplainer(metric)
    explainer.explain()
    print('----------------------------------------')

    return metric, explainer

def prejudice_remover_metrics(dataset_te, y_pred, preprocessor):
    dataset_te_pred = dataset_te.copy()
    dataset_te_pred.labels = y_pred

    print('------------UNBIASED DATASET--------------')
    metric = ClassificationMetric(dataset_te, dataset_te_pred, preprocessor.unprivileged_group, preprocessor.privileged_group)
    explainer = EnhancedMetricTextExplainer(metric)
    explainer.explain()
    print('----------------------------------------')

    return metric, explainer

def ml_model_metrics(x_test, y_test, y_pred, preprocessor):
    df_aif = BinaryLabelDataset(df=pd.concat((x_test, y_test), axis=1), label_names=preprocessor.label_names,
                                protected_attribute_names=preprocessor.protected_attribute_names)
    print(df_aif)

    y_pred_df = pd.DataFrame(y_pred, columns=preprocessor.label_names, index=y_test.index)
    df_aif_pred = BinaryLabelDataset(df=pd.concat((x_test, y_pred_df), axis=1), label_names=preprocessor.label_names,
                                     protected_attribute_names=preprocessor.protected_attribute_names)
    print(df_aif_pred)

    print('------------UNBIASED DATASET--------------')
    metric = ClassificationMetric(df_aif, df_aif_pred, preprocessor.unprivileged_group, preprocessor.privileged_group)
    explainer = EnhancedMetricTextExplainer(metric)
    explainer.explain()
    print('----------------------------------------')

    return metric, explainer

def print_metrics(y_test, y_pred, explainer, is_biased):
    dataset_str = 'BIASED DATASET' if is_biased else 'UNBIASED DATASET'

    print('------------' + dataset_str + '--------------')
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print("Precision:", metrics.precision_score(y_test, y_pred))
    print("Recall:", metrics.recall_score(y_test, y_pred))
    print("F1-Score:", metrics.f1_score(y_test, y_pred))
    print("Fairness Score:", fairness_score(explainer))
    print("Score-ML+F:", ml_fairness_score(y_test, y_pred, explainer))
    print('----------------------------------------')


def ml_fairness_score(y_test, y_pred, explainer):
    return 0.33 * metrics.accuracy_score(y_test, y_pred) + 0.33 * metrics.f1_score(y_test, y_pred) + \
           0.34 * fairness_score(explainer)


def fairness_score(explainer):
    return float(0.2 * explainer.metric.average_abs_odds_difference() + 0.2 * explainer.metric.disparate_impact() + \
                 0.2 * explainer.metric.equal_opportunity_difference() + 0.2 * explainer.metric.theil_index() + \
                 0.2 * explainer.metric.statistical_parity_difference())
