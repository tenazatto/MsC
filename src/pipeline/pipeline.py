import math
from datetime import datetime

from src.pipeline.metrics.disparate_impact_remover import DisparateImpactRemoverMetricsFilter
from src.pipeline.metrics.metrics_file_writer import MetricsFileWriterFilter
from src.pipeline.metrics.metrics_print import MetricsPrintFilter
from src.pipeline.metrics.ml_model import MLModelMetricsFilter
from src.pipeline.metrics.unbias_inproc_algorithms import UnbiasInProcAlgorithmMetricsFilter
from src.pipeline.pipe_filter.pipe import BasePipe
from src.pipeline.processors.preprocessors.data.lendingclub_income import LendingclubIncomePreprocessor, \
    LendingclubIncomeFairnessPipe
from src.pipeline.validation import PipelineValidation
from src.pipeline.processors.enums import Datasets, Preprocessors, UnbiasDataAlgorithms, Algorithms, UnbiasInProcAlgorithms, \
    UnbiasPostProcAlgorithms
from src.pipeline.processors.inprocessors.unbias_algorithms.adversarial_debiasing import AdversarialDebiasingFilter
from src.pipeline.processors.inprocessors.inproc_algorithms.gradient_boost import GradientBoostFilter
from src.pipeline.processors.inprocessors.inproc_algorithms.naive_bayes import NaiveBayesFilter
from src.pipeline.processors.inprocessors.inproc_algorithms.logistic_regression import LogisticRegressionFilter
from src.pipeline.processors.inprocessors.unbias_algorithms.expo_grad_reduction import ExponentiatedGradientReductionFilter
from src.pipeline.processors.inprocessors.unbias_algorithms.grid_search_reduction import GridSearchReductionFilter
from src.pipeline.processors.inprocessors.unbias_algorithms.meta_fair_classifier import MetaFairClassifierFilter
from src.pipeline.processors.inprocessors.unbias_algorithms.prejudice_remover import PrejudiceRemoverFilter
from src.pipeline.processors.inprocessors.inproc_algorithms.random_forest import RandomForestFilter
from src.pipeline.processors.inprocessors.inproc_algorithms.support_vector_machines import SVMFilter
from src.pipeline.processors.inprocessors.unbias_algorithms.rich_subgroup_fairness import RichSubgroupFairnessFilter
from src.pipeline.processors.postprocessors.calibrated_equalized_odds import CalibratedEqualizedOddsFilter
from src.pipeline.processors.postprocessors.equalized_odds import EqualizedOddsFilter
from src.pipeline.processors.postprocessors.reject_option_classification import RejectOptionClassificationFilter
from src.pipeline.processors.preprocessors.data.adult_sex import AdultSexPreprocessor, AdultSexFairnessPipe
from src.pipeline.processors.preprocessors.data.dataset import AdultDataset, GermanDataset, LendingclubDataset
from src.pipeline.processors.preprocessors.data.german_age import GermanAgePreprocessor, GermanAgeFairnessPipe
from src.pipeline.processors.preprocessors.data.german_foreign import GermanForeignPreprocessor, GermanForeignFairnessPipe
from src.pipeline.processors.preprocessors.data.train_test_split import TrainTestSplit
from src.pipeline.processors.preprocessors.data.train_valid_test_split import TrainValidTestSplit
from src.pipeline.processors.preprocessors.inproc_algorithms.unbias_inproc_preprocessor import UnbiasInProcPreprocessor
from src.pipeline.processors.preprocessors.postproc_algorithms.unbias_postproc_preprocessor import UnbiasPostProcPreprocessor
from src.pipeline.processors.preprocessors.unbias_algorithms.disparate_impact_remover import DisparateImpactRemoverUnbiasAlgorithm
from src.pipeline.processors.preprocessors.unbias_algorithms.learning_fair_representations import LFRUnbiasAlgorithm
from src.pipeline.processors.preprocessors.unbias_algorithms.optim_preprocess import OptimizedPreprocessingUnbiasAlgorithm
from src.pipeline.processors.preprocessors.unbias_algorithms.reweighing import ReweighingUnbiasAlgorithm


class Pipeline:
    @staticmethod
    def new_pipe():
        return BasePipe()

    def find_algorithm(self, algorithm):
        indexes = {
            'Algorithms.LOGISTIC_REGRESSION': 1,
            'Algorithms.RANDOM_FOREST': 2,
            'Algorithms.GRADIENT_BOOST': 3,
            'Algorithms.SUPPORT_VECTOR_MACHINES': 4,
            'Algorithms.LINEAR_REGRESSION': 901,
            'Algorithms.DECISION_TREE': 902,
            'Algorithms.KERNEL_RIDGE': 903,
            'Algorithms.NAIVE_BAYES': 5,
            'UnbiasInProcAlgorithms.PREJUDICE_REMOVER': 101,
            'UnbiasInProcAlgorithms.ADVERSARIAL_DEBIASING': 102,
            'UnbiasInProcAlgorithms.EXPONENTIATED_GRADIENT_REDUCTION': 103,
            'UnbiasInProcAlgorithms.RICH_SUBGROUP_FAIRNESS': 104,
            'UnbiasInProcAlgorithms.GRID_SEARCH_REDUCTION': 105,
            'UnbiasInProcAlgorithms.META_FAIR_CLASSIFIER': 106,
            'UnbiasInProcAlgorithms.ART_CLASSIFIER': 107
        }

        return next(filter(lambda a: a[1] == algorithm, indexes.items()))[0]

    def pipe_parameters(self, dataset, preprocessor, algorithm, unbias_data_algorithm, unbias_postproc_algorithm):
        params_pipe = self.new_pipe()

        params_pipe.value = {
            'pipeline_params': {
                'dataset': str(dataset),
                'preprocessor': str(preprocessor),
                'unbias_data_algorithm': str(unbias_data_algorithm),
                'algorithm': self.find_algorithm(algorithm),
                'unbias_postproc_algorithm': str(unbias_postproc_algorithm)
            }
        }

        return params_pipe

    def select_data_preprocessor(self, dataset, preprocessor):
        choice = [dataset, preprocessor]
        options = [
            ([Datasets.ADULT_INCOME, Preprocessors.SEX], (AdultDataset(), AdultSexPreprocessor(), AdultSexFairnessPipe())),
            ([Datasets.GERMAN_CREDIT, Preprocessors.AGE], (GermanDataset(), GermanAgePreprocessor(), GermanAgeFairnessPipe())),
            ([Datasets.GERMAN_CREDIT, Preprocessors.FOREIGN], (GermanDataset(), GermanForeignPreprocessor(), GermanForeignFairnessPipe())),
            ([Datasets.LENDINGCLUB, Preprocessors.INCOME], (LendingclubDataset(), LendingclubIncomePreprocessor(), LendingclubIncomeFairnessPipe())),
        ]

        for option, pipe_filter in options:
            if choice == option:
                dataset_pipe, data_preprocessor_filter, fairness_pipe = pipe_filter
                preprocessed_data_pipe = dataset_pipe >= data_preprocessor_filter == self.new_pipe()
                break

        return preprocessed_data_pipe, fairness_pipe

    def select_train_test_strategy(self, preprocessed_data_pipe, unbias_postproc_algorithm):
        unbias_postproc_options = [
            (UnbiasPostProcAlgorithms.NOTHING, TrainTestSplit()),
            (UnbiasPostProcAlgorithms.EQUALIZED_ODDS, TrainTestSplit()),
            (UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS, TrainTestSplit()),
            (UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION, TrainValidTestSplit())
        ]

        for option, filter in unbias_postproc_options:
            if unbias_postproc_algorithm == option:
                result_pipe = preprocessed_data_pipe >= filter == self.new_pipe()
                break

        return result_pipe

    def unbias_data_preprocessor(self, preprocessed_data_pipe, fairness_pipe, algorithm, unbias_data_algorithm, unbias_postproc_algorithm):
        init_pipe = preprocessed_data_pipe + fairness_pipe
        result_pipe = None

        unbias_data_options = [
            (UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER, DisparateImpactRemoverUnbiasAlgorithm()),
            (UnbiasDataAlgorithms.REWEIGHING, ReweighingUnbiasAlgorithm()),
            (UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING, OptimizedPreprocessingUnbiasAlgorithm()),
            (UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS, LFRUnbiasAlgorithm())
        ]

        for option, filter in unbias_data_options:
            if unbias_data_algorithm == option:
                result_pipe = init_pipe >= filter == self.new_pipe()
                break

        unbias_inproc_options = [
            (UnbiasInProcAlgorithms.PREJUDICE_REMOVER, UnbiasInProcPreprocessor()),
            (UnbiasInProcAlgorithms.ADVERSARIAL_DEBIASING, UnbiasInProcPreprocessor()),
            (UnbiasInProcAlgorithms.EXPONENTIATED_GRADIENT_REDUCTION, UnbiasInProcPreprocessor()),
            (UnbiasInProcAlgorithms.RICH_SUBGROUP_FAIRNESS, UnbiasInProcPreprocessor()),
            (UnbiasInProcAlgorithms.META_FAIR_CLASSIFIER, UnbiasInProcPreprocessor()),
            (UnbiasInProcAlgorithms.GRID_SEARCH_REDUCTION, UnbiasInProcPreprocessor())
        ]

        for option, filter in unbias_inproc_options:
            if algorithm == option:
                result_pipe = init_pipe >= filter == self.new_pipe()
                break

        unbias_postproc_options = [
            (UnbiasPostProcAlgorithms.EQUALIZED_ODDS, UnbiasPostProcPreprocessor()),
            (UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS, UnbiasPostProcPreprocessor()),
            (UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION, UnbiasPostProcPreprocessor())
        ]

        for option, filter in unbias_postproc_options:
            if unbias_postproc_algorithm == option:
                result_pipe = init_pipe >= filter == self.new_pipe()
                break

        if result_pipe is None:
            result_pipe = preprocessed_data_pipe

        return result_pipe

    def data_preprocess(self, dataset, preprocessor, algorithm, unbias_data_algorithm, unbias_postproc_algorithm):
        preprocessed_data_pipe, fairness_pipe = self.select_data_preprocessor(dataset, preprocessor)
        preprocessed_data_pipe = self.select_train_test_strategy(preprocessed_data_pipe, unbias_postproc_algorithm)
        unbiased_data_pipe = self.unbias_data_preprocessor(preprocessed_data_pipe, fairness_pipe, algorithm,
                                                           unbias_data_algorithm, unbias_postproc_algorithm)

        return fairness_pipe, unbiased_data_pipe

    def prepare_process_and_test_pipe(self, data_pipe, fairness_pipe, algorithm, unbias_data_algorithm, unbias_postproc_algorithm):
        if unbias_data_algorithm == UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER:
            process_pipe = data_pipe['x_train', 'y_train', 'x_test']
            test_pipe = data_pipe['df_aif', 'y_test']
        elif unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING or \
                unbias_data_algorithm == UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING or \
                unbias_data_algorithm == UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS:
            process_pipe = data_pipe['x_train', 'y_train', 'x_test', 'df_aif']
            test_pipe = data_pipe['x_test', 'y_test']
        elif algorithm == UnbiasInProcAlgorithms.PREJUDICE_REMOVER or \
                algorithm == UnbiasInProcAlgorithms.EXPONENTIATED_GRADIENT_REDUCTION or \
                algorithm == UnbiasInProcAlgorithms.RICH_SUBGROUP_FAIRNESS or \
                algorithm == UnbiasInProcAlgorithms.GRID_SEARCH_REDUCTION:
            process_pipe = data_pipe['df_aif_tr', 'df_aif_te']
            test_pipe = data_pipe['df_aif_te', 'y_test']
        elif algorithm == UnbiasInProcAlgorithms.ADVERSARIAL_DEBIASING:
            process_pipe = (data_pipe + fairness_pipe)['df_aif_tr', 'df_aif_te', 'privileged_group', 'unprivileged_group']
            test_pipe = data_pipe['df_aif_te', 'y_test']
        elif algorithm == UnbiasInProcAlgorithms.META_FAIR_CLASSIFIER:
            process_pipe = (data_pipe + fairness_pipe)['df_aif_tr', 'df_aif_te', 'protected_attribute_names']
            test_pipe = data_pipe['df_aif_te', 'y_test']
        elif unbias_postproc_algorithm == UnbiasPostProcAlgorithms.EQUALIZED_ODDS or \
                unbias_postproc_algorithm == UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS or \
                unbias_postproc_algorithm == UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION:
            process_pipe = data_pipe['x_train', 'y_train', 'x_test', 'df_aif_te']
            test_pipe = data_pipe['df_aif_val', 'df_aif_te', 'y_test']
        else:
            process_pipe = data_pipe['x_train', 'y_train', 'x_test']
            test_pipe = data_pipe['x_test', 'y_test']

        return process_pipe, test_pipe

    def process(self, process_pipe, algorithm, unbias_data_algorithm):
        weighed_algorithm = unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING or \
                            unbias_data_algorithm == UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS

        process_options = [
            (Algorithms.LOGISTIC_REGRESSION, LogisticRegressionFilter(weighed=weighed_algorithm)),
            (Algorithms.RANDOM_FOREST, RandomForestFilter(weighed=weighed_algorithm)),
            (Algorithms.GRADIENT_BOOST, GradientBoostFilter(weighed=weighed_algorithm)),
            (Algorithms.NAIVE_BAYES, NaiveBayesFilter(weighed=weighed_algorithm)),
            (Algorithms.SUPPORT_VECTOR_MACHINES, SVMFilter(weighed=weighed_algorithm)),
            (UnbiasInProcAlgorithms.PREJUDICE_REMOVER, PrejudiceRemoverFilter()),
            (UnbiasInProcAlgorithms.ADVERSARIAL_DEBIASING, AdversarialDebiasingFilter()),
            (UnbiasInProcAlgorithms.EXPONENTIATED_GRADIENT_REDUCTION, ExponentiatedGradientReductionFilter(algorithm=Algorithms.GRADIENT_BOOST)),
            (UnbiasInProcAlgorithms.RICH_SUBGROUP_FAIRNESS, RichSubgroupFairnessFilter(algorithm=Algorithms.DECISION_TREE)),
            (UnbiasInProcAlgorithms.META_FAIR_CLASSIFIER, MetaFairClassifierFilter()),
            (UnbiasInProcAlgorithms.GRID_SEARCH_REDUCTION, GridSearchReductionFilter(algorithm=Algorithms.RANDOM_FOREST))
        ]

        for option, filter in process_options:
            if algorithm == option:
                prediction_pipe = process_pipe >= filter == self.new_pipe()
                break

        return prediction_pipe

    def data_postprocess(self, test_pipe, prediction_pipe, fairness_pipe, unbias_postproc_algorithm):
        unbias_postproc_options = [
            (UnbiasPostProcAlgorithms.EQUALIZED_ODDS, EqualizedOddsFilter()),
            (UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS, CalibratedEqualizedOddsFilter()),
            (UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION, RejectOptionClassificationFilter())
        ]

        for option, filter in unbias_postproc_options:
            if unbias_postproc_algorithm == option:
                init_pipe = test_pipe + prediction_pipe + fairness_pipe['unprivileged_group', 'privileged_group']
                init_pipe >= filter == prediction_pipe
                break

        return prediction_pipe

    def calculate_metrics(self, test_pipe, prediction_pipe, fairness_pipe, algorithm, unbias_data_algorithm, unbias_postproc_algorithm):
        init_pipe = test_pipe + prediction_pipe + fairness_pipe
        metrics_pipe = None

        unbias_data_options = [
            (UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER, DisparateImpactRemoverMetricsFilter()),
            (UnbiasDataAlgorithms.REWEIGHING, MLModelMetricsFilter()),
            (UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING, MLModelMetricsFilter()),
            (UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS, MLModelMetricsFilter())
        ]

        for option, filter in unbias_data_options:
            if unbias_data_algorithm == option:
                metrics_pipe = init_pipe >= filter == self.new_pipe()
                break

        unbias_inproc_options = [
            (UnbiasInProcAlgorithms.PREJUDICE_REMOVER, UnbiasInProcAlgorithmMetricsFilter()),
            (UnbiasInProcAlgorithms.ADVERSARIAL_DEBIASING, UnbiasInProcAlgorithmMetricsFilter()),
            (UnbiasInProcAlgorithms.EXPONENTIATED_GRADIENT_REDUCTION, UnbiasInProcAlgorithmMetricsFilter()),
            (UnbiasInProcAlgorithms.RICH_SUBGROUP_FAIRNESS, UnbiasInProcAlgorithmMetricsFilter()),
            (UnbiasInProcAlgorithms.META_FAIR_CLASSIFIER, UnbiasInProcAlgorithmMetricsFilter()),
            (UnbiasInProcAlgorithms.GRID_SEARCH_REDUCTION, UnbiasInProcAlgorithmMetricsFilter())
        ]

        for option, filter in unbias_inproc_options:
            if algorithm == option:
                metrics_pipe = init_pipe >= filter == self.new_pipe()
                break

        unbias_postproc_options = [
            (UnbiasPostProcAlgorithms.EQUALIZED_ODDS, UnbiasInProcAlgorithmMetricsFilter()),
            (UnbiasPostProcAlgorithms.CALIBRATED_EQUALIZED_ODDS, UnbiasInProcAlgorithmMetricsFilter()),
            (UnbiasPostProcAlgorithms.REJECT_OPTION_CLASSIFICATION, UnbiasInProcAlgorithmMetricsFilter())
        ]

        for option, filter in unbias_postproc_options:
            if unbias_postproc_algorithm == option:
                metrics_pipe = init_pipe >= filter == self.new_pipe()
                break

        if metrics_pipe is None:
            metrics_pipe = init_pipe >= MLModelMetricsFilter() == self.new_pipe()



        return metrics_pipe

    def date_time_pipe(self, date_start, date_end):
        date_time_pipe = self.new_pipe()

        date_time_pipe.value = {
            'date_start': date_start.strftime("%d/%m/%Y %H:%M:%S.%f"),
            'date_end': date_end.strftime("%d/%m/%Y %H:%M:%S.%f"),
            'execution_time_ms': math.floor((date_end - date_start).total_seconds() * 1000)
        }

        return date_time_pipe

    def print_and_save_results(self, params_pipe, data_pipe, metrics_pipe, date_time_pipe):
        final_pipe = data_pipe['checksum'] + date_time_pipe + params_pipe + metrics_pipe

        final_pipe >= MetricsPrintFilter() == final_pipe
        final_pipe['checksum', 'date_start', 'date_end', 'execution_time_ms',
                   'pipeline_params', 'metrics_summary'] >= MetricsFileWriterFilter() == final_pipe

    def start(self, dataset, preprocessor, algorithm, unbias_data_algorithm, unbias_postproc_algorithm, save_metadata=True):
        date_start = datetime.now()
        PipelineValidation.validate_params(dataset, preprocessor, algorithm, unbias_data_algorithm, unbias_postproc_algorithm)

        params_pipe = self.pipe_parameters(dataset, preprocessor, algorithm, unbias_data_algorithm, unbias_postproc_algorithm)

        fairness_pipe, data_pipe = self.data_preprocess(dataset, preprocessor, algorithm,
                                                        unbias_data_algorithm, unbias_postproc_algorithm)

        process_pipe, test_pipe = self.prepare_process_and_test_pipe(data_pipe, fairness_pipe, algorithm,
                                                                     unbias_data_algorithm, unbias_postproc_algorithm)

        prediction_pipe = self.process(process_pipe, algorithm, unbias_data_algorithm)

        prediction_pipe = self.data_postprocess(test_pipe, prediction_pipe, fairness_pipe, unbias_postproc_algorithm)

        metrics_pipe = self.calculate_metrics(test_pipe, prediction_pipe, fairness_pipe,
                                              algorithm, unbias_data_algorithm, unbias_postproc_algorithm)

        date_end = datetime.now()
        date_time_pipe = self.date_time_pipe(date_start, date_end)

        if save_metadata:
            self.print_and_save_results(params_pipe, data_pipe, metrics_pipe, date_time_pipe)
