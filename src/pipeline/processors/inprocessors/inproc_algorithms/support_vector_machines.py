from sklearn.svm import SVC

from src.pipeline.pipe_filter.pipe import BaseFilter


class SVMFilter(BaseFilter):
    weighed = False
    class_weight = None

    def __init__(self, weighed=False, class_weight=None):
        self.weighed = weighed
        self.class_weight = class_weight

    def support_vector_machine(self):
        att = self.input

        svc = SVC(probability=True, class_weight=self.class_weight)
        svc.fit(att['x_train'], att['y_train'])

        y_pred = svc.predict(att['x_test'])
        scores = svc.predict_proba(att['x_test'])[:,1].reshape(-1, 1)

        return y_pred, scores

    def support_vector_machine_weighed(self):
        att = self.input

        svc = SVC(probability=True, class_weight=self.class_weight)
        svc.fit(att['x_train'], att['y_train'], sample_weight=att['df_aif'].instance_weights)

        y_pred = svc.predict(att['x_test'])
        scores = svc.predict_proba(att['x_test'])[:,1].reshape(-1, 1)

        return y_pred, scores

    def execute(self):
        y_pred, scores = self.support_vector_machine_weighed() if self.weighed else self.support_vector_machine()

        self.output = {
            'y_pred': y_pred,
            'scores': scores
        }
