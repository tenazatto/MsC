from aif360.algorithms.postprocessing import EqOddsPostprocessing

from src.pipeline.pipe_filter.pipe import BaseFilter


class EqualizedOddsFilter(BaseFilter):

    def equalized_odds(self):
        att = self.input

        EOPP = EqOddsPostprocessing(unprivileged_groups=att['unprivileged_group'],
                                    privileged_groups=att['privileged_group'])

        df_aif_te_pred = att['df_aif_te'].copy()
        df_aif_te_pred.labels = att['y_pred']
        df_aif_te_pred.scores = att['scores']

        EOPP.fit(att['df_aif_te'], df_aif_te_pred)

        result = EOPP.predict(att['df_aif_te'])

        return result.labels

    def execute(self):
        y_pred = self.equalized_odds()

        self.output = {
            'y_pred': y_pred
        }
