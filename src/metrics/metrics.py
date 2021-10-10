from sklearn import metrics


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
    return float(0.2 * (1-abs(explainer.metric.average_abs_odds_difference())) +
                 0.2 * explainer.metric.disparate_impact() +
                 0.2 * (1-abs(explainer.metric.equal_opportunity_difference())) +
                 0.2 * (1-abs(explainer.metric.theil_index())) +
                 0.2 * (1-abs(explainer.metric.statistical_parity_difference())))
