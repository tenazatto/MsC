from processors.enums import Datasets, Preprocessors, UnbiasDataAlgorithms, Algorithms, UnbiasInProcAlgorithms


class PipelineValidation:
    @staticmethod
    def validate_params(dataset, preprocessor, algorithm, unbias_data_algorithm):
        existant_preprocessors = \
            (dataset == Datasets.ADULT_INCOME and preprocessor == Preprocessors.SEX) or \
            (dataset == Datasets.GERMAN_CREDIT and preprocessor == Preprocessors.AGE) or \
            (dataset == Datasets.GERMAN_CREDIT and preprocessor == Preprocessors.FOREIGN)

        existant_algorithms = \
            (algorithm == Algorithms.LOGISTIC_REGRESSION and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING) or \
            (algorithm == Algorithms.LOGISTIC_REGRESSION and unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING) or \
            (algorithm == Algorithms.LOGISTIC_REGRESSION and unbias_data_algorithm == UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER) or \
            (algorithm == Algorithms.LOGISTIC_REGRESSION and unbias_data_algorithm == UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING) or \
            (algorithm == UnbiasInProcAlgorithms.PREJUDICE_REMOVER and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING)

        if not existant_preprocessors:
            raise Exception("Pré-processador não existente para o conjunto de dados")
        if not existant_algorithms:
            raise Exception("Algoritmo ainda não implementado ou combinação não suportada")
