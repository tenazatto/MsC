from aif360.algorithms.inprocessing import PrejudiceRemover

from src.pipeline.pipe_filter.pipe import BaseFilter


class PrejudiceRemoverFilter(BaseFilter):
    max_iter = 10000
    weighed = False

    def __init__(self, max_iter=10000, weighed=False):
        self.max_iter = max_iter
        self.weighed = weighed

    def prejudice_remover(self):
        att = self.input

        sens_attr = att['df_aif_tr'].protected_attribute_names[0]

        model = PrejudiceRemover(sensitive_attr=sens_attr, eta=25.0)
        model.fit(att['df_aif_tr'])

        result = model.predict(att['df_aif_te'])

        return result.labels

    def execute(self):
        y_pred = self.prejudice_remover()

        self.output = {
            'y_pred': y_pred
        }
