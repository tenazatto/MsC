from sklearn.linear_model import LogisticRegression

from pipeline.pipe_filter.pipe import BaseFilter


class LogisticRegressionFilter(BaseFilter):
    max_iter = 10000
    weighed = False

    def __init__(self, max_iter=10000, weighed=False):
        self.max_iter = max_iter
        self.weighed = weighed

    def logistic_regression(self):
        att = self.input

        reg = LogisticRegression(max_iter=self.max_iter)
        reg.fit(att['x_train'], att['y_train'])

        y_pred = reg.predict(att['x_test'])

        return y_pred

    def logistic_regression_weighed(self):
        att = self.input

        reg = LogisticRegression(max_iter=self.max_iter)
        reg.fit(att['x_train'], att['y_train'], sample_weight=att['df_aif'].instance_weights)

        y_pred = reg.predict(att['x_test'])

        return y_pred

    def execute(self):
        y_pred = self.logistic_regression_weighed() if self.weighed else self.logistic_regression()

        self.output = {
            'y_pred': y_pred
        }
