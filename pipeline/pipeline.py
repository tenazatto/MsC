from metrics.disparate_impact_remover import DisparateImpactRemoverMetricsFilter
from metrics.ml_model import MLModelMetricsFilter
from metrics.prejudice_remover import PrejudiceRemoverMetricsFilter
from pipeline.pipe_filter.pipe import BasePipe
from pipeline.validation import PipelineValidation
from processors.enums import Datasets, Preprocessors, UnbiasDataAlgorithms, Algorithms, UnbiasInProcAlgorithms
from processors.inprocessors.logistic_regression import LogisticRegressionFilter
from processors.inprocessors.prejudice_remover import PrejudiceRemoverFilter
from processors.preprocessors.data.adult_sex import AdultSexPreprocessor, AdultSexFairnessPipe
from processors.preprocessors.data.dataset import AdultDataset, GermanDataset
from processors.preprocessors.data.german_age import GermanAgePreprocessor, GermanAgeFairnessPipe
from processors.preprocessors.data.german_foreign import GermanForeignPreprocessor, GermanForeignFairnessPipe
from processors.preprocessors.unbias_algorithms.disparate_impact_remover import DisparateImpactRemoverUnbiasAlgorithm
from processors.preprocessors.unbias_algorithms.optim_preprocess import OptimizedPreprocessingUnbiasAlgorithm
from processors.preprocessors.unbias_algorithms.prejudice_remover import PrejudiceRemoverUnbiasAlgorithm
from processors.preprocessors.unbias_algorithms.reweighing import ReweighingUnbiasAlgorithm


class Pipeline:
    @staticmethod
    def new_pipe():
        return BasePipe()

    def select_data_preprocessor(self, dataset, preprocessor):
        if dataset == Datasets.ADULT_INCOME and preprocessor == Preprocessors.SEX:
            preprocessed_data_pipe = AdultDataset() >= AdultSexPreprocessor() == self.new_pipe()
            fairness_pipe = AdultSexFairnessPipe()
        elif dataset == Datasets.GERMAN_CREDIT and preprocessor == Preprocessors.AGE:
            preprocessed_data_pipe = GermanDataset() >= GermanAgePreprocessor() == self.new_pipe()
            fairness_pipe = GermanAgeFairnessPipe()
        elif dataset == Datasets.GERMAN_CREDIT and preprocessor == Preprocessors.FOREIGN:
            preprocessed_data_pipe = GermanDataset() >= GermanForeignPreprocessor() == self.new_pipe()
            fairness_pipe = GermanForeignFairnessPipe()

        return preprocessed_data_pipe, fairness_pipe

    def unbias_data_preprocessor(self, params, algorithm, unbias_data_algorithm):
        preprocessed_data_pipe, fairness_pipe = params
        result_pipe = None

        if algorithm == UnbiasInProcAlgorithms.PREJUDICE_REMOVER:
            result_pipe = preprocessed_data_pipe.merge(fairness_pipe) >= PrejudiceRemoverUnbiasAlgorithm() == self.new_pipe()
        else:
            if unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING:
                result_pipe = preprocessed_data_pipe.merge(fairness_pipe) >= ReweighingUnbiasAlgorithm() == self.new_pipe()
            elif unbias_data_algorithm == UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING:
                result_pipe = preprocessed_data_pipe.merge(fairness_pipe) >= OptimizedPreprocessingUnbiasAlgorithm() == self.new_pipe()
            elif unbias_data_algorithm == UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER:
                result_pipe = preprocessed_data_pipe.merge(fairness_pipe) >= DisparateImpactRemoverUnbiasAlgorithm() == self.new_pipe()
            elif unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING:
                result_pipe = preprocessed_data_pipe

        return result_pipe

    def data_preprocess(self, dataset, preprocessor, algorithm, unbias_data_algorithm):
        preprocessed_data_pipe, fairness_pipe = self.select_data_preprocessor(dataset, preprocessor)

        params = preprocessed_data_pipe, fairness_pipe
        unbiased_data_pipe = self.unbias_data_preprocessor(params, algorithm, unbias_data_algorithm)

        return fairness_pipe, unbiased_data_pipe

    def process(self, params, algorithm, unbias_data_algorithm):
        if algorithm == Algorithms.LOGISTIC_REGRESSION and unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING:
            prediction_pipe = params >= LogisticRegressionFilter(weighed=True) == self.new_pipe()
        elif algorithm == Algorithms.LOGISTIC_REGRESSION:
            prediction_pipe = params >= LogisticRegressionFilter() == self.new_pipe()
        elif algorithm == UnbiasInProcAlgorithms.PREJUDICE_REMOVER:
            prediction_pipe = params >= PrejudiceRemoverFilter() == self.new_pipe()

        return prediction_pipe

    def calculate_metrics(self, test_pipe, prediction_pipe, fairness_pipe, algorithm, unbias_data_algorithm):
        if unbias_data_algorithm == UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER:
            metrics_pipe = test_pipe.merge(prediction_pipe).merge(fairness_pipe) >= DisparateImpactRemoverMetricsFilter() == self.new_pipe()
        elif unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING or unbias_data_algorithm == UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING:
            metrics_pipe = test_pipe.merge(prediction_pipe).merge(fairness_pipe) >= MLModelMetricsFilter() == self.new_pipe()
        elif algorithm == UnbiasInProcAlgorithms.PREJUDICE_REMOVER:
            metrics_pipe = test_pipe.merge(prediction_pipe).merge(fairness_pipe) >= PrejudiceRemoverMetricsFilter() == self.new_pipe()
        else:
            metrics_pipe = test_pipe.merge(prediction_pipe).merge(fairness_pipe) >= MLModelMetricsFilter() == self.new_pipe()

        return metrics_pipe

    def start(self, dataset, preprocessor, algorithm, unbias_data_algorithm):
        PipelineValidation.validate_params(dataset, preprocessor, algorithm, unbias_data_algorithm)

        fairness_pipe, data_pipe = self.data_preprocess(dataset, preprocessor, algorithm, unbias_data_algorithm)

        if unbias_data_algorithm == UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER:
            process_pipe = data_pipe.partial_pipe(['x_train', 'y_train', 'x_test'])
            test_pipe = data_pipe.partial_pipe(['df_aif', 'y_test'])
        elif unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING or unbias_data_algorithm == UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING:
            process_pipe = data_pipe.partial_pipe(['x_train', 'y_train', 'x_test', 'df_aif'])
            test_pipe = data_pipe.partial_pipe(['x_test', 'y_test'])
        elif algorithm == UnbiasInProcAlgorithms.PREJUDICE_REMOVER:
            process_pipe = data_pipe.partial_pipe(['df_aif_tr', 'df_aif_te'])
            test_pipe = data_pipe.partial_pipe(['df_aif_te', 'y_test'])
        else:
            process_pipe = data_pipe.partial_pipe(['x_train', 'y_train', 'x_test'])
            test_pipe = data_pipe.partial_pipe(['x_test', 'y_test'])

        prediction_pipe = self.process(process_pipe, algorithm, unbias_data_algorithm)

        metrics_pipe = self.calculate_metrics(test_pipe, prediction_pipe, fairness_pipe, algorithm, unbias_data_algorithm)

        return prediction_pipe.value['y_pred'], test_pipe.value['y_test'], metrics_pipe.value['explainer']
