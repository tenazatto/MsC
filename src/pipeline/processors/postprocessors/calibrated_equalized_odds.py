from aif360.algorithms.postprocessing import CalibratedEqOddsPostprocessing

from src.pipeline.pipe_filter.pipe import BaseFilter


class CalibratedEqualizedOddsFilter(BaseFilter):
    cost_constraint = 'fnr'

    def __init__(self, cost_constraint='fnr'):
        self.cost_constraint = cost_constraint

    def calibrated_equalized_odds(self):
        att = self.input

        CPP = CalibratedEqOddsPostprocessing(unprivileged_groups=att['unprivileged_group'],
                                             privileged_groups=att['privileged_group'],
                                             cost_constraint=self.cost_constraint)

        df_aif_te_pred = att['df_aif_te'].copy()
        df_aif_te_pred.labels = att['y_pred']
        df_aif_te_pred.scores = att['scores']

        CPP.fit(att['df_aif_te'], df_aif_te_pred)

        result = CPP.predict(att['df_aif_te'])

        return result.labels

    def execute(self):
        y_pred = self.calibrated_equalized_odds()

        self.output = {
            'y_pred': y_pred
        }
