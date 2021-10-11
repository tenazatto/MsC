from enum import Enum


class Datasets(Enum):
    ADULT_INCOME = 1
    GERMAN_CREDIT = 2


class Preprocessors(Enum):
    SEX = 1
    AGE = 2
    FOREIGN = 3


class Algorithms:
    LOGISTIC_REGRESSION = 1
    RANDOM_FOREST = 2
    GRADIENT_BOOST = 3
    SUPPORT_VECTOR_MACHINES = 4


class UnbiasInProcAlgorithms(Algorithms):
    PREJUDICE_REMOVER = 101
    ADVERSARIAL_DEBIASING = 102
    EXPONENTIATED_GRADIENT_REDUCTION = 103
    RICH_SUBGROUP_FAIRNESS = 104
    GRID_SEARCH_REDUCTION = 105
    META_FAIR_CLASSIFIER = 106
    ART_CLASSIFIER = 107 # Adversarial Robustness Toolbox (Security)


class UnbiasDataAlgorithms(Enum):
    NOTHING = 0
    REWEIGHING = 1
    OPTIMIZED_PREPROCESSING = 2
    DISPARATE_IMPACT_REMOVER = 3
    LEARNING_FAIR_REPRESENTATIONS = 4

class UnbiasPostProcAlgorithms(Enum):
    NOTHING = 0
    EQUALIZED_ODDS = 1
    CALIBRATED_EQUALIZED_ODDS = 2
    REJECT_OPTION_CLASSIFICATION = 3
