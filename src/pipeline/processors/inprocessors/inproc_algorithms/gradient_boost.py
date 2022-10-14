from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from src.pipeline.pipe_filter.pipe import BaseFilter


class GradientBoostFilter(BaseFilter):
    weighed = False

    def __init__(self, weighed=False):
        self.weighed = weighed

    def gradient_boost(self):
        att = self.input

        gbc = GradientBoostingClassifier()
        gbc.fit(att['x_train'], att['y_train'])

        y_pred = gbc.predict(att['x_test'])
        scores = gbc.predict_proba(att['x_test'])[:,1].reshape(-1, 1)

        return y_pred, scores

    def gradient_boost_weighed(self):
        att = self.input

        gbc = GradientBoostingClassifier()
        gbc.fit(att['x_train'], att['y_train'], sample_weight=att['df_aif'].instance_weights)

        y_pred = gbc.predict(att['x_test'])
        scores = gbc.predict_proba(att['x_test'])[:,1].reshape(-1, 1)

        return y_pred, scores

    def execute(self):
        y_pred, scores = self.gradient_boost_weighed() if self.weighed else self.gradient_boost()

        self.output = {
            'y_pred': y_pred,
            'scores': scores
        }
