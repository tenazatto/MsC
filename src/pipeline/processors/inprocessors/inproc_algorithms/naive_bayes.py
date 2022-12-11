from sklearn.naive_bayes import GaussianNB

from src.pipeline.pipe_filter.pipe import BaseFilter

class NaiveBayesFilter(BaseFilter):
    weighed = False

    def __init__(self, weighed=False):
        self.weighed = weighed

    def gaussian_nb(self):
        att = self.input

        reg = GaussianNB()
        reg.fit(att['x_train'], att['y_train'])

        y_pred = reg.predict(att['x_test'])
        scores = reg.predict_proba(att['x_test'])[:,1].reshape(-1, 1)

        return y_pred, scores

    def gaussian_nb_weighed(self):
        att = self.input

        reg = GaussianNB()
        reg.fit(att['x_train'], att['y_train'], sample_weight=att['df_aif'].instance_weights)

        y_pred = reg.predict(att['x_test'])
        scores = reg.predict_proba(att['x_test'])[:,1].reshape(-1, 1)

        return y_pred, scores

    def execute(self):
        y_pred, scores = self.gaussian_nb_weighed() if self.weighed else self.gaussian_nb()

        self.output = {
            'y_pred': y_pred,
            'scores': scores
        }
