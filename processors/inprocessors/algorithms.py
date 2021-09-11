from aif360.algorithms.inprocessing import PrejudiceRemover
from sklearn.linear_model import LogisticRegression


def logistic_regression(x_train, y_train, x_test):
    reg = LogisticRegression(max_iter=10000)
    reg.fit(x_train, y_train)

    y_pred = reg.predict(x_test)

    return y_pred


def logistic_regression_weighed(x_train, y_train, x_test, instance_weights):
    reg = LogisticRegression(max_iter=10000)
    reg.fit(x_train, y_train, sample_weight=instance_weights)

    y_pred = reg.predict(x_test)

    return y_pred


def prejudice_remover(dataset_tr, dataset_te):
    sens_attr = dataset_tr.protected_attribute_names[0]

    model = PrejudiceRemover(sensitive_attr=sens_attr, eta=25.0)
    model.fit(dataset_tr)

    result = model.predict(dataset_te)

    return result.labels
