from sklearn.ensemble import RandomForestClassifier

from src.pipeline.pipe_filter.pipe import BaseFilter


class RandomForestFilter(BaseFilter):
    weighed = False
    class_weight = None

    def __init__(self, weighed=False, class_weight=None):
        self.weighed = weighed
        self.class_weight = class_weight

    def random_forest(self):
        att = self.input

        rfc = RandomForestClassifier(class_weight=self.class_weight)
        rfc.fit(att['x_train'], att['y_train'])

        y_pred = rfc.predict(att['x_test'])
        scores = rfc.predict_proba(att['x_test'])[:,1].reshape(-1, 1)

        return y_pred, scores

    def random_forest_weighed(self):
        att = self.input

        rfc = RandomForestClassifier(class_weight=self.class_weight)
        rfc.fit(att['x_train'], att['y_train'], sample_weight=att['df_aif'].instance_weights)

        y_pred = rfc.predict(att['x_test'])
        scores = rfc.predict_proba(att['x_test'])[:,1].reshape(-1, 1)

        return y_pred, scores

    def execute(self):
        y_pred, scores = self.random_forest_weighed() if self.weighed else self.random_forest()

        self.output = {
            'y_pred': y_pred,
            'scores': scores
        }
