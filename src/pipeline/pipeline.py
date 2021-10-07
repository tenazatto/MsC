from metrics.disparate_impact_remover import DisparateImpactRemoverMetricsFilter
from metrics.ml_model import MLModelMetricsFilter
from metrics.unbias_inproc_algorithms import UnbiasInProcAlgorithmMetricsFilter
from pipeline.pipe_filter.pipe import BasePipe
from pipeline.validation import PipelineValidation
from processors.enums import Datasets, Preprocessors, UnbiasDataAlgorithms, Algorithms, UnbiasInProcAlgorithms
from processors.inprocessors.adversarial_debiasing import AdversarialDebiasingFilter
from processors.inprocessors.logistic_regression import LogisticRegressionFilter
from processors.inprocessors.prejudice_remover import PrejudiceRemoverFilter
from processors.preprocessors.data.adult_sex import AdultSexPreprocessor, AdultSexFairnessPipe
from processors.preprocessors.data.dataset import AdultDataset, GermanDataset
from processors.preprocessors.data.german_age import GermanAgePreprocessor, GermanAgeFairnessPipe
from processors.preprocessors.data.german_foreign import GermanForeignPreprocessor, GermanForeignFairnessPipe
from processors.preprocessors.inproc_algorithms.unbias_inproc_preprocessor import UnbiasInProcPreprocessor
from processors.preprocessors.unbias_algorithms.disparate_impact_remover import DisparateImpactRemoverUnbiasAlgorithm
from processors.preprocessors.unbias_algorithms.learning_fair_representations import LFRUnbiasAlgorithm
from processors.preprocessors.unbias_algorithms.optim_preprocess import OptimizedPreprocessingUnbiasAlgorithm
from processors.preprocessors.unbias_algorithms.reweighing import ReweighingUnbiasAlgorithm


class Pipeline:
    @staticmethod
    def new_pipe():
        return BasePipe()

    def select_data_preprocessor(self, dataset, preprocessor):
        choice = [dataset, preprocessor]
        options = [
            ([Datasets.ADULT_INCOME, Preprocessors.SEX], (AdultDataset(), AdultSexPreprocessor(), AdultSexFairnessPipe())),
            ([Datasets.GERMAN_CREDIT, Preprocessors.AGE], (GermanDataset(), GermanAgePreprocessor(), GermanAgeFairnessPipe())),
            ([Datasets.GERMAN_CREDIT, Preprocessors.FOREIGN], (GermanDataset(), GermanForeignPreprocessor(), GermanForeignFairnessPipe())),
        ]

        for option, pipe_filter in options:
            if choice == option:
                dataset_pipe, data_preprocessor_filter, fairness_pipe = pipe_filter
                preprocessed_data_pipe = dataset_pipe >= data_preprocessor_filter == self.new_pipe()
                break

        return preprocessed_data_pipe, fairness_pipe

    def unbias_data_preprocessor(self, preprocessed_data_pipe, fairness_pipe, algorithm, unbias_data_algorithm):
        init_pipe = preprocessed_data_pipe.merge(fairness_pipe)
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
            (UnbiasInProcAlgorithms.ADVERSARIAL_DEBIASING, UnbiasInProcPreprocessor())
        ]

        for option, filter in unbias_inproc_options:
            if algorithm == option:
                result_pipe = init_pipe >= filter == self.new_pipe()
                break

        if result_pipe is None:
            result_pipe = preprocessed_data_pipe

        return result_pipe

    def data_preprocess(self, dataset, preprocessor, algorithm, unbias_data_algorithm):
        preprocessed_data_pipe, fairness_pipe = self.select_data_preprocessor(dataset, preprocessor)
        unbiased_data_pipe = self.unbias_data_preprocessor(preprocessed_data_pipe, fairness_pipe, algorithm, unbias_data_algorithm)

        return fairness_pipe, unbiased_data_pipe

    def prepare_process_and_test_pipe(self, algorithm, data_pipe, fairness_pipe, unbias_data_algorithm):
        if unbias_data_algorithm == UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER:
            process_pipe = data_pipe.partial_pipe(['x_train', 'y_train', 'x_test'])
            test_pipe = data_pipe.partial_pipe(['df_aif', 'y_test'])
        elif unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING or \
                unbias_data_algorithm == UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING or \
                unbias_data_algorithm == UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS:
            process_pipe = data_pipe.partial_pipe(['x_train', 'y_train', 'x_test', 'df_aif'])
            test_pipe = data_pipe.partial_pipe(['x_test', 'y_test'])
        elif algorithm == UnbiasInProcAlgorithms.PREJUDICE_REMOVER:
            process_pipe = data_pipe.partial_pipe(['df_aif_tr', 'df_aif_te'])
            test_pipe = data_pipe.partial_pipe(['df_aif_te', 'y_test'])
        elif algorithm == UnbiasInProcAlgorithms.ADVERSARIAL_DEBIASING:
            process_pipe = data_pipe.merge(fairness_pipe)\
                .partial_pipe(['df_aif_tr', 'df_aif_te', 'privileged_group', 'unprivileged_group'])
            test_pipe = data_pipe.partial_pipe(['df_aif_te', 'y_test'])
        else:
            process_pipe = data_pipe.partial_pipe(['x_train', 'y_train', 'x_test'])
            test_pipe = data_pipe.partial_pipe(['x_test', 'y_test'])

        return process_pipe, test_pipe

    def process(self, process_pipe, algorithm, unbias_data_algorithm):
        if algorithm == Algorithms.LOGISTIC_REGRESSION and \
            (unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING or
             unbias_data_algorithm == UnbiasDataAlgorithms.LEARNING_FAIR_REPRESENTATIONS):
            prediction_pipe = process_pipe >= LogisticRegressionFilter(weighed=True) == self.new_pipe()
        elif algorithm == Algorithms.LOGISTIC_REGRESSION:
            prediction_pipe = process_pipe >= LogisticRegressionFilter() == self.new_pipe()
        elif algorithm == UnbiasInProcAlgorithms.PREJUDICE_REMOVER:
            prediction_pipe = process_pipe >= PrejudiceRemoverFilter() == self.new_pipe()
        elif algorithm == UnbiasInProcAlgorithms.ADVERSARIAL_DEBIASING:
            prediction_pipe = process_pipe >= AdversarialDebiasingFilter() == self.new_pipe()

        return prediction_pipe

    def calculate_metrics(self, test_pipe, prediction_pipe, fairness_pipe, algorithm, unbias_data_algorithm):
        init_pipe = test_pipe.merge(prediction_pipe).merge(fairness_pipe)
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
            (UnbiasInProcAlgorithms.ADVERSARIAL_DEBIASING, UnbiasInProcAlgorithmMetricsFilter())
        ]

        for option, filter in unbias_inproc_options:
            if algorithm == option:
                metrics_pipe = init_pipe >= filter == self.new_pipe()
                break

        if metrics_pipe is None:
            metrics_pipe = init_pipe >= MLModelMetricsFilter() == self.new_pipe()

        return metrics_pipe

    def start(self, dataset, preprocessor, algorithm, unbias_data_algorithm):
        PipelineValidation.validate_params(dataset, preprocessor, algorithm, unbias_data_algorithm)

        fairness_pipe, data_pipe = self.data_preprocess(dataset, preprocessor, algorithm, unbias_data_algorithm)

        process_pipe, test_pipe = self.prepare_process_and_test_pipe(algorithm, data_pipe, fairness_pipe, unbias_data_algorithm)

        prediction_pipe = self.process(process_pipe, algorithm, unbias_data_algorithm)

        metrics_pipe = self.calculate_metrics(test_pipe, prediction_pipe, fairness_pipe, algorithm, unbias_data_algorithm)

        return prediction_pipe.value['y_pred'], test_pipe.value['y_test'], metrics_pipe.value['explainer']
