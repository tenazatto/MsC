from aif360.algorithms.inprocessing import ExponentiatedGradientReduction
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from src.pipeline.pipe_filter.pipe import BaseFilter
from src.pipeline.processors.enums import Algorithms


class ExponentiatedGradientReductionFilter(BaseFilter):
    '''
    constraints options:
    DemographicParity, EqualizedOdds, TruePositiveRateDifference, ErrorRateRatio
    Uses fairlearn 0.4.6
    '''
    constraints = 'EqualizedOdds'

    def __init__(self, algorithm=Algorithms.LOGISTIC_REGRESSION, constraints='EqualizedOdds', max_iter=50):
        self.max_iter = max_iter
        self.constraints = constraints

        if algorithm == Algorithms.LOGISTIC_REGRESSION:
            self.algorithm = LogisticRegression(solver='lbfgs')
        elif algorithm == Algorithms.SUPPORT_VECTOR_MACHINES:
            self.algorithm = SVC()
        elif algorithm == Algorithms.RANDOM_FOREST:
            self.algorithm = RandomForestClassifier()
        elif algorithm == Algorithms.GRADIENT_BOOST:
            self.algorithm = GradientBoostingClassifier()
        else:
            raise Exception("Algoritmo não implementado")

    def exponentiated_gradient_reduction(self):
        att = self.input

        debiased_model = ExponentiatedGradientReduction(estimator=self.algorithm, constraints=self.constraints,
                                                        drop_prot_attr=False)
        debiased_model.fit(att['df_aif_tr'])

        result = debiased_model.predict(att['df_aif_te'])

        return result.labels

    def execute(self):
        y_pred = self.exponentiated_gradient_reduction()

        self.output = {
            'y_pred': y_pred
        }
