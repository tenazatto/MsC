from metrics.metrics import ml_model_metrics, prejudice_remover_metrics, disparate_impact_remover_metrics
from pipeline.validation import PipelineValidation
from processors.enums import Datasets, Preprocessors, UnbiasDataAlgorithms, Algorithms, UnbiasInProcAlgorithms
from processors.inprocessors.algorithms import logistic_regression_weighed, logistic_regression, prejudice_remover
from processors.preprocessors.data.adult_sex import AdultSexPreprocessor
from processors.preprocessors.data.german_age import GermanAgePreprocessor
from processors.preprocessors.data.german_foreign import GermanForeignPreprocessor
from processors.preprocessors.algorithms import reweighing_preprocess, optim_preprocess, disparate_impact_preprocess, \
    prejudice_remover_preprocess


class Pipeline:
    def select_data_preprocessor(self, dataset, preprocessor):
        if dataset == Datasets.ADULT_INCOME and preprocessor == Preprocessors.SEX:
            preprocessor = AdultSexPreprocessor()
        elif dataset == Datasets.GERMAN_CREDIT and preprocessor == Preprocessors.AGE:
            preprocessor = GermanAgePreprocessor()
        elif dataset == Datasets.GERMAN_CREDIT and preprocessor == Preprocessors.FOREIGN:
            preprocessor = GermanForeignPreprocessor()

        return preprocessor

    def unbias_data_preprocessor(self, params, algorithm, unbias_data_algorithm):
        x_train, x_test, y_train, y_test, preprocessor = params
        result = None

        if algorithm == UnbiasInProcAlgorithms.PREJUDICE_REMOVER:
            dataset_tr, dataset_te = \
                prejudice_remover_preprocess(x_train, x_test, y_train, y_test, preprocessor)
            result = dataset_tr, dataset_te, y_test
        else:
            if unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING:
                df_aif_rw = reweighing_preprocess(x_train, y_train, preprocessor)
                result = x_train, x_test, y_train, y_test, df_aif_rw
            elif unbias_data_algorithm == UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING:
                df_aif_op = optim_preprocess(x_train, y_train, preprocessor)
                result = x_train, x_test, y_train, y_test, df_aif_op
            elif unbias_data_algorithm == UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER:
                x_di_train, x_di_test, y_di_train, df_aif_te = \
                    disparate_impact_preprocess(x_train, x_test, y_train, y_test, preprocessor)
                result = x_train, x_test, y_train, y_test, \
                       x_di_train, x_di_test, y_di_train, df_aif_te
            elif unbias_data_algorithm == UnbiasDataAlgorithms.NOTHING:
                result = x_train, x_test, y_train, y_test

        return result

    def data_preprocess(self, dataset, preprocessor, algorithm, unbias_data_algorithm):
        preprocessor = self.select_data_preprocessor(dataset, preprocessor)
        x_train, x_test, y_train, y_test = preprocessor.dataset_preprocess()

        params = x_train, x_test, y_train, y_test, preprocessor
        final_data = self.unbias_data_preprocessor(params, algorithm, unbias_data_algorithm)

        return final_data, preprocessor

    def process(self, params, algorithm, unbias_data_algorithm):
        if algorithm == Algorithms.LOGISTIC_REGRESSION and unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING:
            x_train, y_train, x_test, df_aif = params
            y_pred = logistic_regression_weighed(x_train, y_train, x_test, df_aif.instance_weights)
        elif algorithm == Algorithms.LOGISTIC_REGRESSION:
            x_train, y_train, x_test = params
            y_pred = logistic_regression(x_train, y_train, x_test)
        elif algorithm == UnbiasInProcAlgorithms.PREJUDICE_REMOVER:
            dataset_tr, dataset_te = params
            y_pred = prejudice_remover(dataset_tr, dataset_te)

        return y_pred

    def calculate_metrics(self, params, y_pred, algorithm, unbias_data_algorithm, preprocessor):
        if unbias_data_algorithm == UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER:
            df_aif_te = params
            metrics, explainer = disparate_impact_remover_metrics(df_aif_te, y_pred, preprocessor)
        elif unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING or unbias_data_algorithm == UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING:
            x_test, y_test = params
            metrics, explainer = ml_model_metrics(x_test, y_test, y_pred, preprocessor)
        elif algorithm == UnbiasInProcAlgorithms.PREJUDICE_REMOVER:
            dataset_te = params
            metrics, explainer = prejudice_remover_metrics(dataset_te, y_pred, preprocessor)
        else:
            x_test, y_test = params
            metrics, explainer = ml_model_metrics(x_test, y_test, y_pred, preprocessor)

        return metrics, explainer

    def start(self, dataset, preprocessor, algorithm, unbias_data_algorithm):
        PipelineValidation.validate_params(dataset, preprocessor, algorithm, unbias_data_algorithm)

        final_data, preprocessor = self.data_preprocess(dataset, preprocessor, algorithm, unbias_data_algorithm)

        if unbias_data_algorithm == UnbiasDataAlgorithms.DISPARATE_IMPACT_REMOVER:
            x_train, x_test, y_train, y_test, x_di_train, x_di_test, y_di_train, df_aif_te = final_data
            params = x_di_train, y_di_train, x_di_test
            params_metric = df_aif_te
        elif unbias_data_algorithm == UnbiasDataAlgorithms.REWEIGHING or unbias_data_algorithm == UnbiasDataAlgorithms.OPTIMIZED_PREPROCESSING:
            x_train, x_test, y_train, y_test, df_aif_rw = final_data
            params = x_train, y_train, x_test, df_aif_rw
            params_metric = x_test, y_test
        elif algorithm == UnbiasInProcAlgorithms.PREJUDICE_REMOVER:
            dataset_tr, dataset_te, y_test = final_data
            params = dataset_tr, dataset_te
            params_metric = dataset_te
        else:
            x_train, x_test, y_train, y_test = final_data
            params = x_train, y_train, x_test
            params_metric = x_test, y_test

        y_pred = self.process(params, algorithm, unbias_data_algorithm)

        metrics, explainer = self.calculate_metrics(params_metric, y_pred, algorithm, unbias_data_algorithm, preprocessor)

        return y_pred, y_test, explainer
