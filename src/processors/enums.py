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


class UnbiasInProcAlgorithms(Algorithms):
    PREJUDICE_REMOVER = 101
    ADVERSARIAL_DEBIASING = 102


class UnbiasDataAlgorithms(Enum):
    NOTHING = 0
    REWEIGHING = 1
    OPTIMIZED_PREPROCESSING = 2
    DISPARATE_IMPACT_REMOVER = 3
    LEARNING_FAIR_REPRESENTATIONS = 4
