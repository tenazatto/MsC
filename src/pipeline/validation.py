from src.pipeline.processors.enums import Datasets, Preprocessors, UnbiasDataAlgorithms, Algorithms, UnbiasInProcAlgorithms, \
    UnbiasPostProcAlgorithms


class PipelineValidation:
    @staticmethod
    def validate_params(dataset, preprocessor, algorithm, unbias_data_algorithm, unbias_postproc_algorithm):
        existant_preprocessors = \
            (dataset == Datasets.ADULT_INCOME and preprocessor == Preprocessors.SEX) or \
            (dataset == Datasets.GERMAN_CREDIT and preprocessor == Preprocessors.AGE) or \
            (dataset == Datasets.GERMAN_CREDIT and preprocessor == Preprocessors.FOREIGN) or \
            (dataset == Datasets.LENDINGCLUB and preprocessor == Preprocessors.INCOME)

        existant_algorithms = \
            (algorithm == Algorithms.LOGISTIC_REGRESSION and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.LOGISTIC_REGRESSION and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.EQUALIZED_ODDS) or \
            (algorithm == Algorithms.LOGISTIC_REGRESSION and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS) or \
            (algorithm == Algorithms.LOGISTIC_REGRESSION and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION) or \
            (algorithm == Algorithms.LOGISTIC_REGRESSION and unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.LOGISTIC_REGRESSION and unbias_data_algorithm == UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.LOGISTIC_REGRESSION and unbias_data_algorithm == UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.LOGISTIC_REGRESSION and unbias_data_algorithm == UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.RANDOM_FOREST and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.RANDOM_FOREST and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.EQUALIZED_ODDS) or \
            (algorithm == Algorithms.RANDOM_FOREST and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS) or \
            (algorithm == Algorithms.RANDOM_FOREST and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION) or \
            (algorithm == Algorithms.RANDOM_FOREST and unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.RANDOM_FOREST and unbias_data_algorithm == UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.RANDOM_FOREST and unbias_data_algorithm == UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.RANDOM_FOREST and unbias_data_algorithm == UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.GRADIENT_BOOST and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.GRADIENT_BOOST and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.EQUALIZED_ODDS) or \
            (algorithm == Algorithms.GRADIENT_BOOST and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS) or \
            (algorithm == Algorithms.GRADIENT_BOOST and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION) or \
            (algorithm == Algorithms.GRADIENT_BOOST and unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.GRADIENT_BOOST and unbias_data_algorithm == UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.GRADIENT_BOOST and unbias_data_algorithm == UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.GRADIENT_BOOST and unbias_data_algorithm == UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.NAIVE_BAYES and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.NAIVE_BAYES and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.EQUALIZED_ODDS) or \
            (algorithm == Algorithms.NAIVE_BAYES and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS) or \
            (algorithm == Algorithms.NAIVE_BAYES and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION) or \
            (algorithm == Algorithms.NAIVE_BAYES and unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.NAIVE_BAYES and unbias_data_algorithm == UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.NAIVE_BAYES and unbias_data_algorithm == UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.NAIVE_BAYES and unbias_data_algorithm == UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.SUPPORT_VECTOR_MACHINES and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.SUPPORT_VECTOR_MACHINES and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.EQUALIZED_ODDS) or \
            (algorithm == Algorithms.SUPPORT_VECTOR_MACHINES and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS) or \
            (algorithm == Algorithms.SUPPORT_VECTOR_MACHINES and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION) or \
            (algorithm == Algorithms.SUPPORT_VECTOR_MACHINES and unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.SUPPORT_VECTOR_MACHINES and unbias_data_algorithm == UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.SUPPORT_VECTOR_MACHINES and unbias_data_algorithm == UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == Algorithms.SUPPORT_VECTOR_MACHINES and unbias_data_algorithm == UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == UnbiasInProcAlgorithms.PREJUDICE_REMOVER and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == UnbiasInProcAlgorithms.ADVERSARIAL_DEBIASING and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == UnbiasInProcAlgorithms.EXPONENTIATED_GRADIENT_REDUCTION and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == UnbiasInProcAlgorithms.RICH_SUBGROUP_FAIRNESS and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == UnbiasInProcAlgorithms.META_FAIR_CLASSIFIER and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING) or \
            (algorithm == UnbiasInProcAlgorithms.GRID_SEARCH_REDUCTION and unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING and unbias_postproc_algorithm == UnbiasPostProcAlgorithms.NOTHING)

        if not existant_preprocessors:
            raise Exception("Pré-processador não existente para o conjunto de dados")
        if not existant_algorithms:
            raise Exception("Algoritmo ainda não implementado ou combinação não suportada")


class MAPEKValidation:
    @staticmethod
    def validate_data_checksum_planner_params(checksum, last_checksum):
        if (checksum is None and not last_checksum) or \
           (checksum is not None and last_checksum):
            raise Exception('Combinação de parâmetros inválida')

    @staticmethod
    def validate_pipeline_planner_params(data):
        if data.size == 0:
            raise Exception('Não há itens para executar o Pipeline')