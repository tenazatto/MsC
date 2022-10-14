from sklearn.linear_model import LogisticRegression

from src.pipeline.pipe_filter.pipe import BaseFilter


class LogisticRegressionFilter(BaseFilter):
    max_iter = 10000
    weighed = False
    class_weight = None
    solver = 'lbfgs'

    def __init__(self, max_iter=10000, weighed=False, class_weight=None, solver='lbfgs'):
        self.max_iter = max_iter
        self.weighed = weighed
        self.class_weight = class_weight
        self.solver = solver

    def logistic_regression(self):
        att = self.input

        reg = LogisticRegression(max_iter=self.max_iter, class_weight=self.class_weight, solver=self.solver)
        reg.fit(att['x_train'], att['y_train'])

        y_pred = reg.predict(att['x_test'])
        scores = reg.predict_proba(att['x_test'])[:,1].reshape(-1, 1)

        return y_pred, scores

    def logistic_regression_weighed(self):
        att = self.input

        reg = LogisticRegression(max_iter=self.max_iter, class_weight=self.class_weight, solver=self.solver)
        reg.fit(att['x_train'], att['y_train'], sample_weight=att['df_aif'].instance_weights)

        y_pred = reg.predict(att['x_test'])
        scores = reg.predict_proba(att['x_test'])[:,1].reshape(-1, 1)

        return y_pred, scores

    def execute(self):
        y_pred, scores = self.logistic_regression_weighed() if self.weighed else self.logistic_regression()

        self.output = {
            'y_pred': y_pred,
            'scores': scores
        }
