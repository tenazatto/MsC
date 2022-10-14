from aif360.algorithms.inprocessing import GerryFairClassifier
from sklearn import linear_model, svm, tree
from sklearn.kernel_ridge import KernelRidge

from src.pipeline.pipe_filter.pipe import BaseFilter
from src.pipeline.processors.enums import Algorithms


class RichSubgroupFairnessFilter(BaseFilter):
    l1_norm_val = 10
    max_iter = 10
    gamma = 0.01
    fairness_def = 'FP' # Fairness notion, FP, FN, SP
    algorithm = linear_model.LinearRegression() # Hypothesis class for the Learner. Supports LR, SVM, KR, Trees.

    def __init__(self, max_iter=10, l1_norm_val=10, gamma=0.01, fairness_def='FP', algorithm=Algorithms.LINEAR_REGRESSION):
        self.max_iter = max_iter
        self.l1_norm_val = l1_norm_val
        self.gamma = gamma
        self.fairness_def = fairness_def

        if algorithm == Algorithms.LINEAR_REGRESSION:
            self.algorithm = linear_model.LinearRegression()
        elif algorithm == Algorithms.SUPPORT_VECTOR_MACHINES:
            self.algorithm = svm.SVR()
        elif algorithm == Algorithms.DECISION_TREE:
            self.algorithm = tree.DecisionTreeRegressor(max_depth=3)
        elif algorithm == Algorithms.KERNEL_RIDGE:
            self.algorithm = KernelRidge(alpha=1.0, gamma=1.0, kernel='rbf')
        else:
            raise Exception("Algoritmo não suportado")

    def rich_subgroup_fairness(self):
        att = self.input

        debiased_model = GerryFairClassifier(C=self.l1_norm_val, gamma=self.gamma, fairness_def=self.fairness_def,
                                             max_iters=self.max_iter, predictor=self.algorithm)

        debiased_model.fit(att['df_aif_tr'])

        result = debiased_model.predict(att['df_aif_te'])

        return result.labels

    def execute(self):
        y_pred = self.rich_subgroup_fairness()

        self.output = {
            'y_pred': y_pred
        }
